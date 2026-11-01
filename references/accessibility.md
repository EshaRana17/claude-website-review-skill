# Accessibility reference (WCAG 2.2 AA essentials)

Use this file for Workflow 3.

## Contents

1. Standard and scope
2. What changed in WCAG 2.2
3. Essentials checklist with fixes
4. Severity guide
5. Manual test routine
6. Output template

## 1. Standard and scope

- **Standard**: Web Content Accessibility Guidelines (WCAG) 2.2, a W3C
  Recommendation first published 5 October 2023; the current edition is dated
  12 December 2024. Source: https://www.w3.org/TR/WCAG22/
- **Target level**: AA, which includes all level A criteria. AA is the level most
  laws and procurement rules reference (for example EN 301 549 in the EU, which the
  European Accessibility Act relies on, and the ADA Title II rule in the US, which
  names WCAG 2.1 AA). Meeting 2.2 AA also meets 2.1 AA except for the removed 4.1.1.
- **Scope of this skill**: the essentials that small sites most often fail. It is
  not a full conformance audit. Say this in every report. Automated tools find only
  part of the issues; manual testing is required for a full picture.
- If the user references a newer W3C publication, defer to it and note the
  difference.

## 2. What changed in WCAG 2.2

Removed: **4.1.1 Parsing** (obsolete; modern browsers and assistive technology
handle markup errors consistently).

Added (level in brackets):

| Criterion | Level | In one line |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | A focused element is not entirely hidden by sticky headers, cookie bars or chat widgets |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | No part of the focused element is hidden |
| 2.4.13 Focus Appearance | AAA | Focus indicator meets size and contrast rules |
| 2.5.7 Dragging Movements | AA | Anything done by dragging also works with single clicks or taps |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets at least 24 by 24 CSS px, or enough spacing, with exceptions |
| 3.2.6 Consistent Help | A | Help options (contact, chat, FAQ) appear in the same relative place across pages |
| 3.3.7 Redundant Entry | A | Do not make users re-type information already given in the same process |
| 3.3.8 Accessible Authentication (Minimum) | AA | Login does not rely on a cognitive test (memorizing, transcribing) without an alternative such as paste or password managers |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | Stricter version with fewer exceptions |

For an AA review, the six A and AA additions apply.

## 3. Essentials checklist with fixes

### Contrast

- **1.4.3 Contrast (Minimum), AA**: body text at least 4.5:1 against its background;
  large text (at least 18 pt / 24 CSS px, or 14 pt / about 18.7 CSS px bold) at
  least 3:1. Placeholder text and text over images count.
- **1.4.11 Non-text Contrast, AA**: UI component boundaries (input borders, toggle
  states) and meaningful graphics at least 3:1 against adjacent colours.
- **1.4.1 Use of Color, A**: colour is not the only way to convey meaning (links in
  body text need underline or another cue; errors need text, not only red).

From screenshots, contrast is an estimate; ask for hex values or run a checker on
the live page. Common fixes: darken grey text (for example `#767676` is about the
lightest grey that passes 4.5:1 on white), add a scrim behind text over photos.

```css
.hero { position: relative; }
.hero::before { content: ""; position: absolute; inset: 0;
  background: rgb(0 0 0 / 0.55); }          /* scrim for text over image */
.hero > * { position: relative; }
a { text-decoration: underline; text-underline-offset: 0.15em; }
```

### Text alternatives

- **1.1.1 Non-text Content, A**: informative images have `alt` that conveys the
  same information; decorative images have `alt=""`; functional images (icon
  buttons, linked logos) describe the action or destination.

```html
<img src="team.jpg" alt="Ana and Raj fitting a kitchen worktop" width="800" height="533">
<img src="divider.svg" alt="">                       <!-- decorative -->
<a href="/"><img src="logo.svg" alt="Brightside Plumbing home"></a>
<button aria-label="Open menu"><svg aria-hidden="true">...</svg></button>
```

Do not start alt with "Image of". Do not stuff keywords.

- **1.2.2 Captions (Prerecorded), A**: videos with speech have captions.

### Structure

- **1.3.1 Info and Relationships, A**: headings use `h1` to `h6` in a logical
  outline; lists use list markup; tables have header cells.
- **2.4.6 Headings and Labels, AA**: headings and labels describe the content.
- **2.4.1 Bypass Blocks, A**: a skip link or landmarks let users skip repeated
  navigation.
- **2.4.2 Page Titled, A** and **3.1.1 Language of Page, A**.

```html
<html lang="en">
<title>Emergency Plumber in Leeds | Brightside Plumbing</title>
<a class="skip" href="#main">Skip to content</a>
<header>...</header><nav aria-label="Main">...</nav>
<main id="main">...</main><footer>...</footer>
```

```css
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 1rem; top: 1rem; z-index: 1000; }
```

One `h1` per page is a common convention and helps users, though not strictly
required by WCAG. Skipped levels (h2 to h4) are a 1.3.1 risk when they misrepresent
structure.

### Forms

- **3.3.2 Labels or Instructions, A** and **4.1.2 Name, Role, Value, A**: every
  input has a programmatic label. Placeholder text is not a label.
