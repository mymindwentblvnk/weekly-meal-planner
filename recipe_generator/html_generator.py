"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS, WEEKLY_PAGE_CSS, SHOPPING_LIST_PAGE_CSS, get_text


def generate_dark_mode_script() -> str:
    """Generate dark mode toggle JavaScript.

    Returns:
        JavaScript code for dark mode functionality
    """
    return '''
        // Dark mode toggle functionality
        function toggleDarkMode() {
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
            updateDarkModeButton(isDark);
        }

        function updateDarkModeButton(isDark) {
            document.querySelectorAll('.light-mode-text').forEach(el => {
                el.style.display = isDark ? 'none' : 'inline';
            });
            document.querySelectorAll('.dark-mode-text').forEach(el => {
                el.style.display = isDark ? 'inline' : 'none';
            });

            // Update dark mode toggle icon
            document.querySelectorAll('.light-mode-icon').forEach(el => {
                if (isDark) {
                    el.classList.remove('active');
                } else {
                    el.classList.add('active');
                }
            });
            document.querySelectorAll('.dark-mode-icon').forEach(el => {
                if (isDark) {
                    el.classList.add('active');
                } else {
                    el.classList.remove('active');
                }
            });
        }

        // Apply dark mode on page load
        function initializeDarkMode() {
            const darkMode = localStorage.getItem('darkMode');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = darkMode === 'enabled' || (darkMode === null && prefersDark);

            if (isDark) {
                document.body.classList.add('dark-mode');
            }
            updateDarkModeButton(isDark);
        }'''


def generate_navigation() -> str:
    """Generate top navigation HTML.

    Returns:
        HTML for top navigation bar
    """
    return f'''<div class="top-nav">
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="index.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="shopping.html" class="nav-link" aria-label="Shopping List">🛒</a>
            <a href="recipes.html" class="nav-link" aria-label="Recipes Catalog">📖</a>
            <button class="nav-toggle-button" onclick="openSettingsModal()" aria-label="Settings">⚙️</button>
        </div>
    </div>'''


def generate_settings_modal() -> str:
    """Generate settings modal HTML.

    Returns:
        HTML for settings modal
    """
    return '''<!-- Settings Modal -->
    <div id="settingsModal" class="add-plan-modal" style="display: none;" onclick="closeSettingsModalOnBackdrop(event)">
        <div class="add-plan-modal-content" onclick="event.stopPropagation()">
            <div class="add-plan-modal-header">
                <h3 class="add-plan-modal-title">Einstellungen</h3>
                <button class="close-modal-btn" onclick="closeSettingsModal()">×</button>
            </div>
            <div class="add-plan-modal-body">
                <div class="form-group">
                    <label>Mahlzeiten, die ich plane:</label>
                    <div class="settings-meal-options">
                        <label class="settings-checkbox">
                            <input type="checkbox" id="settingBreakfast" value="breakfast" checked>
                            <span>Frühstück</span>
                        </label>
                        <label class="settings-checkbox">
                            <input type="checkbox" id="settingLunch" value="lunch" checked>
                            <span>Mittagessen</span>
                        </label>
                        <label class="settings-checkbox">
                            <input type="checkbox" id="settingDinner" value="dinner" checked>
                            <span>Abendessen</span>
                        </label>
                    </div>
                    <p class="settings-hint">Wähle aus, welche Mahlzeiten du in deinem Wochenplan sehen möchtest.</p>
                </div>
                <div class="form-group">
                    <label>Darstellung:</label>
                    <div class="settings-meal-options">
                        <label class="settings-checkbox">
                            <input type="checkbox" id="settingDarkMode">
                            <span>🌙 Dunkelmodus</span>
                        </label>
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="cancel-btn" onclick="closeSettingsModal()">Abbrechen</button>
                    <button class="add-btn" onclick="saveSettings()">Speichern</button>
                </div>
            </div>
        </div>
    </div>'''


def generate_footer(deployment_time: datetime | None = None) -> str:
    """Generate footer HTML with last updated info and data storage disclaimer.

    Args:
        deployment_time: Optional datetime for when the page was last updated

    Returns:
        HTML for page footer
    """
    footer_class = "deployment-info" if deployment_time else "page-footer"
    footer_html = f'<footer class="{footer_class}">'

    if deployment_time:
        formatted_time = deployment_time.strftime("%d. %B %Y um %H:%M %Z")
        footer_html += f'<p class="footer-updated">{get_text("last_updated")}: {formatted_time}</p>'

    footer_html += f'<p class="footer-disclaimer">{get_text("data_stored_locally")}</p>'
    footer_html += '</footer>'

    return footer_html


def generate_page_header(title: str, css: str, additional_css: str = "") -> str:
    """Generate common HTML page header.

    Args:
        title: Page title
        css: CSS styles to include
        additional_css: Optional additional CSS for page-specific styles

    Returns:
        HTML header with DOCTYPE, head, and style tags
    """
    all_css = f"{COMMON_CSS}\n        {css}"
    if additional_css:
        all_css += f"\n        {additional_css}"

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <style>
        {all_css}
    </style>
