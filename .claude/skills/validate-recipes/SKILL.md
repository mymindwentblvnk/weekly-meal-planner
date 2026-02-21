---
description: "Comprehensive recipe validation and automatic fixing of all quality issues"
---

# Validate and Fix Recipes

This skill performs comprehensive validation of all recipes and automatically fixes quality issues including missing descriptions, incomplete tags, unsorted tags, and hierarchical tagging problems.

## What This Skill Does

**COMPREHENSIVE VALIDATION**: This skill checks **ALL recipes** in the `recipes/` folder recursively, including all subdirectories.

1. **Validates all recipes** using `.claude/utils/recipe-utils.py`
2. **Checks for missing required fields** - description, tags, estimated_cost
3. **Fixes missing descriptions** - Generates appetizing German descriptions
4. **Fixes missing tags** - Adds tags based on ingredients
5. **Fixes incomplete hierarchical tags** - Ensures generic + specific tag pairs
6. **Sorts tags alphabetically** - Uses German alphabetization (ä=a, ö=o, ü=u)
7. **Fixes missing costs** - Asks user for estimated_cost if missing
8. **Regenerates HTML** - Runs `python main.py`
9. **Commits and pushes** - Saves all changes to Git

## Using recipe-utils.py

**IMPORTANT:** Use the utility functions from `.claude/utils/recipe-utils.py` for validation:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.claude/utils').absolute()))
from recipe_utils import (
    validate_all_recipes,
    check_hierarchical_tags,
    sort_recipe_tags,
    german_sort_key,
    HIERARCHICAL_TAGS
)

# Run full validation
results = validate_all_recipes()
```

## Step-by-Step Process

### Step 1: Validate All Recipes

Use `validate_all_recipes()` from recipe-utils.py to get a comprehensive report:
- **Recipes missing description field** (or empty/placeholder descriptions)
- **Recipes missing tags field** (or empty tags)
- **Recipes with unsorted tags**
- **Recipes with missing hierarchical tags**
- **Recipes missing estimated_cost field**
- **Count of valid recipes**

The validation now checks for **completely missing required fields**, not just validating existing ones.

### Step 2: Fix Missing Descriptions

For recipes where description is missing, empty, or placeholder ("tbd", "TODO"):

Generate a concise, appetizing German description (1-2 sentences) that:
- Highlights main ingredients (skip salt, pepper, oil, eggs, onions)
- Describes what makes the recipe special
- Matches existing description style
- Is authentic and appetizing

**Example descriptions:**
```
"Knusprige Thunfisch-Bouletten mit Butterbohnen auf frischem Romana-Salat, serviert mit cremiger Aioli-Joghurt-Soße."
"Glasierter Seelachs auf Sushireis mit eingelegtem Gurken-Karotten-Gemüse, verfeinert mit Sweet Chili Soße."
"Herzhafter Eintopf mit Rinderhackfleisch, Gemüse und Buchweizenpasta in würziger Tomatensauce."
```

### Step 3: Fix Missing or Incomplete Tags

#### 3a. Add Missing Tags

For recipes without tags field, analyze ingredients and add appropriate tags following hierarchical rules (see HIERARCHICAL_TAGS in recipe-utils.py).

#### 3b. Fix Incomplete Hierarchical Tags

Use `check_hierarchical_tags(recipe_file)` to find missing generic tags.

**Hierarchical Tagging Rules** (from HIERARCHICAL_TAGS):

| Category | Generic Tag | + Specific Tags |
|----------|-------------|-----------------|
| Fish | Fisch | Lachs, Thunfisch, Seelachs, Garnelen |
| Meat | Fleisch | Rind, Pute, Schinken, Hackfleisch |
| Cheese | Käse | Feta, Schafskäse, Parmesan, Bergkäse, Frischkäse |
| Nuts | Nüsse | Walnüsse, Haselnüsse, Mandeln |
| Berries | Beeren | Himbeeren, Erdbeeren |
| Fruit | Obst | Apfel, Kiwi, Weintrauben |
| Seeds | Kerne | Chiasamen, Leinsamen, Sesam |
| Cabbage | Kohl | Blumenkohl, Brokkoli |
| Potatoes | Kartoffeln | Süßkartoffel |

**Key Rules:**
- Always include BOTH generic AND specific tags
- Never go deeper than one level: "Wildlachs" → "Fisch" + "Lachs" (NOT "Wildlachs")
- Check ingredients to infer missing specific tags (e.g., has "Fisch" but ingredients show "Wildlachsfilet" → add "Lachs")

**Example fixes:**

```yaml
# Before
tags:
  - Lachs