- **1.3.5 Identify Input Purpose, AA**: personal data fields use `autocomplete`.
- **3.3.1 Error Identification, A** and **3.3.3 Error Suggestion, AA**: errors are
  described in text and suggest a fix.
- **3.3.7 Redundant Entry, A**: offer "same as billing address" and similar.

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-describedby="email-err">
<p id="email-err" class="error" hidden>Enter an email like name@example.com</p>
```

When showing an error, set `aria-invalid="true"` on the field and reveal the
message; move focus to an error summary on submit for long forms.

### Keyboard and focus

- **2.1.1 Keyboard, A** and **2.1.2 No Keyboard Trap, A**: everything works with
  Tab, Shift+Tab, Enter, Space, arrow keys where expected, and Escape closes
  dialogs.
- **2.4.3 Focus Order, A**: order follows the visual order.
- **2.4.7 Focus Visible, AA**: never remove outlines without a replacement.
- **2.4.11 Focus Not Obscured (Minimum), AA**: sticky headers, cookie banners and
  chat bubbles must not fully cover the focused element.

```css
:focus-visible { outline: 3px solid #1a5fd0; outline-offset: 2px; }
html { scroll-padding-top: 5rem; }   /* keeps focused items clear of a sticky header */
```

Use real `<button>` and `<a href>` elements instead of clickable `div`s. If a
custom control is unavoidable it needs `role`, `tabindex="0"` and key handlers.

### Pointer and targets

- **2.5.8 Target Size (Minimum), AA**: at least 24 by 24 CSS px, unless spacing
  keeps a 24 px circle around each target clear of others, or the target is inline
  in text, or an equivalent control exists. Small icon links in footers and
  close buttons on pop-ups are frequent failures.
- **2.5.7 Dragging Movements, AA**: sliders, carousels and drag-to-reorder have
  button alternatives.
- **2.5.3 Label in Name, A**: the accessible name contains the visible text
  (do not set `aria-label="Menu toggle"` on a button showing "Open menu").

```css
.icon-link { display: inline-flex; min-width: 24px; min-height: 24px;
  align-items: center; justify-content: center; }
@media (pointer: coarse) { .icon-link { min-width: 44px; min-height: 44px; } }
```

### Motion and time

- **2.2.2 Pause, Stop, Hide, A**: auto-moving content that lasts more than five
  seconds (carousels, tickers, background video) can be paused.
- **2.3.1 Three Flashes or Below Threshold, A**.
- Respect reduced motion preferences (2.3.3 Animation from Interactions is AAA, but
  this is a cheap, high-value fix):

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important; transition-duration: 0.01ms !important;
    scroll-behavior: auto !important; }
}
```

### Zoom and reflow

- **1.4.4 Resize Text, AA**: usable at 200 percent zoom.
- **1.4.10 Reflow, AA**: no two-dimensional scrolling at 320 CSS px width (except
  content like maps and data tables).
- **1.4.12 Text Spacing, AA**: no loss of content when users increase spacing.
- Never block zoom: avoid `maximum-scale=1` and `user-scalable=no` in the viewport
  meta.

### Links and buttons

- **2.4.4 Link Purpose (In Context), A**: avoid lone "Click here" or "Read more";
  add context in text or visually hidden text.
- **3.2.6 Consistent Help, A**: contact links or chat in the same place on every
  page.

### Authentication

- **3.3.8 Accessible Authentication (Minimum), AA**: allow paste into password and
  code fields, support password managers (`autocomplete="current-password"`,
  `one-time-code`), and do not use puzzles without an alternative.

## 4. Severity guide

- **Blocker**: prevents a task (form cannot be submitted by keyboard, unlabeled
  required fields, CTA image with no name, focus trapped in a modal).
- **Serious**: major difficulty (body text contrast failures, missing alt on
  informative images, invisible focus, auto-playing carousel without pause).
- **Minor**: friction or best practice (heading level skips, redundant alt text,
  missing reduced-motion support).

## 5. Manual test routine (about 20 minutes)

1. Unplug the mouse: Tab through the page. Is focus always visible and never hidden?
   Can every menu, modal and form be used and closed?
2. Zoom to 200 percent, then set the window to 320 CSS px wide. Does anything
   overlap, cut off or need sideways scrolling?
3. Run a screen reader for the first screen and the main form: NVDA (Windows, free),
   VoiceOver (macOS and iOS, built in) or TalkBack (Android, built in). Are headings,
   links and fields announced meaningfully?
4. Turn on "reduce motion" in the operating system and reload.
5. Run an automated checker (Lighthouse accessibility audit in Chrome DevTools, or
   another rules engine) and treat its results as a starting point only.

## 6. Output template

```markdown
## Accessibility check: [page] (WCAG 2.2 AA essentials)

Scope: essentials review, not a full conformance audit. Inputs: [HTML / screenshot / URL].

**Summary:** X blockers, Y serious, Z minor.

| # | Issue | WCAG | Level | Severity | Where | Who it affects |
|---|---|---|---|---|---|---|

### Fixes
1. [Issue] - snippet

### Manual tests to run
- ...

### Not checked
- ...
```
