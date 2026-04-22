#!/usr/bin/env python3
"""Validate front matter for all recipe files in recipes/."""

import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = ["title", "tags", "servings", "difficulty", "prep_time", "total_time"]
INT_FIELDS = ["difficulty", "prep_time", "total_time"]


def validate_recipe(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        return [f"{path}: missing front matter block"]

    parts = text.split("---", 2)
    if len(parts) < 3:
        return [f"{path}: malformed front matter (no closing ---)"]

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [f"{path}: invalid YAML — {e}"]

    if not isinstance(fm, dict):
        return [f"{path}: front matter must be a YAML mapping"]

    # Required fields present and non-null
    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] is None:
            errors.append(f"{path}: missing required field '{field}'")

    # Integer fields
    for field in INT_FIELDS:
        if field in fm and fm[field] is not None:
            if not isinstance(fm[field], int):
                errors.append(
                    f"{path}: '{field}' must be an integer"
                    f" (got {type(fm[field]).__name__}: {fm[field]!r})"
                )

    # Difficulty range
    if "difficulty" in fm and isinstance(fm["difficulty"], int):
        if not 1 <= fm["difficulty"] <= 5:
            errors.append(
                f"{path}: 'difficulty' must be between 1 and 5 (got {fm['difficulty']})"
            )

    # Times non-negative
    for field in ["prep_time", "total_time"]:
        if field in fm and isinstance(fm[field], int) and fm[field] < 0:
            errors.append(f"{path}: '{field}' must be non-negative")

    # total_time >= prep_time
    pt = fm.get("prep_time")
    tt = fm.get("total_time")
    if isinstance(pt, int) and isinstance(tt, int) and tt < pt:
        errors.append(
            f"{path}: 'total_time' ({tt}) must be >= 'prep_time' ({pt})"
        )

    # Tags must be a list
    if "tags" in fm and fm["tags"] is not None:
        if not isinstance(fm["tags"], list):
            errors.append(f"{path}: 'tags' must be a YAML list")

    return errors


def main() -> None:
    recipes_dir = Path("recipes")
    if not recipes_dir.exists():
        print("No recipes/ directory found — nothing to validate.")
        sys.exit(0)

    recipe_files = sorted(recipes_dir.glob("*.md"))
    if not recipe_files:
        print("No recipe files found — nothing to validate.")
        sys.exit(0)

    all_errors: list[str] = []
    for path in recipe_files:
        all_errors.extend(validate_recipe(path))

    if all_errors:
        print(f"Validation failed — {len(all_errors)} error(s):\n")
        for error in all_errors:
            print(f"  ✗ {error}")
        sys.exit(1)

    print(f"✓ All {len(recipe_files)} recipe(s) passed validation.")


if __name__ == "__main__":
    main()
