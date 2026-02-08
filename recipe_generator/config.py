"""Configuration and constants for the recipe generator."""

from pathlib import Path


# Directory configuration
RECIPES_DIR = Path("recipes")
OUTPUT_DIR = Path("output")

# Text strings for the application
TEXTS = {
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
    "menu_dark_mode": "Dunkelmodus",
    "menu_light_mode": "Hellmodus",

    # Stats page
    "stats_title": "Rezept-Statistiken",
    "stats_subtitle": "Top 10 am häufigsten zum Kochen eingeplant",
    "stats_count": "× eingeplant",
    "stats_no_data": "Noch keine Daten verfügbar. Füge Rezepte zum Wochenplan hinzu, um Statistiken zu sehen!",
    "stats_disclaimer": "💡 Diese Statistiken werden lokal in deinem Browser gespeichert und gehen verloren, wenn du die Browser-Daten löschst.",

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
    "weekly_plan_disclaimer": "💡 Dein Wochenplan wird lokal in deinem Browser gespeichert und geht verloren, wenn du die Browser-Daten löschst.",
    "current_week": "Aktuelle Woche",
    "previous_week": "← Vorherige Woche",
    "next_week": "Nächste Woche →",
    "week_of": "Woche vom",
    "monday": "Montag",
    "tuesday": "Dienstag",
    "wednesday": "Mittwoch",
    "thursday": "Donnerstag",
    "friday": "Freitag",
    "saturday": "Samstag",
    "sunday": "Sonntag",
    "breakfast": "Frühstück",
    "lunch": "Mittagessen",
    "dinner": "Abendessen",
    "search_recipe": "Rezept suchen...",
    "no_meal_assigned": "Noch kein Rezept zugewiesen",
    "assign_meal": "Rezept zuweisen",
    "remove_meal": "Entfernen",
    "todos": "Notizen & Todos",
    "todos_placeholder": "z.B. TODO: Bake Chiasamenbrot for tomorrow",
    "servings": "Portionen",

    # Shopping list page
    "view_shopping_list": "🛒 Einkaufsliste",
    "shopping_list_title": "Einkaufsliste",
    "shopping_list_subtitle": "Automatisch generiert aus dem Wochenplan",
    "shopping_list_disclaimer": "💡 Die Einkaufsliste wird automatisch aus deinem Wochenplan generiert. Passe die Portionen für jedes Rezept individuell an.",
    "no_shopping_list": "Keine Zutaten",
    "no_shopping_list_message": "Füge Rezepte zum Wochenplan hinzu, um eine Einkaufsliste zu generieren!",
    "servings_label_short": "Portionen:",
}

