# Performance and technical basics reference

Use this file for Workflow 4.

## Contents

1. Core Web Vitals facts
2. Field vs lab data and where to measure
3. Prioritized checklist (P1, P2, P3)
4. Fix snippets
5. Security headers basics
6. Mobile layout basics
7. Output template

## 1. Core Web Vitals facts

Source: https://web.dev/articles/vitals and the individual metric pages on web.dev.

| Metric | Measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| LCP, Largest Contentful Paint | Loading: when the largest image or text block in the viewport renders | 2.5 s or less | over 2.5 s up to 4.0 s | over 4.0 s |
| INP, Interaction to Next Paint | Responsiveness: latency of clicks, taps and key presses across the visit | 200 ms or less | over 200 ms up to 500 ms | over 500 ms |
| CLS, Cumulative Layout Shift | Visual stability: unexpected movement of content | 0.1 or less | over 0.1 up to 0.25 | over 0.25 |

- Assessed at the **75th percentile** of page loads, separately for mobile and
  desktop. A page passes when all three are good at p75.
- **INP replaced First Input Delay (FID)** as a Core Web Vital on 12 March 2024.
  Do not report FID as a Core Web Vital.
- Other useful diagnostics (not Core Web Vitals): TTFB (time to first byte), FCP
  (first contentful paint), TBT (total blocking time, a lab proxy for
  responsiveness).
- If the user cites newer thresholds or metrics from web.dev, defer to them.

## 2. Field vs lab data and where to measure

