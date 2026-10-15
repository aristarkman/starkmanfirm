# Starkman Firm — Blog Playbook

Standing job: **one post every 2 weeks**, on NJ personal injury or workers' compensation,
written for SEO + AI Overviews (AiO). This file is the instruction set the GitHub Action
follows. Read it first, every run.

## How publishing works now

The job runs as a GitHub Action (`.github/workflows/biweekly-blog-post.yml`) on the 1st and
15th. It writes the post, verifies it, and **opens a pull request**. It never merges — a
human does, because this content asserts statutes, dollar figures and filing deadlines under
Morris Starkman's name and bar license. See `claude/README.md` for setup and history.

**If any check in `claude/scripts/verify_site.py` fails, open an issue describing the
failure instead of a pull request.** Shipping a post with a broken link or a 404 in the
sitemap is worse than shipping nothing.

## The firm

- **Starkman Firm** — starkmanfirm.com. Founded 1973; Morris Starkman practicing since 1972.
- Attorneys: Morris Starkman (byline author), Allan Meltzer.
- **New Jersey only.** South & Central Jersey focus.
- Offices: Cherry Hill — 1939 Marlton Pike East, Suite 210, Cherry Hill NJ 08003 ·
  856-424-7277 · Mon–Fri 8:30–5:00. Perth Amboy — 188 Market Street, Perth Amboy NJ 08861 ·
  732-324-2011 · Mon–Fri 9:00–6:00. Both bilingual English/Spanish.
- Practice areas: personal injury (car accidents, slip and fall), workers' compensation
  (incl. construction injuries), criminal/municipal court, real estate & business.
- Selling point in all copy: **"You see the attorney."** No secretaries, no paralegals,
  contingency fee, Se habla español.

## The site

- **Netlify**, project `fabulous-taiyaki-ef2b9e`, site ID
  `a8f54475-8abc-4b22-b310-473ead399b02`, deploying from `main`.
- Posts live under **`/resources/<slug>/`**, Spanish at **`/es/recursos/<slug-es>/`**.
- `robots.txt` allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended.
  Good for AiO — lean into citable, factual content.

## Voice

Short declarative sentences. Second person. Imperative H2s ("Do not quit and do not sign").
No jargon, no throat-clearing, no "In today's world." Posts run **900–1,200 words** —
measure the rendered `<article class="prose">` and trim if over; the 2026-10-15 draft came in
at 1,293 and had to be cut back. Statutes cited plainly (`N.J.S.A. 34:15-40`). Always close
with the "not legal advice" disclaimer.

## Deliverables per post

1. A `.md` draft in `claude/posts/<YYYY-MM-DD>-<slug>.md` with the title tag, meta
   description (≤160), target keywords, internal links, and a dated **Sources verified**
   table listing every asserted fact against the URL checked that run.
2. EN + ES pages built with `claude/scripts/build_post.py`, which also adds the two index
   cards and the two sitemap entries.
3. All five checks in `claude/scripts/verify_site.py` passing.
4. The copy module saved as `claude/scripts/copy_<YYYY-MM-DD>.py`.
5. This file updated: the Published table, the topic queue, and a dated "Facts verified"
   section.

## Research rules — these exist because runs have been burned

- Primary or authoritative sources only: nj.gov, NJ DOBI, NJ Division of Workers'
  Compensation, NJ Courts (including Model Civil Jury Charges), published opinions.
  Law-firm blogs are leads, never sources.
- **Confirm reporter citations before using them.** Justia and CourtListener opinion pages
  often give the docket number and decision date but not the `N.J.` volume and page. If you
  cannot confirm a volume/page, cite the case by name, court and date instead — never guess,
  and never propagate a LEXIS database number (`2022 N.J. LEXIS 242`) as if it were a
  reporter cite.
- **Never take a dollar figure from a multi-state summary.** See the 2026-10-01 trap below.
- Re-verify every fact in the sections below before reusing it. They are dated for a reason.

## Published

| # | Date | Slug | Topic |
|---|------|------|-------|
| 1 | 2026-08-19 | `nj-limited-vs-unlimited-right-to-sue` | Verbal threshold / limitation on lawsuit |
| 2 | 2026-08-31 | `choose-doctor-nj-workers-comp` | Who picks the treating doctor (English-only — no ES page, no hreflang) |
| 3 | 2026-09-15 | `how-much-does-workers-comp-pay-nj` | What NJ comp actually pays |
| 4 | 2026-10-01 | `construction-injury-comp-and-third-party-claim-nj` | Construction injuries: comp vs. the third-party claim |
| 5 | 2026-10-15 | `slip-and-fall-notice-nj` | Slip and fall: proving the owner had notice |
| 6 | 2026-10-15 | `underinsured-motorist-coverage-nj` | Underinsured motorist coverage (second run same day; copy module `copy_2026-10-15-uim.py` so `copy_2026-10-15.py` is not overwritten) |

