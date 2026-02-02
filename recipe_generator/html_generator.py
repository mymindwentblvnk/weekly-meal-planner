"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS, WEEKLY_PAGE_CSS, get_text


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


def generate_navigation(show_back_button: bool = False) -> str:
    """Generate top navigation HTML.

    Args:
        show_back_button: Whether to show the back to recipes button

    Returns:
        HTML for top navigation bar
    """
    back_button = f'<a href="index.html" class="back-button">{get_text("back_to_recipes")}</a>' if show_back_button else ''

    return f'''<div class="top-nav">
        {back_button}
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="weekly.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="stats.html" class="nav-link" aria-label="Statistics">📊</a>
            <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
                <span class="emoji light-mode-icon">☀️</span>
                <span class="emoji dark-mode-icon">🌙</span>
            </button>
        </div>
    </div>'''


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
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
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
    {generate_navigation(show_back_button=True)}
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{escape(recipe['name'])}</h1>

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
    <script>
        // Recipe data for weekly plan
        const recipeData = {{
            name: '{escape(recipe['name'])}',
            slug: '{escape(slug)}',
            category: '{escape(recipe.get('category', ''))}'
        }};

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
    # Sort recipes by category
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
        time_category = 'fast' if total_time <= 30 else 'slow'

        recipe_entry = f'''    <div class="recipe-card" data-category="{category}" data-time="{time_category}">
        <h2><a href="{escape(filename)}">{escape(recipe['name'])}</a></h2>
        <p class="description">{description}</p>
        <p class="meta">
            <span class="servings">🍽️ {servings} {get_text('servings')}</span> •
            <span class="time">⏱️ {total_time} {get_text('min_total')}</span>
        </p>
        <a href="{escape(filename)}" class="view-recipe-btn">{get_text('view_recipe')}</a>
    </div>'''
        recipe_entries.append(recipe_entry)

    # Generate footer with deployment time
    footer_html = ""
    if deployment_time:
        formatted_time = deployment_time.strftime("%d. %B %Y um %H:%M UTC")
        footer_html = f'''
    <footer class="deployment-info">
        <p>{get_text('last_updated')} {formatted_time}</p>
    </footer>'''

    html = f'''{generate_page_header(get_text('overview_title'), OVERVIEW_PAGE_CSS)}
    <div class="page-header">
        <h1>{get_text('overview_title')}</h1>
        {generate_navigation(show_back_button=False)}
    </div>

    <div class="filter-buttons">
        <button class="filter-btn active" data-filter="all" data-filter-type="category">{get_text('filter_all')}</button>
        <button class="filter-btn" data-filter="🥩" data-filter-type="category">🥩 {get_text('filter_meat')}</button>
        <button class="filter-btn" data-filter="🐟" data-filter-type="category">🐟 {get_text('filter_fish')}</button>
        <button class="filter-btn" data-filter="🥦" data-filter-type="category">🥦 {get_text('filter_vegetarian')}</button>
        <button class="filter-btn" data-filter="🍞" data-filter-type="category">🍞 {get_text('filter_bread')}</button>
        <button class="filter-btn" data-filter="🥣" data-filter-type="category">🥣 {get_text('filter_sweet')}</button>
        <button class="filter-btn" data-filter="fast" data-filter-type="time">⚡ {get_text('filter_fast')}</button>
    </div>

    <div class="recipe-grid">
{chr(10).join(recipe_entries)}
    </div>
{footer_html}

    <script>
        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        const recipeCards = document.querySelectorAll('.recipe-card');

        let categoryFilter = 'all';
        let timeFilterActive = false;

        function applyFilters() {{
            recipeCards.forEach(card => {{
                // Check category filter
                const matchesCategory = categoryFilter === 'all' || card.dataset.category === categoryFilter;

                // Check time filter
                const matchesTime = !timeFilterActive || card.dataset.time === 'fast';

                // Show card only if it matches both filters
                if (matchesCategory && matchesTime) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            // Update button states
            filterButtons.forEach(btn => {{
                if (btn.dataset.filterType === 'category') {{
                    if (btn.dataset.filter === categoryFilter) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }} else if (btn.dataset.filterType === 'time') {{
                    if (timeFilterActive) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }}
            }});
        }}

        filterButtons.forEach(button => {{
            button.addEventListener('click', () => {{
                if (button.dataset.filterType === 'category') {{
                    // Toggle category filter: if clicking active category, go back to 'all'
                    if (categoryFilter === button.dataset.filter && categoryFilter !== 'all') {{
                        categoryFilter = 'all';
                    }} else {{
                        categoryFilter = button.dataset.filter;
                    }}
                    localStorage.setItem('recipeCategoryFilter', categoryFilter);
                }} else if (button.dataset.filterType === 'time') {{
                    timeFilterActive = !timeFilterActive;
                    localStorage.setItem('recipeTimeFilter', timeFilterActive ? 'active' : 'inactive');
                }}
                applyFilters();
            }});
        }});

        {generate_dark_mode_script()}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDarkMode();

            // Apply saved filters
            categoryFilter = localStorage.getItem('recipeCategoryFilter') || 'all';
            timeFilterActive = localStorage.getItem('recipeTimeFilter') === 'active';
            applyFilters();
        }});
    </script>
</body>
</html>'''

    return html


