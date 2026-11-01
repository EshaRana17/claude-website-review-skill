#!/usr/bin/env python3
"""page_audit.py - offline markup audit for a single local HTML file.

Part of the website-review Agent Skill. Standard library only. It never opens a
network connection: it reads one file from disk and prints a report.

Checks:
  * <html lang>, viewport meta (and zoom blocking), <title>, meta description
  * <img> missing alt, missing width/height
  * form fields without an accessible label
  * heading order (missing h1, multiple h1, skipped levels)
  * external scripts (count and hosts)
  * CTA-like buttons and links

Usage:
  python page_audit.py PATH_TO_FILE.html [--json]

Exit codes: 0 = no issues, 1 = issues found, 2 = usage or file error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

MAX_BYTES = 10 * 1024 * 1024  # refuse files over 10 MB

# Inputs that never need a separate text label.
NO_LABEL_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}

CTA_VERBS = (
    "get", "start", "book", "buy", "order", "shop", "try", "sign up", "signup",
    "join", "subscribe", "download", "request", "contact", "call", "schedule",
    "claim", "reserve", "register", "add to", "apply", "talk", "chat", "quote",
    "demo", "free", "learn more", "see how", "get started", "enquire", "inquire",
)
CTA_CLASS_HINT = re.compile(r"(^|[\s_-])(btn|button|cta)([\s_-]|$)", re.I)


def _attr_map(attrs):
    return {k.lower(): (v if v is not None else "") for k, v in attrs}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.saw_html = False
        self.viewport = None
        self.title_text = ""
        self.in_title = False
        self.meta_description = None
        self.images = []          # dicts: line, src, alt, width, height
        self.fields = []          # dicts: line, tag, type, id, name, labelled
        self.label_for_ids = set()
        self.label_depth = 0
        self.headings = []        # (level, line, text)
        self.heading_stack = []   # open heading capture: [level, line, parts]
        self.scripts_external = []  # (line, src, host)
        self.scripts_inline = 0
        self.ctas = []            # dicts: line, tag, text, href
        self.cta_stack = []       # open <a>/<button>: [tag, line, attrs, parts]
        self.iframes_untitled = []

    # -- helpers -----------------------------------------------------------
    def _line(self):
        return self.getpos()[0]

    def _push_text(self, data):
        for item in self.heading_stack:
            item[2].append(data)
        for item in self.cta_stack:
            item[3].append(data)

    # -- parser callbacks ---------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = _attr_map(attrs)
        line = self._line()

        if tag == "html":
            self.saw_html = True
            self.html_lang = a.get("lang", "").strip() or None
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "viewport":
                self.viewport = a.get("content", "")
            elif name == "description":
                self.meta_description = a.get("content", "")
        elif tag == "img":
            self.images.append({
                "line": line,
                "src": a.get("src", ""),
                "has_alt": "alt" in a,
                "alt": a.get("alt"),
                "has_width": bool(a.get("width")),
                "has_height": bool(a.get("height")),
            })
            # alt text of an image inside a link or button counts as its text
            if a.get("alt"):
                self._push_text(" " + a["alt"] + " ")
        elif tag == "label":
            self.label_depth += 1
            if a.get("for"):
                self.label_for_ids.add(a["for"])
        elif tag in ("input", "select", "textarea"):
            ftype = a.get("type", "text").lower() if tag == "input" else tag
            if not (tag == "input" and ftype in NO_LABEL_INPUT_TYPES):
                self.fields.append({
                    "line": line,
                    "tag": tag,
                    "type": ftype,
                    "id": a.get("id"),
                    "name": a.get("name"),
                    "wrapped": self.label_depth > 0,
                    "aria": bool(a.get("aria-label", "").strip()
                                 or a.get("aria-labelledby", "").strip()
                                 or a.get("title", "").strip()),
                    "placeholder_only": bool(a.get("placeholder")),
                })
            elif tag == "input" and ftype == "image" and not a.get("alt"):
                self.fields.append({
                    "line": line, "tag": tag, "type": ftype, "id": a.get("id"),
                    "name": a.get("name"), "wrapped": False,
                    "aria": bool(a.get("aria-label")), "placeholder_only": False,
                })
            if tag == "input" and ftype in ("submit", "button") and a.get("value"):
                self._record_cta("input", line, a, a["value"])
        elif re.fullmatch(r"h[1-6]", tag):
            self.heading_stack.append([int(tag[1]), line, []])
        elif tag == "script":
            src = a.get("src", "").strip()
            if src:
                parts = urlsplit(src)
                if parts.scheme in ("http", "https") or src.startswith("//"):
                    host = parts.netloc or urlsplit("https:" + src).netloc
                    self.scripts_external.append((line, src, host))
            else:
                self.scripts_inline += 1
        elif tag in ("a", "button"):
            self.cta_stack.append([tag, line, a, []])
        elif tag == "iframe":
            if not a.get("title", "").strip():
                self.iframes_untitled.append(line)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("a", "button", "label", "title") or re.fullmatch(r"h[1-6]", tag):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "label":
            self.label_depth = max(0, self.label_depth - 1)
        elif re.fullmatch(r"h[1-6]", tag):
            level = int(tag[1])
            for i in range(len(self.heading_stack) - 1, -1, -1):
                if self.heading_stack[i][0] == level:
                    lvl, line, parts = self.heading_stack.pop(i)
                    self.headings.append((lvl, line, _clean("".join(parts))))
                    break
        elif tag in ("a", "button"):
            for i in range(len(self.cta_stack) - 1, -1, -1):
                if self.cta_stack[i][0] == tag:
                    t, line, a, parts = self.cta_stack.pop(i)
                    text = _clean("".join(parts)) or a.get("aria-label", "")
                    self._record_cta(t, line, a, text)
                    break

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data
        self._push_text(data)

    # -- CTA detection ------------------------------------------------------
    def _record_cta(self, tag, line, a, text):
        text = _clean(text)
        low = text.lower()
        href = a.get("href", "")
        cls = a.get("class", "")
        reasons = []
        if tag in ("button", "input"):
            reasons.append("button")
        if CTA_CLASS_HINT.search(cls):
            reasons.append("button-like class")
        if href.startswith(("tel:", "mailto:")):
            reasons.append(href.split(":", 1)[0] + " link")
        if any(re.search(r"\b" + re.escape(v) + r"\b", low) for v in CTA_VERBS):
            reasons.append("action wording")
        # Plain nav links need wording AND a visual hint to count as CTAs.
        is_cta = (
            tag in ("button", "input")
            or "button-like class" in reasons
            or (href.startswith("tel:") or href.startswith("mailto:"))
            or ("action wording" in reasons and len(low.split()) <= 6)
        )
        if is_cta:
            self.ctas.append({
                "line": line, "tag": tag, "text": text or "(no text)",
                "href": href, "signals": reasons,
                "weak_text": low in {"submit", "click here", "learn more",
                                     "read more", "more", "go", "send", "", "(no text)"},
            })


def audit(html: str) -> dict:
    p = AuditParser()
    p.feed(html)
    p.close()
    # Flush headings or CTAs never closed.
    for lvl, line, parts in p.heading_stack:
        p.headings.append((lvl, line, _clean("".join(parts))))
    p.headings.sort(key=lambda h: h[1])

    issues = []

    def add(severity, check, message, line=None):
        issues.append({"severity": severity, "check": check,
                       "message": message, "line": line})

    # Document basics
    if not p.html_lang:
        add("serious", "lang", "Missing lang attribute on <html> (WCAG 3.1.1).")
    if p.viewport is None:
        add("serious", "viewport", "Missing <meta name=\"viewport\"> - phones will show a zoomed-out desktop layout.")
    else:
        vp = p.viewport.replace(" ", "").lower()
        if "user-scalable=no" in vp or "user-scalable=0" in vp or re.search(r"maximum-scale=1(\.0)?(,|$)", vp):
            add("serious", "viewport", "Viewport blocks zoom (user-scalable=no or maximum-scale=1). Remove it (WCAG 1.4.4).")
        if "width=device-width" not in vp:
            add("minor", "viewport", "Viewport does not set width=device-width.")
    title = _clean(p.title_text)
    if not title:
        add("serious", "title", "Missing or empty <title> (WCAG 2.4.2).")
    if p.meta_description is None or not p.meta_description.strip():
        add("minor", "meta-description", "Missing or empty meta description (affects search snippets).")
    elif len(p.meta_description) > 160:
        add("minor", "meta-description", f"Meta description is {len(p.meta_description)} characters; it may be truncated in results.")

    # Images
    for img in p.images:
        label = img["src"] or "(no src)"
        if not img["has_alt"]:
            add("serious", "img-alt", f"Image without alt attribute: {label}  (use alt=\"\" if decorative; WCAG 1.1.1)", img["line"])
        if not (img["has_width"] and img["has_height"]):
            add("minor", "img-dimensions", f"Image without width and height: {label}  (layout shift risk, CLS)", img["line"])

    # Form fields
    for f in p.fields:
        labelled = f["wrapped"] or f["aria"] or (f["id"] and f["id"] in p.label_for_ids)
        if not labelled:
            what = f"<{f['tag']}" + (f" type={f['type']}" if f["tag"] == "input" else "") + ">"
            ident = f["id"] or f["name"] or "unnamed"
            extra = " (placeholder is not a label)" if f["placeholder_only"] else ""
            add("blocker", "form-label", f"Field without accessible label: {what} {ident}{extra} (WCAG 1.3.1, 3.3.2, 4.1.2)", f["line"])

    # Headings
    h1s = [h for h in p.headings if h[0] == 1]
    if not h1s:
        add("minor", "headings", "No <h1> found.")
    elif len(h1s) > 1:
        add("minor", "headings", f"{len(h1s)} <h1> elements found; one main heading is clearer.", h1s[1][1])
    prev = 0
    for lvl, line, text in p.headings:
        if prev and lvl > prev + 1:
            add("minor", "headings", f"Heading level skipped: h{prev} -> h{lvl} \"{text[:60]}\"", line)
        if not text:
            add("serious", "headings", f"Empty <h{lvl}>.", line)
        prev = lvl

    # Iframes
    for line in p.iframes_untitled:
        add("minor", "iframe-title", "Iframe without title attribute (WCAG 4.1.2).", line)

    # Scripts
    hosts = sorted({h for _, _, h in p.scripts_external})
    if len(p.scripts_external) > 5:
        add("minor", "scripts", f"{len(p.scripts_external)} external scripts from {len(hosts)} hosts; review third-party cost.")

    # CTAs
    if not p.ctas:
        add("serious", "cta", "No CTA-like button or link detected.")
    for c in p.ctas:
        if c["weak_text"]:
            add("minor", "cta", f"Weak or missing CTA text: \"{c['text']}\" - say what happens next.", c["line"])

    counts = {"blocker": 0, "serious": 0, "minor": 0}
    for i in issues:
        counts[i["severity"]] += 1

    return {
        "document": {
            "lang": p.html_lang,
            "title": title or None,
            "meta_description": p.meta_description,
            "viewport": p.viewport,
        },
        "stats": {
            "images": len(p.images),
            "form_fields_checked": len(p.fields),
            "headings": len(p.headings),
            "external_scripts": len(p.scripts_external),
            "inline_scripts": p.scripts_inline,
            "ctas": len(p.ctas),
        },
        "headings_outline": [{"level": l, "line": ln, "text": t} for l, ln, t in p.headings],
        "external_scripts": [{"line": l, "src": s, "host": h} for l, s, h in p.scripts_external],
        "external_script_hosts": hosts,
        "ctas": p.ctas,
        "issues": issues,
        "issue_counts": counts,
        "limits": "Markup only: CSS, contrast, JavaScript-rendered content and real performance are not checked.",
    }


def render_text(path: str, r: dict) -> str:
    out = []
    w = out.append
    w(f"Page audit: {path}")
    w("=" * 60)
    d = r["document"]
    w(f"lang: {d['lang'] or '(missing)'}")
    w(f"title: {d['title'] or '(missing)'}")
    w(f"meta description: {d['meta_description'] if d['meta_description'] else '(missing)'}")
    w(f"viewport: {d['viewport'] if d['viewport'] is not None else '(missing)'}")
    s = r["stats"]
    w("")
    w(f"Images: {s['images']} | Form fields: {s['form_fields_checked']} | Headings: {s['headings']} | "
      f"External scripts: {s['external_scripts']} | Inline scripts: {s['inline_scripts']} | CTAs: {s['ctas']}")

    w("")
    w("Heading outline")
    w("-" * 60)
    for h in r["headings_outline"]:
        w(f"{'  ' * (h['level'] - 1)}h{h['level']} (line {h['line']}): {h['text'][:70]}")
    if not r["headings_outline"]:
        w("(none)")

    w("")
    w("External scripts")
    w("-" * 60)
    for sc in r["external_scripts"]:
        w(f"line {sc['line']}: {sc['host']}  {sc['src']}")
    if not r["external_scripts"]:
        w("(none)")

    w("")
    w("CTA-like buttons and links")
    w("-" * 60)
    for c in r["ctas"]:
        target = f" -> {c['href']}" if c["href"] else ""
        w(f"line {c['line']}: <{c['tag']}> \"{c['text'][:60]}\"{target}  [{', '.join(c['signals'])}]")
    if not r["ctas"]:
        w("(none)")

    w("")
    c = r["issue_counts"]
    w(f"Issues: {c['blocker']} blocker, {c['serious']} serious, {c['minor']} minor")
    w("-" * 60)
    order = {"blocker": 0, "serious": 1, "minor": 2}
    for i in sorted(r["issues"], key=lambda x: (order[x["severity"]], x["line"] or 0)):
        loc = f"line {i['line']}" if i["line"] else "document"
        w(f"[{i['severity'].upper()}] {i['check']} ({loc}): {i['message']}")
    if not r["issues"]:
        w("No issues found by this script.")
    w("")
    w("Note: " + r["limits"])
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Offline markup audit of a local HTML file (no network).")
    ap.add_argument("file", help="path to a local .html or .htm file")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = ap.parse_args(argv)

    if re.match(r"^[a-z][a-z0-9+.-]*://", args.file, re.I):
        print("error: pass a local file path, not a URL. This script does not use the network.", file=sys.stderr)
        return 2
    path = Path(args.file)
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    if path.stat().st_size > MAX_BYTES:
        print(f"error: file is larger than {MAX_BYTES // (1024 * 1024)} MB", file=sys.stderr)
        return 2
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"error: cannot read file: {exc}", file=sys.stderr)
        return 2
    html = raw.decode("utf-8", errors="replace")

    result = audit(html)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_text(str(path), result))
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
