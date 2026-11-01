# Website-from-scratch plan reference

Use this file for Workflow 5: planning a new small business website.

## Contents

1. Discovery brief
2. Sitemap patterns
3. Page blueprints
4. Copy outline format
5. Launch checklist
6. Content to-do list
7. Output template

## 1. Discovery brief

Ask in one grouped message; skip what is already known.

1. What do you sell, and to whom? (one sentence each)
2. Where do you operate (town, region, online only)?
3. Top 3 services or products, in the order you most want to sell them.
4. What should a visitor do: call, book, request a quote, buy, sign up, visit?
5. What makes you different from the two competitors customers compare you with?
6. What proof do you have: reviews (where, how many), photos of work, clients,
   qualifications, years trading?
7. How would you describe your voice: three words.
8. Who will write and update content, and on what platform (if chosen)?
9. Any must-haves: booking system, shop, blog, languages, member area?

If the user wants to move fast, proceed with clearly labeled assumptions.

## 2. Sitemap patterns

Start small. Each page must answer a customer question or target a search people
make. Add pages when there is content to fill them, not before.

**Local service business** (plumber, salon, clinic, trades):

```
Home
Services
  Service A (one page per core service that people search for)
  Service B
  Service C
Areas served (only if covering several towns, with genuinely local content)
About
Reviews / Our work
Contact / Book
Legal: Privacy, Terms
```

**Freelancer or consultant**:

```
Home
Services (or "How I help")
Work / Case studies
About
Contact / Book a call
Writing (optional, only if publishing regularly)
Legal: Privacy
```

**Small product or e-commerce brand**:

```
Home
Shop (category pages)
  Product pages
About / Our story
FAQ / Delivery and returns
Contact
Legal: Privacy, Terms, Returns, Cookies
```

**SaaS or app (early stage)**:

```
Home
Features (or by use case)
Pricing
Customers / Case studies (when real ones exist)
About
Docs / Help
Sign in / Start trial
Legal: Privacy, Terms, Security
```

Navigation: five to seven top-level items at most; primary CTA as a button at the
right of the header; contact details in the footer on every page (supports WCAG
3.2.6 Consistent Help).

## 3. Page blueprints

Sections in recommended order. Adapt, do not force every section.

### Home
1. Hero: headline (what plus who plus outcome), subheadline (how or where), primary
   CTA, optional secondary CTA, hero image of the real product, work or team.
2. Proof strip: rating with source and count, client logos, or a key credential
   (only real ones).
3. Problems we solve / who it is for: three short cards.
4. Services or products overview: cards linking to detail pages.
5. How it works: three or four steps from first contact to result.
6. Featured testimonial or case study.
7. Why us: differentiators with evidence.
8. FAQ: top five objections.
9. Final CTA block with contact options.
10. Footer: contact, hours, area, social links, legal links.

### Service page (one per core service)
1. Headline naming the service and location or audience.
2. Who it is for and the problem it solves.
3. What is included, process, timeline.
4. Pricing or "from" price and what changes the price.
5. Proof specific to this service.
6. FAQ specific to this service.
7. CTA (and a short form or booking embed).
8. Links to related services.

### About
1. Why the business exists (short story tied to customer benefit).
2. Real people with photos and roles.
3. Credentials, memberships, insurance.
4. Values in practice (examples, not slogans).
5. CTA.

### Reviews / Our work
1. Gallery or case studies with context: problem, approach, result.
2. Reviews with name, location or role, date, and source link where possible.
3. CTA.

### Contact / Book
1. The one preferred action first (booking widget, quote form, phone).
2. Short form: name, contact method, message, optional details.
3. What happens next and response time.
4. Address, map, hours, service area, phone as a `tel:` link.

### Pricing (SaaS or packaged services)
1. Two to four tiers, recommended tier highlighted.
2. What is included, in customer language.
3. FAQ on billing, cancellation, refunds.
4. Proof and CTA.

## 4. Copy outline format

For each page, deliver an outline, not finished copy, unless asked:

```markdown
### [Page name] - /url-slug
**Purpose:** ...
**Primary CTA:** ...
**Target search (if any):** ...

| Section | Headline direction | Key points | Proof to place |
|---|---|---|---|
| Hero | Outcome for [audience] in [place] | ... | Google rating [to confirm] |

**Internal links:** ...
**Title tag (under about 60 chars):** ...
**Meta description (under about 155 chars):** ...
```

Use placeholders for any proof or number not supplied by the user.

## 5. Launch checklist

Technical:
- [ ] HTTPS everywhere; www/non-www and http/https redirect to one version.
- [ ] Unique `<title>` and meta description per page.
- [ ] `lang` attribute, viewport meta, favicon.
- [ ] XML sitemap and robots.txt; submit to Google Search Console and Bing
      Webmaster Tools.
- [ ] Local business: Google Business Profile complete and consistent name,
      address and phone (NAP) with the site.
- [ ] Structured data where relevant (LocalBusiness, Product, FAQ only where
      visible on the page); validate with the Rich Results Test.
- [ ] 404 page with links home and to contact.
- [ ] Images compressed and sized; Core Web Vitals checked in PageSpeed Insights.
- [ ] Security headers basics (see `performance.md`).

Accessibility:
- [ ] Keyboard walk-through, visible focus, skip link.
- [ ] Contrast checked, alt text written, form labels present.
- [ ] Run `scripts/page_audit.py` on exported HTML of key pages.

Measurement:
- [ ] Analytics installed with consent handling appropriate to the region.
- [ ] Conversions tracked: form submit, call click, booking, purchase.

Legal (owner to confirm with local rules):
- [ ] Privacy policy, cookie notice where required, terms for e-commerce,
      business registration details where required.

## 6. Content to-do list

Typical items to hand the owner:

- 10 to 20 real photos: team, premises, work in progress, finished results.
- 3 to 6 customer quotes with permission (name, role or town).
- Price ranges or "from" prices.
- Credentials, insurance and membership numbers.
- Answers to the 10 questions customers ask most on the phone.
- Logo files (SVG preferred) and brand colours (hex values).

## 7. Output template

```markdown
## Website plan: [business]

### Brief (with assumptions marked)
### Sitemap
### Page plans
### Launch checklist
### Content to-do for you
```
