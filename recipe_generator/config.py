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
        "view_stats": "📊 Statistiken",
        "menu_language": "Sprache",
        "menu_dark_mode": "Dunkelmodus",
        "menu_light_mode": "Hellmodus",

        # Stats page
        "stats_title": "Rezept-Statistiken",
        "stats_subtitle": "Top 10 beliebteste Rezepte",
        "stats_views": "Aufrufe",
        "stats_no_data": "Noch keine Daten verfügbar. Öffne einige Rezepte, um Statistiken zu sehen!",
        "stats_disclaimer": "💡 Diese Statistiken basieren auf deinem lokalen Browser-Verlauf und werden nicht geräteübergreifend synchronisiert.",

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

        # Weekly plan page
        "view_weekly_plan": "🗓️ Wochenplan",
        "weekly_plan_title": "Wochenplan",
        "add_to_weekly": "📅 Diese Woche kochen",
        "in_weekly_plan": "✓ In Wochenplan",
        "mark_cooked": "Als gekocht markieren",
        "mark_uncooked": "Als ungekocht markieren",
        "remove_from_plan": "Entfernen",
        "clear_all": "Alle löschen",
        "clear_all_confirm": "Möchtest du wirklich alle Rezepte aus dem Wochenplan entfernen?",
        "no_recipes_planned": "Noch keine Rezepte geplant",
        "no_recipes_message": "Füge Rezepte aus den Detail-Seiten hinzu, um deinen Wochenplan zu erstellen!",
        "cooked": "✓ Gekocht",
        "not_cooked": "Nicht gekocht",
        "added_on": "Hinzugefügt:",
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
        "view_stats": "📊 Statistics",
        "menu_language": "Language",
        "menu_dark_mode": "Dark Mode",
        "menu_light_mode": "Light Mode",

        # Stats page
        "stats_title": "Recipe Statistics",
        "stats_subtitle": "Top 10 most popular recipes",
        "stats_views": "Views",
        "stats_no_data": "No data available yet. Open some recipes to see statistics!",
        "stats_disclaimer": "💡 These statistics are based on your local browser history and are not synced across devices.",

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

        # Weekly plan page
        "view_weekly_plan": "🗓️ Weekly Plan",
        "weekly_plan_title": "Weekly Plan",
        "add_to_weekly": "📅 Cook This Week",
        "in_weekly_plan": "✓ In Weekly Plan",
        "mark_cooked": "Mark as Cooked",
        "mark_uncooked": "Mark as Uncooked",
        "remove_from_plan": "Remove",
        "clear_all": "Clear All",
        "clear_all_confirm": "Do you really want to remove all recipes from your weekly plan?",
        "no_recipes_planned": "No Recipes Planned Yet",
        "no_recipes_message": "Add recipes from detail pages to create your weekly meal plan!",
        "cooked": "✓ Cooked",
        "not_cooked": "Not cooked",
        "added_on": "Added:",
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
    --primary-color: #6b46c1;
    --primary-hover: #553c9a;
    --bg-secondary: #f7fafc;
    --border-color: #e2e8f0;
    --card-bg: #f7fafc;
    --table-header-bg: #6b46c1;
    --shadow: rgba(0, 0, 0, 0.1);
}

body.dark-mode {
    --bg-color: #1a202c;
    --text-color: #e2e8f0;
    --text-secondary: #cbd5e0;
    --text-tertiary: #a0aec0;
    --primary-color: #a78bfa;
    --primary-hover: #8b5cf6;
    --bg-secondary: #2d3748;
    --border-color: #4a5568;
    --card-bg: #2d3748;
    --table-header-bg: #a78bfa;
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

/* Top Navigation */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

/* Navigation Links */
.nav-link {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px var(--shadow);
    cursor: pointer;
    font-size: 1.5em;
    line-height: 1;
    transition: background-color 0.2s, transform 0.1s;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
}

.nav-link:hover {
    background-color: var(--primary-hover);
    text-decoration: none;
}

.nav-link:active {
    transform: scale(0.95);
}

/* Toggle buttons in top nav */
.nav-toggle-button {
    background-color: var(--primary-color);
    border: none;
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px var(--shadow);
    cursor: pointer;
    font-size: 1.5em;
    line-height: 1;
    transition: background-color 0.2s, transform 0.1s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-toggle-button:hover {
    background-color: var(--primary-hover);
}

.nav-toggle-button:active {
    transform: scale(0.95);
}

.nav-toggle-button .emoji {
    display: none;
}

.nav-toggle-button .emoji.active {
    display: block;
}

.light-mode-icon, .dark-mode-icon {
    display: block;
}

.light-mode-icon.active, .dark-mode-icon.active {
    display: none;
}

/* iOS-style toggle switches */
.toggle-switch {
    position: relative;
    width: 64px;
    height: 32px;
    flex-shrink: 0;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--border-color);
    transition: 0.3s;
    border-radius: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6px;
}

.toggle-slider .icon {
    font-size: 1em;
    z-index: 1;
    transition: opacity 0.3s;
}

.toggle-slider .icon.inactive {
    opacity: 0.4;
}

.toggle-slider .icon.active {
    opacity: 1;
}

.toggle-slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 3px;
    background-color: white;
    transition: 0.3s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input:checked + .toggle-slider {
    background-color: var(--primary-color);
}

input:checked + .toggle-slider:before {
    transform: translateX(32px);
}

/* Language toggle with flags */
.language-toggle-switch {
    position: relative;
    width: 64px;
    height: 32px;
    flex-shrink: 0;
}

.language-toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.language-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--border-color);
    transition: 0.3s;
    border-radius: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6px;
}

