# Fill Recipe Tags

Find all recipe YAML files in the recipes/ directory that are missing the 'tags' field.

For each recipe without tags:
1. Read the full recipe YAML file
2. Analyze the ingredients list
3. Generate tags based on high-level ingredient categories using the rules and examples below
4. Add the tags field after the cook_time line
5. Save the updated file

## Tagging Rules

### General Principles

1. **Remove descriptors and adjectives**: "Griechischer Joghurt" → "Joghurt", "Rote Zwiebel" → "Zwiebel"
2. **Use base ingredient name**: "Kräuterfrischkäse" → "Frischkäse", "Salatgurke" → "Gurke"
3. **Group similar items**: "Möhren" and "Karotte" both → "Karotte"
4. **Be specific for vegetables**: Don't use generic "Gemüse", use specific names like "Karotte", "Zwiebel", "Tomate"
5. **Use singular form**: "Eier" → "Eier", "Tomaten" → "Tomate"
6. **Capitalize tags**: All tags should start with an uppercase letter
7. **Sort alphabetically**: Tags list should be sorted
8. **Use hierarchical tags**: For categorized ingredients, include BOTH the generic category tag AND the specific ingredient tag (e.g., both "Fisch" and "Lachs", both "Nüsse" and "Mandeln")

### Hierarchical Tagging

For ingredients that belong to broader categories, add BOTH the generic tag AND the specific tag. Do NOT go deeper than one level of specificity.

**Examples:**
- Wildlachs → Add tags: "Fisch" + "Lachs" (NOT "Wildlachs")
- Haselnüsse → Add tags: "Nüsse" + "Haselnüsse"
- Süßkartoffel → Add tags: "Kartoffeln" + "Süßkartoffel"
- Frischkäse → Add tags: "Käse" + "Frischkäse"

**Tag Hierarchies:**

1. **Fish (Fisch):**
   - Add "Fisch" + specific type: "Lachs", "Thunfisch", "Seelachs", "Garnelen"
   - Example: Wildlachsfilet → tags: "Fisch", "Lachs"

2. **Meat (Fleisch):**
   - Add "Fleisch" + specific type: "Rind", "Pute", "Schinken", "Hackfleisch"
   - Example: Rinderfilet → tags: "Fleisch", "Rind"

3. **Cheese (Käse):**
   - Add "Käse" + specific type: "Feta", "Schafskäse", "Parmesan", "Bergkäse", "Frischkäse"
   - Example: Kräuterfrischkäse → tags: "Käse", "Frischkäse"

4. **Nuts (Nüsse):**
   - Add "Nüsse" + specific type: "Walnüsse", "Haselnüsse", "Mandeln"
   - Example: Haselnüsse (gehackt) → tags: "Nüsse", "Haselnüsse"

5. **Berries (Beeren):**
   - Add "Beeren" + specific type: "Himbeeren", "Erdbeeren"
   - Example: Himbeeren (frisch) → tags: "Beeren", "Himbeeren"

6. **Fruit (Obst):**
   - Add "Obst" + specific type: "Apfel", "Kiwi", "Weintrauben"
   - Example: Äpfel → tags: "Obst", "Apfel"

7. **Seeds (Kerne):**
   - Add "Kerne" + specific type: "Chiasamen", "Leinsamen", "Sesam"
   - Example: Chiasamen → tags: "Kerne", "Chiasamen"
   - Note: "Kürbiskerne", "Sonnenblumenkerne" → only "Kerne" (these ARE the specific level)

8. **Potatoes (Kartoffeln):**
   - Add "Kartoffeln" + specific type: "Süßkartoffel"
   - Example: Süßkartoffel → tags: "Kartoffeln", "Süßkartoffel"

9. **Cabbage/Brassica (Kohl):**
   - Add "Kohl" + specific type: "Blumenkohl", "Brokkoli"
   - Example: Blumenkohl → tags: "Kohl", "Blumenkohl"

### Category Guidelines