**Shelved:** a 2026-09-01 retaliation post (`fired-for-filing-workers-comp-nj`) was written
and verified, then shelved at Ari's direction. `copy_2026-09-01.py` is retained. Do not
publish it unasked.

## Pre-existing pages (do not duplicate)

- `/resources/what-to-do-after-a-car-accident-in-nj/` (Jul 14, 2026)
- `/resources/workers-comp-claim-denied-nj/` (Jun 2, 2026)
- `/resources/how-long-do-i-have-to-file-nj/` (May 8, 2026)

## Topic queue — take the top unused one, unless something more timely has happened

1. Injured driving for work in NJ: comp, third-party, or both — **narrow or merge**; the
   construction post covers the comp/third-party split and the 34:15-40 lien in general
   terms. Keep only if it goes deep on auto-specific ground: PIP vs. comp primacy, the
   verbal threshold applying to the third-party auto case, UM/UIM stacking with a comp lien
2. Hurt at work but the employer says you're a 1099 contractor
3. Social media and your NJ injury claim: what the carrier's investigator actually looks for
4. The independent medical exam: what the carrier's doctor is actually measuring
5. The workers' comp lien on your injury settlement: what N.J.S.A. 34:15-40 really leaves
   you — a numbers post working a sample recovery through subsections (b), (c) and (e),
   including the $750 cap and the 33 1/3% reduction. "Workers comp lien" is high-intent
6. **Snow and ice on a New Jersey sidewalk: whose job was it?** The 10-15 post states the
   *Stewart* / *Luchejko* commercial-vs-residential line in two sentences but does not work
   it — lease-shifting between landlord and tenant, the condo and co-op cases, the "created
   or exacerbated" exception for residential owners, and municipal snow ordinances that
   impose a duty to the town but not to you. Strongly seasonal; schedule for December
   or January
7. Uninsured motorist (UM) claims — hit-and-run and no-insurance drivers: what 17:28-1.1 and the tort-option language
   require, and what the notice and proof rules are (verify the hit-and-run corroboration rule, N.J.S.A. 39:6-78, before writing)

**Dropped:** NJ permanency awards / the schedule of disabilities — the 2026-09-15 post
already covers the 600-week math and the scheduled members. The authorized treating
physician — covered by the 2026-08-31 doctor post; revisit only from the IME angle (item 4).

## Facts verified 2026-10-15, second run (UIM) (re-verify before reuse)

- **N.J.S.A. 17:28-1.1** as amended by P.L. 2022, c.87 (pub.njleg.state.nj.us/Bills/2022/PL22/87_.HTM):
  (a) Basic policy excepted; UM/UIM floor $15,000/$30,000 pre-2023, $25,000/$50,000 from 1/1/2023,
  **$35,000/$70,000 from 1/1/2026**. (b) insurer must **offer** up to $250,000/$500,000 BI, but UM/UIM
  limits "shall not exceed the insured's motor vehicle liability policy limits." (c) **no stacking**
  across vehicles or policies. (e) underinsured = sum of available liability limits **less than** the
  insured's UIM limits; not underinsured unless liability limits are exhausted by settlement or
  judgment; UIM limits "reduced by the amount he has recovered under all bodily injury liability
  insurance or bonds." (f) employee UM/UIM. Text confirmed against the 2022 chaptered law and the
  quotations of (a), (b), (f) in *Chiaccheri*; no later amendment was checked.
- ***Chiaccheri v. Zurich American Ins. Co.*** (A-9-25), N.J. Supreme Court, decided **Aug. 6, 2026**
  (njcourts.gov). Employee's maximum UIM under (f) = the UIM limit the employer chose for the named
  insured, not the liability limit; a UIM endorsement below the liability limit is valid if (a)/(b)
  are met. Facts: $2M liability, $15,000 UIM, tortfeasor $100,000. **No N.J. reporter cite
  confirmed — cite by name, court and date.** Only the syllabus and opinion text were read; the
  Third Circuit's disposition of Chiaccheri's own claim is not stated.
- ***Ferrante v. N.J. Manufacturers Ins. Group*** (A-87-16), decided **Apr. 11, 2018**: no notice to the
  UIM carrier for years lets the carrier refuse UIM benefits; prejudice not weighed. **No reporter cite
  confirmed.** Via its text: *Zirger*, 144 N.J. 327 (1996) (notice at institution of suit);
  *Longworth v. Van Houten*, 223 N.J. Super. 174 (App. Div. 1988); *Rutgers Cas. Ins. Co. v. Vassas*,
  139 N.J. 163 (1995) (carrier either pays the offer amount for subrogation or lets the insured settle).
