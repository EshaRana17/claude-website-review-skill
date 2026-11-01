---
name: website-review
description: Reviews websites and landing pages for founders, freelancers and small businesses. Scores conversion (5-second test, value proposition, hierarchy, CTAs, social proof, objections, form friction) and returns a ranked top 10 fix list; rewrites homepage and landing page copy in the brand's own voice; checks accessibility against WCAG 2.2 AA essentials with fix snippets; audits page speed and technical basics (Core Web Vitals LCP, INP, CLS, images, fonts, third-party scripts, mobile, security headers); and plans a new small business website from scratch. Use when the user shares a URL, screenshot, HTML or pasted copy and mentions a website, landing page, homepage copy, conversion, CRO, accessibility, a11y, page speed, Lighthouse or PageSpeed, or asks for a site plan or sitemap.
license: MIT
metadata:
  author: Esha Sabir
  version: "1.0.0"
---

# Website Review

A practical reviewer for small business websites and landing pages. It produces
evidence-based findings, scores and prioritized fixes that a non-specialist owner
can act on this week.

## Pick the workflow

Read the request and choose one or more workflows. If the user just says "review my
site", run Workflow 1 and offer 3 and 4 as follow-ups.

| User asks about | Workflow | Load reference |
|---|---|---|
| "Why isn't this converting?", review, CRO, homepage feedback | 1. Conversion review | `references/conversion.md` |
| Rewrite headline, copy, CTA, bullets | 2. Copy rewrite | `references/copywriting.md` |
| Accessibility, a11y, WCAG, screen readers, contrast | 3. Accessibility check | `references/accessibility.md` |
| Slow site, page speed, Lighthouse, Core Web Vitals, headers | 4. Performance and technical | `references/performance.md` |
| New site, sitemap, "what pages do I need" | 5. Site plan | `references/site-plan.md` |

Load only the reference file(s) the chosen workflow needs.

## Inputs and what they allow

Work with whatever the user provides and say plainly what could not be checked.

- **URL**: if a fetch or browser tool is available, read the page. If not, ask for a
  screenshot, pasted copy or saved HTML. Never pretend to have visited a page.
- **Screenshot**: good for hierarchy, above-the-fold content, visual contrast
  (estimate only), CTA placement. Cannot verify alt text, labels, headers or speed.
- **Pasted copy**: good for messaging and copy. Cannot judge layout or visuals.
- **HTML file**: good for structure and accessibility markup. Run
  `scripts/page_audit.py` on it (see below). Cannot measure real-world speed.
- **Lighthouse or PageSpeed report** (pasted or exported): use it as the source of
  truth for performance numbers.

Before starting, collect (or infer and state assumptions about): who the page is for,
the single primary action the page wants, and the traffic source (ads, search,
social, referral). If missing, ask one short question or state the assumption and
continue.

## Ground rules

1. **Evidence first.** Every finding cites what was observed (quote the copy,
   name the element, give the measured value). No generic advice without a hook
   in the actual page.
2. **No invented facts.** Never fabricate testimonials, reviews, customer counts,
   statistics, awards, logos or guarantees. Where proof is missing, use a clearly
   marked placeholder such as `[real customer quote here]` and say what to collect.
3. **Keep the brand voice.** Rewrites match the existing tone, reading level and
   vocabulary unless the user asks for a new voice.
4. **Prioritize by impact and effort.** Owners have limited time. Rank fixes, do not
   dump checklists.
5. **Separate measured from estimated.** Mark contrast ratios guessed from a
   screenshot or speed issues inferred from markup as estimates.
6. **Standards stated precisely.** Use the facts in the reference files (WCAG 2.2,
   Core Web Vitals thresholds). If the user cites a newer standard, defer to it and
   say which version the advice is based on.
7. **Plain language.** Explain jargon in a few words the first time it appears.

## Workflow 1: Landing page conversion review

Details, scoring rubric and checks: `references/conversion.md`.

Steps:

1. **5-second test.** From only the first screen (above the fold on mobile and
   desktop if both are available), answer: What is it? Who is it for? Why should
   I care (outcome or differentiator)? What do I do next? Mark each Pass / Partial /
   Fail and quote the text that answers it.
2. **Score the eight dimensions** (0 to 5 each) using the rubric in the reference:
   clarity of value proposition, visual hierarchy, CTA strength and placement,
   social proof, objection handling, form and checkout friction, message match with
   traffic source, trust and credibility signals.
3. **List issues** with evidence, impact (High / Medium / Low) and effort
   (Quick / Moderate / Heavy).
4. **Rank the top 10 fixes** by impact first, then by effort (quick wins higher).
5. **Suggest tests** for the top 2 or 3 fixes if the site has enough traffic
   (see the traffic note in the reference); otherwise recommend just shipping them.

Output template:

```markdown
## Conversion review: [page name]

**Assumed audience:** ... | **Primary action:** ... | **Traffic source:** ...

### 5-second test
| Question | Result | Evidence |
|---|---|---|
| What is it? | Pass/Partial/Fail | "quoted headline" |
| Who is it for? | ... | ... |
| Why care? | ... | ... |
| What next? | ... | ... |

### Scorecard (total X / 40)
| Dimension | Score (0-5) | One-line reason |
|---|---|---|

### Top 10 fixes (ranked by impact)
1. **[Fix]** - Impact: High | Effort: Quick
   Why: ... Evidence: ... How: ...

### What is already working
- ...

### Not checked
- ... (and what input would allow it)
```

## Workflow 2: Copy rewrite

Details, formulas and voice-matching method: `references/copywriting.md`.