**For vegetables:** Use the specific vegetable name (e.g., "Karotte", "Zwiebel", "Tomate", "Gurke", "Spinat")
- Exception: For cabbage family, use both "Kohl" + specific type ("Blumenkohl", "Brokkoli")

**For proteins:** Use hierarchical tagging:
- Fish → Always add BOTH "Fisch" + specific type ("Lachs", "Thunfisch", "Seelachs", "Garnelen")
- Meat → Always add BOTH "Fleisch" + specific type ("Rind", "Pute", "Schinken", "Hackfleisch")
- Eggs → "Eier" (no subtypes)

**For dairy:** Use hierarchical tagging for cheese:
- Cheese → Always add BOTH "Käse" + specific type ("Feta", "Schafskäse", "Parmesan", "Bergkäse", "Frischkäse")
- Milk products → "Milch", "Joghurt", "Quark" (no subtypes)
- Butter → "Butter" (no subtypes)

**For grains/starches:** Use the base name:
- Any rice → "Reis"
- Any pasta/noodles → "Pasta"
- Potatoes → "Kartoffeln" (add "Süßkartoffel" if applicable)
- Flour → "Mehl"

**For nuts/seeds:** Use hierarchical tagging:
- Nuts → Always add BOTH "Nüsse" + specific type ("Walnüsse", "Haselnüsse", "Mandeln")
- Seeds → Always add BOTH "Kerne" + specific type ("Chiasamen", "Leinsamen", "Sesam")
  - Exception: "Kürbiskerne", "Sonnenblumenkerne" use only "Kerne"

**For fruits:** Use hierarchical tagging:
- Berries → Always add BOTH "Beeren" + specific type ("Himbeeren", "Erdbeeren")
- Other fruits → Always add BOTH "Obst" + specific type ("Apfel", "Kiwi", "Weintrauben")

## Ingredient Mapping Examples

Use these examples as a guide. For new ingredients not listed, apply the general principles above.

**IMPORTANT**: For categorized ingredients, add BOTH the generic category tag AND the specific tag.