</head>
<body>'''


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


def generate_recipe_detail_html(recipe: dict[str, Any], slug: str) -> str:
    """Generate HTML with Schema.org microdata and Bring! widget from recipe data.

    Args:
        recipe: Recipe dictionary containing name, ingredients, instructions, etc.
        slug: Recipe slug/filename (without .html extension) for weekly plan tracking

    Returns:
        Complete HTML page as a string
    """
    # Generate ingredients table rows
    ingredients_rows = []
    for ingredient in recipe['ingredients']:
        ingredients_rows.append(f'''            <tr itemprop="recipeIngredient">
                <td>{escape(str(ingredient['amount']))}</td>
                <td>{escape(ingredient['name'])}</td>
            </tr>''')

    # Generate instructions HTML
    instructions_html = []
    for instruction in recipe['instructions']:
        instructions_html.append(f'''                <li itemprop="itemListElement" itemscope itemtype="https://schema.org/HowToStep">
                    <span itemprop="text">{escape(instruction)}</span>
                </li>''')

    # Get category emoji if available
    category = recipe.get('category', '')

    title = f"{recipe['name']} {get_text('recipe_title_suffix')}"
    html = f'''{generate_page_header(title, DETAIL_PAGE_CSS)}
    <div itemscope itemtype="https://schema.org/Recipe">
        <div class="page-header">
            <h1 itemprop="name">{escape(recipe['name'])}</h1>
            {generate_navigation()}
        </div>

        <p itemprop="description">{escape(recipe.get('description', ''))}</p>

        <div itemprop="author" itemscope itemtype="https://schema.org/Person">
            <meta itemprop="name" content="{escape(recipe.get('author', 'Unknown'))}">
        </div>

        <div style="display: flex; gap: 15px; align-items: center; margin: 20px 0; flex-wrap: wrap;">
            {generate_bring_widget()}
            <button id="weeklyPlanButton" class="weekly-plan-button" onclick="toggleWeeklyPlan()">📅 Diese Woche kochen</button>
        </div>

        <table class="recipe-info-table">
            <tr>
                <td><time itemprop="prepTime" datetime="{format_time(recipe['prep_time'])}">{get_text('prep_time')}</time></td>
                <td>{recipe['prep_time']} {get_text('minutes')}</td>
            </tr>
            <tr>
                <td><time itemprop="cookTime" datetime="{format_time(recipe['cook_time'])}">{get_text('cook_time')}</time></td>
                <td>{recipe['cook_time']} {get_text('minutes')}</td>
            </tr>
            <tr>
                <td><meta itemprop="recipeYield" content="{recipe['servings']} servings">{get_text('servings_label')}</td>
                <td>{recipe['servings']}</td>
            </tr>
        </table>

        <h2>{get_text('ingredients_heading')}</h2>

        <table class="ingredients-table">
            <thead>
                <tr>
                    <th>{get_text('amount_label')}</th>
                    <th>{get_text('ingredient_label')}</th>
                </tr>
            </thead>
            <tbody>
{chr(10).join(ingredients_rows)}
            </tbody>
        </table>

        <h2>{get_text('instructions_heading')}</h2>
        <div itemprop="recipeInstructions" itemscope itemtype="https://schema.org/HowToSection">
            <ol>
{chr(10).join(instructions_html)}
            </ol>
        </div>
    </div>

    {generate_settings_modal()}

    {generate_footer()}

    <script>
        // Recipe data for weekly plan
        const recipeData = {{
            name: '{escape(recipe['name'])}',
            slug: '{escape(slug)}',
            category: '{escape(recipe.get('category', ''))}'
        }};

        // Settings functions
        function getEnabledMeals() {{
            try {{
                const stored = localStorage.getItem('mealSettings');
                if (stored) {{
                    return JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error loading meal settings:', e);
            }}
            return {{ breakfast: true, lunch: true, dinner: true }};
        }}

        function saveSettings() {{
            const settings = {{
                breakfast: document.getElementById('settingBreakfast').checked,
                lunch: document.getElementById('settingLunch').checked,
                dinner: document.getElementById('settingDinner').checked
            }};

            const darkModeEnabled = document.getElementById('settingDarkMode').checked;

            try {{
                localStorage.setItem('mealSettings', JSON.stringify(settings));
                localStorage.setItem('darkMode', darkModeEnabled ? 'enabled' : 'disabled');
                closeSettingsModal();

                // Apply dark mode immediately
                if (darkModeEnabled) {{
                    document.body.classList.add('dark-mode');
                }} else {{
                    document.body.classList.remove('dark-mode');
                }}
            }} catch (e) {{
                console.error('Error saving settings:', e);
                alert('Fehler beim Speichern der Einstellungen');
            }}
        }}

        function openSettingsModal() {{
            const settings = getEnabledMeals();
            document.getElementById('settingBreakfast').checked = settings.breakfast;
            document.getElementById('settingLunch').checked = settings.lunch;
            document.getElementById('settingDinner').checked = settings.dinner;

            // Load dark mode setting
            const darkMode = localStorage.getItem('darkMode');
            document.getElementById('settingDarkMode').checked = darkMode === 'enabled';

            document.getElementById('settingsModal').style.display = 'flex';
        }}

        function closeSettingsModal() {{
            document.getElementById('settingsModal').style.display = 'none';
        }}

        function closeSettingsModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeSettingsModal();
            }}
        }}

        // Track page view
        (function trackPageView() {{
            const recipeName = '{escape(recipe['name'])}';
            const viewsKey = 'recipeViews';

            // Get current view counts
            let views = {{}};
            try {{
                const stored = localStorage.getItem(viewsKey);
                if (stored) {{
                    views = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading view counts:', e);
            }}

            // Increment view count for this recipe
            views[recipeName] = (views[recipeName] || 0) + 1;

            // Save back to localStorage
            try {{
                localStorage.setItem(viewsKey, JSON.stringify(views));
            }} catch (e) {{
                console.error('Error saving view counts:', e);
            }}
        }})();

        // Track cumulative "add to plan" clicks
        // Weekly plan functionality
        function toggleWeeklyPlan() {{
            const planKey = 'weeklyMealPlan';
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem(planKey);
                if (stored) {{
                    plan = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading weekly plan:', e);
            }}

            // Always add to plan (allow duplicates)
            plan.recipes.push({{
                id: String(Date.now() + Math.random()), // Unique ID for each instance (as string)
                name: recipeData.name,
                slug: recipeData.slug,
                category: recipeData.category,
                addedAt: Date.now(),
                cooked: false
            }});

            // Update lastModified timestamp
            plan.lastModified = Date.now();

            // Save back to localStorage
            try {{
                localStorage.setItem(planKey, JSON.stringify(plan));
                updateWeeklyPlanButton();

                // Trigger sync by posting message to any open weekly plan tabs
                try {{
                    localStorage.setItem('weeklyPlanNeedsSync', Date.now().toString());
                }} catch (e) {{
                    // Ignore if localStorage is full
                }}
            }} catch (e) {{
                console.error('Error saving weekly plan:', e);
            }}
        }}

        function updateWeeklyPlanButton() {{
            const planKey = 'weeklyMealPlan';
            const button = document.getElementById('weeklyPlanButton');
            if (!button) return;

            let plan = {{ recipes: [] }};
            try {{
                const stored = localStorage.getItem(planKey);
                if (stored) {{
                    plan = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading weekly plan:', e);
            }}

            const count = plan.recipes.filter(r => r.slug === recipeData.slug).length;

            if (count > 0) {{
                button.classList.add('in-plan');
                const countText = count > 1 ? ` (${{count}}×)` : '';
                button.textContent = `✓ In Wochenplan${{countText}}`;
            }} else {{
                button.classList.remove('in-plan');
                button.textContent = '📅 Diese Woche kochen';
            }}
        }}

        {generate_dark_mode_script()}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDarkMode();

            // Update weekly plan button state
            updateWeeklyPlanButton();
        }});
    </script>
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
    # Collect unique authors and categories
    authors = sorted(set(recipe.get('author', 'Unknown') for _, recipe in recipes_data))

    # Category labels (for known categories)
    category_labels = {
        '🥩': get_text('filter_meat'),
        '🐟': get_text('filter_fish'),
        '🥦': get_text('filter_vegetarian'),
        '🍞': get_text('filter_bread'),
        '🥣': get_text('filter_sweet')
    }

    # Get all unique categories from recipes (automatically detected)
    used_categories = sorted(set(recipe.get('category', '') for _, recipe in recipes_data if recipe.get('category')))
    categories = []
    for cat in used_categories:
        # Use label from map if available, otherwise just use the emoji
        label = category_labels.get(cat, cat)
        categories.append((cat, label))

    # Collect all unique tags, authors, categories, and recipe names for unified search
    all_tags = set()
    all_recipe_names = []
    all_search_items = []

    for filename, recipe in recipes_data:
        if 'tags' in recipe and recipe['tags']:
            all_tags.update(recipe['tags'])
        if 'name' in recipe and recipe['name']:
            all_recipe_names.append({'name': recipe['name'], 'slug': filename.replace('.html', '')})

    # Add recipe names with type indicator
    for recipe_info in sorted(all_recipe_names, key=lambda x: x['name']):
        all_search_items.append({'label': recipe_info['name'], 'value': recipe_info['slug'], 'type': 'recipe'})

    # Add tags with type indicator
    for tag in sorted(all_tags):
        all_search_items.append({'label': tag, 'type': 'tag'})

    # Add authors with type indicator
    for author in authors:
        all_search_items.append({'label': author, 'type': 'author'})

    # Add categories with type indicator
    for cat_emoji, cat_name in categories:
        all_search_items.append({'label': f'{cat_emoji} {cat_name}', 'value': cat_emoji, 'type': 'category'})

    # Sort recipes by category (known categories first, then unknown)
    category_order = {'🥩': 0, '🐟': 1, '🥦': 2, '🍞': 3, '🥣': 4}
    sorted_recipes = sorted(
        recipes_data,
        key=lambda x: category_order.get(x[1].get('category', ''), 999)
    )

    # Generate recipe entries
    recipe_entries = []
    for filename, recipe in sorted_recipes:
        description = escape(recipe.get('description', ''))
        servings = recipe['servings']
        prep_time = recipe['prep_time']
        cook_time = recipe['cook_time']
        total_time = prep_time + cook_time
        category = recipe.get('category', '')
        author = escape(recipe.get('author', 'Unknown'))
        time_category = 'fast' if total_time <= 30 else 'slow'

        # Get tags for this recipe
        recipe_tags = recipe.get('tags', [])
        tags_json = escape(','.join(recipe_tags))  # Comma-separated tags for data attribute
        slug = filename.replace('.html', '')  # Recipe slug for search filtering

        recipe_entry = f'''    <div class="recipe-card" data-category="{category}" data-author="{author}" data-time="{time_category}" data-tags="{tags_json}" data-slug="{slug}" data-name="{escape(recipe['name'])}">
        <h2><a href="{escape(filename)}">{escape(recipe['name'])}</a></h2>
        <p class="description">{description}</p>
        <p class="meta">
            <span class="servings">🍽️ {servings} {get_text('servings')}</span> •
            <span class="time">⏱️ {total_time} {get_text('min_total')}</span>
        </p>
        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <a href="{escape(filename)}" class="view-recipe-btn">{get_text('view_recipe')}</a>
            <button class="weekly-plan-button-card" data-slug="{slug}" data-name="{escape(recipe['name'])}" data-category="{category}" data-servings="{servings}" onclick="toggleWeeklyPlanFromCard(this)">📅 Diese Woche kochen</button>
        </div>
    </div>'''
        recipe_entries.append(recipe_entry)

    # Generate category checkboxes
    category_checkboxes = []
    for cat_emoji, cat_name in categories:
        category_checkboxes.append(f'''
                <label class="filter-dropdown-option">
                    <input type="checkbox" value="{cat_emoji}" class="category-checkbox">
                    <span>{cat_emoji} {cat_name}</span>
                </label>''')

    # Generate author checkboxes
    author_checkboxes = []
    for author in authors:
        author_checkboxes.append(f'''
                <label class="filter-dropdown-option">
                    <input type="checkbox" value="{escape(author)}" class="author-checkbox">
                    <span>{escape(author)}</span>
                </label>''')

    # Prepare search items as JSON for JavaScript
    import json
    search_items_json = json.dumps(all_search_items)

    html = f'''{generate_page_header(get_text('recipes_catalog_title'), OVERVIEW_PAGE_CSS)}
    <div class="page-header">
        <h1>{get_text('recipes_catalog_title')}</h1>
        {generate_navigation()}
    </div>

    <div class="search-container">
        <label for="search" class="search-label">🔍 Suchen</label>
        <input type="text" id="search" class="search-input" placeholder="z.B. Fisch, HelloFresh, Vegetarisch..." autocomplete="off">
        <div id="autocomplete" class="autocomplete"></div>
        <div id="selectedItems" class="selected-items"></div>

        <div class="filter-row">
            <label class="filter-checkbox">
                <input type="checkbox" id="fastFilter">
                <span>⚡ {get_text('filter_fast')}</span>
            </label>
            <button id="resetSearch" class="reset-button">🔄 Suche zurücksetzen</button>
        </div>
    </div>

    <div class="recipe-grid">
{chr(10).join(recipe_entries)}
    </div>

    {generate_footer(deployment_time)}

    {generate_settings_modal()}

    <!-- Add to Plan Modal -->
    <div id="addToPlanModal" class="add-plan-modal" style="display: none;" onclick="closeModalOnBackdrop(event)">
        <div class="add-plan-modal-content" onclick="event.stopPropagation()">
            <div class="add-plan-modal-header">
                <h3 class="add-plan-modal-title">{get_text('add_to_plan_title')}</h3>
                <button class="close-modal-btn" onclick="closeAddToPlanModal()">×</button>
            </div>
            <div class="add-plan-modal-body">
                <div class="recipe-preview" id="recipePreview"></div>

                <div class="form-group">
                    <label>{get_text('select_day')}</label>
                    <div class="button-group" id="dayButtons">
                        <button type="button" class="selection-btn" data-value="montag">Mo</button>
                        <button type="button" class="selection-btn" data-value="dienstag">Di</button>
                        <button type="button" class="selection-btn" data-value="mittwoch">Mi</button>
                        <button type="button" class="selection-btn" data-value="donnerstag">Do</button>
                        <button type="button" class="selection-btn" data-value="freitag">Fr</button>
                        <button type="button" class="selection-btn" data-value="samstag">Sa</button>
                        <button type="button" class="selection-btn" data-value="sonntag">So</button>
                    </div>
                </div>

                <div class="form-group">
                    <label>{get_text('select_meal')}</label>
                    <div class="button-group" id="mealButtons">
                        <button type="button" class="selection-btn" data-value="breakfast">{get_text('breakfast')}</button>
                        <button type="button" class="selection-btn" data-value="lunch">{get_text('lunch')}</button>
                        <button type="button" class="selection-btn" data-value="dinner">{get_text('dinner')}</button>
                    </div>
                </div>

                <div class="modal-actions">
                    <button class="cancel-btn" onclick="closeAddToPlanModal()">{get_text('cancel')}</button>
                    <button class="add-btn" onclick="confirmAddToPlan()">{get_text('add_to_plan')}</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Unified search functionality
        const allSearchItems = {search_items_json};
        const searchInput = document.getElementById('search');
        const autocomplete = document.getElementById('autocomplete');
        const selectedItemsContainer = document.getElementById('selectedItems');
        let selectedItems = [];
        let currentFocus = -1;

        // Search autocomplete
        searchInput.addEventListener('input', function() {{
            const value = this.value.toLowerCase().trim();
            autocomplete.innerHTML = '';
            currentFocus = -1;

            if (!value) {{
                autocomplete.classList.remove('show');
                return;
            }}

            // Filter search items based on input
            const matches = allSearchItems.filter(item => {{
                const label = item.label.toLowerCase();
                const isSelected = selectedItems.some(s => s.label === item.label && s.type === item.type);
                return label.includes(value) && !isSelected;
            }});

            if (matches.length > 0) {{
                matches.forEach(item => {{
                    const div = document.createElement('div');
                    div.className = 'search-suggestion';

                    // Add type indicator
                    const typeLabel = item.type === 'tag' ? '🏷️ ' : item.type === 'author' ? '👤 ' : item.type === 'recipe' ? '🍽️ ' : '';
                    div.innerHTML = `${{typeLabel}}${{item.label}}`;

                    div.addEventListener('click', () => addItem(item));
                    autocomplete.appendChild(div);
                }});
                autocomplete.classList.add('show');
            }} else {{
                autocomplete.classList.remove('show');
            }}
        }});

        // Keyboard navigation
        searchInput.addEventListener('keydown', function(e) {{
            const suggestions = autocomplete.getElementsByClassName('search-suggestion');
            if (e.key === 'ArrowDown') {{
                e.preventDefault();
                currentFocus++;
                updateActiveSuggestion(suggestions);
            }} else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                currentFocus--;
                updateActiveSuggestion(suggestions);
            }} else if (e.key === 'Enter') {{
                e.preventDefault();
                if (currentFocus > -1 && suggestions[currentFocus]) {{
                    const index = currentFocus;
                    const matches = allSearchItems.filter(item => {{
                        const label = item.label.toLowerCase();
                        const isSelected = selectedItems.some(s => s.label === item.label && s.type === item.type);
                        return label.includes(searchInput.value.toLowerCase().trim()) && !isSelected;
                    }});
                    if (matches[index]) {{
                        addItem(matches[index]);
                    }}
                }}
            }}
        }});

        function updateActiveSuggestion(suggestions) {{
            if (!suggestions.length) return;
            if (currentFocus >= suggestions.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = suggestions.length - 1;

            Array.from(suggestions).forEach((s, i) => {{
                s.classList.toggle('active', i === currentFocus);
                if (i === currentFocus) {{
                    s.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
                }}
            }});
        }}

        function addItem(item) {{
            if (!selectedItems.some(s => s.label === item.label && s.type === item.type)) {{
                selectedItems.push(item);
                renderSelectedItems();
                searchInput.value = '';
                autocomplete.innerHTML = '';
                autocomplete.classList.remove('show');
                applyFilters();
            }}
        }}

        function removeItem(item) {{
            selectedItems = selectedItems.filter(i => !(i.label === item.label && i.type === item.type));
            renderSelectedItems();
            applyFilters();
        }}

        function renderSelectedItems() {{
            selectedItemsContainer.innerHTML = '';
            selectedItems.forEach(item => {{
                const itemEl = document.createElement('div');
                itemEl.className = 'selected-item';

                // Add type indicator
                const typeLabel = item.type === 'tag' ? '🏷️ ' : item.type === 'author' ? '👤 ' : item.type === 'recipe' ? '🍽️ ' : '';
                itemEl.innerHTML = `
                    <span>${{typeLabel}}${{item.label}}</span>
                    <span class="selected-item-remove" onclick='removeItem(${{JSON.stringify(item)}})'>&times;</span>
                `;
                selectedItemsContainer.appendChild(itemEl);
            }});
        }}

        // Close autocomplete when clicking outside
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.search-container')) {{
                autocomplete.classList.remove('show');
            }}
        }});

        // Filter functionality
        const recipeCards = document.querySelectorAll('.recipe-card');
        const fastFilter = document.getElementById('fastFilter');

        function applyFilters() {{
            // Separate selected items by type
            const selectedTags = selectedItems.filter(i => i.type === 'tag').map(i => i.label);
            const selectedAuthors = selectedItems.filter(i => i.type === 'author').map(i => i.label);
            const selectedCategories = selectedItems.filter(i => i.type === 'category').map(i => i.value);
            const selectedRecipes = selectedItems.filter(i => i.type === 'recipe').map(i => i.value);
            const fastOnly = fastFilter.checked;

            // Filter recipe cards
            recipeCards.forEach(card => {{
                const category = card.dataset.category;
                const author = card.dataset.author;
                const time = card.dataset.time;
                const slug = card.dataset.slug;
                const recipeTags = card.dataset.tags ? card.dataset.tags.split(',') : [];

                // Check if matches recipe name filter (empty = show all)
                const matchesRecipe = selectedRecipes.length === 0 || selectedRecipes.includes(slug);

                // Check if matches category filter (empty = show all)
                const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(category);

                // Check if matches author filter (empty = show all)
                const matchesAuthor = selectedAuthors.length === 0 || selectedAuthors.includes(author);

                // Check if matches time filter
                const matchesTime = !fastOnly || time === 'fast';

                // Check if matches tag filter (recipe must have ALL selected tags)
                const matchesTags = selectedTags.length === 0 || selectedTags.every(tag => recipeTags.includes(tag));

                // Show card only if it matches all filters
                if (matchesRecipe && matchesCategory && matchesAuthor && matchesTime && matchesTags) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            // Save filter state
            saveFilters();
        }}

        function saveFilters() {{
            localStorage.setItem('recipeSelectedItems', JSON.stringify(selectedItems));
            localStorage.setItem('recipeFastFilter', fastFilter.checked ? 'true' : 'false');
        }}

        function loadFilters() {{
            try {{
                const savedItems = JSON.parse(localStorage.getItem('recipeSelectedItems') || '[]');
                const savedFast = localStorage.getItem('recipeFastFilter');

                selectedItems = savedItems;
                renderSelectedItems();

                if (savedFast !== null) {{
                    fastFilter.checked = savedFast === 'true';
                }}
            }} catch (e) {{
                // Ignore errors loading saved filters
            }}
        }}

        // Reset search functionality
        function resetSearch() {{
            selectedItems = [];
            fastFilter.checked = false;
            searchInput.value = '';
            autocomplete.innerHTML = '';
            autocomplete.classList.remove('show');
            renderSelectedItems();
            applyFilters();
        }}

        // Add event listeners
        fastFilter.addEventListener('change', applyFilters);
        document.getElementById('resetSearch').addEventListener('click', resetSearch);

        // Track cumulative "add to plan" clicks
        // Weekly plan functionality for overview page
        // Modal state
        let currentRecipeForPlan = null;

        function toggleWeeklyPlanFromCard(button) {{
            const slug = button.dataset.slug;
            const name = button.dataset.name;
            const category = button.dataset.category;
            const servings = parseInt(button.dataset.servings) || 2;

            // Store current recipe info
            currentRecipeForPlan = {{ slug, name, category, servings }};

            // Show recipe preview in modal
            document.getElementById('recipePreview').innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px; padding: 10px; background-color: var(--bg-secondary); border-radius: 6px; margin-bottom: 20px;">
                    <span style="font-size: 2em;">${{category}}</span>
                    <span style="font-weight: 600; font-size: 1.1em;">${{name}}</span>
                </div>
            `;

            // Set default to current day
            const today = new Date().getDay();
            const dayMap = ['sonntag', 'montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag'];
            const defaultDay = dayMap[today];

            // Select default day button
            document.querySelectorAll('#dayButtons .selection-btn').forEach(btn => {{
                if (btn.dataset.value === defaultDay) {{
                    btn.classList.add('selected');
                }} else {{
                    btn.classList.remove('selected');
                }}
            }});

            // Select default meal button (breakfast)
            document.querySelectorAll('#mealButtons .selection-btn').forEach(btn => {{
                if (btn.dataset.value === 'breakfast') {{
                    btn.classList.add('selected');
                }} else {{
                    btn.classList.remove('selected');
                }}
            }});

            // Show modal
            document.getElementById('addToPlanModal').style.display = 'flex';
        }}

        function closeAddToPlanModal() {{
            document.getElementById('addToPlanModal').style.display = 'none';
            currentRecipeForPlan = null;
        }}

        function closeModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeAddToPlanModal();
            }}
        }}

        function getISOWeek(date) {{
            const d = new Date(date);
            d.setHours(0, 0, 0, 0);
            d.setDate(d.getDate() + 4 - (d.getDay() || 7));
            const yearStart = new Date(d.getFullYear(), 0, 1);
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            return d.getFullYear() + '-W' + String(weekNo).padStart(2, '0');
        }}

        function confirmAddToPlan() {{
            if (!currentRecipeForPlan) return;

            // Get selected day and meal from buttons
            const selectedDayBtn = document.querySelector('#dayButtons .selection-btn.selected');
            const selectedMealBtn = document.querySelector('#mealButtons .selection-btn.selected');

            if (!selectedDayBtn || !selectedMealBtn) {{
                alert('Bitte wählen Sie einen Tag und eine Mahlzeit aus.');
                return;
            }}

            const day = selectedDayBtn.dataset.value;
            const meal = selectedMealBtn.dataset.value;
            const currentWeek = getISOWeek(new Date());

            try {{
                // Get meal plans
                const stored = localStorage.getItem('mealPlansV2');
                const mealPlans = stored ? JSON.parse(stored) : {{}};

                // Initialize structure
                if (!mealPlans[currentWeek]) mealPlans[currentWeek] = {{}};
                if (!mealPlans[currentWeek][day]) mealPlans[currentWeek][day] = {{}};

                // Add to plan with recipe's default servings
                mealPlans[currentWeek][day][meal] = {{
                    slug: currentRecipeForPlan.slug,
                    servings: currentRecipeForPlan.servings
                }};

                // Save back
                localStorage.setItem('mealPlansV2', JSON.stringify(mealPlans));

                // Close modal
                closeAddToPlanModal();

                // Update button states
                updateAllWeeklyPlanButtons();
            }} catch (e) {{
                console.error('Error adding to plan:', e);
                alert('Fehler beim Hinzufügen zum Wochenplan');
            }}
        }}

        function updateAllWeeklyPlanButtons() {{
            const currentWeek = getISOWeek(new Date());

            try {{
                const stored = localStorage.getItem('mealPlansV2');
                const mealPlans = stored ? JSON.parse(stored) : {{}};
                const weekData = mealPlans[currentWeek] || {{}};

                // Count recipes in current week
                const recipeCounts = {{}};
                Object.values(weekData).forEach(dayMeals => {{
                    Object.entries(dayMeals).forEach(([mealType, mealData]) => {{
                        if (mealType === 'todo' || !mealData) return;
                        const slug = typeof mealData === 'string' ? mealData : mealData.slug;
                        recipeCounts[slug] = (recipeCounts[slug] || 0) + 1;
                    }});
                }});

                document.querySelectorAll('.weekly-plan-button-card').forEach(button => {{
                    const slug = button.dataset.slug;
                    const count = recipeCounts[slug] || 0;

                    if (count > 0) {{
                        button.classList.add('in-plan');
                        const countText = count > 1 ? ` (${{count}}×)` : '';
                        button.textContent = `✓ In Wochenplan${{countText}}`;
                    }} else {{
                        button.classList.remove('in-plan');
                        button.textContent = '📅 Diese Woche kochen';
                    }}
                }});
            }} catch (e) {{
                console.error('Error reading weekly plan:', e);
            }}
        }}

        // Settings functions
        function getEnabledMeals() {{
            try {{
                const stored = localStorage.getItem('mealSettings');
                if (stored) {{
                    return JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error loading meal settings:', e);
            }}
            return {{ breakfast: true, lunch: true, dinner: true }};
        }}

        function saveSettings() {{
            const settings = {{
                breakfast: document.getElementById('settingBreakfast').checked,
                lunch: document.getElementById('settingLunch').checked,
                dinner: document.getElementById('settingDinner').checked
            }};

            const darkModeEnabled = document.getElementById('settingDarkMode').checked;

            try {{
                localStorage.setItem('mealSettings', JSON.stringify(settings));
                localStorage.setItem('darkMode', darkModeEnabled ? 'enabled' : 'disabled');
                closeSettingsModal();

                // Apply dark mode immediately
                if (darkModeEnabled) {{
                    document.body.classList.add('dark-mode');
                }} else {{
                    document.body.classList.remove('dark-mode');
                }}

                // Reload page to apply new meal settings
                location.reload();
            }} catch (e) {{
                console.error('Error saving settings:', e);
                alert('Fehler beim Speichern der Einstellungen');
            }}
        }}

        function openSettingsModal() {{
            const settings = getEnabledMeals();
            document.getElementById('settingBreakfast').checked = settings.breakfast;
            document.getElementById('settingLunch').checked = settings.lunch;
            document.getElementById('settingDinner').checked = settings.dinner;

            // Load dark mode setting
            const darkMode = localStorage.getItem('darkMode');
            document.getElementById('settingDarkMode').checked = darkMode === 'enabled';

            document.getElementById('settingsModal').style.display = 'flex';
        }}

        function closeSettingsModal() {{
            document.getElementById('settingsModal').style.display = 'none';
        }}

        function closeSettingsModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeSettingsModal();
            }}
        }}

        {generate_dark_mode_script()}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDarkMode();

            // Load and apply saved filters
            loadFilters();
            applyFilters();

            // Update weekly plan button states
            updateAllWeeklyPlanButtons();

            // Add event listeners for day and meal selection buttons
            document.querySelectorAll('#dayButtons .selection-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    document.querySelectorAll('#dayButtons .selection-btn').forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                }});
            }});

            // Filter meal buttons based on settings
            const enabledMeals = getEnabledMeals();
            document.querySelectorAll('#mealButtons .selection-btn').forEach(btn => {{
                const mealType = btn.dataset.value;
                if (!enabledMeals[mealType]) {{
                    btn.style.display = 'none';
                }} else {{
                    btn.style.display = '';
                    btn.addEventListener('click', function() {{
                        document.querySelectorAll('#mealButtons .selection-btn').forEach(b => b.classList.remove('selected'));
                        this.classList.add('selected');
                    }});
                }}
            }});

            // Select first visible meal button by default
            const firstVisibleMeal = document.querySelector('#mealButtons .selection-btn:not([style*="display: none"])');
            if (firstVisibleMeal) {{
                firstVisibleMeal.classList.add('selected');
            }}
        }});
    </script>
</body>
</html>'''

    return html


def generate_weekly_html(recipes_data: list[tuple[str, dict[str, Any]]], deployment_time: datetime | None = None) -> str:
    """Generate week-based meal planner page.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)
        deployment_time: Optional datetime for when the page was deployed

    Returns:
        Complete HTML page as a string
    """
    # Create recipe lookup by slug with tags and servings
    recipe_lookup = {}
    for filename, recipe in recipes_data:
        slug = filename.replace('.html', '')
        recipe_lookup[slug] = {
            'name': recipe['name'],
            'filename': filename,
            'category': recipe.get('category', ''),
            'tags': recipe.get('tags', []),
            'servings': recipe.get('servings', 2)
        }

    # Generate recipe lookup as JSON for JavaScript
    import json
    recipe_lookup_json = json.dumps(recipe_lookup, ensure_ascii=False)

    html = f'''{generate_page_header(get_text('weekly_plan_title'), WEEKLY_PAGE_CSS)}
    <div class="page-header">
        <h1>{get_text('weekly_plan_title')}</h1>
        {generate_navigation()}
    </div>

    <div class="week-navigation">
        <div class="week-nav-buttons">
            <button class="week-nav-btn current-week-btn" id="thisWeekBtn" onclick="goToCurrentWeek()">{get_text('current_week')}</button>
            <button class="week-nav-btn" id="nextWeekBtn" onclick="goToNextWeek()">{get_text('next_week')}</button>
        </div>
        <div class="week-info" id="weekInfo"></div>
    </div>

    <div id="daysContainer" class="days-container"></div>

    {generate_settings_modal()}

    <div id="searchModal" class="search-modal" style="display: none;" onclick="closeModalOnBackdrop(event)">
        <div class="search-modal-content" onclick="event.stopPropagation()">
            <div class="search-modal-header">
                <h3 class="search-modal-title">Rezept auswählen</h3>
                <button class="close-modal-btn" onclick="closeSearchModal()">×</button>
            </div>
            <input type="text" id="searchInput" class="search-input" placeholder="{get_text('search_recipe')}" oninput="filterRecipes()">
            <div id="searchResults" class="search-results"></div>
        </div>
    </div>

    {generate_footer(deployment_time)}

    <script>
        const recipeData = {recipe_lookup_json};
        let currentWeek = null;
        let currentDay = null;
        let currentMeal = null;

        {generate_dark_mode_script()}

        // ISO Week calculation
        function getISOWeek(date) {{
            const d = new Date(date);
            d.setHours(0, 0, 0, 0);
            d.setDate(d.getDate() + 4 - (d.getDay() || 7));
            const yearStart = new Date(d.getFullYear(), 0, 1);
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            return d.getFullYear() + '-W' + String(weekNo).padStart(2, '0');
        }}

        function getWeekDates(weekString) {{
            const [year, week] = weekString.split('-W');
            const jan4 = new Date(year, 0, 4);
            const monday = new Date(jan4);
            const dayOffset = (week - 1) * 7 - (jan4.getDay() || 7) + 1;
            monday.setDate(jan4.getDate() + dayOffset);

            const dates = [];
            for (let i = 0; i < 7; i++) {{
                const date = new Date(monday);
                date.setDate(monday.getDate() + i);
                dates.push(date);
            }}
            return dates;
        }}

        function formatDate(date) {{
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            return `${{day}}.${{month}}.`;
        }}

        // Meal plan storage
        function getMealPlans() {{
            try {{
                const stored = localStorage.getItem('mealPlansV2');
                return stored ? JSON.parse(stored) : {{}};
            }} catch (e) {{
                console.error('Error loading meal plans:', e);
                return {{}};
            }}
        }}

        function saveMealPlans(plans) {{
            try {{
                localStorage.setItem('mealPlansV2', JSON.stringify(plans));
            }} catch (e) {{
                console.error('Error saving meal plans:', e);
            }}
        }}

        function getMealForSlot(week, day, meal) {{
            const plans = getMealPlans();
            const mealData = plans[week]?.[day]?.[meal];
            // Support both old format (string) and new format (object)
            if (!mealData) return null;
            if (typeof mealData === 'string') {{
                // Old format: just recipe slug
                const recipe = recipeData[mealData];
                return {{ slug: mealData, servings: recipe?.servings || 2 }};
            }}
            // New format: object with slug and servings
            return mealData;
        }}

        function setMealForSlot(week, day, meal, recipeSlug, servings) {{
            const plans = getMealPlans();
            if (!plans[week]) plans[week] = {{}};
            if (!plans[week][day]) plans[week][day] = {{}};
            plans[week][day][meal] = {{ slug: recipeSlug, servings: servings }};
            saveMealPlans(plans);
        }}

        function updateServingsForSlot(week, day, meal, servings) {{
            const plans = getMealPlans();
            if (plans[week]?.[day]?.[meal]) {{
                const mealData = plans[week][day][meal];
                const slug = typeof mealData === 'string' ? mealData : mealData.slug;
                plans[week][day][meal] = {{ slug: slug, servings: servings }};
                saveMealPlans(plans);
            }}
        }}

        function removeMealFromSlot(week, day, meal) {{
            const plans = getMealPlans();
            if (plans[week]?.[day]?.[meal]) {{
                delete plans[week][day][meal];
                saveMealPlans(plans);
            }}
        }}

        function getTodoForDay(week, day) {{
            const plans = getMealPlans();
            return plans[week]?.[day]?.todo || '';
        }}

        function saveTodoForDay(week, day, todo) {{
            const plans = getMealPlans();
            if (!plans[week]) plans[week] = {{}};
            if (!plans[week][day]) plans[week][day] = {{}};
            plans[week][day].todo = todo;
            saveMealPlans(plans);
        }}

        // Clean up old weeks from localStorage (keep only current week and next week)
        function cleanupOldWeeks() {{
            try {{
                const stored = localStorage.getItem('mealPlansV2');
                if (!stored) return;

                const mealPlans = JSON.parse(stored);
                const currentDate = new Date();

                // Calculate weeks to keep (current week and next week only)
                const weeksToKeep = new Set();
                const thisWeek = getISOWeek(currentDate);
                const nextWeekDate = new Date(currentDate);
                nextWeekDate.setDate(nextWeekDate.getDate() + 7);
                const nextWeek = getISOWeek(nextWeekDate);

                weeksToKeep.add(thisWeek);
                weeksToKeep.add(nextWeek);

                // Remove weeks outside the range
                let hasChanges = false;
                for (const week in mealPlans) {{
                    if (!weeksToKeep.has(week)) {{
                        delete mealPlans[week];
                        hasChanges = true;
                    }}
                }}

                // Save back if we made changes
                if (hasChanges) {{
                    localStorage.setItem('mealPlansV2', JSON.stringify(mealPlans));
                }}
            }} catch (e) {{
                console.error('Error cleaning up old weeks:', e);
            }}
        }}

        // Week navigation
        function goToNextWeek() {{
            const dates = getWeekDates(currentWeek);
            const nextMonday = new Date(dates[0]);
            nextMonday.setDate(nextMonday.getDate() + 7);
            currentWeek = getISOWeek(nextMonday);
            updateWeekButtons();
            renderWeek();
        }}

        function goToCurrentWeek() {{
            currentWeek = getISOWeek(new Date());
            updateWeekButtons();
            renderWeek();
        }}

        function updateWeekButtons() {{
            const today = getISOWeek(new Date());
            const dates = getWeekDates(currentWeek);
            const nextMonday = new Date(dates[0]);
            nextMonday.setDate(nextMonday.getDate() + 7);
            const nextWeek = getISOWeek(nextMonday);

            // Update button states
            document.getElementById('thisWeekBtn').classList.toggle('active', currentWeek === today);
            document.getElementById('nextWeekBtn').classList.toggle('active', currentWeek === nextWeek);

            // Disable next week button if already viewing it
            document.getElementById('nextWeekBtn').disabled = currentWeek === nextWeek;
        }}

        // Recipe search and assignment
        function openSearchModal(day, meal) {{
            currentDay = day;
            currentMeal = meal;
            document.getElementById('searchInput').value = '';
            filterRecipes();
            document.getElementById('searchModal').style.display = 'flex';
        }}

        function closeSearchModal() {{
            document.getElementById('searchModal').style.display = 'none';
        }}

        function closeModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeSearchModal();
            }}
        }}

        function filterRecipes() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const results = Object.entries(recipeData).filter(([slug, recipe]) => {{
                const nameMatch = recipe.name.toLowerCase().includes(query);
                const tagMatch = recipe.tags?.some(tag => tag.toLowerCase().includes(query));
                return nameMatch || tagMatch;
            }});

            const resultsHtml = results.map(([slug, recipe]) => `
                <div class="search-result-item">
                    <div class="search-result-info">
                        <span class="search-result-emoji">${{recipe.category}}</span>
                        <span class="search-result-name">${{recipe.name}}</span>
                    </div>
                    <button class="select-recipe-btn" onclick="selectRecipe('${{slug}}')">Auswählen</button>
                </div>
            `).join('');

            document.getElementById('searchResults').innerHTML = resultsHtml || '<p style="color: var(--text-tertiary); padding: 20px; text-align: center;">Keine Rezepte gefunden</p>';
        }}

        function selectRecipe(slug) {{
            const recipe = recipeData[slug];
            const defaultServings = recipe?.servings || 2;
            setMealForSlot(currentWeek, currentDay, currentMeal, slug, defaultServings);
            closeSearchModal();
            renderWeek();
        }}

        function removeMeal(day, meal) {{
            removeMealFromSlot(currentWeek, day, meal);
            renderWeek();
        }}

        function adjustServings(day, meal, delta) {{
            const mealData = getMealForSlot(currentWeek, day, meal);
            if (mealData) {{
                const newServings = Math.max(1, mealData.servings + delta);
                updateServingsForSlot(currentWeek, day, meal, newServings);
                renderWeek();
            }}
        }}

        // Settings functions
        function getEnabledMeals() {{
            try {{
                const stored = localStorage.getItem('mealSettings');
                if (stored) {{
                    return JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error loading meal settings:', e);
            }}
            return {{ breakfast: true, lunch: true, dinner: true }};
        }}

        function saveSettings() {{
            const settings = {{
                breakfast: document.getElementById('settingBreakfast').checked,
                lunch: document.getElementById('settingLunch').checked,
                dinner: document.getElementById('settingDinner').checked
            }};

            const darkModeEnabled = document.getElementById('settingDarkMode').checked;

            try {{
                localStorage.setItem('mealSettings', JSON.stringify(settings));
                localStorage.setItem('darkMode', darkModeEnabled ? 'enabled' : 'disabled');
                closeSettingsModal();

                // Apply dark mode immediately
                if (darkModeEnabled) {{
                    document.body.classList.add('dark-mode');
                }} else {{
                    document.body.classList.remove('dark-mode');
                }}

                // Reload to apply new meal settings
                renderWeek();
            }} catch (e) {{
                console.error('Error saving settings:', e);
                alert('Fehler beim Speichern der Einstellungen');
            }}
        }}

        function openSettingsModal() {{
            const settings = getEnabledMeals();
            document.getElementById('settingBreakfast').checked = settings.breakfast;
            document.getElementById('settingLunch').checked = settings.lunch;
            document.getElementById('settingDinner').checked = settings.dinner;

            // Load dark mode setting
            const darkMode = localStorage.getItem('darkMode');
            document.getElementById('settingDarkMode').checked = darkMode === 'enabled';

            document.getElementById('settingsModal').style.display = 'flex';
        }}

        function closeSettingsModal() {{
            document.getElementById('settingsModal').style.display = 'none';
        }}

        function closeSettingsModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeSettingsModal();
            }}
        }}

        // Render week view
        function renderWeek() {{
            const dates = getWeekDates(currentWeek);
            const dayNames = ['{get_text('monday')}', '{get_text('tuesday')}', '{get_text('wednesday')}', '{get_text('thursday')}', '{get_text('friday')}', '{get_text('saturday')}', '{get_text('sunday')}'];
            const allMealTypes = ['breakfast', 'lunch', 'dinner'];
            const allMealLabels = ['{get_text('breakfast')}', '{get_text('lunch')}', '{get_text('dinner')}'];

            // Filter meals based on user settings
            const enabledMeals = getEnabledMeals();
            const mealTypes = [];
            const mealLabels = [];
            allMealTypes.forEach((type, index) => {{
                if (enabledMeals[type]) {{
                    mealTypes.push(type);
                    mealLabels.push(allMealLabels[index]);
                }}
            }});

            document.getElementById('weekInfo').textContent = `{get_text('week_of')} ${{formatDate(dates[0])}} - ${{formatDate(dates[6])}}`;

            let html = '';
            dates.forEach((date, dayIndex) => {{
                const dayName = dayNames[dayIndex];
                const dayKey = dayName.toLowerCase();

                html += `
                    <div class="day-card">
                        <div class="day-header">${{dayName}}, ${{formatDate(date)}}</div>
                        <div class="meals-grid">
                `;

                mealTypes.forEach((mealType, mealIndex) => {{
                    const mealLabel = mealLabels[mealIndex];
                    const mealData = getMealForSlot(currentWeek, dayKey, mealType);
                    const recipe = mealData ? recipeData[mealData.slug] : null;

                    if (recipe && mealData) {{
                        html += `
                            <div class="meal-slot">
                                <div class="meal-type">${{mealLabel}}</div>
                                <div class="meal-content assigned">
                                    <div class="assigned-recipe">
                                        <span class="recipe-emoji">${{recipe.category}}</span>
                                        <a href="${{recipe.filename}}" class="recipe-link">${{recipe.name}}</a>
                                    </div>
                                    <div class="servings-control">
                                        <span class="servings-label">{get_text('servings')}:</span>
                                        <div class="servings-adjuster">
                                            <button class="servings-btn" onclick="adjustServings('${{dayKey}}', '${{mealType}}', -1)">−</button>
                                            <span class="servings-value">${{mealData.servings}}</span>
                                            <button class="servings-btn" onclick="adjustServings('${{dayKey}}', '${{mealType}}', 1)">+</button>
                                        </div>
                                    </div>
                                    <div class="meal-actions">
                                        <button class="change-btn" onclick="openSearchModal('${{dayKey}}', '${{mealType}}')">Ändern</button>
                                        <button class="remove-meal-btn" onclick="removeMeal('${{dayKey}}', '${{mealType}}')">Entfernen</button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }} else {{
                        html += `
                            <div class="meal-slot">
                                <div class="meal-type">${{mealLabel}}</div>
                                <div class="meal-content empty">
                                    <p>{get_text('no_meal_assigned')}</p>
                                    <button class="assign-btn" onclick="openSearchModal('${{dayKey}}', '${{mealType}}')">{get_text('assign_meal')}</button>
                                </div>
                            </div>
                        `;
                    }}
                }});

                const todo = getTodoForDay(currentWeek, dayKey);
                html += `
                        </div>
                        <div class="day-todos">
                            <div class="todos-header">{get_text('todos')}</div>
                            <textarea
                                class="todos-textarea"
                                placeholder="{get_text('todos_placeholder')}"
                                oninput="saveTodoForDay('${{currentWeek}}', '${{dayKey}}', this.value)"
                            >${{todo}}</textarea>
                        </div>
                    </div>
                `;
            }});

            document.getElementById('daysContainer').innerHTML = html;
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            currentWeek = getISOWeek(new Date());
            cleanupOldWeeks();
            updateWeekButtons();
            renderWeek();
            initializeDarkMode();
        }});
    </script>
</body>
</html>'''

    return html


def generate_shopping_list_html(recipes_data: list[tuple[str, dict[str, Any]]], deployment_time: datetime | None = None) -> str:
    """Generate shopping list page based on weekly meal plan.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)
        deployment_time: Optional datetime for when the page was deployed

    Returns:
        Complete HTML page as a string
    """
    # Create recipe lookup by slug with full recipe data including ingredients
    recipe_lookup = {}
    for filename, recipe in recipes_data:
        slug = filename.replace('.html', '')
        recipe_lookup[slug] = {
            'name': recipe['name'],
            'filename': filename,
            'category': recipe.get('category', ''),
            'servings': recipe.get('servings', 2),
            'ingredients': recipe.get('ingredients', [])
        }

    # Generate recipe lookup as JSON for JavaScript
    import json
    recipe_lookup_json = json.dumps(recipe_lookup, ensure_ascii=False)

    html = f'''{generate_page_header(get_text('shopping_list_title'), SHOPPING_LIST_PAGE_CSS)}
    <div class="page-header">
        <h1>{get_text('shopping_list_title')}</h1>
        {generate_navigation()}
    </div>

    <div class="week-navigation">
        <div class="week-nav-buttons">
            <button class="week-nav-btn current-week-btn" id="thisWeekBtn" onclick="goToCurrentWeek()">{get_text('current_week')}</button>
            <button class="week-nav-btn" id="nextWeekBtn" onclick="goToNextWeek()">{get_text('next_week')}</button>
        </div>
        <div class="week-info" id="weekInfo"></div>
    </div>

    <div style="display: flex; justify-content: center;">
        <div class="view-toggle">
            <button class="view-toggle-btn active" id="viewByRecipeBtn" onclick="switchView('recipe')">{get_text('view_by_recipe')}</button>
            <button class="view-toggle-btn" id="viewAlphabeticallyBtn" onclick="switchView('alphabetical')">{get_text('view_alphabetically')}</button>
        </div>
    </div>

    <div id="shoppingListContainer"></div>

    {generate_settings_modal()}

    {generate_footer(deployment_time)}

    <script>
        const recipeData = {recipe_lookup_json};
        let currentWeek = null;
        let currentView = 'recipe'; // 'recipe' or 'alphabetical'

        // Settings functions
        function getEnabledMeals() {{
            try {{
                const stored = localStorage.getItem('mealSettings');
                if (stored) {{
                    return JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error loading meal settings:', e);
            }}
            return {{ breakfast: true, lunch: true, dinner: true }};
        }}

        function saveSettings() {{
            const settings = {{
                breakfast: document.getElementById('settingBreakfast').checked,
                lunch: document.getElementById('settingLunch').checked,
                dinner: document.getElementById('settingDinner').checked
            }};

            const darkModeEnabled = document.getElementById('settingDarkMode').checked;

            try {{
                localStorage.setItem('mealSettings', JSON.stringify(settings));
                localStorage.setItem('darkMode', darkModeEnabled ? 'enabled' : 'disabled');
                closeSettingsModal();

                // Apply dark mode immediately
                if (darkModeEnabled) {{
                    document.body.classList.add('dark-mode');
                }} else {{
                    document.body.classList.remove('dark-mode');
                }}

                // Reload shopping list
                loadShoppingList();
            }} catch (e) {{
                console.error('Error saving settings:', e);
                alert('Fehler beim Speichern der Einstellungen');
            }}
        }}

        function openSettingsModal() {{
            const settings = getEnabledMeals();
            document.getElementById('settingBreakfast').checked = settings.breakfast;
            document.getElementById('settingLunch').checked = settings.lunch;
            document.getElementById('settingDinner').checked = settings.dinner;

            // Load dark mode setting
            const darkMode = localStorage.getItem('darkMode');
            document.getElementById('settingDarkMode').checked = darkMode === 'enabled';

            document.getElementById('settingsModal').style.display = 'flex';
        }}

        function closeSettingsModal() {{
            document.getElementById('settingsModal').style.display = 'none';
        }}

        function closeSettingsModalOnBackdrop(event) {{
            if (event.target === event.currentTarget) {{
                closeSettingsModal();
            }}
        }}

        {generate_dark_mode_script()}

        // ============ Shopping List Functions ============

        // View switching
        function switchView(view) {{
            currentView = view;

            // Update button states
            document.getElementById('viewByRecipeBtn').classList.toggle('active', view === 'recipe');
            document.getElementById('viewAlphabeticallyBtn').classList.toggle('active', view === 'alphabetical');

            // Reload the shopping list with the new view
            if (view === 'recipe') {{
                loadShoppingList();
            }} else {{
                loadShoppingListAlphabetical();
            }}
        }}

        // ISO Week calculation
        function getISOWeek(date) {{
            const d = new Date(date);
            d.setHours(0, 0, 0, 0);
            d.setDate(d.getDate() + 4 - (d.getDay() || 7));
            const yearStart = new Date(d.getFullYear(), 0, 1);
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            return d.getFullYear() + '-W' + String(weekNo).padStart(2, '0');
        }}

        function getWeekDates(weekString) {{
            const [year, week] = weekString.split('-W');
            const jan4 = new Date(year, 0, 4);
            const monday = new Date(jan4);
            const dayOffset = (week - 1) * 7 - (jan4.getDay() || 7) + 1;
            monday.setDate(jan4.getDate() + dayOffset);

            const dates = [];
            for (let i = 0; i < 7; i++) {{
                const date = new Date(monday);
                date.setDate(monday.getDate() + i);
                dates.push(date);
            }}
            return dates;
        }}

        function formatDate(date) {{
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            return `${{day}}.${{month}}.`;
        }}

        // Get meal plan for specific week
        function getLocalWeeklyPlan(week) {{
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem('mealPlansV2');
                if (stored) {{
                    const mealPlans = JSON.parse(stored);
                    const weekData = mealPlans[week] || {{}};

                    // Aggregate all meals from the week with servings and day/meal info
                    const meals = [];
                    Object.entries(weekData).forEach(([day, dayMeals]) => {{
                        Object.entries(dayMeals).forEach(([mealType, mealData]) => {{
                            // Skip 'todo' entries
                            if (mealType === 'todo' || !mealData) return;

                            // Support both old format (string) and new format (object)
                            if (typeof mealData === 'string') {{
                                meals.push({{ slug: mealData, servings: 2, day: day, meal: mealType }});
                            }} else if (mealData.slug) {{
                                meals.push({{ slug: mealData.slug, servings: mealData.servings || 2, day: day, meal: mealType }});
                            }}
                        }});
                    }});

                    plan.recipes = meals;
                }}
            }} catch (e) {{
                console.error('Error reading local plan:', e);
            }}

            return plan;
        }}

        // Get checked items from localStorage (by item ID)
        function getCheckedItems(week) {{
            const checkedKey = 'shoppingListChecked';
            let allChecked = {{}};

            try {{
                const stored = localStorage.getItem(checkedKey);
                if (stored) {{
                    allChecked = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading checked items:', e);
            }}

            return allChecked[week] || {{}};
        }}

        // Save checked items to localStorage (by item ID) for a specific week
        function saveCheckedItems(week, checked) {{
            const checkedKey = 'shoppingListChecked';
            try {{
                const stored = localStorage.getItem(checkedKey);
                let allChecked = {{}};
                if (stored) {{
                    allChecked = JSON.parse(stored);
                }}
                allChecked[week] = checked;
                localStorage.setItem(checkedKey, JSON.stringify(allChecked));
            }} catch (e) {{
                console.error('Error saving checked items:', e);
            }}
        }}

        // Update servings and sync back to weekly plan
        function updateServings(recipeSlug, newServings) {{
            newServings = Math.max(1, Math.min(20, parseInt(newServings) || 2));

            // Get current week's meal plan
            const mealPlans = getMealPlans();
            const weekData = mealPlans[currentWeek] || {{}};

            // Find all instances of this recipe in the current week
            const instances = [];
            let totalCurrentServings = 0;

            Object.entries(weekData).forEach(([day, dayMeals]) => {{
                Object.entries(dayMeals).forEach(([mealType, mealData]) => {{
                    if (mealType === 'todo' || !mealData) return;

                    const slug = typeof mealData === 'string' ? mealData : mealData.slug;
                    if (slug === recipeSlug) {{
                        const servings = typeof mealData === 'string' ? 2 : (mealData.servings || 2);
                        instances.push({{ day, mealType, servings }});
                        totalCurrentServings += servings;
                    }}
                }});
            }});

            // Distribute new servings proportionally across all instances
            if (instances.length > 0) {{
                const scaleFactor = newServings / totalCurrentServings;

                instances.forEach(instance => {{
                    const newInstanceServings = Math.max(1, Math.round(instance.servings * scaleFactor));

                    if (!mealPlans[currentWeek]) mealPlans[currentWeek] = {{}};
                    if (!mealPlans[currentWeek][instance.day]) mealPlans[currentWeek][instance.day] = {{}};

                    mealPlans[currentWeek][instance.day][instance.mealType] = {{
                        slug: recipeSlug,
                        servings: newInstanceServings
                    }};
                }});

                saveMealPlans(mealPlans);
            }}

            loadShoppingList();
        }}

        function incrementServings(recipeSlug, currentServings) {{
            if (currentServings < 20) {{
                updateServings(recipeSlug, currentServings + 1);
            }}
        }}

        function decrementServings(recipeSlug, currentServings) {{
            if (currentServings > 1) {{
                updateServings(recipeSlug, currentServings - 1);
            }}
        }}

        // Update servings for a specific recipe instance (by instance index in plan.recipes)
        function updateServingsInstance(instanceIndex, newServings) {{
            newServings = Math.max(1, Math.min(20, parseInt(newServings) || 2));

            const plan = getLocalWeeklyPlan(currentWeek);
            if (instanceIndex >= 0 && instanceIndex < plan.recipes.length) {{
                const instance = plan.recipes[instanceIndex];
                const mealPlans = getMealPlans();

                if (!mealPlans[currentWeek]) mealPlans[currentWeek] = {{}};
                if (!mealPlans[currentWeek][instance.day]) mealPlans[currentWeek][instance.day] = {{}};

                mealPlans[currentWeek][instance.day][instance.meal] = {{
                    slug: instance.slug,
                    servings: newServings
                }};

                saveMealPlans(mealPlans);
                loadShoppingList();
            }}
        }}

        function incrementServingsInstance(instanceIndex, currentServings) {{
            if (currentServings < 20) {{
                updateServingsInstance(instanceIndex, currentServings + 1);
            }}
        }}

        function decrementServingsInstance(instanceIndex, currentServings) {{
            if (currentServings > 1) {{
                updateServingsInstance(instanceIndex, currentServings - 1);
            }}
        }}

        function getMealPlans() {{
            try {{
                const stored = localStorage.getItem('mealPlansV2');
                return stored ? JSON.parse(stored) : {{}};
            }} catch (e) {{
                console.error('Error loading meal plans:', e);
                return {{}};
            }}
        }}

        function saveMealPlans(plans) {{
            try {{
                localStorage.setItem('mealPlansV2', JSON.stringify(plans));
            }} catch (e) {{
                console.error('Error saving meal plans:', e);
            }}
        }}

        // Toggle checkbox state
        function toggleIngredientCheck(itemId) {{
            const checkbox = document.getElementById(`check-${{itemId}}`);
            const listItem = checkbox.closest('.ingredient-item');
            const isChecked = checkbox.checked;

            // Update visual state
            if (isChecked) {{
                listItem.classList.add('checked');
            }} else {{
                listItem.classList.remove('checked');
            }}

            // Update localStorage (by item ID) for current week
            let checked = getCheckedItems(currentWeek);
            if (isChecked) {{
                checked[itemId] = true;
            }} else {{
                delete checked[itemId];
            }}
            saveCheckedItems(currentWeek, checked);
        }}

        // Scale ingredient amount from original servings to target servings (2)
        function scaleAmount(amount, originalServings, targetServings) {{
            if (!amount) return amount;

            const amountStr = String(amount);

            // Try to extract number from the beginning of the string
            const match = amountStr.match(/^([0-9]+(?:[.,][0-9]+)?)/);

            if (match) {{
                const number = parseFloat(match[1].replace(',', '.'));
                const scaledNumber = (number * targetServings) / originalServings;

                // Round to reasonable precision
                const rounded = Math.round(scaledNumber * 100) / 100;

                // Replace the original number with the scaled number
                return amountStr.replace(match[1], formatNumber(rounded));
            }}

            // If no number found, return original (e.g., "nach Geschmack", "1 Prise")
            return amountStr;
        }}

        // Format number for display (avoid unnecessary decimals)
        function formatNumber(num) {{
            if (num === Math.floor(num)) {{
                return String(Math.floor(num));
            }}
            return String(num).replace('.', ',');
        }}

        // Week navigation functions
        function updateWeekInfo() {{
            const dates = getWeekDates(currentWeek);
            document.getElementById('weekInfo').textContent = `{get_text('week_of')} ${{formatDate(dates[0])}} - ${{formatDate(dates[6])}}`;
        }}

        function goToNextWeek() {{
            const dates = getWeekDates(currentWeek);
            const nextMonday = new Date(dates[0]);
            nextMonday.setDate(nextMonday.getDate() + 7);
            currentWeek = getISOWeek(nextMonday);
            updateWeekButtons();
            updateWeekInfo();
            loadShoppingList();
        }}

        function goToCurrentWeek() {{
            currentWeek = getISOWeek(new Date());
            updateWeekButtons();
            updateWeekInfo();
            loadShoppingList();
        }}

        function updateWeekButtons() {{
            const today = getISOWeek(new Date());
            const dates = getWeekDates(currentWeek);
            const nextMonday = new Date(dates[0]);
            nextMonday.setDate(nextMonday.getDate() + 7);
            const nextWeek = getISOWeek(nextMonday);

            // Update button states
            document.getElementById('thisWeekBtn').classList.toggle('active', currentWeek === today);
            document.getElementById('nextWeekBtn').classList.toggle('active', currentWeek === nextWeek);

            // Disable next week button if already viewing it
            document.getElementById('nextWeekBtn').disabled = currentWeek === nextWeek;
        }}

        function loadShoppingList() {{
            let plan = getLocalWeeklyPlan(currentWeek);
            const container = document.getElementById('shoppingListContainer');

            if (plan.recipes.length === 0) {{
                container.innerHTML = `
                    <div class="no-shopping-items">
                        <h2>{get_text('no_shopping_list')}</h2>
                        <p>{get_text('no_shopping_list_message')}</p>
                    </div>
                `;
                // Clear checked items for current week when no recipes
                saveCheckedItems(currentWeek, {{}});
                return;
            }}

            // Load checked state (by item ID) for current week
            let checked = getCheckedItems(currentWeek);

            // Track valid item IDs in current shopping list
            const validItemIds = new Set();

            let html = '<div class="shopping-list-container">';

            // Show each recipe instance separately (no aggregation)
            plan.recipes.forEach((recipeInstance, instanceIndex) => {{
                const slug = recipeInstance.slug;
                const recipeInfo = recipeData[slug];
                if (!recipeInfo) return; // Skip if recipe not found

                const originalServings = recipeInfo.servings || 2;
                const targetServings = recipeInstance.servings || 2;

                html += `
                    <div class="recipe-shopping-section">
                        <div class="recipe-header">
                            <h2 class="recipe-title">${{recipeInfo.category}} ${{recipeInfo.name}}</h2>
                            <div class="servings-control">
                                <label for="servings-${{slug}}-${{instanceIndex}}">{get_text('servings_label_short')}</label>
                                <div class="servings-buttons">
                                    <button
                                        class="servings-btn"
                                        onclick="decrementServingsInstance(${{instanceIndex}}, ${{targetServings}})"
                                        aria-label="Portionen verringern"
                                        ${{targetServings <= 1 ? 'disabled' : ''}}
                                    >−</button>
                                    <input
                                        type="number"
                                        id="servings-${{slug}}-${{instanceIndex}}"
                                        class="servings-input"
                                        min="1"
                                        max="20"
                                        value="${{targetServings}}"
                                        onchange="updateServingsInstance(${{instanceIndex}}, this.value)"
                                        aria-label="Anzahl Portionen"
                                    >
                                    <button
                                        class="servings-btn"
                                        onclick="incrementServingsInstance(${{instanceIndex}}, ${{targetServings}})"
                                        aria-label="Portionen erhöhen"
                                        ${{targetServings >= 20 ? 'disabled' : ''}}
                                    >+</button>
                                </div>
                            </div>
                        </div>
                        <p class="recipe-meta">Original: ${{originalServings}} Portionen → Aktuell: ${{targetServings}} Portionen</p>
                        <ul class="ingredients-list">
                `;

                if (recipeInfo.ingredients && recipeInfo.ingredients.length > 0) {{
                    recipeInfo.ingredients.forEach((ingredient, index) => {{
                        const scaledAmount = scaleAmount(ingredient.amount, originalServings, targetServings);
                        const itemId = `${{slug}}-${{instanceIndex}}-${{index}}`;
                        validItemIds.add(itemId);
                        const isChecked = checked[itemId] || false;
                        const checkedClass = isChecked ? 'checked' : '';
                        const checkedAttr = isChecked ? 'checked' : '';

                        html += `
                            <li class="ingredient-item ${{checkedClass}}">
                                <input
                                    type="checkbox"
                                    id="check-${{itemId}}"
                                    class="ingredient-checkbox"
                                    ${{checkedAttr}}
                                    onchange="toggleIngredientCheck('${{itemId}}')"
                                >
                                <div class="ingredient-info">
                                    <span class="ingredient-name">${{ingredient.name}}</span>
                                    <span class="ingredient-amount">${{scaledAmount}}</span>
                                </div>
                            </li>
                        `;
                    }});
                }} else {{
                    html += `<li class="ingredient-item"><span class="ingredient-name">Keine Zutaten verfügbar</span></li>`;
                }}

                html += `
                        </ul>
                    </div>
                `;
            }});

            html += '</div>';
            container.innerHTML = html;
        }}

        function loadShoppingListAlphabetical() {{
            let plan = getLocalWeeklyPlan(currentWeek);
            const container = document.getElementById('shoppingListContainer');

            if (plan.recipes.length === 0) {{
                container.innerHTML = `
                    <div class="no-shopping-items">
                        <h2>{get_text('no_shopping_list')}</h2>
                        <p>{get_text('no_shopping_list_message')}</p>
                    </div>
                `;
                // Clear checked items for current week when no recipes
                saveCheckedItems(currentWeek, {{}});
                return;
            }}

            // Load checked state (by item ID) for current week
            let checked = getCheckedItems(currentWeek);

            // Track valid item IDs in current shopping list
            const validItemIds = new Set();

            // Collect all ingredients from all recipe instances (no aggregation)
            const allIngredients = [];
            plan.recipes.forEach((recipeInstance, instanceIndex) => {{
                const slug = recipeInstance.slug;
                const recipeInfo = recipeData[slug];
                if (!recipeInfo || !recipeInfo.ingredients) return;

                const originalServings = recipeInfo.servings || 2;
                const targetServings = recipeInstance.servings || 2;

                recipeInfo.ingredients.forEach((ingredient, index) => {{
                    const scaledAmount = scaleAmount(ingredient.amount, originalServings, targetServings);
                    const itemId = `${{slug}}-${{instanceIndex}}-${{index}}`;
                    validItemIds.add(itemId);
                    allIngredients.push({{
                        itemId: itemId,
                        name: ingredient.name,
                        amount: scaledAmount,
                        recipeName: recipeInfo.name
                    }});
                }});
            }});

            // Sort alphabetically by ingredient name
            const sortedIngredients = allIngredients.sort((a, b) =>
                a.name.localeCompare(b.name, 'de')
            );

            // Render alphabetical list
            let html = '<div class="shopping-list-container">';
            html += '<div class="recipe-shopping-section">';
            html += '<h2 class="recipe-title">Alle Zutaten alphabetisch</h2>';
            html += '<ul class="ingredients-list">';

            sortedIngredients.forEach((ingredient) => {{
                const itemId = ingredient.itemId;
                const isChecked = checked[itemId] || false;
                const checkedClass = isChecked ? 'checked' : '';
                const checkedAttr = isChecked ? 'checked' : '';

                html += `
                    <li class="ingredient-item ${{checkedClass}}">
                        <input
                            type="checkbox"
                            id="check-${{itemId}}"
                            class="ingredient-checkbox"
                            ${{checkedAttr}}
                            onchange="toggleIngredientCheck('${{itemId}}')"
                        >
                        <div class="ingredient-info">
                            <span class="ingredient-name">${{ingredient.name}}</span>
                            <span class="ingredient-amount">${{ingredient.amount}}</span>
                        </div>
                    </li>
                `;
            }});

            html += '</ul>';
            html += '</div>';
            html += '</div>';
            container.innerHTML = html;
        }}

        // Clean up old weeks from localStorage (keep only current week and next week)
        function cleanupOldWeeks() {{
            try {{
                const stored = localStorage.getItem('mealPlansV2');
                if (!stored) return;

                const mealPlans = JSON.parse(stored);
                const currentDate = new Date();

                // Calculate weeks to keep (current week and next week only)
                const weeksToKeep = new Set();
                const thisWeek = getISOWeek(currentDate);
                const nextWeekDate = new Date(currentDate);
                nextWeekDate.setDate(nextWeekDate.getDate() + 7);
                const nextWeek = getISOWeek(nextWeekDate);

                weeksToKeep.add(thisWeek);
                weeksToKeep.add(nextWeek);

                // Remove weeks outside the range from meal plans
                let hasChanges = false;
                for (const week in mealPlans) {{
                    if (!weeksToKeep.has(week)) {{
                        delete mealPlans[week];
                        hasChanges = true;
                    }}
                }}

                // Save back if we made changes
                if (hasChanges) {{
                    localStorage.setItem('mealPlansV2', JSON.stringify(mealPlans));
                }}

                // Also clean up checked items for old weeks
                const checkedStored = localStorage.getItem('shoppingListChecked');
                if (checkedStored) {{
                    const allChecked = JSON.parse(checkedStored);
                    let checkedHasChanges = false;
                    for (const week in allChecked) {{
                        if (!weeksToKeep.has(week)) {{
                            delete allChecked[week];
                            checkedHasChanges = true;
                        }}
                    }}
                    if (checkedHasChanges) {{
                        localStorage.setItem('shoppingListChecked', JSON.stringify(allChecked));
                    }}
                }}
            }} catch (e) {{
                console.error('Error cleaning up old weeks:', e);
            }}
        }}

        // Load shopping list on page load
        document.addEventListener('DOMContentLoaded', function() {{
            currentWeek = getISOWeek(new Date());
            updateWeekInfo();
            cleanupOldWeeks();
            updateWeekButtons();
            loadShoppingList();
            initializeDarkMode();

            // Listen for storage changes from other tabs (when weekly plan is modified)
            window.addEventListener('storage', function(e) {{
                if (e.key === 'mealPlansV2' || e.key === 'weeklyPlanNeedsSync') {{
                    loadShoppingList(); // Refresh shopping list
                }}
            }});
        }});
    </script>
</body>
</html>'''

    return html
