# Update Ingredient Prices

Maintains the BIO ingredient price database by scanning recipes and updating missing prices.

## Usage

```
/update-prices [mode]
```

**Modes:**
- `check` - Show missing ingredients (default)
- `add` - Add missing ingredients with price estimates
- `search` - Search online for BIO prices and update
- `report` - Generate full coverage report

## What This Skill Does

1. **Scans all recipes** - Extracts unique ingredients from all YAML files
2. **Checks price database** - Compares with `ingredient_prices.yaml`
3. **Identifies missing prices** - Lists ingredients without prices
4. **Updates database** - Adds estimated prices for missing items
5. **Generates report** - Shows coverage statistics

## Workflow

### Mode: check (default)

```bash
/update-prices
/update-prices check
```

**Output:**
- List of ingredients in recipes
- Missing ingredients (not in price database)
- Coverage percentage
- Suggestions for updating

### Mode: add

```bash
/update-prices add
```

**Actions:**
1. Find all missing ingredients
2. Research BIO prices online
3. Add to `ingredient_prices.yaml`
4. Regenerate HTML with updated costs
5. Commit changes

**Research sources:**
- REWE Bio online shop
- Edeka Bio
- Bio Company
- General BIO price databases

### Mode: search

```bash
/update-prices search
```

**Actions:**
1. For each missing ingredient:
   - Search online for current BIO prices
   - Extract price and unit
   - Add to database with source note
2. Review and confirm before adding
3. Regenerate and commit

### Mode: report

```bash
/update-prices report
```

**Output:**
- Total ingredients in recipes: XX
- Ingredients with prices: XX (XX%)
- Missing ingredients: XX (XX%)
- Most expensive ingredients
- Cheapest ingredients
- Average recipe cost
- Recipes with incomplete costs

## Process Details

### Step 1: Scan Recipes

```python
# Scan all YAML files in recipes/ directory
for yaml_file in recipes_dir.glob("**/*.yaml"):
    - Extract ingredients list
    - Get ingredient names
    - Normalize variations (e.g., "Tomate" vs "Tomaten")
```

### Step 2: Load Price Database

```python
# Read ingredient_prices.yaml
prices = load_yaml("ingredient_prices.yaml")
existing_ingredients = set(prices.keys())
```

### Step 3: Find Missing

```python
recipe_ingredients = set(all_ingredient_names)
missing = recipe_ingredients - existing_ingredients
```

### Step 4: Research Prices (add/search mode)

For each missing ingredient:
1. Search "BIO [ingredient] Preis Deutschland 2026"
2. Check REWE Bio, Edeka Bio online shops
3. Extract typical BIO price
4. Determine appropriate unit (kg, L, piece, bunch)
5. Calculate average if multiple sources

### Step 5: Update Database

```yaml
# Add to ingredient_prices.yaml in alphabetical order
New_Ingredient: {price: X.XX, unit: "kg/L/piece", notes: "added by update-prices YYYY-MM-DD"}
```

### Step 6: Validate

- Check price format (positive number)
- Check unit is valid (kg, L, piece, bunch)
- Verify ingredient name matches recipe usage
- Sort alphabetically within categories

### Step 7: Regenerate & Commit

```bash
python main.py
git add ingredient_prices.yaml
git commit -m "Update prices: add XX new ingredients"
```

## Price Research Strategy

### Online Sources (in order of preference)

1. **REWE Bio** (rewe.de/bio)
   - Most reliable online shop
   - Current prices
   - Clear per-unit pricing

2. **Edeka Bio** (edeka.de)
   - Good coverage
   - Regional availability

3. **Bio Company**
   - Premium BIO prices
   - Good for specialty items

4. **Amazon Fresh Bio**
   - Backup source
   - May be higher than supermarket

5. **Price comparison sites**
   - idealo.de
   - geizhals.de
   - Filter for BIO products

### Price Estimation Rules

When exact price not found:
- Use similar ingredient as baseline
- Apply BIO markup (~30-50% over conventional)
- Conservative estimate (round up)
- Add note: "estimated - needs verification"

**Examples:**
- No BIO tomato price → Use conventional price × 1.4
- Specialty item → Use similar category average
- Imported item → Add 20% premium

### Unit Determination

