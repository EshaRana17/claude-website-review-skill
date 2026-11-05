# Website Review: an Agent Skill for landing pages and small business sites

An open-source [Agent Skill](https://agentskills.io) (`SKILL.md` format) that turns
Claude, or any agent that supports skills, into a practical website reviewer for
founders, freelancers and small businesses.

It covers five workflows:

1. **Landing page conversion review**: a 5-second test, an 8-dimension scorecard
   (out of 40), and the top 10 fixes ranked by impact and effort.
2. **Copy rewrite**: headline options with rationale, subheadline, CTA variants and
   benefit-led bullets, written in your existing brand voice. It never invents
   testimonials, ratings or statistics.
3. **Accessibility check** against WCAG 2.2 level AA essentials, with copy-paste fix
   snippets and a manual test routine.
4. **Performance and technical basics**: Core Web Vitals (LCP, INP, CLS), images,
   fonts, third-party scripts, mobile layout and security headers, as a P1/P2/P3
   checklist that tells you what to look for in Lighthouse or PageSpeed Insights.
5. **Website-from-scratch plan**: sitemap, page-by-page sections, copy outlines,
   launch checklist and a content to-do list.

It also includes `scripts/page_audit.py`, a small offline Python script that checks
a saved HTML file for common markup problems.

## Repository layout

```
website-review/
  SKILL.md                    Main instructions (loaded when the skill triggers)
  references/
    conversion.md             Scorecard rubric, CRO checks, ranking rules
    copywriting.md            Voice profile, headline angles, CTAs, honesty rules
    accessibility.md          WCAG 2.2 AA essentials with fix snippets
    performance.md            Core Web Vitals, Lighthouse guide, security headers
    site-plan.md              Sitemaps, page blueprints, launch checklist
  scripts/
    page_audit.py             Offline HTML audit (Python 3 standard library only)
  assets/
    sample.html               Sample page with deliberate issues for testing
  agent.json                  Manifest (no network, no env vars)
  LICENSE                     MIT
  README.md
```

Reference files load only when the matching workflow runs, which keeps context use low.

## Example prompts

- "Review this landing page for conversions: https://example.com" (with a fetch
  or browser tool enabled), or attach a screenshot.
- "Here is my homepage copy. Rewrite the headline and CTAs but keep our friendly,
  no-jargon tone."
- "Run an accessibility check on this HTML file against WCAG 2.2 AA."
- "My site feels slow. Here is my PageSpeed Insights result. What should I fix first?"
- "I'm opening a bakery in Bristol that does custom cakes. Plan a website for me:
  sitemap, sections and copy outline."
- "Full review of my site: conversion, accessibility and speed, one combined priority list."

## Installation

The skill folder must be named `website-review` to match the `name` field in
`SKILL.md`. If you cloned this repository under another name, rename the folder (or
copy its contents into a `website-review` folder) when installing.

### Claude Code

Personal skill (available in all projects):

```bash
git clone https://github.com/EshaRana17/claude-website-review-skill.git ~/.claude/skills/website-review
```

Project skill (shared with your team through the repository):

```bash
git clone https://github.com/EshaRana17/claude-website-review-skill.git .claude/skills/website-review
```

On Windows, the personal path is `%USERPROFILE%\.claude\skills\website-review`.
Claude Code discovers the skill automatically; ask a website question or mention
the skill by name to use it.

### Claude.ai (web and desktop apps)

1. Make sure code execution is on: **Settings > Capabilities > Code execution and
   file creation** (Team and Enterprise owners enable skills under
   **Organization settings**).
2. Zip the `website-review` folder so that the ZIP contains the folder with
   `SKILL.md` inside it.
3. Go to **Customize > Skills**, click **+**, then **Create skill > Upload a skill**,
   and choose the ZIP.
4. Toggle the skill on. It triggers automatically when relevant.

Menu names can change; if these steps differ, see Anthropic's help article
"Using Skills in Claude".

### Other agents that support SKILL.md

The skill follows the open Agent Skills specification and uses no product-specific
features. Copy the `website-review` folder into the skills directory your agent
reads (check its documentation), keeping the folder structure intact. The
script needs only Python 3.8 or newer.

## Using the audit script directly

```bash
python scripts/page_audit.py assets/sample.html
python scripts/page_audit.py path/to/saved-page.html --json
```

It reports:

- missing `lang`, viewport meta (and zoom blocking), `<title>`, meta description
- images missing `alt`, `width` or `height`
- form fields with no accessible label
- heading order problems (no `h1`, several `h1`, skipped levels)
- external scripts and their hosts
- CTA-like buttons and links, flagging weak text such as "Submit"
- iframes without a `title`

Exit code 0 means no issues, 1 means issues were found, 2 means a usage or file error.
It checks markup only: it cannot see CSS, colour contrast, JavaScript-rendered content
or real-world speed.

## Security

- **Local-only script, no network.** `page_audit.py` uses only the Python standard
  library (`argparse`, `html.parser`, `json`, `pathlib`, `re`, `sys`, and
  `urllib.parse` for splitting script URLs into hostnames as text). It opens no
  sockets, makes no HTTP requests, refuses URLs as input, and reads a single local
  file (up to 10 MB). It writes nothing to disk.
- **No secrets or environment variables.** `agent.json` declares `"network": []`
  and `"env": []`.
- **No hidden instructions.** All behaviour is in readable Markdown and one Python file.
- Scanned on AgenticMart: https://agenticmart.org/verified

## Standards this skill is based on

- WCAG 2.2 (W3C Recommendation, edition of 12 December 2024):
  https://www.w3.org/TR/WCAG22/
- Core Web Vitals (LCP, INP, CLS) and thresholds: https://web.dev/articles/vitals
- Agent Skills specification: https://agentskills.io/specification

Standards evolve. If a newer version is published, the skill is instructed to defer
to it and state which version its advice is based on. Pull requests that update the
references are welcome.

## Limitations

- It gives expert-style guidance, not a legal accessibility conformance statement.
- Speed findings without PageSpeed or Lighthouse data are hypotheses to verify.
- Reviewing a live URL requires the host agent to have a web fetch or browser tool.

## Contributing

Issues and pull requests are welcome. Please keep the skill free of invented
statistics, keep `SKILL.md` concise, and put detail in `references/`.

## License

MIT. Copyright (c) 2026 Esha Sabir. See [LICENSE](LICENSE).