Steps:

1. **Capture the voice.** Note tone (for example warm, direct, technical, playful),
   sentence length, person (we/you/I), words the brand uses and avoids. State this
   voice profile in two or three lines before rewriting.
2. **Find the core message.** Customer, problem, outcome, differentiator, proof
   available. If the differentiator is unclear, ask, or offer two framings.
3. **Write headline options** (5 is a good default), each using a different angle
   (outcome, problem, audience call-out, differentiator, specificity). Give a one-line
   rationale for each and recommend one.
4. **Write a subheadline** that adds the how, who or proof the headline left out.
5. **Write CTA variants** (3 to 5): verb-led, specific about what happens next,
   with an optional risk reducer line underneath (for example "No card needed"),
   only if true for this business.
6. **Rewrite feature bullets as benefits**: feature, then what it means for the
   customer. Keep claims the user can stand behind.
7. **Flag claims that need proof** and list the evidence to collect instead of
   inventing it.

Output: voice profile, headline table (option, angle, rationale), recommended pick,
subheadline, CTA list, before/after bullets, proof-needed list.

Never write fake testimonials, review counts, ratings, customer logos, "as seen in"
lines or numeric results the user has not supplied.

## Workflow 3: Accessibility check (WCAG 2.2 AA essentials)

Details, criteria list and fix snippets: `references/accessibility.md`.

WCAG 2.2 has been a W3C Recommendation since October 2023 (latest edition dated
12 December 2024). It removed 4.1.1 Parsing and added nine success criteria, six of
which are at level A or AA. This check covers the essentials most small sites fail;
it is not a full conformance audit, and say so in the output.

Steps:

1. If HTML is available, run `scripts/page_audit.py` and use its output as evidence.
2. Check the essentials in this order: text contrast, non-text contrast, alternative
   text, headings and landmarks, form labels and errors, keyboard access and visible
   focus, focus not obscured, target size, motion and animation, language and page
   title, link and button names.
3. For each failure give: criterion number and name, level, where it occurs,
   who it affects, and a copy-paste fix snippet.
4. Recommend a manual test pass: keyboard-only walk-through, 200 percent zoom and
   320 CSS px width reflow, and one screen reader (NVDA, VoiceOver or TalkBack).

Output: summary (blocker / serious / minor counts), findings table, fix snippets,
manual test checklist, "not checked" list.

## Workflow 4: Performance and technical basics

Details, thresholds and measurement guide: `references/performance.md`.

Core Web Vitals are LCP (loading), INP (responsiveness, replaced FID in March 2024)
and CLS (visual stability). Good thresholds at the 75th percentile of page loads:
LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less.

Steps:

1. Ask whether the user has a PageSpeed Insights or Lighthouse result. Field data
   (real users, from the Chrome UX Report) outranks lab data; say which you have.
2. Without measurements, infer likely issues from markup or screenshots and label
   them as hypotheses to verify.
3. Check: LCP element and how it loads, image formats and sizing, font loading,
   render-blocking CSS and JS, third-party scripts, layout shift sources, mobile
   viewport and tap targets, caching and compression, HTTPS and security headers.
4. Output a prioritized checklist: P1 (fix now), P2 (this month), P3 (nice to have),
   each with "how to measure" naming the exact Lighthouse audit or PageSpeed field.

## Workflow 5: Website-from-scratch plan

Details, page blueprints and copy outlines: `references/site-plan.md`.

Steps:

1. **Brief.** Collect business type, location or service area, main customer,
   top 3 services or products, primary conversion (call, booking, quote, purchase,
   sign-up), proof available, brand voice, budget for content. Ask for gaps in one
   grouped question, or proceed with stated assumptions.
2. **Sitemap.** Start minimal (typically 5 to 8 pages). Justify every page by a
   customer question it answers or a search it can rank for.
3. **Page-by-page plan.** For each page: purpose, primary CTA, sections in order,
   copy outline (headline direction plus key points), proof to place, internal links.
4. **Launch checklist.** Technical, accessibility, analytics and legal basics.
5. **Content to-do list** for the owner (photos, quotes, numbers to collect).

Output: brief recap, sitemap tree, page plans, launch checklist, content to-do.

## Helper script: page_audit.py

`scripts/page_audit.py` is a standard-library-only Python 3 script. It reads one
local HTML file and never touches the network. Use it whenever the user provides
HTML (saved page, export or source).

```bash
python scripts/page_audit.py path/to/page.html            # readable report
python scripts/page_audit.py path/to/page.html --json     # machine-readable
```

It reports: missing `lang`, viewport meta, title and meta description; images
without `alt` or without `width`/`height`; form fields without an accessible
label; heading order problems (skipped levels, missing or multiple `h1`); count of
external scripts and their hosts; CTA-like buttons and links.

Exit code is 0 when no issues are found, 1 when issues are found, 2 on usage or
file errors. Treat its findings as markup evidence only: it cannot see CSS, contrast,
JavaScript-rendered content or real performance. A sample file to try it on is at
`assets/sample.html`.

If the user only gives a URL, do not download pages with the script. Ask them to
save the page (browser "Save page as", HTML only) or paste the source.

## Combining workflows

For a "full review", run 1, then 3 and 4 in short form (top findings only), and
finish with a single merged priority list of no more than 10 items so the owner
has one plan, not three.

## Quality checklist before replying

- Every score and finding has evidence from the page.
- No invented proof, numbers or quotes.
- Fixes are ranked and each has impact and effort.
- Standards are cited by number and version where relevant.
- The "not checked" section is honest about input limits.
- Rewrites match the stated voice profile.
