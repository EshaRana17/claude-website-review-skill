# Conversion review reference

Use this file for Workflow 1. It holds the scoring rubric, the checks behind each
dimension, impact and effort guidance, and notes on testing.

## Contents

1. The 5-second test
2. Scoring rubric (8 dimensions, 0 to 5)
3. Dimension checks
4. Ranking fixes
5. Page-type adjustments
6. Testing and traffic
7. Common anti-patterns

## 1. The 5-second test

Look only at the first screen. On mobile that is roughly the first 600 to 700 CSS px
of height; on desktop roughly the first 800 px. Answer four questions:

| Question | Pass looks like | Typical fail |
|---|---|---|
| What is it? | Category is obvious in plain words ("bookkeeping for cafes") | Clever slogan with no category ("Unlock your potential") |
| Who is it for? | Audience named or clearly implied | Speaks to "everyone" or "businesses" |
| Why care? | Concrete outcome or differentiator | Feature list or vague superlatives ("best-in-class") |
| What next? | One visible, specific primary action | No CTA above the fold, or 3+ competing CTAs of equal weight |

Partial means a visitor could work it out with effort (for example the audience is
only in the subheadline in small grey text).

If you only have pasted copy, run the test on the first 2 to 3 lines and say that
layout could not be judged.

## 2. Scoring rubric

Score each dimension 0 to 5. Total out of 40. Describe the score in words too, as
owners care more about the reason than the number.

| Score | Meaning |
|---|---|
| 0 | Missing entirely |
| 1 | Present but works against the goal |
| 2 | Weak; most visitors would miss or misread it |
| 3 | Adequate; does the job with clear gaps |
| 4 | Strong; minor polish left |
| 5 | Excellent; hard to improve without testing |

Overall bands: 0 to 15 needs a rethink; 16 to 25 fixable foundations; 26 to 33
solid, optimize; 34 to 40 strong, test refinements.

### Dimensions

1. **Value proposition clarity** - what, who, outcome, differentiator.
2. **Visual hierarchy** - the eye lands on headline, then support, then CTA.
3. **CTA strength and placement** - specific, visible, repeated at decision points.
4. **Social proof** - real, specific, relevant, near the claims it supports.
5. **Objection handling** - price, risk, time, trust, fit, effort answered.
6. **Form and checkout friction** - fields, steps, errors, surprises.
7. **Message match** - page continues the promise of the ad, search or post.
8. **Trust and credibility** - contact details, real people, policies, security.

If the traffic source is unknown, score message match as "n/a" and total out of 35,
or state the assumption.

## 3. Dimension checks

### Value proposition clarity
- Headline names the outcome or category, not just the brand.
- Subheadline explains how, for whom, or why different.
- Specifics beat adjectives: "Same-week bathroom refits in Leeds" beats "Quality
  renovations".
- Jargon count: internal terms the customer would not search for.
- Differentiator is believable and checkable (local, faster, specialist, price
  model, guarantee) rather than "passionate" or "innovative".

### Visual hierarchy
- One dominant element per screen; the headline is the largest text.
- CTA has the highest contrast colour on the page and is not repeated in that
  colour for unrelated elements.
- Scannable: short paragraphs, subheads every screen or so, meaningful images
  (product in use, real team) rather than generic stock.
- Reading pattern: important items on the left or centre of the first screen;
  nothing important hidden in carousels (later slides get little attention).
- Mobile: headline not pushed below the fold by a large hero image or banner.

### CTA strength and placement
- Verb plus outcome: "Get my free quote", "Book a 15-minute call", not "Submit"
  or "Learn more" as the primary action.
- Sets expectation of what happens next (time, cost, commitment).
- One primary action per page; secondary actions visually quieter (outline or
  text link).
- Present above the fold, after each major proof or benefit block, and at the end.
- Risk reducers next to the button, only if true: "No card needed", "Cancel any
  time", "Reply within 1 working day".
- Sticky mobile CTA for call or booking businesses, if it does not cover content.
- Tap target at least 24 by 24 CSS px (WCAG 2.2 minimum); 44 to 48 px is the
  comfortable size on mobile.

### Social proof
- Types, strongest first for small businesses: named reviews with photo or role,
  ratings from third-party platforms with count, case studies with numbers, client
  logos (with permission), certifications and memberships, press.
