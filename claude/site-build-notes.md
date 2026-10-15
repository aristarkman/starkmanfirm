# How to add a post to the starkmanfirm.com codebase

Static HTML, **no build step** — `netlify.toml` sets `publish = "."` and there is no build
command. Netlify deploys whatever lands on `main`.

## Layout

```
index.html                     assets/site.css, logos, photos
personal-injury/…              workers-compensation/…   resources/…
es/…                           full Spanish mirror
_lib.js                        the original page generator (NOT loaded by the site — do not run)
netlify.toml  robots.txt  sitemap.xml  readme.md
claude/                        playbook, these notes, scripts (not served)
```

**Spanish paths are translated, not mirrored literally:**
`/resources/` → `/es/recursos/`, `/personal-injury/` → `/es/lesiones-personales/`,
`/workers-compensation/` → `/es/compensacion-laboral/`, `/free-case-review/` → `/es/consulta-gratis/`.

**Internal links include `index.html`** (`../../resources/index.html`, not `../../resources/`).

## The recipe

Do **not** hand-write a page. Copy the chrome from an existing article so the header, nav,
mobile menu, CTA block, form and footer stay byte-identical. `build_post.py` does all of
this; what follows is what it does, for when something needs debugging.

1. Skeleton: `resources/workers-comp-claim-denied-nj/index.html` (EN, `../../` depth) and
   `es/recursos/reclamo-negado/index.html` (ES, `../../../` depth).
2. Split the skeleton at `</head><body>`, at `<main>`, and at `<section class="cta">`.
   Keep the header chunk and the CTA+footer chunk verbatim. Replace the middle.
3. New `<head>`: title `"<Title> | Starkman Firm"`, meta description ≤160, canonical,
   en/es hreflang alternates + x-default, OG/Twitter, GA4 `G-NG99FGY5L4`, then the JSON-LD.
4. JSON-LD `@graph`: reuse the four firm nodes from the skeleton
   (`LegalService`, two `Attorney` offices, `Person` Morris), then append `BreadcrumbList`,
   `BlogPosting`, and `FAQPage`. The FAQPage is what AI overviews quote — always include it.
5. Body structure:
   - `<div class="pagehero">` with breadcrumbs, `<h1>`, and a one-line lead `<p>`.
   - `<section><div class="wrap twocol"><article class="prose">` — byline as
     `<p class="fine" style="margin-bottom:6px">Published <date> · Morris Starkman</p>`,
     then `<h2>`/`<p>`/`<ul>`, closing with the disclaimer in another `p.fine`.
   - `<aside class="rail">` — dark "Free consultation" card + "More reading" card.
   - `<section class="faq">` with `<details><summary>` pairs, matching the FAQPage LD.
6. Add a card to the **top** of `<div class="postlist">` in `resources/index.html` and
   `es/recursos/index.html` (date format `Oct 15, 2026` / `15 oct 2026`).
7. Add two `<url>` entries to `sitemap.xml` with hreflang alternates, before `</urlset>`.

## Running the generator

Write the cycle's copy module, save it as `claude/scripts/copy_<YYYY-MM-DD>.py`, copy it to
`claude/scripts/copy.py`, then:

```sh
python3 -I claude/scripts/build_post.py
```

It finds the site automatically: `--site PATH` wins, then `$SITE_DIR`, then a `./site/`
directory beside the script, then the repo root two levels up. In a GitHub Actions checkout
the repo root *is* the site, so no argument is needed. In a sandbox that cloned the repo into
`./site/` beside the script, also no argument.

`build_post.py` is generic and needs no editing between cycles — it reads the byline, the
index-card date, the "More reading" links and the citation list from `copy.py` along with the
body copy. Copy modules written before 2026-09-15 predate those fields; a `cp()` helper
derives sensible defaults so old modules still build.

## Always verify before shipping

```sh
python3 -I claude/scripts/verify_site.py
```

Exit 0 means safe. The five checks:

1. **Relative links** — walk every `.html`, resolve each relative `href`/`src`, assert the
   file exists. Must be 0 broken.
2. **Sitemap** — `sitemap.xml` parses, and every `<loc>` has a real file behind it.
3. **Render** — serves the tree and loads every changed page plus both index pages in
   Playwright. Must be status 200, zero `pageerror`, zero failed local requests. Pass
   `--skip-render` only when Playwright genuinely isn't available.
4. **Diff scope** — only the 2 new pages, the 2 index pages and `sitemap.xml`. Pass
   `--expect N` when shipping more than one post at once (7 for two posts).
5. **Absolute self-links** — every `https://www.starkmanfirm.com/...` URL in an `href` or
   `content` attribute, which is where canonical and hreflang live, must point at a real
   file. **Added 2026-10-15**, after `accessibility/index.html` was found advertising an
   `es-us` alternate at `/es/accessibility/` when the real page is `/es/accesibilidad/`.
   Google follows hreflang, so that was a live Search Console 404 that check 1 could never
   catch, because check 1 deliberately skips absolute URLs.

## Known issues on the site (pre-existing)

- The 2026-08-31 doctor post is **English-only** — no `/es/recursos/` counterpart and no
  hreflang alternates at all, while every other article has both. Worth a follow-up cycle.
- `googlexxxxxxxxxxxxxxxx.html` is a **placeholder**, not a real Google Search Console
  verification file, so verification is not actually working.
- At around 1200–1300px the header's "Español" nav link collides with the `856-424-7277`
  button.
- `readme.md` says the contact form "posts nowhere," but the forms are wired with
  `data-netlify="true"` and Netlify Forms is enabled. Worth confirming email notifications
  are on.
- Ari reported **16 Search Console 404s** on 2026-10-15. One was the hreflang bug above.
  The others are unidentified; the sitemap is clean and there are no broken relative links,
  so they are most likely retired URLs from an earlier version of the site and want
  `netlify.toml` redirects rather than new pages.
