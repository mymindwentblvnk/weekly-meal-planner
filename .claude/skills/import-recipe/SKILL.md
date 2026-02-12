---
description: "Import a recipe from a URL and create YAML file"
---

# Import Recipe from URL

This skill imports a recipe from a URL (currently supports Chefkoch.de) and creates a properly formatted YAML file.

## Usage

```
/import-recipe <URL>
```

## What This Skill Does

1. **Fetches recipe data** - Uses curl to download the recipe page
2. **Extracts structured data** - Parses JSON-LD Schema.org recipe data
3. **Generates tags** - Creates appropriate tags from ingredients following hierarchical rules
4. **Creates YAML file** - Saves recipe in correct author folder
5. **Regenerates HTML** - Runs `python main.py`
6. **Commits changes** - Saves to Git with descriptive message

## Supported Sites

Currently supports:
- **Chefkoch.de** - Extracts from JSON-LD structured data

## Step-by-Step Process

### Step 1: Extract Recipe Data

Use curl to fetch the page and extract JSON-LD:

```bash
curl -s "URL" | grep -o '<script type="application/ld+json">.*</script>' | sed 's/<script type="application\/ld+json">//g' | sed 's/<\/script>//g' | python3 -m json.tool
```

Extract:
- `name` - Recipe name
- `description` - Recipe description
- `recipeYield` - Number of servings
- `prepTime` - Prep time (ISO 8601 format like "P0DT0H5M")
- `totalTime` - Total time (ISO 8601 format)
- `recipeIngredient` - Array of ingredient strings
- `recipeInstructions` - Array of instruction steps

### Step 2: Convert Times

Convert ISO 8601 duration format to minutes:
- `P0DT0H5M` → 5 minutes
- `P0DT0H30M` → 30 minutes
- `P0DT1H15M` → 75 minutes

Formula: Parse hours (H) and minutes (M), calculate total minutes.

### Step 3: Parse Ingredients

Convert ingredient strings to YAML format:

**Input:**
```
"4 große Ei(er)"
"1 TL, gehäuft Butter"
```

**Output:**
```yaml
- name: Eier (groß)
  amount: 4
- name: Butter
  amount: 1 TL gehäuft
```

**Rules:**
- Extract amount (number + unit at start)
- Clean ingredient name (remove parentheses, descriptors)
- Keep it simple and readable

### Step 4: Parse Instructions

Convert instruction steps from JSON-LD:

**Input:** Array of `HowToStep` objects with `text` field
**Output:** Simple array of instruction strings

Skip overly detailed steps, combine related steps, focus on actionable instructions.

### Step 5: Generate Tags

Use the ingredient tag mapping from `/validate-recipes` skill:

**Key Rules:**
- Use hierarchical tags (generic + specific)
- Remove descriptors: "Griechischer Joghurt" → "Joghurt"
- Use base names: "Kräuterfrischkäse" → "Frischkäse"
- Capitalize: "tomate" → "Tomate"

**Examples:**
- Wildlachsfilet → `Fisch`, `Lachs`
- Haselnüsse → `Nüsse`, `Haselnüsse`
- Feta → `Käse`, `Feta`
- Aubergine → `Aubergine` (no hierarchical rule)
- Knoblauch → `Knoblauch`
- Tahini → `Sesam`, `Kerne` (tahini is sesame paste)

### Step 6: Sort Tags

Use German alphabetization (DIN 5007-1):
- ä → a
- ö → o
- ü → u
- ß → ss

### Step 7: Determine Category

Based on recipe name/description:
- `🥣` - Breakfast items (Müsli, Porridge, Frühstück, etc.)
- `🍲` - Main dishes (default)

### Step 8: Determine Author Folder

Based on URL domain:
- `chefkoch.de` → `recipes/Chefkoch/`
- `hellofresh.de` → `recipes/HelloFresh/`
- Otherwise → `recipes/mymindwentblvnk/`

Set `author` field to match folder name.

### Step 9: Create Filename

Convert recipe name to slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Replace umlauts: ä→ae, ö→oe, ü→ue, ß→ss

**Examples:**
- "Baba Ghanoush" → `baba-ghanoush.yaml`
- "Rührei wie im Hotel" → `ruehrei-wie-im-hotel.yaml`

### Step 10: Create YAML File

Format:
```yaml
name: Recipe Name
description: Description from site
author: Chefkoch
category: 🍲
servings: 4
prep_time: 15  # minutes
cook_time: 30  # minutes
tags:
  - Tag1
  - Tag2

ingredients:
  - name: Ingredient 1
    amount: 100 g
  - name: Ingredient 2
    amount: 2

instructions:
  - Step 1
  - Step 2
```

### Step 11: Regenerate HTML and Commit

```bash
python main.py
git add recipes/
git commit -m "Import recipe: [Recipe Name]

- Imported from [URL]
- [X] servings, [Y] minutes total time
- Source: [domain]

Co-Authored-By: Claude (@vertex-ai/anthropic.claude-sonnet-4-5@20250929) <noreply@anthropic.com>"
git push
```

## Important Notes

- **Verify tags** - Check hierarchical tags are complete
- **Review description** - May need editing for quality
- **Check times** - Ensure prep_time + cook_time makes sense
- **Simplify instructions** - Don't copy verbose text verbatim
- **Clean ingredients** - Remove unnecessary descriptors

## Example Workflow

```bash
# User invokes skill
/import-recipe https://www.chefkoch.de/rezepte/734461176124108/Baba-Ghanoush.html

# Skill executes:
1. curl + grep + sed + python to extract JSON-LD
2. Parse recipe data
3. Generate tags from ingredients
4. Create recipes/Chefkoch/baba-ghanoush.yaml
5. python main.py
6. git add + commit + push
```

## Error Handling

- **URL not accessible** - Inform user, ask for alternative
- **No JSON-LD found** - Try alternative parsing or ask user for manual entry
- **Invalid data** - Report what's missing, attempt reasonable defaults
- **Duplicate recipe** - Check if file exists, ask user if should overwrite
