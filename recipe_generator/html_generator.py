"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

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
    <a href="index.html" class="back-button">← Back to Recipes</a>
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
        <span>Servings: {recipe['servings']}</span>

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


def generate_overview_html(
    recipes_data: list[tuple[str, dict[str, Any]]],
    deployment_time: datetime | None = None
) -> str:
    """Generate overview page listing all recipes.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)
        deployment_time: Optional datetime for when the page was deployed

    Returns:
        Complete HTML page as a string
    """
    # Generate recipe entries
    recipe_entries = []
    for filename, recipe in recipes_data:
        description = escape(recipe.get('description', ''))
        servings = recipe['servings']
        prep_time = recipe['prep_time']
        cook_time = recipe['cook_time']

        recipe_entry = f'''    <div class="recipe-card">
        <h2><a href="{escape(filename)}">{escape(recipe['name'])}</a></h2>
        <p class="description">{description}</p>
        <p class="meta">
            <span class="servings">🍽️ {servings} servings</span> •
            <span class="time">⏱️ {prep_time + cook_time} min total</span>
        </p>
        <a href="{escape(filename)}" class="view-recipe-btn">View Recipe →</a>
    </div>'''
        recipe_entries.append(recipe_entry)

    # Generate footer with deployment time
    footer_html = ""
    if deployment_time:
        formatted_time = deployment_time.strftime("%B %d, %Y at %H:%M UTC")
        footer_html = f'''
    <footer class="deployment-info">
        <p>Last updated: {formatted_time}</p>
    </footer>'''

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
    <p>Browse recipes and click through to add ingredients to your Bring! shopping list.</p>

{chr(10).join(recipe_entries)}{footer_html}
</body>
</html>'''

    return html
