# Starkman Firm — website

36 pages: 18 in English, 18 in Spanish. Static HTML, one shared stylesheet, no build step.
Open `site/index.html`.

## Deploying to Netlify

1. Upload the **contents** of this folder (drag the unzipped `site` folder's contents onto app.netlify.com/drop, or connect the repo).
2. Forms are already wired: every form carries `data-netlify="true"`, form names `case-review` (English) and `consulta-es` (Spanish). Submissions appear under **Site configuration → Forms**. Turn on email notifications there so the office is alerted.
3. Spam protection: a honeypot field named `company` is in place. Netlify's built-in Akismet filter can be enabled alongside it.
4. On submit, visitors land on `/thank-you/` (or `/es/gracias/`), which is `noindex` and repeats both phone numbers.
5. `netlify.toml` sets security headers and a one-year cache on `/assets/*`.
6. Point `starkmanfirm.com` at the site under **Domain management**. Netlify issues the HTTPS certificate automatically.

**Before launch:** every canonical URL and the sitemap assume `https://www.starkmanfirm.com`. If the live domain differs, those need rewriting.

## Real data used (pulled from starkmanfirm.com and the firm's directory listings)
- **Cherry Hill** — 1939 Marlton Pike East, Suite 210, Cherry Hill, NJ 08003 · (856) 424-7277 · Mon–Fri 8:30–5:00
- **Perth Amboy** — 188 Market Street, Perth Amboy, NJ 08861 · (732) 324-2011 · Mon–Fri 9:00–6:00
- info@starkmanfirm.com · ameltzer@starkmanfirm.com
- **Morris Starkman** — practicing since 1972, firm founded 1973; Rutgers College 1969, Rutgers Law 1972; admitted NJ, Federal and Bankruptcy Court bars (D.N.J.); synagogue and charitable involvement; married 54 years, three children, seven grandchildren.
- **Allan Meltzer** — 30+ years, personal injury and workers' comp; American University, New York Law School.
- Firm promises taken verbatim in substance from Morris's own statement: clients see the attorney, free consultations, payment plans in criminal/municipal matters, no injury fee unless we collect, verbal and zero threshold cases, equal treatment regardless of race/color/creed/religion/economic status, appointments optional, house calls when necessary.
- Client reviews on the home page are real published quotes; reviewer names were not published with them.

## Still placeholder — needs the firm
- All photography (portraits, office exteriors, hero).
- Case results other than the $700,000 Middlesex County car accident.
- Bar admission years for Allan Meltzer.
- Real estate closing fee schedule.
- Accessibility details for both offices; the "last reviewed" date on `/accessibility/`.
- The form posts nowhere — wire `action` to your CRM or mail handler.

## SEO / GEO / AIO
- Per-page `<title>`, meta description, canonical, and en/es `hreflang` pairs on every page.
- JSON-LD `@graph` on every page: LegalService, two Attorney branch offices with geo + hours, Person entries for both attorneys, BreadcrumbList, Service, FAQPage, BlogPosting.
- Location pages for each office with directions, service areas and city/county names in prose.
- Answer-first Q&A blocks and FAQ sections written to be quotable by AI overviews.
- `sitemap.xml` with hreflang alternates; `robots.txt` explicitly allows GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot and Google-Extended.
- Google Maps embeds on both location pages and both home pages.

## Before launch
1. Point `SITE` (used in the schema) at the production domain if it is not `https://www.starkmanfirm.com/`.
2. Verify the NJ attorney-advertising disclaimer wording on `/results/`.
3. Connect the Google Business Profile for each office and link the live review feed.
4. Add analytics and call tracking.

## Files
`_lib.js` is the page generator used to build these files (head, header, footer, CTA blocks). It is not loaded by the site — it exists so pages can be regenerated consistently. `direction-a-home.html` and `direction-b-home.html` are the two identity drafts; B was chosen. Both can be deleted.
