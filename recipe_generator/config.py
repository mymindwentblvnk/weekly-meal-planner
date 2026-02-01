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
        "filter_bread": "Brot",
        "filter_sweet": "Frühstück",
        "filter_fast": "Schnell (≤30 min)",

        # Detail page
        "recipe_title_suffix": "Rezept",
        "back_to_recipes": "← Zurück zur Übersicht",
        "prep_time": "Vorbereitungszeit",
        "cook_time": "Kochzeit",
        "minutes": "Minuten",
        "servings_label": "Portionen",
        "ingredients_heading": "Zutaten",
        "instructions_heading": "Zubereitung",
        "amount_label": "Menge",
        "ingredient_label": "Zutat",
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
        "filter_bread": "Bread",
        "filter_sweet": "Breakfast",
        "filter_fast": "Fast (≤30 min)",

        # Detail page
        "recipe_title_suffix": "Recipe",
        "back_to_recipes": "← Back to Recipes",
        "prep_time": "Prep time",
        "cook_time": "Cook time",
        "minutes": "minutes",
        "servings_label": "Servings",
        "ingredients_heading": "Ingredients",
        "instructions_heading": "Instructions",
        "amount_label": "Amount",
        "ingredient_label": "Ingredient",
    },
}

def get_text(key: str) -> str:
    """Get text string for the current language."""
    return TEXTS[LANGUAGE].get(key, key)

# CSS Styles
COMMON_CSS = """
:root {
    --bg-color: #ffffff;
    --text-color: #2d3748;
    --text-secondary: #4a5568;
    --text-tertiary: #718096;
    --primary-color: #2c5282;
    --primary-hover: #1e3a5f;
    --bg-secondary: #f7fafc;
    --border-color: #e2e8f0;
    --card-bg: #f7fafc;
    --table-header-bg: #2c5282;
    --shadow: rgba(0, 0, 0, 0.1);
}

body.dark-mode {
    --bg-color: #1a202c;
    --text-color: #e2e8f0;
    --text-secondary: #cbd5e0;
    --text-tertiary: #a0aec0;
    --primary-color: #4299e1;
    --primary-hover: #3182ce;
    --bg-secondary: #2d3748;
    --border-color: #4a5568;
    --card-bg: #2d3748;
    --table-header-bg: #4299e1;
    --shadow: rgba(0, 0, 0, 0.3);
}

body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.3s, color 0.3s;
}

.language-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.9em;
    box-shadow: 0 2px 8px var(--shadow);
    transition: background-color 0.2s;
    z-index: 1000;
}

.language-toggle:hover {
    background-color: var(--primary-hover);
}

.dark-mode-toggle {
    position: fixed;
    top: 70px;
    right: 20px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.9em;
    box-shadow: 0 2px 8px var(--shadow);
    transition: background-color 0.2s;
    z-index: 1000;
}

.dark-mode-toggle:hover {
    background-color: var(--primary-hover);
}

.lang-de, .lang-en {
    display: none;
}

.lang-de.active, .lang-en.active {
    display: inline;
}
"""

DETAIL_PAGE_CSS = """
.back-button {
    display: inline-block;
    padding: 8px 16px;
    margin-bottom: 20px;
    background-color: var(--border-color);
    color: var(--text-color);
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}
.back-button:hover {
    background-color: var(--bg-secondary);
    text-decoration: none;
}
h1 {
    color: var(--primary-color);
    font-size: 2.5em;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 3px solid var(--primary-color);
}
h2 {
    color: var(--primary-color);
    font-size: 1.8em;
    margin-top: 40px;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 5px solid var(--primary-color);
    background: linear-gradient(to right, var(--bg-secondary) 0%, transparent 100%);
    padding: 12px 15px;
    border-radius: 4px;
}
.recipe-info-table {
    width: 100%;
    max-width: 500px;
    margin: 20px 0;
    border-collapse: collapse;
    background-color: var(--bg-secondary);
    border-radius: 8px;
    overflow: hidden;
}
.recipe-info-table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
}
.recipe-info-table td:first-child {
    font-weight: 600;
    color: var(--text-color);
    width: 50%;
}
.recipe-info-table td:last-child {
    color: var(--text-secondary);
}
.recipe-info-table tr:last-child td {
    border-bottom: none;
}
.ingredients-table {
    width: 100%;
    margin: 20px 0;
    border-collapse: collapse;
    background-color: var(--bg-secondary);
    border-radius: 8px;
    overflow: hidden;
}
.ingredients-table th {
    background-color: var(--table-header-bg);
    color: white;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
}
.ingredients-table td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--border-color);
}
.ingredients-table tr:last-child td {
    border-bottom: none;
}
.ingredients-table td:first-child {
    font-weight: 600;
    color: var(--primary-color);
    width: 30%;
}
.ingredients-table td:last-child {
    color: var(--text-color);
}
ul {
    list-style-type: none;
    padding-left: 0;
}
li {
    padding: 5px 0;
}
ol {
    counter-reset: step-counter;
    list-style: none;
    padding-left: 0;
}
ol li {
    counter-increment: step-counter;
    margin-bottom: 20px;
    padding: 20px;
    background-color: var(--bg-secondary);
    border-left: 4px solid var(--primary-color);
    border-radius: 4px;
    position: relative;
    line-height: 1.6;
}
ol li::before {
    content: counter(step-counter);
    position: absolute;
    left: -20px;
    top: 15px;
    background-color: var(--primary-color);
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.9em;
}
ol li span {
    display: block;
    padding-left: 20px;
}
"""

OVERVIEW_PAGE_CSS = """
h1 {
    color: var(--primary-color);
}
.filter-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    flex-wrap: wrap;
}
.recipe-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 20px;
}
@media (min-width: 900px) {
    .recipe-grid {
        grid-template-columns: 1fr 1fr;
    }
}
.filter-btn {
    padding: 10px 20px;
    border: 2px solid var(--primary-color);
    background-color: var(--bg-color);
    color: var(--primary-color);
    border-radius: 6px;
    font-size: 1em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}
.filter-btn:hover {
    background-color: var(--border-color);
}
.filter-btn.active {
    background-color: var(--primary-color);
    color: white;
}
.recipe-card {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    background-color: var(--card-bg);
    transition: box-shadow 0.2s;
}
.recipe-card.hidden {
    display: none;
}
.recipe-card:hover {
    box-shadow: 0 4px 6px var(--shadow);
}
.recipe-card h2 {
    margin-top: 0;
    margin-bottom: 10px;
    color: var(--text-color);
}
.recipe-card h2 a {
    color: var(--primary-color);
    text-decoration: none;
}
.recipe-card h2 a:hover {
    text-decoration: underline;
}
.description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 12px;
}
.meta {
    color: var(--text-tertiary);
    font-size: 0.9em;
    margin-bottom: 15px;
}
.view-recipe-btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}
.view-recipe-btn:hover {
    background-color: var(--primary-hover);
    text-decoration: none;
}
.deployment-info {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
    text-align: center;
    color: var(--text-tertiary);
    font-size: 0.85em;
}
.deployment-info p {
    margin: 0;
}
"""