### Fish & Seafood
- "Lachs", "Seelachs", "Wildlachs", "Räucherlachs" → "Fisch" + "Lachs"
- "Wildlachs" → "Fisch" + "Lachs" (NOT "Wildlachs" - don't go deeper)
- "Seelachs" → "Fisch" + "Seelachs"
- "Thunfisch" → "Fisch" + "Thunfisch"
- "Garnelen" → "Fisch" + "Garnelen"

### Meat & Poultry
- "Rinderhackfleisch", "Rindfleisch", "Rinderfilet" → "Fleisch" + "Rind"
- "Hackfleisch" → "Fleisch" + "Hackfleisch"
- "Putenbrustfilet", "Pute" → "Fleisch" + "Pute"
- "Kochschinken" → "Fleisch" + "Schinken"

### Dairy & Cheese
- "Frischkäse", "Kräuterfrischkäse", "Körniger Frischkäse" → "Käse" + "Frischkäse"
- "Magerquark", "Quark" → "Quark"
- "Schafskäse" → "Käse" + "Schafskäse"
- "Feta" → "Käse" + "Feta"
- "Parmesan" → "Käse" + "Parmesan"
- "Bergkäse" → "Käse" + "Bergkäse"
- "Joghurt", "Griechischer Joghurt", "Naturjoghurt" → "Joghurt"
- "Milch", "Hafermilch", "Haferdrink", "Kokosdrink" → "Milch"
- "Butter", "Butterschmalz" → "Butter"

### Vegetables (IMPORTANT: Use SPECIFIC tags, NOT "Gemüse")
- "Zwiebel", "Frühlingszwiebel", "Rote Zwiebel" → "Zwiebel"
- "Knoblauch", "Knoblauchzehe" → "Knoblauch"
- "Möhren", "Karotte" → "Karotte"
- "Zucchini" → "Zucchini"
- "Aubergine" → "Aubergine"
- "Paprika", "Gelbe Paprika" → "Paprika"
- "Tomate", "Tomaten", "Kirschtomaten", "Getrocknete Tomaten" → "Tomate"
- "Blumenkohl" → "Kohl" + "Blumenkohl"
- "Brokkoli" → "Kohl" + "Brokkoli"
- "Spinat", "Blattspinat" → "Spinat"
- "Porree", "Porreestange" → "Porree"
- "Sellerie", "Knollensellerie", "Stangensellerie", "Petersilienwurzel" → "Sellerie"
- "Gurke", "Salatgurke" → "Gurke"
- "Avocado" → "Avocado"
- "Radieschen" → "Radieschen"
- "Rucola", "Salatherz", "Romana" → "Salat"
- "Erbsen" → "Erbsen"

### Herbs
- "Minze", "Petersilie", "Dill", "Schnittlauch" → "Kräuter"

### Potatoes & Pasta
- "Kartoffel" → "Kartoffeln"
- "Süßkartoffel" → "Kartoffeln" + "Süßkartoffel"
- "Gnocchi", "Pasta", "Nudeln", "Buchweizenpasta" → "Pasta"

### Rice & Grains
- "Reis", "Wildreis", "Risottoreis" → "Reis"
- "Haferflocken" → "Haferflocken"

### Flour
- "Mehl", "Buchweizenmehl", "Dinkelmehl", "Mandelmehl" → "Mehl"

### Nuts & Seeds
- "Walnüsse" → "Nüsse" + "Walnüsse"
- "Haselnüsse" → "Nüsse" + "Haselnüsse"
- "Mandeln (gemahlen)" → "Nüsse" + "Mandeln"
- "Chiasamen" → "Kerne" + "Chiasamen"
- "Leinsamen" → "Kerne" + "Leinsamen"
- "Sesam" → "Kerne" + "Sesam"
- "Kürbiskerne", "Sonnenblumenkerne" → "Kerne" (these are the specific level)

### Eggs
- "Eier", "Ei" → "Eier"

### Fruits & Berries
- "Himbeeren" → "Beeren" + "Himbeeren"
- "Erdbeeren" → "Beeren" + "Erdbeeren"
- "Äpfel", "Apfel" → "Obst" + "Apfel"
- "Kiwi" → "Obst" + "Kiwi"
- "Weintrauben" → "Obst" + "Weintrauben"

### Fats & Oils
- "Kokosöl", "Olivenöl", "Leinöl", "Sesamöl" → "Öl"

### Other
- "Honig" → "Honig"

## How to Handle Unknown Ingredients

If you encounter an ingredient not in the examples:

1. **Identify the base ingredient**: Remove brands, adjectives, preparation methods
   - "Bio-Vollkornmehl" → "Mehl"
   - "Geräucherter Tofu" → "tofu"
   - "Wildlachs" → "Lachs" (don't go too specific)

2. **Determine the category and apply hierarchical tagging**:
   - Vegetable? Use the specific vegetable name (or "Kohl" + specific for cabbage family)
   - Fish? Add BOTH "Fisch" + specific type ("Lachs", "Thunfisch", etc.)
   - Meat? Add BOTH "Fleisch" + specific type ("Rind", "Pute", "Schinken", "Hackfleisch")
   - Cheese? Add BOTH "Käse" + specific type ("Feta", "Parmesan", "Frischkäse", etc.)
   - Nuts? Add BOTH "Nüsse" + specific type ("Walnüsse", "Mandeln", "Haselnüsse")
   - Berries? Add BOTH "Beeren" + specific type ("Himbeeren", "Erdbeeren")
   - Fruit? Add BOTH "Obst" + specific type ("Apfel", "Kiwi", "Weintrauben")
   - Seeds? Add BOTH "Kerne" + specific type ("Chiasamen", "Leinsamen", "Sesam")
   - Eggs? Use "Eier"
   - Other dairy? Use "Joghurt", "Milch", "Quark", or "Butter"
   - Grains? Use "Reis", "Pasta", "Mehl", "Haferflocken"

3. **Use German base form**: Keep it simple and in German
   - "Cherry tomatoes" → "Tomate"
   - "Spring onions" → "Zwiebel"
   - "Wild salmon" → "Fisch" + "Lachs" (NOT "Wildlachs")

4. **Be consistent**: If similar ingredients already have tags, use the same pattern
   - If "Karotten" → "Karotte", then "Babymöhren" → "Karotte"
   - If "Wildlachs" → "Fisch" + "Lachs", then "Räucherlachs" → "Fisch" + "Lachs"

5. **Don't go deeper than one level of specificity**:
   - ✓ Correct: "Wildlachs" → "Fisch" + "Lachs"
   - ✗ Wrong: "Wildlachs" → "Fisch" + "Lachs" + "Wildlachs"

## Implementation Notes

- Match ingredient names in a case-insensitive manner
- For compound ingredients (e.g., "Kräuterfrischkäse"), extract the base ingredient
- Apply the tagging rules to determine the appropriate tag
- Tags should be sorted alphabetically
- Insert tags after the "cook_time:" line in the YAML file
- Format:
  ```yaml
  tags:
    - tag1
    - tag2
  ```

## Hierarchical Tagging Summary

### Quick Reference Table

| Ingredient | Generic Tag | + Specific Tag | Example |
|------------|-------------|----------------|---------|
| Wildlachs | fisch | lachs | "Fisch", "Lachs" |
| Thunfisch | fisch | thunfisch | "Fisch", "Thunfisch" |
| Seelachs | fisch | seelachs | "Fisch", "Seelachs" |
| Garnelen | fisch | garnelen | "Fisch", "Garnelen" |
| Rinderfilet | fleisch | rind | "Fleisch", "Rind" |
| Hackfleisch | fleisch | hackfleisch | "Fleisch", "Hackfleisch" |
| Putenbrustfilet | fleisch | pute | "Fleisch", "Pute" |
| Kochschinken | fleisch | schinken | "Fleisch", "Schinken" |
| Frischkäse | käse | frischkäse | "Käse", "Frischkäse" |
| Feta | käse | feta | "Käse", "Feta" |
| Schafskäse | käse | schafskäse | "Käse", "Schafskäse" |
| Parmesan | käse | parmesan | "Käse", "Parmesan" |
| Bergkäse | käse | bergkäse | "Käse", "Bergkäse" |
| Walnüsse | nüsse | walnüsse | "Nüsse", "Walnüsse" |
| Haselnüsse | nüsse | haselnüsse | "Nüsse", "Haselnüsse" |
| Mandeln | nüsse | mandeln | "Nüsse", "Mandeln" |
| Himbeeren | beeren | himbeeren | "Beeren", "Himbeeren" |
| Erdbeeren | beeren | erdbeeren | "Beeren", "Erdbeeren" |
| Äpfel | obst | apfel | "Obst", "Apfel" |
| Kiwi | obst | kiwi | "Obst", "Kiwi" |
| Weintrauben | obst | weintrauben | "Obst", "Weintrauben" |
| Chiasamen | kerne | chiasamen | "Kerne", "Chiasamen" |
| Leinsamen | kerne | leinsamen | "Kerne", "Leinsamen" |
| Sesam | kerne | sesam | "Kerne", "Sesam" |
| Süßkartoffel | kartoffeln | süßkartoffel | "Kartoffeln", "Süßkartoffel" |
| Blumenkohl | kohl | blumenkohl | "Kohl", "Blumenkohl" |
| Brokkoli | kohl | brokkoli | "Kohl", "Brokkoli" |

### Key Rule: ONE LEVEL OF SPECIFICITY

**Always stop at the second level. Never go deeper.**

- ✓ Correct: Wildlachsfilet → "Fisch", "Lachs"
- ✗ Wrong: Wildlachsfilet → "Fisch", "Lachs", "Wildlachs"

## After Processing

- Show a summary of which recipes were updated
- Regenerate HTML files using: python main.py
- Commit changes with message: "Add tags to recipes without tags"
