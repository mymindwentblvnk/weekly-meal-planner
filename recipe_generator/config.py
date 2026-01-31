"""Configuration and constants for the recipe generator."""

from pathlib import Path


# Directory configuration
RECIPES_DIR = Path("recipes")
OUTPUT_DIR = Path("output")

# Language configuration - set to "de" for German or "en" for English
LANGUAGE = "de"

# Text strings for internationalization
TEXTS = {
    "de": {
        # Overview page
        "overview_title": "Rezeptsammlung",
        "servings": "Portionen",
        "min_total": "min gesamt",
        "view_recipe": "Rezept ansehen →",
        "last_updated": "Zuletzt aktualisiert:",
        "filter_all": "Alle",
        "filter_meat": "Fleisch",
        "filter_fish": "Fisch",
        "filter_vegetarian": "Vegetarisch",
        "filter_sweet": "Süß",

        # Detail page
        "recipe_title_suffix": "Rezept",
        "back_to_recipes": "← Zurück zur Übersicht",
        "prep_time": "Vorbereitungszeit:",
        "cook_time": "Kochzeit:",
        "minutes": "Minuten",
        "servings_label": "Portionen:",
        "ingredients_heading": "Zutaten:",
        "instructions_heading": "Zubereitung:",
    },
    "en": {
        # Overview page
        "overview_title": "Recipe Collection",
        "servings": "servings",
        "min_total": "min total",
        "view_recipe": "View Recipe →",
        "last_updated": "Last updated:",
        "filter_all": "All",
        "filter_meat": "Meat",
        "filter_fish": "Fish",
        "filter_vegetarian": "Vegetarian",
        "filter_sweet": "Sweet",

        # Detail page
        "recipe_title_suffix": "Recipe",
        "back_to_recipes": "← Back to Recipes",
        "prep_time": "Prep time:",
        "cook_time": "Cook time:",
        "minutes": "minutes",
        "servings_label": "Servings:",
        "ingredients_heading": "Ingredients:",
        "instructions_heading": "Instructions:",
    },
}

def get_text(key: str) -> str:
    """Get text string for the current language."""
    return TEXTS[LANGUAGE].get(key, key)

# CSS Styles
COMMON_CSS = """
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
"""

DETAIL_PAGE_CSS = """
.back-button {
    display: inline-block;
    padding: 8px 16px;
    margin-bottom: 20px;
    background-color: #e2e8f0;
    color: #2d3748;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}
.back-button:hover {
    background-color: #cbd5e0;
    text-decoration: none;
}
.amount {
    font-weight: bold;
    min-width: 80px;
    display: inline-block;
    color: #2c5282;
}
.ingredient {
    color: #333;
}
ul {
    list-style-type: none;
    padding-left: 0;
}
li {
    padding: 5px 0;
}
"""

OVERVIEW_PAGE_CSS = """
h1 {
    color: #2c5282;
}
.filter-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    flex-wrap: wrap;
}
.filter-btn {
    padding: 10px 20px;
    border: 2px solid #2c5282;
    background-color: white;
    color: #2c5282;
    border-radius: 6px;
    font-size: 1em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}
.filter-btn:hover {
    background-color: #e2e8f0;
}
.filter-btn.active {
    background-color: #2c5282;
    color: white;
}
.recipe-card {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #f7fafc;
    transition: box-shadow 0.2s;
}
.recipe-card.hidden {
    display: none;
}
.recipe-card:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.recipe-card h2 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #2d3748;
}
.recipe-card h2 a {
    color: #2c5282;
    text-decoration: none;
}
.recipe-card h2 a:hover {
    text-decoration: underline;
}
.description {
    color: #4a5568;
    line-height: 1.6;
    margin-bottom: 12px;
}
.meta {
    color: #718096;
    font-size: 0.9em;
    margin-bottom: 15px;
}
.view-recipe-btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: #2c5282;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}
.view-recipe-btn:hover {
    background-color: #1e3a5f;
    text-decoration: none;
}
.deployment-info {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    color: #718096;
    font-size: 0.85em;
}
.deployment-info p {
    margin: 0;
}
"""