# After (missing generic tag)
tags:
  - Fisch
  - Lachs
```

```yaml
# Before (has generic but ingredients show "Haselnüsse")
tags:
  - Butter
  - Mehl

# After (add both levels)
tags:
  - Butter
  - Haselnüsse
  - Mehl
  - Nüsse
```

### Step 4: Sort Tags Alphabetically

Use `sort_recipe_tags(recipe_file)` or `german_sort_key()` to sort tags.

German alphabetization (DIN 5007-1):
- ä treated as 'a'
- ö treated as 'o'
- ü treated as 'u'
- ß treated as 'ss'

### Step 5: Fix Missing Costs

Check for missing `estimated_cost` field and ask user to provide it:

**Process:**
1. Identify recipes without `estimated_cost` field
2. For each recipe, ask user: "What is the estimated cost for [Recipe Name] (for [X] servings)? Please provide in EUR."
3. User provides cost as number (e.g., "12.50" or "8")
4. Add to recipe file after `cook_time` field
5. If user skips/says "don't know", use 0.00 as placeholder

**Key Points:**
- Add `estimated_cost` field after `cook_time`
- Format: `estimated_cost: 11.68  # EUR`
- Cost is user-provided, not automatically calculated
- If user provides 0.00, it can be adjusted later

**Example:**
```yaml
# Before
prep_time: 10  # minutes
cook_time: 20  # minutes
tags:
  - Lachs

# After (user provided 15.50)
prep_time: 10  # minutes
cook_time: 20  # minutes
estimated_cost: 15.50  # EUR
tags:
  - Lachs
```

### Step 6: Validate Again

After fixes, run `validate_all_recipes()` again to confirm all issues are resolved.

Also verify all recipes have `estimated_cost`:
```bash
# Check for recipes without cost
grep -L "estimated_cost:" recipes/**/*.yaml
```

### Step 7: Regenerate HTML

```bash
python main.py
```

### Step 8: Commit and Push

```bash
git add recipes/
git commit -m "Validate and fix recipe metadata

- Fixed [X] recipes with missing descriptions
- Fixed [Y] recipes with incomplete hierarchical tags
- Fixed [Z] recipes with unsorted tags
- Fixed [N] recipes with missing costs
- All recipes now pass validation

Co-Authored-By: Claude (@vertex-ai/anthropic.claude-sonnet-4-5@20250929) <noreply@anthropic.com>"
git push
```

## Ingredient Tag Mapping Guidelines

### General Principles

1. **Remove descriptors**: "Griechischer Joghurt" → "Joghurt", "Rote Zwiebel" → "Zwiebel"
2. **Use base name**: "Kräuterfrischkäse" → "Frischkäse"
3. **Capitalize tags**: All tags start with uppercase
4. **Use singular where logical**: "Tomaten" → "Tomate", but "Eier" stays "Eier"
5. **Be specific for vegetables**: Use "Karotte", "Zwiebel", "Tomate" (NOT generic "Gemüse")
6. **Hierarchical tags**: Always include BOTH levels for categorized ingredients

### Common Ingredients

**Fish & Seafood:**
- Any salmon → "Fisch" + "Lachs"
- Tuna → "Fisch" + "Thunfisch"
- Pollock → "Fisch" + "Seelachs"
- Shrimp → "Fisch" + "Garnelen"

