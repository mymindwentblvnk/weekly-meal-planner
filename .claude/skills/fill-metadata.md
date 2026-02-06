---
description: "Fill missing recipe metadata, validate and improve tags for all recipes"
---

# Fill Recipe Metadata

This command performs a comprehensive check and update of all recipe metadata, including descriptions, tags, and tag quality validation.

## What This Command Does

1. **Fill Missing Descriptions**: Generates descriptions for recipes without proper descriptions
2. **Fill Missing Tags**: Adds tags to recipes that don't have them
3. **Validate Tag Quality**: Reviews existing tags and improves them based on hierarchical tagging rules
4. **Check Other Metadata**: Validates that all required fields are present and properly formatted

## Process

### Step 1: Scan All Recipes

Find all recipe YAML files in the recipes/ directory and check each one for:
- Missing or placeholder descriptions
- Missing tags field
- Incomplete hierarchical tags
- Other metadata issues

### Step 2: Fill Missing Descriptions

For recipes where the description field is:
- Missing entirely
- Empty ("")
- A placeholder ("tbd", "TODO", etc.)

Generate a concise, appetizing German description (1-2 sentences) that:
- Highlights the main ingredients (skip common ones like salt, pepper, oil, eggs, onions)
- Describes what makes this recipe special or appealing
- Matches the style of existing recipe descriptions
- Is authentic and appetizing

**Example descriptions:**
- "Knusprige Thunfisch-Bouletten mit Butterbohnen auf frischem Romana-Salat, serviert mit cremiger Aioli-Joghurt-Soße und eingelegten Zwiebeln."
- "Glasierter Seelachs auf Sushireis mit eingelegtem Gurken-Karotten-Gemüse, verfeinert mit Sweet Chili Soße und Sesamöl."

### Step 3: Fill Missing Tags

For recipes without a tags field, analyze the ingredients and add appropriate tags following the hierarchical tagging rules (see fill-tags.md for complete rules).

### Step 4: Validate and Improve Existing Tags

**This is the most important step.** For EVERY recipe, even those with tags, validate that:

1. **Hierarchical tags are complete**:
   - If a recipe has "lachs", does it also have "fisch"?
   - If a recipe has "walnüsse", does it also have "nüsse"?
   - If a recipe has "himbeeren", does it also have "beeren"?
   - If a recipe has "frischkäse", does it also have "käse"?
   - If a recipe has "sesam", does it also have "kerne"?

2. **Specific tags are present**:
   - If a recipe has "fisch" but the ingredient is specifically salmon, add "lachs"
   - If a recipe has "fleisch" but the ingredient is beef, add "rind"
   - If a recipe has "käse" but the ingredient is feta, add "feta"
   - If a recipe has "nüsse" but the ingredient is walnuts, add "walnüsse"

3. **Tags match the hierarchical system**:
   - Fish: "fisch" + ("lachs" | "thunfisch" | "seelachs" | "garnelen")
   - Meat: "fleisch" + ("rind" | "pute" | "schinken" | "hackfleisch")
   - Cheese: "käse" + ("feta" | "schafskäse" | "parmesan" | "bergkäse" | "frischkäse")
   - Nuts: "nüsse" + ("walnüsse" | "haselnüsse" | "mandeln")
   - Berries: "beeren" + ("himbeeren" | "erdbeeren")
   - Fruit: "obst" + ("apfel" | "kiwi" | "weintrauben")
   - Seeds: "kerne" + ("chiasamen" | "leinsamen" | "sesam")
   - Cabbage: "kohl" + ("blumenkohl" | "brokkoli")
   - Potatoes: "kartoffeln" (+ "süßkartoffel" if applicable)

4. **No overly specific tags**:
   - "wildlachs" should be "fisch" + "lachs" (NOT "wildlachs")
   - "räucherlachs" should be "fisch" + "lachs" (NOT "räucherlachs")
   - "rinderhackfleisch" should be "fleisch" + "hackfleisch" + "rind"

5. **Tags are sorted alphabetically**

6. **No duplicate tags**

### Step 5: Check Other Metadata

Verify that each recipe has:
- `name`: Present and non-empty
- `author`: Present and non-empty
- `category`: Present with a valid emoji
- `servings`: Present and a number
- `prep_time`: Present and a number
- `cook_time`: Present and a number
- `tags`: Present and non-empty array
- `description`: Present and meaningful
- `ingredients`: Present and non-empty array
- `instructions`: Present and non-empty array

## Validation Examples

### Example 1: Missing Generic Tag
**Before:**
```yaml
tags:
  - lachs
  - kartoffeln
```
**After:**
```yaml
tags:
  - fisch
  - kartoffeln
  - lachs
```

### Example 2: Missing Specific Tag
**Before:**
```yaml
tags:
  - fisch
  - kartoffeln
```
**Ingredients:** Contains "Wildlachsfilet"
**After:**
```yaml
tags:
  - fisch
  - kartoffeln
  - lachs
```

### Example 3: Missing Both Levels
**Before:**
```yaml
tags:
  - butter
  - eier
```
**Ingredients:** Contains "Haselnüsse"
**After:**
```yaml
tags:
  - butter
  - eier
  - haselnüsse
  - nüsse
```

### Example 4: Overly Specific Tag
**Before:**
```yaml
tags:
  - fisch
  - wildlachs
```
**After:**
```yaml
tags:
  - fisch
  - lachs
```

## Reporting

After processing all recipes, provide a summary report:

1. **Recipes with added descriptions**: List recipe names
2. **Recipes with added tags**: List recipe names
3. **Recipes with improved tags**: List recipe names and what was changed
4. **Recipes with metadata issues**: List any remaining problems
5. **Total recipes processed**: Count

## After Processing

1. Show the summary report
2. Regenerate HTML files using: `python main.py`
3. Commit all changes with message: "Fill and validate recipe metadata"
4. Push to remote

## Important Notes

- **Always validate tag quality**, even if tags already exist
- Use the complete tag hierarchy rules from fill-tags.md
- Be thorough in checking ingredient lists against tags
- Don't skip validation - every recipe should be checked
- Tags must be sorted alphabetically after updates
- Preserve existing good metadata, only improve what's missing or incorrect
