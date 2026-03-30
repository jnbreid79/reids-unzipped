#!/usr/bin/env python3
"""
update_tags.py — Replace tags in Jekyll post front matter.

Run from the root of your reids-unzipped repo:
    python update_tags.py

Writes changes in-place. Run `git diff` afterwards to review before committing.
"""

import re
from pathlib import Path

# ── Tag mapping ───────────────────────────────────────────────────────────────
# Key: post filename (without path)
# Value: list of new tags

TAG_MAP = {
    "2023-10-06-beyond-the-obstacle.md": [
        "loc/atlantic/europe/france",
        "subject/reflections",
        "subject/boat-life",
    ],
    "2023-10-06-the-art-of-connection.md": [
        "loc/atlantic",
        "subject/reflections",
    ],
    "2024-01-04-boatlife-daily-challenges.md": [
        "loc/atlantic/europe/canary-islands",
        "subject/boat-life",
        "subject/boat-work",
    ],
    "2024-01-04-extending-our-90-day-schengen-allowance.md": [
        "loc/atlantic/europe/canary-islands",
        "subject/bureaucracy",
        "subject/boat-work",
    ],
    "2024-02-09-pit-stop-mindelo-cape-verde.md": [
        "loc/atlantic/cape-verde",
        "subject/boat-work",
    ],
    "2024-02-14-dolphin.md": [
        "loc/atlantic",
        "subject/wildlife",
        "subject/passages",
    ],
    "2024-02-16-official-cruiser-status.md": [
        "loc/caribbean/barbados",
        "subject/reflections",
        "subject/wildlife",
        "subject/family",
    ],
    "2024-02-19-barbados-marine-parks-and-lifeguards.md": [
        "loc/caribbean/barbados",
        "subject/wildlife",
        "subject/boat-work",
        "subject/boat-life",
    ],
    "2024-02-20-checked-out-ready-to-leave-thank-you-barbados.md": [
        "loc/caribbean/barbados",
        "subject/boat-life",
    ],
    "2024-02-23-martinique-back-where-it-all-began.md": [
        "loc/caribbean/martinique",
        "subject/passages",
        "subject/boat-work",
    ],
    "2024-03-19-boat-work-in-marin.md": [
        "loc/caribbean/martinique",
        "subject/boat-work",
    ],
    "2024-03-23-scope-creep.md": [
        "loc/caribbean/martinique",
        "subject/boat-work",
    ],
    "2024-04-02-beautiful-bequia.md": [
        "loc/caribbean/grenadines/bequia",
        "subject/wildlife",
        "subject/passages",
        "subject/family",
    ],
    "2024-04-03-between-the-boat-work-jobs.md": [
        "loc/caribbean/martinique",
        "subject/boat-life",
        "subject/family",
        "subject/snorkelling",
    ],
    "2024-04-04-st-lucia.md": [
        "loc/caribbean/st-lucia",
        "subject/landscapes",
        "subject/family",
        "subject/fishing",
    ],
    "2024-04-06-tobago-cays.md": [
        "loc/caribbean/grenadines/tobago-cays",
        "subject/wildlife",
        "subject/snorkelling",
    ],
    "2024-04-28-panama-and-preparing-for-the-canal.md": [
        "loc/caribbean/panama",
        "subject/bureaucracy",
        "subject/passages",
    ],
    "2024-06-19-arriving-in-the-marquesas.md": [
        "loc/pacific/french-polynesia/marquesas",
        "subject/bureaucracy",
        "subject/landscapes",
    ],
    "2024-07-09-marquesas-to-tuamotus.md": [
        "loc/pacific/french-polynesia/tuamotus",
        "subject/passages",
        "subject/weather",
    ],
    "2024-07-13-the-tuamotus-landfall-in-raroia.md": [
        "loc/pacific/french-polynesia/tuamotus/raroia",
        "subject/wildlife",
        "subject/family",
        "subject/boat-life",
    ],
    "2024-07-20-video-highlights-first-few-days-tuamotus.md": [
        "loc/pacific/french-polynesia/tuamotus",
        "subject/video",
    ],
    "2024-07-21-finding-shelter-in-tahanea.md": [
        "loc/pacific/french-polynesia/tuamotus/tahanea",
        "subject/snorkelling",
        "subject/wildlife",
        "subject/weather",
    ],
    "2024-07-27-chilling-out-in-kauehi.md": [
        "loc/pacific/french-polynesia/tuamotus/kauehi",
        "subject/anchorages",
        "subject/snorkelling",
        "subject/family",
    ],
    "2024-08-01-front-wind-shift-anchor-drag.md": [
        "loc/pacific/french-polynesia/tuamotus/fakarava",
        "subject/anchoring",
        "subject/weather",
    ],
    "2024-08-04-fakarava-aka-sharkarava.md": [
        "loc/pacific/french-polynesia/tuamotus/fakarava",
        "subject/diving",
        "subject/wildlife",
    ],
    "2024-08-04-tuamotus-passes.md": [
        "loc/pacific/french-polynesia/tuamotus",
        "subject/passages",
        "subject/boat-life",
    ],
    "2024-08-07-enjoying-toau-anse-amyot.md": [
        "loc/pacific/french-polynesia/tuamotus/toau",
        "subject/diving",
        "subject/fishing",
    ],
    "2024-08-07-video-highlights-the-tuamotus.md": [
        "loc/pacific/french-polynesia/tuamotus",
        "subject/video",
    ],
    "2024-08-08-arrival-in-makatea.md": [
        "loc/pacific/french-polynesia/makatea",
        "subject/landscapes",
        "subject/anchorages",
    ],
    "2024-08-10-makatea-mined-abandoned-and-reborn.md": [
        "loc/pacific/french-polynesia/makatea",
        "subject/history",
        "subject/landscapes",
    ],
    "2024-08-10-video-highlights-makatea.md": [
        "loc/pacific/french-polynesia/makatea",
        "subject/video",
    ],
    "2024-11-06-cherbourg-to-whangarei-15577nm.md": [
        "loc/pacific/new-zealand/whangarei",
        "subject/reflections",
        "subject/passages",
    ],
    "2025-11-28-a-year-in-whangarei.md": [
        "loc/pacific/new-zealand/whangarei",
        "subject/reflections",
        "subject/boat-work",
        "subject/family",
    ],
    "2026-03-26-anchoring-out-a-storm-in-kiriwiki-great-barrier-island.md": [
        "loc/pacific/new-zealand/great-barrier-island",
        "subject/anchoring",
        "subject/weather",
    ],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def build_tags_yaml(tags: list[str]) -> str:
    """Render a tags list as Jekyll front matter YAML."""
    lines = ["tags:"]
    for tag in tags:
        lines.append(f"  - {tag}")
    return "\n".join(lines)


def replace_tags_in_frontmatter(content: str, new_tags: list[str]) -> tuple[str, bool]:
    """
    Replace the tags: block in Jekyll front matter.
    Returns (new_content, was_changed).
    Handles both inline [tag1, tag2] and block (- tag) styles.
    """
    # Match the front matter block (between first pair of ---)
    fm_match = re.match(r"^(---\n)(.*?)(---\n)", content, re.DOTALL)
    if not fm_match:
        return content, False

    pre, fm, post_fm = fm_match.group(1), fm_match.group(2), fm_match.group(3)
    rest = content[fm_match.end():]

    # Remove existing tags block (inline or multi-line)
    # Inline style: tags: [a, b, c]
    fm_new = re.sub(r"^tags:[ \t]*\[.*?\]\n", "", fm, flags=re.MULTILINE)
    # Block style: tags:\n  - a\n  - b
    fm_new = re.sub(r"^tags:\n([ \t]+-[ \t]+\S+\n)+", "", fm_new, flags=re.MULTILINE)

    # Append new tags block
    new_tags_yaml = build_tags_yaml(new_tags)
    fm_new = fm_new.rstrip("\n") + "\n" + new_tags_yaml + "\n"

    new_content = pre + fm_new + post_fm + rest
    return new_content, new_content != content


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    posts_dir = Path("_posts")
    if not posts_dir.exists():
        print("ERROR: _posts/ directory not found. Run this script from your repo root.")
        return

    updated = []
    skipped = []
    not_found = []

    for filename, new_tags in TAG_MAP.items():
        filepath = posts_dir / filename
        if not filepath.exists():
            not_found.append(filename)
            continue

        original = filepath.read_text(encoding="utf-8")
        updated_content, changed = replace_tags_in_frontmatter(original, new_tags)

        if changed:
            filepath.write_text(updated_content, encoding="utf-8")
            updated.append(filename)
        else:
            skipped.append(filename)

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"\n✓ Updated:   {len(updated)} files")
    for f in updated:
        print(f"    {f}")

    if skipped:
        print(f"\n~ Unchanged: {len(skipped)} files (tags already matched or no tags found)")
        for f in skipped:
            print(f"    {f}")

    if not_found:
        print(f"\n✗ Not found: {len(not_found)} files")
        for f in not_found:
            print(f"    {f}")

    print("\nDone. Run `git diff _posts/` to review changes before committing.")


if __name__ == "__main__":
    main()
