# Contributing

Thanks for adding a recipe!

## Adding a recipe

1. Copy `RECIPE_TEMPLATE.md` to `recipes/your-recipe-name.md`
   - Use lowercase kebab-case for the filename (e.g. `pasta-carbonara.md`)
2. Fill in the front matter fields (see table below)
3. Write the recipe body using the template structure: **Ingredients**, **Method**, **Notes**
4. Open a pull request — front matter will be validated automatically before merging

## Front matter reference

| Field | Required | Type | Notes |
|-------|:--------:|------|-------|
| `title` | ✓ | string | Full recipe name |
| `difficulty` | ✓ | integer | 1 (very easy) – 5 (challenging) |
| `tags` | ✓ | list | e.g. `[pasta, dinner, quick]` |
| `prep_time` | ✓ | integer | Hands-on prep time in minutes |
| `total_time` | ✓ | integer | Total time in minutes (must be ≥ prep_time) |
| `servings` | ✓ | integer or string | e.g. `4` or `"4-6"` |
| `cuisine` | | string | e.g. Italian, Thai, Mexican |
| `source` | | string | URL or book title |
| `image` | | string | Path or URL to a photo |

## Style guide

- Write ingredient quantities precisely (`200g plain flour`, not `some flour`)
- Number the method steps
- Keep **Notes** for tips, substitutions, and variations
- Filename should match the recipe title closely (`chicken-tikka-masala.md`)