.language-slider .flag {
    font-size: 1.2em;
    z-index: 1;
    transition: opacity 0.3s;
}

.language-slider .flag.inactive {
    opacity: 0.4;
}

.language-slider .flag.active {
    opacity: 1;
}

.language-slider:before {
    content: "";
    position: absolute;
    height: 26px;
    width: 26px;
    left: 3px;
    background-color: white;
    transition: 0.3s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input:checked + .language-slider {
    background-color: var(--border-color);
}

input:checked + .language-slider:before {
    transform: translateX(32px);
}


.lang-de, .lang-en {
    display: inline;
}

.lang-de.active, .lang-en.active {
    display: none;
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
    font-size: 2em;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--primary-color);
}
h2 {
    color: var(--primary-color);
    font-size: 1.5em;
    margin-top: 40px;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 4px solid var(--primary-color);
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
.weekly-plan-button {
    display: inline-block;
    padding: 8px 16px;
    margin: 0;
    background-color: var(--primary-color);
    color: white;
    border: 2px solid var(--primary-color);
    border-radius: 6px;
    font-size: 0.95em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
    white-space: nowrap;
}
.weekly-plan-button:hover {
    background-color: var(--primary-hover);
    border-color: var(--primary-hover);
}
.weekly-plan-button.in-plan {
    background-color: var(--bg-color);
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}
.weekly-plan-button.in-plan:hover {
    background-color: var(--bg-secondary);
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

/* Heading with navigation in same row */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.page-header h1 {
    flex: 1;
    min-width: 200px;
    margin: 0;
    word-wrap: break-word;
    overflow-wrap: break-word;
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

WEEKLY_PAGE_CSS = """
h1 {
    color: var(--primary-color);
}
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
.weekly-plan-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin: 20px 0;
}
.weekly-recipe-card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    transition: box-shadow 0.2s, opacity 0.2s;
}
.weekly-recipe-card:hover {
    box-shadow: 0 4px 6px var(--shadow);
}
.weekly-recipe-card.cooked {
    opacity: 0.6;
}
.recipe-category {
    font-size: 2em;
    min-width: 50px;
    text-align: center;
}
.recipe-details {
    flex: 1;
}
.recipe-details h3 {
    margin: 0 0 5px 0;
    color: var(--text-color);
}
.recipe-details a {
    color: var(--primary-color);
    text-decoration: none;
    font-size: 1.2em;
}
.recipe-details a:hover {
    text-decoration: underline;
}
.recipe-status {
    color: var(--text-secondary);
    font-size: 0.9em;
    margin-top: 5px;
}
.recipe-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.action-button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.cook-button {
    background-color: var(--primary-color);
    color: white;
}
.cook-button:hover {
    background-color: var(--primary-hover);
}
.uncook-button {
    background-color: var(--border-color);
    color: var(--text-color);
}
.uncook-button:hover {
    background-color: var(--bg-secondary);
}
.remove-button {
    background-color: #e53e3e;
    color: white;
}
.remove-button:hover {
    background-color: #c53030;
}
.clear-all-button {
    display: inline-block;
    padding: 10px 20px;
    margin-bottom: 20px;
    background-color: #e53e3e;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1em;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
}
.clear-all-button:hover {
    background-color: #c53030;
}
.clear-all-button:disabled {
    background-color: var(--border-color);
    color: var(--text-tertiary);
    cursor: not-allowed;
}
.no-recipes {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
    background-color: var(--bg-secondary);
    border: 2px dashed var(--border-color);
    border-radius: 8px;
    margin: 20px 0;
}
.no-recipes h2 {
    color: var(--text-secondary);
    margin-bottom: 10px;
}
.no-recipes p {
    font-size: 1.1em;
}
"""
