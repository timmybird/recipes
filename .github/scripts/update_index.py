#!/usr/bin/env python3
"""Regenerate README.md and recipes.json from recipe front matter."""

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path

README_HEADER = """\
<!-- AUTO-GENERATED — do not edit manually. Regenerated on every push to main. -->
# Recipes

| Recipe | Cuisine | Difficulty | Prep | Total | Servings | Tags |
|--------|---------|:----------:|-----:|------:|----------|------|
"""

README_FOOTER = "\n\n---\n_Index last updated: {ts}_\n"


def parse_recipe(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    fm: dict = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
    fm["_file"] = path.name
    fm["_slug"] = path.stem
    return fm


def difficulty_stars(n: int) -> str:
    n = max(1, min(5, int(n)))
    return "★" * n + "☆" * (5 - n)


def fmt_time(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes}m"
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m" if m else f"{h}h"


def main() -> None:
    recipes_dir = Path("recipes")
    recipe_files = sorted(recipes_dir.glob("*.md"))
    recipes = [parse_recipe(p) for p in recipe_files]
    recipes.sort(key=lambda r: r.get("title", r["_slug"]).lower())

    # --- README ---
    rows = []
    for r in recipes:
        title = r.get("title", r["_slug"])
        file = r["_file"]
        cuisine = r.get("cuisine") or "—"
        diff = difficulty_stars(r["difficulty"]) if "difficulty" in r else "—"
        prep = fmt_time(r["prep_time"]) if "prep_time" in r else "—"
        total = fmt_time(r["total_time"]) if "total_time" in r else "—"
        servings = str(r.get("servings", "—"))
        tags = " ".join(f"`{t}`" for t in (r.get("tags") or []))
        rows.append(
            f"| [{title}](recipes/{file}) | {cuisine} | {diff}"
            f" | {prep} | {total} | {servings} | {tags} |"
        )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    readme = README_HEADER + "\n".join(rows) + README_FOOTER.format(ts=ts)
    Path("README.md").write_text(readme, encoding="utf-8")
    print(f"README.md updated ({len(recipes)} recipe(s)).")

    # --- recipes.json ---
    export = [
        {
            "title": r.get("title", r["_slug"]),
            "slug": r["_slug"],
            "file": r["_file"],
            "difficulty": r.get("difficulty"),
            "tags": r.get("tags") or [],
            "cuisine": r.get("cuisine") or None,
            "prep_time": r.get("prep_time"),
            "total_time": r.get("total_time"),
            "servings": r.get("servings"),
            "source": r.get("source") or None,
            "image": r.get("image") or None,
        }
        for r in recipes
    ]
    Path("recipes.json").write_text(
        json.dumps(export, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"recipes.json updated ({len(recipes)} recipe(s)).")


if __name__ == "__main__":
    main()