def generate_stats_html(recipes_data: list[tuple[str, dict[str, Any]]]) -> str:
    """Generate stats page showing top 10 most viewed recipes.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)

    Returns:
        Complete HTML page as a string
    """
    # Create recipe lookup by name
    recipe_lookup = {recipe['name']: (filename, recipe) for filename, recipe in recipes_data}

    # Generate recipe list as JSON for JavaScript
    recipe_names = [recipe['name'] for _, recipe in recipes_data]
    recipe_names_json = str(recipe_names).replace("'", '"')

    # Stats-specific CSS
    stats_css = '''.stats-list {{
            list-style: none;
            padding: 0;
            margin: 20px 0;
        }}
        .stats-item {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            transition: box-shadow 0.2s;
        }}
        .stats-item:hover {{
            box-shadow: 0 4px 6px var(--shadow);
        }}
        .rank {{
            font-size: 2em;
            font-weight: bold;
            color: var(--primary-color);
            min-width: 60px;
            text-align: center;
        }}
        .recipe-info {{
            flex: 1;
            margin-left: 20px;
        }}
        .recipe-info h3 {{
            margin: 0 0 5px 0;
            color: var(--text-color);
        }}
        .recipe-info a {{
            color: var(--primary-color);
            text-decoration: none;
            font-size: 1.2em;
        }}
        .recipe-info a:hover {{
            text-decoration: underline;
        }}
        .view-count {{
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary-color);
            min-width: 100px;
            text-align: right;
        }}
        .no-data {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-style: italic;
        }}
        .back-button {{
            display: inline-block;
            padding: 8px 16px;
            margin-bottom: 20px;
            background-color: var(--border-color);
            color: var(--text-color);
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
            transition: background-color 0.2s;
        }}
        .back-button:hover {{
            background-color: var(--bg-secondary);
            text-decoration: none;
        }}'''

    html = f'''{generate_page_header(get_text('stats_title'), OVERVIEW_PAGE_CSS, stats_css)}
    {generate_navigation(show_back_button=True)}
    <h1>{get_text('stats_title')}</h1>
    <p style="color: var(--text-secondary); margin-bottom: 15px;">{get_text('stats_subtitle')}</p>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{get_text('stats_disclaimer')}</p>

    <div id="stats-container">
        <p class="no-data">{get_text('stats_no_data')}</p>
    </div>

    <script>
        const recipeNames = {recipe_names_json};
        const recipeData = {{{','.join(f'"{recipe["name"]}": {{"filename": "{filename}", "category": "{recipe.get("category", "")}"}}' for filename, recipe in recipes_data)}}};

        function displayStats() {{
            const viewsKey = 'recipeViews';
            let views = {{}};

            try {{
                const stored = localStorage.getItem(viewsKey);
                if (stored) {{
                    views = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading view counts:', e);
            }}

            // Filter to only include recipes that exist
            const validViews = {{}};
            for (const [name, count] of Object.entries(views)) {{
                if (recipeNames.includes(name)) {{
                    validViews[name] = count;
                }}
            }}

            // Sort by view count and take top 10
            const sortedRecipes = Object.entries(validViews)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);

            const container = document.getElementById('stats-container');

            if (sortedRecipes.length === 0) {{
                container.innerHTML = '<p class="no-data">{get_text("stats_no_data")}</p>';
                return;
            }}

            // Generate stats list
            let html = '<ol class="stats-list">';
            sortedRecipes.forEach(([name, count], index) => {{
                const data = recipeData[name];
                const rankEmoji = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
                html += `
                    <li class="stats-item">
                        <div class="rank">${{rankEmoji || (index + 1)}}</div>
                        <div class="recipe-info">
                            <h3><a href="${{data.filename}}">${{name}}</a></h3>
                        </div>
                        <div class="view-count">${{count}} Aufrufe</div>
                    </li>
                `;
            }});
            html += '</ol>';

            container.innerHTML = html;
        }}

        {generate_dark_mode_script()}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Display stats
            displayStats();

            initializeDarkMode();
        }});
    </script>
</body>
</html>'''

    return html