def get_text(key: str) -> str:
    """Get text string."""
    return TEXTS.get(key, key)

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
    font-size: 1.75em;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--primary-color);
}
h2 {
    color: var(--primary-color);
    font-size: 1.3em;
    margin-top: 40px;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 3px solid var(--primary-color);
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
.search-container {
    margin-bottom: 30px;
    padding: 20px;
    background-color: var(--bg-secondary);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}
.filter-row {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
}
.reset-button {
    padding: 8px 16px;
    background-color: var(--bg-secondary);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95em;
    transition: all 0.2s ease;
}
.reset-button:hover {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}
.search-label {
    display: block;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 10px;
    font-size: 1em;
}
.search-input {
    width: 100%;
    box-sizing: border-box;
    padding: 12px 15px;
    border: 2px solid var(--border-color);
    background-color: var(--bg-color);
    color: var(--text-color);
    border-radius: 6px;
    font-size: 1em;
    transition: border-color 0.2s;
}
.search-input:focus {
    outline: none;
    border-color: var(--primary-color);
}
.autocomplete {
    position: relative;
    margin-top: 5px;
    background-color: var(--bg-color);
    border: 2px solid var(--border-color);
    border-radius: 6px;
    max-height: 200px;
    overflow-y: auto;
    display: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.autocomplete.show {
    display: block;
}
.search-suggestion {
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.15s;
    color: var(--text-color);
}
.search-suggestion:hover, .search-suggestion.active {
    background-color: var(--primary-color);
    color: white;
}
.selected-items {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}
.selected-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background-color: var(--primary-color);
    color: white;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 500;
}
.selected-item-remove {
    cursor: pointer;
    font-weight: bold;
    font-size: 1.1em;
    line-height: 1;
    transition: opacity 0.2s;
}
.selected-item-remove:hover {
    opacity: 0.7;
}
.filter-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 0.95em;
    color: var(--text-color);
    user-select: none;
}
.filter-checkbox input[type="checkbox"] {
    cursor: pointer;
    width: 18px;
    height: 18px;
}
.filter-checkbox:hover {
    color: var(--primary-color);
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
    flex: 1;
}
.view-recipe-btn:hover {
    background-color: var(--primary-hover);
    text-decoration: none;
}
.weekly-plan-button-card {
    display: inline-block;
    padding: 8px 16px;
    background-color: var(--primary-color);
    color: white;
    border: 2px solid var(--primary-color);
    border-radius: 6px;
    font-size: 0.9em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
    white-space: nowrap;
    flex: 1;
}
.weekly-plan-button-card:hover {
    background-color: var(--primary-hover);
    border-color: var(--primary-hover);
}
.weekly-plan-button-card.in-plan {
    background-color: var(--bg-color);
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}
.weekly-plan-button-card.in-plan:hover {
    background-color: var(--bg-secondary);
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
    margin-bottom: 10px;
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
.week-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 20px 0;
    gap: 10px;
    flex-wrap: wrap;
}
.week-nav-buttons {
    display: flex;
    gap: 10px;
}
.week-nav-btn {
    padding: 10px 16px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95em;
    font-weight: 500;
    transition: all 0.2s;
}
.week-nav-btn:hover {
    background-color: #5a35a1;
}
.current-week-btn {
    background-color: var(--bg-secondary);
    color: var(--text-color);
    border: 2px solid var(--primary-color);
}
.current-week-btn:hover {
    background-color: var(--border-color);
}
.week-info {
    font-size: 1.1em;
    color: var(--text-secondary);
    font-weight: 500;
}
.days-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin: 20px 0;
}
.day-card {
    background-color: var(--card-bg);
    border: 2px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    transition: box-shadow 0.2s;
}
.day-card:hover {
    box-shadow: 0 4px 8px var(--shadow);
}
.day-header {
    font-size: 1.4em;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-color);
}
.meals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}
.meal-slot {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px;
    min-height: 100px;
}
.meal-type {
    font-weight: 600;
    font-size: 0.9em;
    color: var(--text-secondary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.meal-content.empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60px;
    color: var(--text-tertiary);
    font-size: 0.9em;
}
.meal-content.assigned {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.assigned-recipe {
    display: flex;
    align-items: center;
    gap: 8px;
}
.recipe-emoji {
    font-size: 1.5em;
}
.recipe-name {
    flex: 1;
    font-weight: 500;
    color: var(--text-color);
}
.recipe-link {
    color: var(--primary-color);
    text-decoration: none;
    font-size: 0.95em;
}
.recipe-link:hover {
    text-decoration: underline;
}
.meal-actions {
    display: flex;
    gap: 6px;
    margin-top: 8px;
}
.assign-btn, .remove-meal-btn, .change-btn {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}
.assign-btn, .change-btn {
    background-color: var(--primary-color);
    color: white;
}
.assign-btn:hover, .change-btn:hover {
    background-color: #5a35a1;
}
.remove-meal-btn {
    background-color: #e53e3e;
    color: white;
}
.remove-meal-btn:hover {
    background-color: #c53030;
}
.servings-control {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
    padding: 6px 0;
}
.servings-label {
    font-size: 0.85em;
    color: var(--text-secondary);
    font-weight: 500;
}
.servings-adjuster {
    display: flex;
    align-items: center;
    gap: 8px;
}
.servings-btn {
    width: 32px;
    height: 32px;
    border: 2px solid var(--primary-color);
    background-color: var(--bg-color);
    color: var(--primary-color);
    border-radius: 50%;
    font-size: 1.2em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    line-height: 1;
}
.servings-btn:hover {
    background-color: var(--primary-color);
    color: white;
}
.servings-btn:active {
    transform: scale(0.95);
}
.servings-value {
    font-size: 1em;
    font-weight: 600;
    color: var(--text-color);
    min-width: 30px;
    text-align: center;
}
.search-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}
.search-modal-content {
    background-color: var(--bg-color);
    border-radius: 8px;
    padding: 24px;
    max-width: 600px;
    width: 100%;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}
.search-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.search-modal-title {
    font-size: 1.3em;
    font-weight: 600;
    color: var(--primary-color);
    margin: 0;
}
.close-modal-btn {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    color: var(--text-secondary);
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.close-modal-btn:hover {
    color: var(--text-color);
}
.search-input {
    width: 100%;
    padding: 12px;
    border: 2px solid var(--border-color);
    border-radius: 6px;
    font-size: 1em;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin-bottom: 16px;
}
.search-input:focus {
    outline: none;
    border-color: var(--primary-color);
}
.search-results {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.search-result-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    transition: all 0.2s;
}
.search-result-item:hover {
    border-color: var(--primary-color);
    background-color: var(--card-bg);
}
.search-result-info {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}
.search-result-emoji {
    font-size: 1.3em;
}
.search-result-name {
    font-weight: 500;
    color: var(--text-color);
}
.select-recipe-btn {
    padding: 6px 14px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}
.select-recipe-btn:hover {
    background-color: #5a35a1;
}

/* Todo section */
.day-todos {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 2px solid var(--border-color);
}
.todos-header {
    font-weight: 600;
    font-size: 0.9em;
    color: var(--text-secondary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.todos-textarea {
    width: 100%;
    min-height: 60px;
    padding: 10px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.95em;
    color: var(--text-color);
    background-color: var(--bg-color);
    resize: vertical;
    transition: border-color 0.2s;
}
.todos-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}
.todos-textarea::placeholder {
    color: var(--text-tertiary);
    opacity: 0.7;
}

/* Mobile optimizations */
@media (max-width: 768px) {
    .week-navigation {
        flex-direction: column;
        align-items: stretch;
    }
    .week-info {
        text-align: center;
    }
    .week-nav-buttons {
        justify-content: center;
    }
    .meals-grid {
        grid-template-columns: 1fr;
    }
    .search-modal-content {
        max-height: 90vh;
        padding: 16px;
    }
}
"""

SHOPPING_LIST_PAGE_CSS = """
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
.shopping-list-container {
    display: flex;
    flex-direction: column;
    gap: 25px;
    margin: 20px 0;
}
.recipe-shopping-section {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
}
.recipe-shopping-section h2 {
    color: var(--primary-color);
    margin: 0 0 15px 0;
    font-size: 1.3em;
}
.recipe-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 10px;
}
.recipe-title {
    font-size: 1.3em;
    color: var(--primary-color);
    margin: 0;
}
.servings-control {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9em;
    color: var(--text-secondary);
}
.servings-display {
    display: flex;
    align-items: center;
    font-size: 1em;
    color: var(--text-color);
    background-color: var(--bg-secondary);
    padding: 8px 16px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
}
.servings-text {
    font-weight: 600;
}
.servings-buttons {
    display: flex;
    align-items: center;
    gap: 6px;
}
.servings-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1.3em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}
.servings-btn:hover {
    background-color: #5a35a1;
    transform: scale(1.05);
}
.servings-btn:active {
    transform: scale(0.95);
}
.servings-btn:disabled {
    background-color: var(--border-color);
    color: var(--text-tertiary);
    cursor: not-allowed;
    transform: none;
}
.servings-input {
    width: 50px;
    padding: 8px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    background-color: var(--bg-color);
    color: var(--text-color);
    font-size: 1em;
    font-weight: 600;
    text-align: center;
}
.servings-input:focus {
    outline: none;
    border-color: var(--primary-color);
}
.recipe-meta {
    color: var(--text-tertiary);
    font-size: 0.9em;
    margin-bottom: 15px;
}
.ingredients-list {
    list-style: none;
    padding: 0;
    margin: 0;
}
.ingredient-item {
    padding: 10px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}
.ingredient-item:last-child {
    border-bottom: none;
}
.ingredient-checkbox {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    cursor: pointer;
}
.ingredient-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex: 1;
}
.ingredient-name {
    font-weight: 500;
    color: var(--text-color);
    transition: all 0.2s;
}
.ingredient-amount {
    color: var(--text-secondary);
    font-size: 0.95em;
    transition: all 0.2s;
}
.ingredient-item.checked .ingredient-name,
.ingredient-item.checked .ingredient-amount {
    text-decoration: line-through;
    color: var(--text-tertiary);
    opacity: 0.6;
}
.no-shopping-items {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
    background-color: var(--bg-secondary);
    border: 2px dashed var(--border-color);
    border-radius: 8px;
    margin: 20px 0;
}
.no-shopping-items h2 {
    color: var(--text-secondary);
    margin-bottom: 10px;
}
.no-shopping-items p {
    font-size: 1.1em;
}
"""
