# starkmanfirm.com — project standards

Static site for the **Starkman Firm**, a New Jersey personal injury and workers'
compensation firm. Hand-written HTML, no framework, no build step. Netlify publishes
whatever lands on `main` (`netlify.toml` sets `publish = "."`).

## Before changing anything

Read `claude/blog-playbook.md` and `claude/site-build-notes.md`. They are the
operating instructions for this repo and they are more specific than this file.

## Hard rules

- **New Jersey law only.** Never cite another state's statute, rate or case.
- **Never state a number you have not verified against a primary source in this run** —
  nj.gov, NJ Department of Banking and Insurance, NJ Division of Workers' Compensation,
  NJ Courts, or a published opinion. This applies to statute cites, dollar figures,
  deadlines, week counts and case names. Law-firm blogs are leads, not sources.
  `claude/blog-playbook.md` records specific traps that have already caught earlier runs.
- **Never merge your own pull request.** This content asserts law under Morris Starkman's
  name and bar license. A human merges.
- **Never hand-write a page.** Copy the chrome from an existing article with
  `claude/scripts/build_post.py` so the header, nav, mobile menu, CTA block, form and
  footer stay byte-identical across the site.
- **Never ship without `claude/scripts/verify_site.py` passing.** If a check fails, open
  an issue describing the failure instead of a PR.
- Every article page carries `BlogPosting` **and** `FAQPage` JSON-LD. The FAQ block is
  what AI overviews quote; it is not optional.
- Every article exists in **English and Spanish**. Spanish paths are translated, not
  mirrored: `/resources/` → `/es/recursos/`, `/personal-injury/` → `/es/lesiones-personales/`,
  `/workers-compensation/` → `/es/compensacion-laboral/`, `/free-case-review/` → `/es/consulta-gratis/`.
- Internal links include `index.html` (`../../resources/index.html`, not `../../resources/`).
- Cross-link only to pages that actually exist on `main`.

## Voice

Short declarative sentences. Second person. Imperative H2s ("Do not quit and do not sign").
No jargon, no throat-clearing, no "In today's world." Statutes cited plainly
(`N.J.S.A. 34:15-40`). Posts run **900–1,200 words** — measure and trim. Always close with
the "not legal advice" disclaimer.

The firm's selling point, in all copy: **"You see the attorney."** No secretaries, no
paralegals, contingency fee, Se habla español. Cherry Hill 856-424-7277 · Perth Amboy
732-324-2011.

## Layout

```
index.html              assets/            personal-injury/     workers-compensation/
resources/<slug>/       es/                sitemap.xml          robots.txt
claude/                 the playbook, site notes and scripts (not served; no links point at it)
.github/workflows/      the biweekly post job
```

`_lib.js` is the generator used to author the site originally. It is **not** loaded by the
site and it has a known bug (undefined `rel` in `header()`/`footer()`). Do not run it.