- **DOBI 2026 Auto Insurance Buyer's Guide** (nj.gov/dobi/division_consumers/pdf/autoguide2026.pdf):
  UIM example ($100,000 UIM, $35,000 at-fault limit, $45,000 damages -> $10,000 from UIM); Basic
  Policy UM/UIM "None." The guide's UM/UIM limit options in the chart were garbled in text extraction
  and were **not** used.
- Not verified, so not stated: the limitations period for a UIM claim; whether the tort option
  applies to UIM (the statute's text names only *uninsured* coverage).

## Facts verified 2026-10-15 (re-verify before reuse)

- ***Jeter v. Sam's Club*, 250 N.J. 240 (2022)** (decided Mar. 17, 2022) — a business owner
  is liable "if the owner had actual or constructive knowledge" of the dangerous condition.
  Constructive notice = present "for such a length of time as reasonably to have resulted in
  knowledge and correction"; may be inferred from eyewitness testimony or the
  "characteristics of the dangerous condition." **"[E]xistence of an alleged dangerous
  condition is not constructive notice of it."**
- **Mode-of-operation, three elements** (*Jeter*): self-service setting; accident in an area
  affected by the self-service operation; a "reasonable factual nexus" between the
  self-service activity and the hazard. Held **not** to apply to grapes in sealed clamshell
  containers — that "does not create a reasonably foreseeable risk that grapes will fall to
  the ground."
- ***Nisivoccia v. Glass Gardens, Inc.*, 175 N.J. 559 (2003)** — mode-of-operation
  **applied**; grapes sold in "open-top, vented plastic bags that permitted spillage."
- ***Stewart v. 104 Wallace St., Inc.*, 87 N.J. 146 (1981)** — "[t]he duty to maintain
  abutting sidewalks that we impose today is confined to owners of commercial property."
- ***Luchejko v. City of Hoboken*, 207 N.J. 191 (2011)** — residential owners are not subject
  to sidewalk liability; a 104-unit condo is residential. The test turns on whether the
  predominant use "has the capacity to generate income." Residential owners can still be
  liable for creating or exacerbating a condition.
- **N.J.S.A. 59:8-8** — notice of claim against a public entity "not later than the 90th day
  after accrual"; forever barred after two years.
- **N.J.S.A. 59:8-9** — a Superior Court judge may permit late notice "at any time within one
  year after the accrual," on motion with affidavit "showing sufficient reasons constituting
  extraordinary circumstances," and only if the entity "has not been substantially
  prejudiced."
- **N.J.S.A. 59:4-2** — public-entity conduct must be **palpably unreasonable**: "plainly and
  obviously without reason or a reasonable basis" (NJ Model Civil Jury Charge 5.20A); actual
  or constructive notice also required.
- **N.J.S.A. 59:9-2(d)** — no pain and suffering against a public entity except permanent
  loss of a bodily function, permanent disfigurement or dismemberment, where medical
  treatment expenses exceed **$3,600**.
- **N.J.S.A. 2A:15-5.1** — modified comparative negligence; "[a]ny damages sustained shall be
  diminished by the percentage sustained of negligence attributable to the person
  recovering"; no recovery where the plaintiff's fault is greater than the defendant's.
- **N.J.S.A. 2A:14-2** — personal injury "shall be commenced within two years next after the
  cause of any such action shall have accrued."

## Facts verified 2026-10-01 (re-verify before reuse)

- **N.J.S.A. 34:15-8** — no one "in the same employ as the person injured" is liable at
  common law, "except for intentional wrong."
- **N.J.S.A. 34:15-40(b)/(c)/(e)/(f)** — carrier reimbursed "less employee's expenses of suit
  and attorney's fee"; expenses **not in excess of $750**; fee **not in excess of 33 1/3%**
  of the reimbursed portion; if the recovery is less than the carrier's liability the carrier
  owes the difference; after **1 year** the carrier may, **10 days** after written demand,
  sue or settle itself and its recovery bars the employee's.
- **N.J.S.A. 34:15-79** — a contractor becomes liable for comp owed to an uninsured sub's
  employees. Penalties for failure to insure: disorderly persons offense, fourth-degree crime
  if knowing; up to $5,000 for a failure of at least 10 consecutive days plus up to $5,000
  per additional 10-day period.
- **N.J.S.A. 2A:58C-2** — manufacturing defect, inadequate warnings, design defect; standard
  is "not reasonably fit, suitable or safe for its intended purpose."
- ***Laidlow v. Hariton Machinery Co.***, **170 N.J. 602 (2002)** — intentional wrong
  **applied**: guard off ~13 years, two near-misses, three complaints, restored only for OSHA.
- ***Van Dunk v. Reckson Assocs. Realty Corp.***, **210 N.J. 449 (2012)** — **not** applied
  despite a willful OSHA violation for an unshored trench collapse. A willful OSHA violation
  "is not conclusive"; "[t]he mere knowledge and appreciation of a risk — something short of
  substantial certainty — is not intent."
- **N.J.S.A. 34:15-17** — notice: 14 days clean; within 30 days a defect bars only to the
  extent of prejudice; "[u]nless knowledge be obtained, or notice given, within ninety days
  after the occurrence of the injury, no compensation shall be allowed."
- **N.J.S.A. 34:15-51** — comp petition within two years of the accident or last payment.
- **2026 comp maximum weekly benefit: $1,199** (2025: $1,159) for temporary disability,
  permanent total, permanent partial and dependency — NJDOL press release 2025-12-29.

⚠️ **Fact-check trap, 2026-10-01.** A secondary law-firm alert reported a 2026 NJ "wage loss
maximum" of **$1,598.66**. That is not in the NJDOL release and looks like the
**Pennsylvania** figure from a two-state summary. Take the comp max from
`nj.gov/labor/lwdhome/press/` only.

## Facts verified 2026-09-15 (re-verify before reuse)

- **2026 minimums: $320** temporary/total (2025: $309), **$35** permanent partial (unchanged)
  — NJ Division of Workers' Compensation, Rates and Statistics.
- Rates are **set by the date of the accident**, not the date of payment.
- **N.J.S.A. 34:15-12** — temporary disability 70% of weekly wages, **not beyond 400 weeks**;
  permanent total 70% for **450 weeks**, extendable if the worker shows it remains impossible
  to earn prior wages; partial permanent paid as a corresponding portion of **600 weeks**.
- **N.J.S.A. 34:15-12(c) schedule** — hand 260 weeks (300 where loss of function is 25% or
  more), arm 330, foot 250 (285 at the same threshold), leg 315, eye 200, thumb 80, first
  finger 60, great toe 40, hearing in both ears 200.
- **N.J.S.A. 34:15-14** — no compensation other than medical aid until disabled **seven
  days**; if disability extends beyond seven days the waiting period "shall at once become
  payable."
- **N.J.S.A. 34:15-13** — death benefits 70% of wages, **450 weeks**; spouse for life unless
  remarriage; minors to 18, or 23 if enrolled full time; burial **not to exceed $5,000**.
- **IRS Publication 525** — workers' comp for occupational injury generally excluded from
  income; exceptions for amounts exceeding lost wages on return to work, and Social Security
  offset.

## Facts verified 2026-09-01 (re-verify before reuse)

- **N.J.S.A. 34:15-39.1** — unlawful to discharge or discriminate because the employee
  "claimed or attempted to claim" comp benefits, or testified / is about to testify. Fine
  **$100–$1,000**, or up to **60 days** jail, or both; employee restored with lost wages.
- **N.J.S.A. 34:15-39.2** — additional penalty **up to $1,000**.
- **NJ Model Civil Jury Charge 2.41** — three elements; the claim must have "played a role
  and made an actual difference"; circumstantial evidence permitted. Cites *Cerrachio v.
  Alden Leeds, Inc.*, 223 N.J. Super. 435 (App. Div. 1988) for "attempted to claim."
- ***Lally v. Copygraphics***, 85 N.J. 668 (1981) — common-law retaliatory discharge action,
  compensatory **and punitive** damages, on top of statutory remedies.
- **CEPA, N.J.S.A. 34:19-5** — **one year** to sue. **N.J.S.A. 34:19-8** — filing under CEPA
  waives other contract, State-law and common-law remedies. **The trap worth repeating.**
- ***Montells v. Haynes***, 133 N.J. 282 (1993) — LAD claims get **two years** under 2A:14-2.
- **NJDOL Form SCF-4** — signed, notarized, filed in duplicate, Office of Special
  Compensation Funds, P.O. Box 399, Trenton NJ 08625-0399.

## Facts verified 2026-08-19 (re-verify before reuse)

- NJ minimum auto liability from **Jan 1, 2026: $35k/$70k BI, $25k PD** (P.L. 2022 c.87;
  DOBI Bulletin 25-06). Basic Policy unchanged.
- Verbal threshold categories, **N.J.S.A. 39:6A-8(a)**: death; dismemberment; significant
  disfigurement or significant scarring; displaced fractures; loss of a fetus; permanent
  injury within a reasonable degree of medical probability.
- Physician certification due **60 days after the answer**; objective clinical evidence;
  under penalty of perjury.
- *DiProspero v. Penn*, 183 N.J. 477 (2005) killed the "serious life impact" requirement.
