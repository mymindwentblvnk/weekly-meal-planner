---
description: "Generate descriptions for all recipes that are missing a description",
---

Find all recipe YAML files in the recipes/ directory that are missing the 'description' field or have an empty/placeholder description.

**Look for recipes where:**
- The 'description' field is missing entirely
- The description is empty ("")
- The description is "tbd." or "tbd"
- The description is "TODO" or similar placeholder

For each recipe without a proper description:
1. Read the full recipe YAML file
2. Analyze the recipe name, ingredients, and instructions
3. Generate a concise, appetizing German description (1-2 sentences) that:
   - Highlights the main ingredients (skip common ones like salt, pepper, oil, eggs, onions)
   - Describes what makes this recipe special or appealing
   - Matches the style of existing recipe descriptions
   - Is authentic and appetizing
4. Add or replace the description field with the generated description
5. Save the updated file

**Examples of good descriptions:**
- "Knusprige Thunfisch-Bouletten mit Butterbohnen auf frischem Romana-Salat, serviert mit cremiger Aioli-Joghurt-Soße und eingelegten Zwiebeln."
- "Glasierter Seelachs auf Sushireis mit eingelegtem Gurken-Karotten-Gemüse, verfeinert mit Sweet Chili Soße und Sesamöl."
- "Herzhaftes Brot mit Rucola, Haferflocken und Sesam."

After updating all recipes:
  - Regenerate the HTML files using: python main.py
  - Show a summary of which recipes were updated
  - Commit all changes with message: 'Generate descriptions for recipes without descriptions'
  - Push to remote

Be creative but keep descriptions authentic and appetizing!