```python
def determine_unit(ingredient_name, typical_usage):
    if ingredient in ['Milch', 'Öl', 'Essig', 'Brühe']:
        return "L"
    elif ingredient in ['Eier', 'Gurke', 'Zitrone', 'Zwiebel']:
        return "piece"
    elif ingredient in ['Petersilie', 'Koriander', 'Basilikum']:
        return "bunch"
    else:
        return "kg"  # Default for most items
```

## Ingredient Normalization

Handle variations:
- Singular/plural: "Tomate" ↔ "Tomaten"
- Descriptors: "Griechischer Joghurt" → "Joghurt"
- Parentheses: "Eier (groß)" → "Eier"
- Qualifiers: Remove "frisch", "gefroren", etc.

**Normalization rules:**
1. Use base form in price database
2. Strip parentheses content
3. Remove adjectives (groß, klein, frisch)
4. Use plural form for countables
5. Keep compound words intact

## Coverage Report Format

```
╔════════════════════════════════════════╗
║   BIO Price Database Coverage Report   ║
╠════════════════════════════════════════╣
║ Total unique ingredients:         127  ║
║ With prices:                      98   ║
║ Missing prices:                   29   ║
║ Coverage:                      77.2%   ║
╠════════════════════════════════════════╣
║ Total recipes:                    42   ║
║ Recipes with full costs:          31   ║
║ Recipes with partial costs:       11   ║
╠════════════════════════════════════════╣
║ Most expensive ingredients:            ║
║   - Pinienkerne: 45.00 €/kg           ║
║   - Lachs: 38.00 €/kg                 ║
║   - Zimt: 40.00 €/kg                  ║
╠════════════════════════════════════════╣
║ Missing ingredients:                   ║
║   - Aubergine                          ║
║   - Zucchini                           ║
║   - Brokkoli                           ║
║   ... (show first 20)                  ║
╚════════════════════════════════════════╝
```

## Examples

### Example 1: Check mode

```bash
$ /update-prices check

Scanning recipes...
Found 127 unique ingredients across 42 recipes

Price database coverage: 77.2% (98/127)

Missing ingredients (29):
  - Aubergine (used in: Baba Ghanoush, Moussaka)
  - Zucchini (used in: Ratatouille, Gemüsepfanne)
  - Brokkoli (used in: Brokkoli-Auflauf)
  ...

Recommendations:
  1. Run '/update-prices add' to research and add prices
  2. Manually update ingredient_prices.yaml
  3. Check REWE Bio for current prices
```

### Example 2: Add mode

```bash
$ /update-prices add

Scanning recipes...
Found 29 missing ingredients

Researching BIO prices online...

Found prices:
  ✓ Aubergine: 6.00 €/kg (from REWE Bio)
  ✓ Zucchini: 4.50 €/kg (from Edeka Bio)
  ✓ Brokkoli: 7.00 €/kg (from REWE Bio)
  ...

Adding to ingredient_prices.yaml...
Updated database with 29 new prices

Regenerating HTML...
Done! Generated 42 recipe(s)

Committing changes...
[main abc1234] Update prices: add 29 new ingredients
```

## Important Notes

- **Always verify prices** - Online searches are estimates
- **BIO quality required** - Only use organic/BIO prices
- **Regional variation** - Prices vary by location
- **Seasonal items** - May need seasonal price ranges
- **Update quarterly** - Keep prices current

## Error Handling

- **Ingredient not found online** - Add with note "needs manual pricing"
- **Ambiguous ingredient** - Ask for clarification
- **Invalid unit** - Default to "kg" with warning
- **Duplicate entries** - Merge variations, keep lower price
- **Missing recipe data** - Skip and report

## Maintenance

After running update-prices:
1. Review added prices for accuracy
2. Check for duplicate/similar entries
3. Merge variations (e.g., "Tomate" and "Tomaten")
4. Verify units are correct
5. Add helpful notes for specialty items
6. Sort database alphabetically
7. Commit with descriptive message

## Success Criteria

- ✅ Coverage > 95%
- ✅ All common ingredients priced
- ✅ Prices updated in last 3 months
- ✅ Database sorted and clean
- ✅ All prices have valid units
- ✅ Notes for estimated/uncertain prices