**Meat & Poultry:**
- Beef → "Fleisch" + "Rind"
- Ground meat → "Fleisch" + "Hackfleisch"
- Turkey → "Fleisch" + "Pute"
- Ham → "Fleisch" + "Schinken"

**Cheese:**
- Cream cheese → "Käse" + "Frischkäse"
- Feta → "Käse" + "Feta"
- Parmesan → "Käse" + "Parmesan"
- Mountain cheese → "Käse" + "Bergkäse"
- Sheep cheese → "Käse" + "Schafskäse"

**Nuts & Seeds:**
- Walnuts → "Nüsse" + "Walnüsse"
- Hazelnuts → "Nüsse" + "Haselnüsse"
- Almonds → "Nüsse" + "Mandeln"
- Chia seeds → "Kerne" + "Chiasamen"
- Flax seeds → "Kerne" + "Leinsamen"
- Sesame → "Kerne" + "Sesam"

**Fruits & Berries:**
- Raspberries → "Beeren" + "Himbeeren"
- Strawberries → "Beeren" + "Erdbeeren"
- Apples → "Obst" + "Apfel"
- Kiwi → "Obst" + "Kiwi"
- Grapes → "Obst" + "Weintrauben"

**Vegetables (use specific names):**
- Onions → "Zwiebel"
- Carrots → "Karotte"
- Tomatoes → "Tomate"
- Paprika → "Paprika"
- Cauliflower → "Kohl" + "Blumenkohl"
- Broccoli → "Kohl" + "Brokkoli"
- Cucumber → "Gurke"
- Zucchini → "Zucchini"
- Spinach → "Spinat"
- Celery → "Sellerie"
- Avocado → "Avocado"
- Lettuce/Arugula → "Salat"

**Potatoes & Grains:**
- Regular potatoes → "Kartoffeln"
- Sweet potato → "Kartoffeln" + "Süßkartoffel"
- Any pasta → "Pasta"
- Any rice → "Reis"
- Flour → "Mehl"
- Oats → "Haferflocken"

**Dairy:**
- Milk → "Milch"
- Yogurt → "Joghurt"
- Quark → "Quark"
- Butter → "Butter"
- Eggs → "Eier"

**Herbs & Seasonings:**
- Any herbs → "Kräuter"
- Garlic → "Knoblauch"
- Honey → "Honig"
- Oil → "Öl"

## Reporting

After processing, provide a summary:

```
Recipe Validation Report
========================

Total recipes: 28

Fixed Issues:
- Added descriptions: 2 recipes
  - Recipe A
  - Recipe B
- Fixed incomplete hierarchical tags: 3 recipes
  - Recipe C (added "Fisch" for "Lachs")
  - Recipe D (added "Nüsse" for "Walnüsse")
  - Recipe E (added "Käse" for "Feta")
- Sorted tags: 5 recipes

Final Status:
✓ All 28 recipes pass validation
✓ HTML regenerated
✓ Changes committed and pushed
```

## Important Notes

- **Always validate using recipe-utils.py** - Don't reimplement validation logic
- **Check ingredients carefully** - Missing specific tags often found in ingredient list
- **Preserve good metadata** - Only fix what's broken
- **Test after changes** - Run validation again to confirm fixes worked
- **Be thorough** - Check every recipe, even ones that look correct

## Example Usage

```python
#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

# Add utils directory to path
sys.path.insert(0, str(Path('.claude/utils').absolute()))
from recipe_utils import validate_all_recipes, check_hierarchical_tags, sort_recipe_tags

# Step 1: Validate
print("=== Validating all recipes ===")
results = validate_all_recipes()

# Step 2: Fix issues
for issue in results['missing_hierarchical']:
    file_path = issue['file']
    print(f"Fixing hierarchical tags in {file_path}")
    # ... add missing tags ...

for issue in results['unsorted_tags']:
    file_path = issue['file']
    print(f"Sorting tags in {file_path}")
    sort_recipe_tags(file_path)

# Step 3: Validate again
final_results = validate_all_recipes()
print(f"✓ {len(final_results['valid'])} recipes pass validation")
```