def generate_weekly_html(recipes_data: list[tuple[str, dict[str, Any]]]) -> str:
    """Generate weekly meal plan page.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)

    Returns:
        Complete HTML page as a string
    """
    # Create recipe lookup by slug
    recipe_lookup = {}
    for filename, recipe in recipes_data:
        slug = filename.replace('.html', '')
        recipe_lookup[slug] = {
            'name': recipe['name'],
            'filename': filename,
            'category': recipe.get('category', '')
        }

    # Generate recipe lookup as JSON for JavaScript
    recipe_lookup_json = str(recipe_lookup).replace("'", '"')

    html = f'''{generate_page_header(get_text('weekly_plan_title'), WEEKLY_PAGE_CSS)}
    {generate_navigation(show_back_button=True)}
    <h1>{get_text('weekly_plan_title')}</h1>

    <button id="clearAllButton" class="clear-all-button" onclick="clearAllRecipes()">Alle löschen</button>

    <div id="weeklyPlanContainer"></div>

    <script>
        const recipeData = {recipe_lookup_json};

        // ============ Weekly Plan Functions ============

        // Get local weekly plan with metadata
        function getLocalWeeklyPlan() {{
            const planKey = 'weeklyMealPlan';
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem(planKey);
                if (stored) {{
                    plan = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading local plan:', e);
            }}

            return plan;
        }}

        // Save weekly plan locally
        function saveLocalWeeklyPlan(planData) {{
            const planKey = 'weeklyMealPlan';
            try {{
                localStorage.setItem(planKey, JSON.stringify(planData));
            }} catch (e) {{
                console.error('Error saving local plan:', e);
            }}
        }}

        function formatDate(timestamp) {{
            const date = new Date(timestamp);
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            return `${{day}}.${{month}}.${{year}}`;
        }}

        function loadWeeklyPlan() {{
            let plan = getLocalWeeklyPlan();

            const container = document.getElementById('weeklyPlanContainer');
            const clearButton = document.getElementById('clearAllButton');

            if (plan.recipes.length === 0) {{
                container.innerHTML = `
                    <div class="no-recipes">
                        <h2>Noch keine Rezepte geplant</h2>
                        <p>Füge Rezepte aus den Detail-Seiten hinzu, um deinen Wochenplan zu erstellen!</p>
                    </div>
                `;
                clearButton.disabled = true;
                return;
            }}

            clearButton.disabled = false;

            let html = '<div class="weekly-plan-list">';
            plan.recipes.forEach((recipe) => {{
                const recipeInfo = recipeData[recipe.slug];
                if (!recipeInfo) return; // Skip if recipe not found

                // Use recipe.id or fall back to slug+addedAt for backwards compatibility
                const recipeId = String(recipe.id || `${{recipe.slug}}-${{recipe.addedAt}}`);

                const cookedClass = recipe.cooked ? 'cooked' : '';
                const statusText = recipe.cooked ? '✓ Gekocht' : 'Nicht gekocht';
                const dateAdded = formatDate(recipe.addedAt);

                const actionButton = recipe.cooked
                    ? `<button class="action-button uncook-button" onclick="toggleCooked('${{recipeId}}')">Als ungekocht markieren</button>`
                    : `<button class="action-button cook-button" onclick="toggleCooked('${{recipeId}}')">Als gekocht markieren</button>`;

                html += `
                    <div class="weekly-recipe-card ${{cookedClass}}">
                        <div class="recipe-category">${{recipe.category}}</div>
                        <div class="recipe-details">
                            <h3><a href="${{recipeInfo.filename}}">${{recipeInfo.name}}</a></h3>
                            <div class="recipe-status">
                                ${{statusText}} • Hinzugefügt: ${{dateAdded}}
                            </div>
                        </div>
                        <div class="recipe-actions">
                            ${{actionButton}}
                            <button class="action-button remove-button" onclick="removeRecipe('${{recipeId}}')">Entfernen</button>
                        </div>
                    </div>
                `;
            }});
            html += '</div>';

            container.innerHTML = html;
        }}

        function toggleCooked(recipeId) {{
            let plan = getLocalWeeklyPlan();

            // Find recipe by ID (or fallback to slug+addedAt for backwards compatibility)
            const recipe = plan.recipes.find(r => {{
                const id = String(r.id || `${{r.slug}}-${{r.addedAt}}`);
                return id === String(recipeId);
            }});

            if (recipe) {{
                recipe.cooked = !recipe.cooked;
                plan.lastModified = Date.now();

                saveLocalWeeklyPlan(plan);
                loadWeeklyPlan();
            }}
        }}

        function removeRecipe(recipeId) {{
            let plan = getLocalWeeklyPlan();

            // Find and remove recipe by ID (or fallback to slug+addedAt for backwards compatibility)
            const index = plan.recipes.findIndex(r => {{
                const id = String(r.id || `${{r.slug}}-${{r.addedAt}}`);
                return id === String(recipeId);
            }});

            if (index >= 0) {{
                plan.recipes.splice(index, 1);
                plan.lastModified = Date.now();

                saveLocalWeeklyPlan(plan);
                loadWeeklyPlan();
            }}
        }}

        function clearAllRecipes() {{
            if (!confirm('Möchtest du wirklich alle Rezepte aus dem Wochenplan entfernen?')) {{
                return;
            }}

            const emptyPlan = {{
                recipes: [],
                lastModified: Date.now()
            }};

            saveLocalWeeklyPlan(emptyPlan);
            loadWeeklyPlan();
        }}

        {generate_dark_mode_script()}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Load weekly plan
            loadWeeklyPlan();

            initializeDarkMode();

            // Listen for storage changes from other tabs (e.g., recipe pages adding items)
            window.addEventListener('storage', function(e) {{
                if (e.key === 'weeklyPlanNeedsSync') {{
                    // Another tab/window modified the weekly plan
                    loadWeeklyPlan(); // Refresh UI
                }}
            }});
        }});
    </script>
</body>
</html>'''

    return html
