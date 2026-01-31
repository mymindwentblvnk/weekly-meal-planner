import yaml
from pathlib import Path
from typing import Any


def format_time(minutes: int) -> str:
    """Convert minutes to ISO 8601 duration format (PT{minutes}M)."""
    return f"PT{minutes}M"


def generate_html(recipe: dict[str, Any]) -> str:
    """Generate HTML with Schema.org microdata and Bring! widget from recipe data."""

    # Generate ingredients HTML
    ingredients_html = []
    for ingredient in recipe['ingredients']:
        ingredients_html.append(f'''            <li itemprop="recipeIngredient">
                <span class="amount">{ingredient['amount']}</span>
                <span class="ingredient">{ingredient['name']}</span>
            </li>''')

    # Generate instructions HTML
    instructions_html = []
    for instruction in recipe['instructions']:
        instructions_html.append(f'''                <li itemprop="itemListElement" itemscope itemtype="https://schema.org/HowToStep">
                    <span itemprop="text">{instruction}</span>
                </li>''')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{recipe['name']} Recipe</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .amount {{
            font-weight: bold;
            min-width: 80px;
            display: inline-block;
            color: #2c5282;
        }}
        .ingredient {{
            color: #333;
        }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        li {{
            padding: 5px 0;
        }}
    </style>
</head>
<body>
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{recipe['name']}</h1>

        <p itemprop="description">{recipe.get('description', '')}</p>

        <div itemprop="author" itemscope itemtype="https://schema.org/Person">
            <meta itemprop="name" content="{recipe.get('author', 'Unknown')}">
        </div>

        <time itemprop="prepTime" datetime="{format_time(recipe['prep_time'])}">Prep time: {recipe['prep_time']} minutes</time>
        <br>
        <time itemprop="cookTime" datetime="{format_time(recipe['cook_time'])}">Cook time: {recipe['cook_time']} minutes</time>
        <br>
        <meta itemprop="recipeYield" content="{recipe['servings']} servings">
        <span>Yield: {recipe['servings']} servings</span>

        <h2>Ingredients:</h2>
        <ul>
{chr(10).join(ingredients_html)}
        </ul>

        <h2>Instructions:</h2>
        <div itemprop="recipeInstructions" itemscope itemtype="https://schema.org/HowToSection">
            <ol>
{chr(10).join(instructions_html)}
            </ol>
        </div>
    </div>
    <script async="async" src="//platform.getbring.com/widgets/import.js"></script>
<div data-bring-import style="display:none">
       <a href="https://www.getbring.com">Bring! Einkaufsliste App f&uuml;r iPhone und Android</a>
</div>
</body>
</html>'''

    return html


def generate_overview_html(recipes_data: list[tuple[str, dict[str, Any]]]) -> str:
    """Generate overview page listing all recipes with Bring! widgets."""

    # Generate recipe entries
    recipe_entries = []
    for filename, recipe in recipes_data:
        # Get ingredient names only (without amounts) for display
        ingredient_names = [ing['name'] for ing in recipe['ingredients']]
        ingredients_list = ', '.join(ingredient_names)

        # Generate full ingredient list with Schema.org markup for Bring! widget
        ingredients_schema = []
        for ingredient in recipe['ingredients']:
            # Format: amount + name (e.g., "500g flour")
            ingredients_schema.append(f'            <meta itemprop="recipeIngredient" content="{ingredient["amount"]} {ingredient["name"]}">')

        recipe_entry = f'''    <div class="recipe-card" itemscope itemtype="https://schema.org/Recipe">
        <h2><a href="{filename}" itemprop="name">{recipe['name']}</a></h2>
        <p class="ingredients"><strong>Ingredients:</strong> {ingredients_list}</p>

        <meta itemprop="description" content="{recipe.get('description', '')}">
        <meta itemprop="recipeYield" content="{recipe['servings']} servings">
        <meta itemprop="prepTime" content="{format_time(recipe['prep_time'])}">
        <meta itemprop="cookTime" content="{format_time(recipe['cook_time'])}">
{chr(10).join(ingredients_schema)}

        <script async="async" src="//platform.getbring.com/widgets/import.js"></script>
        <div data-bring-import style="display:none">
            <a href="https://www.getbring.com">Bring! Einkaufsliste App f&uuml;r iPhone und Android</a>
        </div>
    </div>'''
        recipe_entries.append(recipe_entry)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Collection</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c5282;
        }}
        .recipe-card {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f7fafc;
        }}
        .recipe-card h2 {{
            margin-top: 0;
            color: #2d3748;
        }}
        .recipe-card a {{
            color: #2c5282;
            text-decoration: none;
        }}
        .recipe-card a:hover {{
            text-decoration: underline;
        }}
        .ingredients {{
            color: #4a5568;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <h1>Recipe Collection</h1>
    <p>Browse all recipes and add ingredients to your Bring! shopping list with one click.</p>

{chr(10).join(recipe_entries)}
</body>
</html>'''

    return html


def main():
    """Generate HTML files from YAML recipes."""
    recipes_dir = Path("recipes")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Store recipes for overview generation
    recipes_data = []

    # Process all YAML files in recipes directory
    for yaml_file in recipes_dir.glob("*.yaml"):
        print(f"Processing {yaml_file.name}...")

        # Read YAML recipe
        with open(yaml_file, 'r', encoding='utf-8') as f:
            recipe = yaml.safe_load(f)

        # Generate recipe detail HTML
        html = generate_html(recipe)

        # Write HTML file
        output_filename = f"{yaml_file.stem}.html"
        output_file = output_dir / output_filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  → Generated {output_file}")

        # Store recipe data for overview
        recipes_data.append((output_filename, recipe))

    # Generate overview page
    print("Generating overview page...")
    overview_html = generate_overview_html(recipes_data)
    overview_file = output_dir / "index.html"
    with open(overview_file, 'w', encoding='utf-8') as f:
        f.write(overview_html)
    print(f"  → Generated {overview_file}")

    print("\nDone! HTML files are in the 'output' directory.")


if __name__ == "__main__":
    main()