- Specific beats generic: a quote describing a result beats "Great service!".
- Placed next to the claim it supports, and near the CTA.
- Recency: dated or recent-feeling proof.
- If proof is missing, recommend how to collect it (follow-up email after a job,
  review request link, permission to quote). Never write sample testimonials that
  could be mistaken for real ones.

### Objection handling
Map the likely objections and check each is answered on the page:

| Objection | Typical answer element |
|---|---|
| Too expensive / unclear price | Pricing or "from" price, what is included, value framing |
| Will it work for me? | Audience fit section, use cases, examples like me |
| Is this business legit? | Address, real photos, reviews, registration numbers |
| Risky / locked in | Guarantee, trial, cancellation terms, refund policy |
| Takes too long / too much effort | Process steps ("How it works" in 3 steps), timeline |
| What happens after I click? | Expectation line under the CTA, FAQ |

An FAQ is a good home for leftover objections; write answers in the brand voice and
keep them short.

### Form and checkout friction
- Count fields. Remove anything not needed for the next step (collect it later).
- Single column, labels above fields, input types set (email, tel) for mobile
  keyboards, autocomplete attributes.
- Required vs optional is clear; errors are specific and next to the field.
- No surprise costs or account creation before purchase (offer guest checkout).
- Button text repeats the outcome ("Send my quote request").
- Privacy reassurance near email or phone fields.
- No CAPTCHA puzzles where an invisible check would do; if a cognitive test exists,
  WCAG 2.2 3.3.8 requires an alternative.

### Message match
- Headline echoes the ad or search keyword the visitor came from.
- Offer on the page equals the offer in the ad (same price, same discount).
- Ad-specific landing pages hide unrelated navigation to reduce exits.

### Trust and credibility
- Visible contact details (phone, email, address or service area).
- About section with real people.
- Policies: privacy, terms, refunds, delivery.
- HTTPS, no browser warnings, no broken images or links, current copyright year.
- Consistent branding and no typos in the first screen.

## 4. Ranking fixes

Impact is about how many visitors a fix touches and how close it is to the decision:

- **High**: first screen, primary CTA, pricing clarity, form, broken or misleading
  elements, mobile layout issues.
- **Medium**: proof placement, objection gaps, secondary sections, page speed issues
  that are noticeable but not severe.
- **Low**: polish, copy tweaks below the fold, footer items.

Effort:

- **Quick**: copy or settings change, under an hour.
- **Moderate**: design or content work, a day or so.
- **Heavy**: new pages, new proof to collect, rebuild of a component.

Sort by impact (High first), then effort (Quick first). Cap the list at 10. Each fix
must say what to change, why (evidence) and how (concrete instruction or example).

## 5. Page-type adjustments

- **Local service business**: phone and booking CTA dominant, service area in the
  headline or subheadline, reviews from local platforms, opening hours, photos of
  real work.
- **SaaS / app**: product visual early, free trial or demo CTA, pricing page link,
  integration and security notes for B2B.
- **E-commerce product page**: price, delivery cost and time, returns, stock,
  reviews near the add-to-cart button, image gallery quality.
- **Freelancer / consultant**: specialism and ideal client stated, portfolio with
  outcomes, process and availability, simple contact or booking.
- **Lead magnet / event page**: single CTA, no navigation, what they get and when,
  minimal fields.

## 6. Testing and traffic

A/B testing needs enough conversions to detect a difference. As a rough rule, a
page with fewer than about 100 conversions per variant over a few weeks cannot
reliably detect modest changes. For low-traffic small business sites recommend:

- Ship clear best-practice fixes directly, and compare before/after over similar
  periods, noting seasonality.
- Use qualitative checks: five-person hallway test, session recordings, asking
  recent customers what nearly stopped them.
- Test only big swings (new headline angle, new offer) when traffic allows.

## 7. Common anti-patterns

- Hero carousel with rotating messages.
- "Welcome to our website" headline.
- Primary CTA "Submit", "Click here" or "Learn more".
- Pop-up on page load before the visitor has read anything.
- Pricing hidden behind "Contact us" when competitors show it (sometimes valid for
  custom work; then show a "from" price or typical range if possible).
- Stock photos of handshakes and headsets.
- Testimonials with first name only and no context.
- Long form asking budget, company size and phone before any value is given.
- Chat widget covering the mobile CTA.
