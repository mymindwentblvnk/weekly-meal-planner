"""HTML generation functions for recipes."""

from typing import Any
from html import escape

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS


def format_time(minutes: int) -> str:
    """Convert minutes to ISO 8601 duration format (PT{minutes}M)."""
    return f"PT{minutes}M"


def generate_bring_widget(url: str = "") -> str:
    """Generate Bring! widget HTML.

    Args:
        url: Optional URL to import from. If empty, widget parses current page.
    """
    data_attr = f'data-bring-import="{escape(url)}"' if url else 'data-bring-import'
    return f'''<script async="async" src="//platform.getbring.com/widgets/import.js"></script>
<div {data_attr} style="display:none">
    <a href="https://www.getbring.com">Bring! Einkaufsliste App f&uuml;r iPhone und Android</a>
</div>'''


def generate_schema_metadata(recipe: dict[str, Any]) -> str:
    """Generate Schema.org metadata meta tags for a recipe."""
    metadata = f'''<meta itemprop="description" content="{escape(recipe.get('description', ''))}">
    <meta itemprop="recipeYield" content="{recipe['servings']} servings">
    <meta itemprop="prepTime" content="{format_time(recipe['prep_time'])}">
    <meta itemprop="cookTime" content="{format_time(recipe['cook_time'])}">'''

    # Add ingredient meta tags
    ingredient_tags = []
    for ingredient in recipe['ingredients']:
        # Convert to string and escape
        content = f"{escape(str(ingredient['amount']))} {escape(ingredient['name'])}"
        ingredient_tags.append(f'    <meta itemprop="recipeIngredient" content="{content}">')

    if ingredient_tags:
        metadata += '\n' + '\n'.join(ingredient_tags)

    return metadata


def generate_recipe_detail_html(recipe: dict[str, Any]) -> str:
    """Generate HTML with Schema.org microdata and Bring! widget from recipe data.

    Args:
        recipe: Recipe dictionary containing name, ingredients, instructions, etc.

    Returns:
        Complete HTML page as a string
    """
    # Generate ingredients HTML
    ingredients_html = []
    for ingredient in recipe['ingredients']:
        ingredients_html.append(f'''            <li itemprop="recipeIngredient">
                <span class="amount">{escape(str(ingredient['amount']))}</span>
                <span class="ingredient">{escape(ingredient['name'])}</span>
            </li>''')

    # Generate instructions HTML
    instructions_html = []
    for instruction in recipe['instructions']:
        instructions_html.append(f'''                <li itemprop="itemListElement" itemscope itemtype="https://schema.org/HowToStep">
                    <span itemprop="text">{escape(instruction)}</span>
                </li>''')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(recipe['name'])} Recipe</title>
    <style>
        {COMMON_CSS}
        {DETAIL_PAGE_CSS}
    </style>
</head>
<body>
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{escape(recipe['name'])}</h1>

        <p itemprop="description">{escape(recipe.get('description', ''))}</p>

        <div itemprop="author" itemscope itemtype="https://schema.org/Person">
            <meta itemprop="name" content="{escape(recipe.get('author', 'Unknown'))}">
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
    {generate_bring_widget()}
</body>
</html>'''

    return html


def generate_overview_html(recipes_data: list[tuple[str, dict[str, Any]]]) -> str:
    """Generate overview page listing all recipes with Bring! widgets.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)

    Returns:
        Complete HTML page as a string
    """
    # Generate recipe entries
    recipe_entries = []
    for filename, recipe in recipes_data:
        # Get ingredient names only (without amounts) for display
        ingredient_names = [escape(ing['name']) for ing in recipe['ingredients']]
        ingredients_list = ', '.join(ingredient_names)

        # Generate Schema.org metadata
        schema_metadata = generate_schema_metadata(recipe)

        recipe_entry = f'''    <div class="recipe-card" itemscope itemtype="https://schema.org/Recipe">
        <h2><a href="{escape(filename)}" itemprop="name">{escape(recipe['name'])}</a></h2>
        <p class="ingredients"><strong>Ingredients:</strong> {ingredients_list}</p>

        {schema_metadata}

        {generate_bring_widget()}
    </div>'''
        recipe_entries.append(recipe_entry)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Collection</title>
    <style>
        {COMMON_CSS}
        {OVERVIEW_PAGE_CSS}
    </style>
</head>
<body>
    <h1>Recipe Collection</h1>
    <p>Browse all recipes and add ingredients to your Bring! shopping list with one click.</p>

{chr(10).join(recipe_entries)}
</body>
</html>'''

    return html
