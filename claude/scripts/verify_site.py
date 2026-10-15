#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the starkmanfirm.com tree before anything ships.

Runs the four checks from claude/site-build-notes.md, plus a fifth added
2026-10-15 after a broken hreflang was found to be causing a Search Console 404.

Usage, from anywhere:
    python3 -I claude/scripts/verify_site.py                 # auto-detect the site
    python3 -I claude/scripts/verify_site.py --site ./site   # explicit
    python3 -I claude/scripts/verify_site.py --skip-render   # no Playwright available

Exit code 0 = every check passed. Non-zero = do not ship; the output names the failure.
"""
import io
import os
import re
import subprocess
import sys
import xml.dom.minidom
from urllib.parse import urlparse, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_HOST = "starkmanfirm.com"

# The only files a single post is allowed to touch: 2 new pages, 2 index pages, sitemap.
# Pass --expect N when a run is shipping more than one post (e.g. --expect 7 for two).
DEFAULT_EXPECTED_DIFF = 5
INDEX_PAGES = {"resources/index.html", "es/recursos/index.html"}


def expected_diff():
    argv = sys.argv
    if "--expect" in argv:
        return int(argv[argv.index("--expect") + 1])
    return DEFAULT_EXPECTED_DIFF


def site_dir():
    argv = sys.argv
    if "--site" in argv:
        return os.path.abspath(argv[argv.index("--site") + 1])
    if os.environ.get("SITE_DIR"):
        return os.path.abspath(os.environ["SITE_DIR"])
    beside = os.path.join(HERE, "site")
    if os.path.isdir(beside):
        return beside
    repo_root = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
    if os.path.isfile(os.path.join(repo_root, "sitemap.xml")):
        return repo_root
    return beside


S = site_dir()
results = []


def record(name, ok, detail):
    results.append((name, ok, detail))
    print(("  PASS  " if ok else "  FAIL  ") + name + " — " + detail)


def html_files():
    out = []
    for dp, dn, fn in os.walk(S):
        if ".git" in dp.split(os.sep):
            continue
        for f in fn:
            if f.endswith(".html"):
                out.append(os.path.join(dp, f))
    return sorted(out)


def git(*args):
    # rstrip only: `git status --porcelain` puts status in columns 0-1 and the path
    # at column 3, so stripping leading whitespace would eat the path's first character.
    return subprocess.run(["git", "-C", S] + list(args),
                          capture_output=True, text=True).stdout.rstrip("\n")


def porcelain_paths():
    """Working-tree changes, as site-relative paths, with directories expanded."""
    out = set()
    for line in git("status", "--porcelain").splitlines():
        if len(line) < 4:
            continue
        p = line[3:]
        if " -> " in p:          # rename
            p = p.split(" -> ", 1)[1]
        p = p.strip().strip('"')
        if p.endswith("/"):
            for dp, dn, fn in os.walk(os.path.join(S, p)):
                for f in fn:
                    out.add(os.path.relpath(os.path.join(dp, f), S))
        elif p:
            out.add(p)
    return out


def committed_paths():
    """Paths changed in commits not yet on origin/main."""
    raw = git("diff", "--name-only", "origin/main...HEAD")
    return {p.strip() for p in raw.splitlines() if p.strip()}


def all_changed_paths():
    return porcelain_paths() | committed_paths()


# --- Check 1: relative links -------------------------------------------------
def check_links():
    bad, n, files = [], 0, html_files()
    for p in files:
        h = io.open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]+)"', h):
            u = m.group(1).strip()
            if not u or u.startswith(("http://", "https://", "mailto:", "tel:",
                                      "#", "data:", "//", "javascript:")):
                continue
            path = unquote(urlparse(u).path)
            if not path:
                continue
            if path.startswith("/"):
                target = os.path.normpath(os.path.join(S, path.lstrip("/")))
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(p), path))
            n += 1
            if not os.path.exists(target):
                bad.append((os.path.relpath(p, S), u))
    detail = f"{len(files)} HTML files, {n} relative links, {len(bad)} broken"
    record("1. relative links", not bad, detail)
    for b in bad[:25]:
        print(f"         BROKEN  {b[0]}  ->  {b[1]}")
    return not bad


# --- Check 2: sitemap --------------------------------------------------------
def check_sitemap():
    path = os.path.join(S, "sitemap.xml")
    try:
        d = xml.dom.minidom.parse(path)
    except Exception as e:
        record("2. sitemap.xml", False, f"does not parse: {e}")
        return False
    locs = [n.firstChild.data.strip() for n in d.getElementsByTagName("loc")]
    missing = []
    for l in locs:
        rel = re.sub(r"^https?://(?:www\.)?" + re.escape(SITE_HOST) + r"/?", "", l)
        cand = rel + "index.html" if (rel == "" or rel.endswith("/")) else rel
        if not os.path.isfile(os.path.join(S, cand)):
            missing.append(l)
    ok = not missing
    record("2. sitemap.xml", ok,
           f"parses, {len(locs)} URLs, {len(missing)} with no file behind them")
    for l in missing[:25]:
        print(f"         WILL 404  {l}")
    return ok


# --- Check 3: render ---------------------------------------------------------
def changed_pages():
    """New or modified HTML pages, as site-relative paths."""
    out = {p for p in all_changed_paths() if p.endswith(".html")}
    return sorted(out | INDEX_PAGES)


def check_render():
    if "--skip-render" in sys.argv:
        record("3. render", True, "skipped by --skip-render")
        return True
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        record("3. render", False,
               "playwright not installed (pip install playwright && playwright install chromium)")
        return False

    pages = [p for p in changed_pages() if os.path.isfile(os.path.join(S, p))]
    if not pages:
        record("3. render", True, "no changed pages to render")
        return True

    import http.server
    import socketserver
    import threading
    import functools

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=S)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    failures = []
    exe = "/opt/pw-browsers/chromium"
    launch = {"executable_path": exe} if os.path.exists(exe) else {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(**launch)
            for rel in pages:
                url = f"http://127.0.0.1:{port}/" + rel
                pg = b.new_page(viewport={"width": 1280, "height": 900})
                errs, reqfail = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("requestfailed",
                      lambda r: reqfail.append(r.url) if "127.0.0.1" in r.url else None)
                r = pg.goto(url, wait_until="load", timeout=30000)
                bad = bool(errs) or bool(reqfail) or r.status != 200
                if bad:
                    failures.append((rel, r.status, errs, reqfail))
                pg.close()
            b.close()
    finally:
        srv.shutdown()

    record("3. render", not failures,
           f"{len(pages)} pages rendered, {len(failures)} with errors")
    for rel, status, errs, reqfail in failures:
        print(f"         {rel}  status={status}  pageerrors={len(errs)}")
        for e in errs[:3]:
            print(f"           ERR {e}")
        for u in reqfail[:3]:
            print(f"           REQFAIL {u}")
    return not failures


# --- Check 4: diff scope -----------------------------------------------------
def check_diff():
    expanded = all_changed_paths()

    allowed = re.compile(
        r"^(resources/index\.html"
        r"|es/recursos/index\.html"
        r"|resources/[^/]+/index\.html"
        r"|es/recursos/[^/]+/index\.html"
        r"|sitemap\.xml"
        r"|claude/.*"
        r"|\.github/.*)$")
    stray = sorted(p for p in expanded if not allowed.match(p))
    site_files = sorted(p for p in expanded
                        if not p.startswith("claude/") and not p.startswith(".github/"))
    want = expected_diff()
    ok = not stray and len(site_files) == want
    record("4. diff scope", ok,
           f"{len(site_files)} site files changed (expected {want}), "
           f"{len(stray)} outside the allowed set")
    for p in site_files:
        print(f"         touched  {p}")
    for p in stray:
        print(f"         STRAY    {p}")
    return ok


# --- Check 5: absolute self-links and hreflang -------------------------------
def check_absolute_links():
    """Catches hreflang and canonical URLs pointing at pages that do not exist.

    Added 2026-10-15: accessibility/index.html advertised an es-us alternate at
    /es/accessibility/ while the real page is /es/accesibilidad/. Google follows
    hreflang, so that was a live 404 in Search Console that check 1 could not see,
    because check 1 deliberately skips absolute URLs.
    """
    bad = {}
    pat = re.compile(
        r'(?:href|content)\s*=\s*"(https?://(?:www\.)?'
        + re.escape(SITE_HOST) + r'[^"]*)"')
    for p in html_files():
        h = io.open(p, encoding="utf-8", errors="replace").read()
        for m in pat.finditer(h):
            u = m.group(1)
            rel = re.sub(r"^https?://(?:www\.)?" + re.escape(SITE_HOST) + r"/?", "", u)
            rel = rel.split("#")[0].split("?")[0]
            cand = rel + "index.html" if (rel == "" or rel.endswith("/")) else rel
            if not os.path.exists(os.path.join(S, cand)):
                bad.setdefault(u, set()).add(os.path.relpath(p, S))
    record("5. absolute self-links", not bad,
           f"{len(bad)} absolute URL(s) pointing at a path with no file")
    for u, fs in sorted(bad.items()):
        print(f"         WILL 404  {u}")
        print(f"                   referenced by {', '.join(sorted(fs)[:3])}")
    return not bad


if __name__ == "__main__":
    print(f"verifying {S}\n")
    check_links()
    check_sitemap()
    check_render()
    check_diff()
    check_absolute_links()
    failed = [n for n, ok, _ in results if not ok]
    print()
    if failed:
        print(f"FAILED: {', '.join(failed)}  — do not ship.")
        sys.exit(1)
    print("All checks passed.")
