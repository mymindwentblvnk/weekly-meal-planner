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

1. **Remove descriptors and adjectives**: "Griechischer Joghurt" → "joghurt", "Rote Zwiebel" → "zwiebel"
2. **Use base ingredient name**: "Kräuterfrischkäse" → "frischkäse", "Salatgurke" → "gurke"
3. **Group similar items**: "Möhren" and "Karotte" both → "karotte"
4. **Be specific for vegetables**: Don't use generic "gemüse", use specific names like "karotte", "zwiebel", "tomate"
5. **Use singular form**: "Eier" → "eier", "Tomaten" → "tomate"
6. **Lowercase tags**: All tags should be lowercase
7. **Sort alphabetically**: Tags list should be sorted

### Category Guidelines

**For vegetables:** Use the specific vegetable name (e.g., "karotte", "zwiebel", "tomate", "gurke", "spinat")

**For proteins:** Group into main categories:
- Fish → "fisch"
- Meat → "fleisch" or specific type like "pute"
- Eggs → "eier"

**For dairy:** Be specific about the type:
- Cheese → "käse" (or specific like "frischkäse")
- Milk products → "milch", "joghurt", "quark"
- Butter → "butter"

**For grains/starches:** Use the base name:
- Any rice → "reis"
- Any pasta/noodles → "pasta"
- Potatoes → "kartoffeln"
- Flour → "mehl"

**For nuts/seeds:** Use the base name:
- Nuts → "nüsse"
- Seeds → use specific name like "sesam", "leinsamen", "chiasamen", or generic "kerne"

## Ingredient Mapping Examples

Use these examples as a guide. For new ingredients not listed, apply the general principles above:

### Fish & Seafood
- "Lachs", "Seelachs", "Wildlachs", "Räucherlachs" → "fisch"
- "Thunfisch" → "fisch"
- "Garnelen" → "fisch"

### Meat & Poultry
- "Rinderhackfleisch", "Rindfleisch", "Rinderfilet", "Hackfleisch" → "fleisch"
- "Putenbrustfilet", "Pute" → "pute"
- "Kochschinken" → "fleisch"

### Dairy & Cheese
- "Frischkäse", "Kräuterfrischkäse", "Körniger Frischkäse" → "frischkäse"
- "Magerquark", "Quark" → "quark"
- "Schafskäse", "Feta", "Parmesan", "Bergkäse" → "käse"
- "Joghurt", "Griechischer Joghurt", "Naturjoghurt" → "joghurt"
- "Milch", "Hafermilch", "Haferdrink", "Kokosdrink" → "milch"
- "Butter", "Butterschmalz" → "butter"

### Vegetables (IMPORTANT: Use SPECIFIC tags, NOT "gemüse")
- "Zwiebel", "Frühlingszwiebel", "Rote Zwiebel" → "zwiebel"
- "Knoblauch", "Knoblauchzehe" → "knoblauch"
- "Möhren", "Karotte" → "karotte"
- "Zucchini" → "zucchini"
- "Aubergine" → "aubergine"
- "Paprika", "Gelbe Paprika" → "paprika"
- "Tomate", "Tomaten", "Kirschtomaten", "Getrocknete Tomaten" → "tomate"
- "Blumenkohl", "Brokkoli" → "kohl"
- "Spinat", "Blattspinat" → "spinat"
- "Porree", "Porreestange" → "porree"
- "Sellerie", "Knollensellerie", "Stangensellerie", "Petersilienwurzel" → "sellerie"
- "Gurke", "Salatgurke" → "gurke"
- "Avocado" → "avocado"
- "Radieschen" → "radieschen"
- "Rucola", "Salatherz", "Romana" → "salat"
- "Erbsen" → "erbsen"

### Herbs
- "Minze", "Petersilie", "Dill", "Schnittlauch" → "kräuter"

### Potatoes & Pasta
- "Kartoffel", "Süßkartoffel" → "kartoffeln"
- "Gnocchi", "Pasta", "Nudeln", "Buchweizenpasta" → "pasta"

### Rice & Grains
- "Reis", "Wildreis", "Risottoreis" → "reis"
- "Haferflocken" → "haferflocken"
- "Chiasamen" → "chiasamen"

### Flour
- "Mehl", "Buchweizenmehl", "Dinkelmehl", "Mandelmehl" → "mehl"

### Nuts & Seeds
- "Nüsse", "Walnüsse", "Mandeln", "Haselnüsse" → "nüsse"
- "Sesam" → "sesam"
- "Leinsamen" → "leinsamen"
- "Kürbiskerne", "Sonnenblumenkerne" → "kerne"

### Eggs
- "Eier", "Ei" → "eier"

### Fruits
- "Himbeeren", "Erdbeeren" → "beeren"
- "Äpfel", "Apfel", "Kiwi", "Weintrauben" → "obst"

### Fats & Oils
- "Kokosöl", "Olivenöl", "Leinöl", "Sesamöl" → "öl"

### Other
- "Honig" → "honig"

## How to Handle Unknown Ingredients

If you encounter an ingredient not in the examples:

1. **Identify the base ingredient**: Remove brands, adjectives, preparation methods
   - "Bio-Vollkornmehl" → "mehl"
   - "Geräucherter Tofu" → "tofu"

2. **Determine the category**:
   - Vegetable? Use the specific vegetable name
   - Protein? Use "fleisch", "fisch", "pute", or "eier"
   - Dairy? Use "käse", "joghurt", "milch", "quark", or "frischkäse"
   - Grain? Use "reis", "pasta", "mehl", "haferflocken"

3. **Use German base form**: Keep it simple and in German
   - "Cherry tomatoes" → "tomate"
   - "Spring onions" → "zwiebel"

4. **Be consistent**: If similar ingredients already have tags, use the same pattern
   - If "Karotten" → "karotte", then "Babymöhren" → "karotte"

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

## After Processing

- Show a summary of which recipes were updated
- Regenerate HTML files using: python main.py
- Commit changes with message: "Add tags to recipes without tags"