- **Field data** (real Chrome users, from the Chrome UX Report): shown at the top of
  PageSpeed Insights (https://pagespeed.web.dev/) when the page or origin has enough
  traffic, and in Google Search Console's Core Web Vitals report. This is what
  counts for the pass/fail assessment.
- **Lab data** (Lighthouse, simulated device and network): good for diagnosing, but
  a single run varies; run three times and use the median. Lighthouse in navigation
  mode cannot measure INP because there is no user interaction; use TBT as a proxy,
  or a Lighthouse timespan recording or the DevTools Performance panel while
  interacting.
- Small sites often have no field data. Then rely on lab data and say so.

Where to look (names of Lighthouse audits and insights change between versions;
search the report for these terms if the exact label differs):

| Question | Where in PageSpeed Insights / Lighthouse |
|---|---|
| What is the LCP element and why is it slow? | "LCP breakdown" and "LCP request discovery" insights, or the "Largest Contentful Paint element" diagnostic |
| Oversized or old-format images? | "Improve image delivery" (older: "Properly size images", "Serve images in next-gen formats") |
| Render-blocking CSS/JS? | "Render blocking requests" (older: "Eliminate render-blocking resources") |
| Layout shift sources? | "Layout shift culprits" (older: "Avoid large layout shifts"), "Image elements do not have explicit width and height" |
| Font issues? | "Font display" insight |
| Third parties? | "3rd parties" insight / "Reduce the impact of third-party code" |
| Slow server? | "Document request latency" insight, TTFB |
| Caching? | "Use efficient cache lifetimes" |
| JS cost? | "Reduce unused JavaScript", "Minimize main-thread work", TBT |

## 3. Prioritized checklist

### P1: fix now (biggest wins for small sites)

1. **Hero image is the LCP element and is heavy or lazy-loaded.** Compress, serve
   AVIF or WebP with a fallback, size it for the viewport, do not lazy-load it, add
   `fetchpriority="high"`.
2. **Images without `width` and `height`** (or CSS `aspect-ratio`) causing layout
   shift.
3. **Huge images** (multi-megabyte photos straight from a camera or phone). Resize
   to the largest displayed size times device pixel ratio (about 2x), use `srcset`.
4. **Too many third-party scripts**: chat widgets, multiple analytics tags, heat
   maps, social embeds, A/B testing tools. Remove unused ones; load the rest after
   interaction or with `defer`.
5. **Render-blocking scripts in `<head>`** without `defer` or `async`.
6. **No HTTPS or mixed content.**
7. **Missing or broken viewport meta** causing a desktop layout on phones.

### P2: this month

1. Web fonts: limit families and weights, self-host or preconnect, use
   `font-display: swap` (or `optional`), preload the one critical font file, use
   WOFF2, match fallback metrics to limit shift.
2. Late-injected banners (cookie bars, promos) pushing content down; reserve space
   or overlay them.
3. Heavy JavaScript handlers on click (INP): break up long tasks, avoid large
   framework re-renders on simple interactions, yield to the main thread.
4. Caching: long `Cache-Control` max-age for versioned static assets; compression
   (Brotli or gzip) on text responses.
5. Slow server response (TTFB): use a CDN or the host's cache; avoid redirect
   chains (http to https to www to page).
6. Video backgrounds: replace with a poster image on mobile or use a lightweight
   click-to-play.
7. Security headers beyond HTTPS (section 5).

### P3: nice to have

1. Preconnect to critical third-party origins.
2. Inline critical CSS for above-the-fold content.
3. Remove unused CSS and JavaScript from page builders and themes.
4. Use `content-visibility: auto` for long pages below the fold.
5. Use the bfcache-friendly patterns (avoid `unload` handlers).

## 4. Fix snippets

```html
<!-- LCP hero image: responsive, modern formats, high priority, no lazy loading -->
<picture>
  <source type="image/avif" srcset="hero-800.avif 800w, hero-1600.avif 1600w" sizes="100vw">
  <source type="image/webp" srcset="hero-800.webp 800w, hero-1600.webp 1600w" sizes="100vw">
  <img src="hero-1600.jpg" alt="..." width="1600" height="900" fetchpriority="high">
</picture>

<!-- Below-the-fold images -->
<img src="gallery-1.webp" alt="..." width="600" height="400" loading="lazy" decoding="async">

<!-- Scripts -->
<script src="/js/site.js" defer></script>

<!-- Fonts -->
<link rel="preload" href="/fonts/brand.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: "Brand";
  src: url("/fonts/brand.woff2") format("woff2");
  font-display: swap;
}
img, video { max-width: 100%; height: auto; }
.embed { aspect-ratio: 16 / 9; }   /* reserve space for iframes and embeds */
```

Load a chat widget only when asked for:

```html
<button id="chat-btn" type="button">Chat with us</button>
<script>
  document.getElementById("chat-btn").addEventListener("click", function () {
    var s = document.createElement("script");
    s.src = "https://chat.example.com/widget.js"; /* vendor URL */
    document.body.appendChild(s);
  }, { once: true });
</script>
```

## 5. Security headers basics

Check response headers in the browser DevTools Network panel (select the document
request) or by asking the user for their host's header settings. Reference:
MDN Web Docs (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) and the
OWASP Secure Headers Project.

| Header | Basic recommendation | Notes |
|---|---|---|
| HTTPS | Whole site on HTTPS, HTTP redirects to HTTPS with a single 301 | Free certificates via the host or Let's Encrypt |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` once every subdomain is HTTPS | Start with a short max-age; add `preload` only after reading the preload list requirements, as removal is slow |
| `Content-Security-Policy` | Start in `Content-Security-Policy-Report-Only` mode, then enforce | Page builders and tag managers need careful allow-lists; `frame-ancestors 'self'` is an easy first win |
| `X-Content-Type-Options` | `nosniff` | Low risk |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | The modern browser default; set it explicitly |
| `Permissions-Policy` | Disable features not used, for example `camera=(), microphone=(), geolocation=()` | Adjust if the site uses them |
| Clickjacking | `frame-ancestors` in CSP (or `X-Frame-Options: SAMEORIGIN` for older browsers) | |

A starter CSP for a simple static site (adjust to the real sources):

```
Content-Security-Policy: default-src 'self'; img-src 'self' data:; script-src 'self';
  style-src 'self'; font-src 'self'; frame-ancestors 'self'; base-uri 'self';
  form-action 'self'; upgrade-insecure-requests
```

Warn the user that an enforced CSP can break analytics, embeds and payment widgets;
always test in report-only mode first.

Also check: no mixed content warnings, cookie consent behaviour matches local law
(owner's responsibility), forms submit over HTTPS, admin login pages are not linked
publicly.

## 6. Mobile layout basics

- `<meta name="viewport" content="width=device-width, initial-scale=1">` and no
  zoom blocking.
- Body text at least 16 px to avoid tiny text and iOS input zoom.
- Tap targets: at least 24 by 24 CSS px (WCAG 2.2 AA); 44 to 48 px recommended for
  primary actions.
- No horizontal scroll at 320 to 375 px widths.
- Phone numbers as `tel:` links; addresses link to maps.
- Sticky elements take no more than a small part of the screen height.
- Test on a real mid-range Android phone if possible; Lighthouse mobile simulates a
  throttled device.

## 7. Output template

```markdown
## Performance and technical check: [page]

**Data used:** field (CrUX) / lab (Lighthouse vX, median of 3) / markup only (hypotheses)

| Metric | Value | Status | Source |
|---|---|---|---|
| LCP | ... | Good / NI / Poor | ... |
| INP (or TBT proxy) | ... | ... | ... |
| CLS | ... | ... | ... |

### P1 - fix now
- [ ] Issue - evidence - fix - how to measure: [audit or insight name]

### P2 - this month
### P3 - nice to have

### Security headers
| Header | Present | Recommendation |

### Not checked
```
