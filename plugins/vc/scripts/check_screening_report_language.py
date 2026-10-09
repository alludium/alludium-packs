#!/usr/bin/env python3
"""Check exported Screening HTML and its completion summary for issue #4452 leaks.

This is a read-only QA check, not runtime sanitization or a browser visibility engine.
It ignores comments, HTML-hidden/inline-hidden content and inert elements so the
required hidden evidence manifest and citation URL/ID/hash provenance remain intact.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import yaml

TASK_SCHEMA = Path(__file__).resolve().parents[1] / "alludium/task-definition-templates/vc-workflows/generate-refresh-screening-report.yaml"
TASK_FIELDS = yaml.safe_load(TASK_SCHEMA.read_text())["fields"]
RUNTIME_FIELD_NAMES = {field["key"] for direction in ("input", "output") for field in TASK_FIELDS[direction]}

FORBIDDEN = {
    "runtime field name": re.compile(r"\b(?:" + "|".join(re.escape(key) for key in sorted(RUNTIME_FIELD_NAMES)) + r")\b", re.I),
    "internal evidence manifest terminology": re.compile(r"\bevidence[\s‐‑–—-]+basis[\s‐‑–—-]+manifest\b", re.I),
    "provider search terminology": re.compile(r"\bprovider[\s‐‑–—-]+searchable\b", re.I),
}
# Report source indexes may legitimately expose provenance identifiers. These
# section labels are forbidden only in the reader-facing completion summary.
SUMMARY_FORBIDDEN = {
    "internal completion bookkeeping section": re.compile(
        r"^[ \t]*(?:(?:[-*+]|\d+[.)]|\#{1,6})[ \t]+)?(?:\*\*|__)?"
        r"(?:artifact[ \t‐‑–—-]+ids?|structured[ \t‐‑–—-]+output|"
        r"saved[ \t‐‑–—-]+field|validation[ \t‐‑–—-]+checklist|bookkeeping)"
        r"(?:\*\*|__)?[ \t]*(?::|$)",
        re.I | re.M,
    ),
}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
INERT_TAGS = {"head", "script", "style", "template"}
# Preserve rendered text boundaries without splitting words across inline formatting.
TEXT_BOUNDARY_TAGS = {
    "address", "article", "aside", "blockquote", "br", "caption", "dd", "details",
    "dialog", "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer",
    "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "hr",
    "legend", "li", "main", "menu", "nav", "ol", "p", "pre", "section",
    "summary", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
}


class ReportText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        hidden = bool(self.stack and self.stack[-1][1]) or tag in INERT_TAGS or "hidden" in attrs or bool(
            re.search(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b", attrs.get("style") or "", re.I)
        )
        if not hidden:
            if tag in TEXT_BOUNDARY_TAGS:
                self.parts.append("\n")
            self.parts.extend(value for key, value in attributes if key in {"alt", "title"} and value)
        if tag not in VOID_TAGS:
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                if tag in TEXT_BOUNDARY_TAGS and not self.stack[index][1]:
                    self.parts.append("\n")
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.stack or not self.stack[-1][1]:
            self.parts.append(data)


def check_language(html: str, summary: str) -> list[str]:
    parser = ReportText()
    parser.feed(html)
    findings = [
        f"{surface}: {label} ({match.group(0)})"
        for surface, text in (("report", "".join(parser.parts)), ("summary", summary))
        for label, pattern in FORBIDDEN.items()
        for match in pattern.finditer(text)
    ]
    findings.extend(
        f"summary: {label} ({match.group(0).strip()})"
        for label, pattern in SUMMARY_FORBIDDEN.items()
        for match in pattern.finditer(summary)
    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    args = parser.parse_args()
    findings = check_language(args.html.read_text(), args.summary.read_text())
    for finding in findings:
        print(finding)
    if not findings:
        print("Screening report language check passed (source HTML and summary only).")
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
