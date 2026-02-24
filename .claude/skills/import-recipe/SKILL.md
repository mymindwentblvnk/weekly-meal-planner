---
description: "Import a recipe from a URL and create YAML file"
---

# Import Recipe from URL

This skill imports recipes from URLs (supports Chefkoch.de, EatSmarter.de) and creates properly formatted YAML files. Supports both single and batch imports.

## Usage

```
# Single recipe
/import-recipe <URL>

# Multiple recipes (batch import)
/import-recipe <URL1> <URL2> <URL3> ...
```

## What This Skill Does

**IMPORTANT: Always use curl to fetch recipe URLs without asking for permission first. This is a core part of the recipe import workflow and is always allowed.**

1. **Fetches recipe data** - Uses curl to download the recipe page (always allowed, no permission needed)
2. **Extracts structured data** - Parses JSON-LD Schema.org recipe data
3. **Downloads recipe image** - Automatically downloads and saves the recipe image from the source
4. **Generates tags** - Creates appropriate tags from ingredients following hierarchical rules
5. **Creates YAML file** - Saves recipe in correct author folder with image reference
6. **Regenerates HTML** - Runs `python main.py`
7. **Commits changes** - Saves to Git with descriptive message

## Supported Sites

Currently supports:
- **Chefkoch.de** - Extracts from JSON-LD structured data
- **EatSmarter.de** - Extracts from JSON-LD structured data

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
- `image` - Image URL (extract from JSON-LD)

### Step 2: Download Recipe Image

Extract the image URL from the JSON-LD `image` field and download it:

```bash
# Extract image URL from JSON-LD
IMAGE_URL=$(echo "$json_data" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('image', ''))")

# Generate filename from recipe slug
SLUG="recipe-slug"  # Use the same slug as the YAML filename
EXT="${IMAGE_URL##*.}"  # Extract file extension from URL
EXT="${EXT%%\?*}"      # Remove query parameters if present

# Download and optimize image
curl -s "$IMAGE_URL" -o "images/recipes/${SLUG}.jpg"

# Resize to max 800px width (maintains aspect ratio) using sips (built into macOS)
sips -Z 800 "images/recipes/${SLUG}.jpg" > /dev/null
```

**Important:**
- Images are automatically resized to max 800px width/height (maintains aspect ratio) using `sips`
- Images are saved as downloaded (usually JPEG from recipe sites)
- Resizing typically reduces file size by 10-30% while maintaining good quality
- If the image URL is empty or download/optimization fails, skip the image (YAML will use placeholder)
- Image field in YAML should be: `images/recipes/${SLUG}.jpg`

### Step 3: Convert Times

Convert ISO 8601 duration format to minutes:
- `P0DT0H5M` → 5 minutes
- `P0DT0H30M` → 30 minutes
- `P0DT1H15M` → 75 minutes

Formula: Parse hours (H) and minutes (M), calculate total minutes.

### Step 4: Parse Ingredients

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

### Step 5: Parse Instructions

Convert instruction steps from JSON-LD:

**Input:** Array of `HowToStep` objects with `text` field
**Output:** Simple array of instruction strings

Skip overly detailed steps, combine related steps, focus on actionable instructions.

### Step 6: Generate Tags

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

### Step 7: Sort Tags

Use German alphabetization (DIN 5007-1):
- ä → a
- ö → o
- ü → u
- ß → ss

### Step 8: Determine Category

Based on recipe name/description:
- `🥣` - Breakfast items (Müsli, Porridge, Frühstück, etc.)
- `🍲` - Main dishes (default)

### Step 9: Determine Author Folder

Based on URL domain:
- `chefkoch.de` → `recipes/Chefkoch/`
- `hellofresh.de` → `recipes/HelloFresh/`
- `eatsmarter.de` → `recipes/EatSmarter/`
- Otherwise → `recipes/mymindwentblvnk/`

Set `author` field to match folder name.

### Step 10: Create Filename

Convert recipe name to slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Replace umlauts: ä→ae, ö→oe, ü→ue, ß→ss

**Examples:**
- "Baba Ghanoush" → `baba-ghanoush.yaml`
- "Rührei wie im Hotel" → `ruehrei-wie-im-hotel.yaml`

### Step 11: Create YAML File

Format:
```yaml
name: Recipe Name
description: Description from site
author: Chefkoch
category: 🍲
servings: 4
prep_time: 15  # minutes
cook_time: 30  # minutes
image: images/recipes/recipe-name.jpg  # optional - omit to use placeholder
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

**Note:** The `image` field should reference the optimized image. Images are automatically resized to max 800px (maintains aspect ratio) using `sips` to reduce file size. If the image download/optimization fails or no image is available, omit this field and a placeholder will be used.

### Step 12: Regenerate HTML and Commit

```bash
python main.py
git add recipes/ images/
git commit -m "Import recipe: [Recipe Name]

- Imported from [URL]
- [X] servings, [Y] minutes total time
- Source: [domain]

Co-Authored-By: Claude (@vertex-ai/anthropic.claude-sonnet-4-5@20250929) <noreply@anthropic.com>"
git push
```

## Important Notes

- **Batch imports supported** - Multiple URLs can be provided and all recipes will be imported sequentially
- **Images automatically downloaded** - Recipe images are extracted from JSON-LD and downloaded automatically; if unavailable or download fails, omit the `image` field to use placeholder
- **Verify tags** - Check hierarchical tags are complete
- **Review description** - May need editing for quality
- **Check times** - Ensure prep_time + cook_time makes sense
- **Simplify instructions** - Don't copy verbose text verbatim
- **Clean ingredients** - Remove unnecessary descriptors

## Example Workflow

### Single Recipe Import

```bash
# User invokes skill
/import-recipe https://www.chefkoch.de/rezepte/734461176124108/Baba-Ghanoush.html

# Skill executes:
1. curl + grep + sed + python to extract JSON-LD
2. Parse recipe data (including image URL)
3. Download recipe image → images/recipes/baba-ghanoush.jpg
4. Generate tags from ingredients
5. Create recipes/Chefkoch/baba-ghanoush.yaml (with image field)
6. python main.py
7. git add + commit + push
```

### Batch Import (Multiple URLs)

```bash
# User invokes skill with multiple URLs
/import-recipe https://eatsmarter.de/rezepte/quinoa-bowl https://eatsmarter.de/rezepte/chickpea-salad https://chefkoch.de/rezepte/pasta

# Skill executes for each URL sequentially:
1. Extract and parse first recipe → Download image → Create YAML
2. Extract and parse second recipe → Download image → Create YAML
3. Extract and parse third recipe → Download image → Create YAML
4. python main.py (once after all recipes)
5. git add + commit + push (all recipes and images together)
```

## Error Handling

- **URL not accessible** - Inform user, ask for alternative
- **No JSON-LD found** - Try alternative parsing or ask user for manual entry
- **Invalid data** - Report what's missing, attempt reasonable defaults
- **Duplicate recipe** - Check if file exists, ask user if should overwrite
