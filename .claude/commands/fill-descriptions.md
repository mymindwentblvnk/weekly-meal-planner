---
description: "Generate descriptions for all recipes that have 'tbd.' as description",
---

Find all recipe YAML files in the recipes/ directory that have 'description: tbd.' in them.
For each recipe with tbd. description:
1. Read the full recipe YAML file
2. Analyze the recipe name, ingredients, and instructions
3. Generate a concise, appetizing German description (1-2 sentences) that:
   - Highlights the main ingredients (skip common ones like salt, pepper, oil, eggs, onions)
   - Describes what makes this recipe special or appealing
   - Matches the style of existing recipe descriptions
4. Replace 'description: tbd.' with the generated description
5. Save the updated file

After updating all recipes:
  - Regenerate the HTML files using: uv run python main.py
  - Show a summary of which recipes were updated
  - Commit all changes with message: 'Generate descriptions for recipes with tbd.'
  - Push to remote

Be creative but keep descriptions authentic and appetizing!
