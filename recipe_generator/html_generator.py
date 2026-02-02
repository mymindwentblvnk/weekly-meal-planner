"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS, WEEKLY_PAGE_CSS, get_text, TEXTS, GOOGLE_DRIVE_CLIENT_ID


def bilingual_text(key: str) -> str:
    """Generate bilingual span elements for a text key.

    Args:
        key: The text key to look up in TEXTS dictionary

    Returns:
        HTML with both German and English spans
    """
    de_text = TEXTS['de'].get(key, key)
    en_text = TEXTS['en'].get(key, key)
    return f'<span class="lang-de">{de_text}</span><span class="lang-en">{en_text}</span>'


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

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(recipe['name'])} {get_text('recipe_title_suffix')}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <style>
        {COMMON_CSS}
        {DETAIL_PAGE_CSS}
    </style>
</head>
<body>
    <div class="top-nav">
        <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="weekly.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="stats.html" class="nav-link" aria-label="Statistics">📊</a>
            <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
                <span class="emoji lang-de">🇩🇪</span>
                <span class="emoji lang-en">🇬🇧</span>
            </button>
            <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
                <span class="emoji light-mode-icon">☀️</span>
                <span class="emoji dark-mode-icon">🌙</span>
            </button>
        </div>
    </div>
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{escape(recipe['name'])}</h1>

        <p itemprop="description">{escape(recipe.get('description', ''))}</p>

        <div itemprop="author" itemscope itemtype="https://schema.org/Person">
            <meta itemprop="name" content="{escape(recipe.get('author', 'Unknown'))}">
        </div>

        <div style="display: flex; gap: 15px; align-items: center; margin: 20px 0; flex-wrap: wrap;">
            {generate_bring_widget()}
            <button id="weeklyPlanButton" class="weekly-plan-button" onclick="toggleWeeklyPlan()">
                <span class="lang-de">📅 Diese Woche kochen</span>
                <span class="lang-en">📅 Cook This Week</span>
            </button>
        </div>

        <table class="recipe-info-table">
            <tr>
                <td><time itemprop="prepTime" datetime="{format_time(recipe['prep_time'])}">{bilingual_text('prep_time')}</time></td>
                <td>{recipe['prep_time']} {bilingual_text('minutes')}</td>
            </tr>
            <tr>
                <td><time itemprop="cookTime" datetime="{format_time(recipe['cook_time'])}">{bilingual_text('cook_time')}</time></td>
                <td>{recipe['cook_time']} {bilingual_text('minutes')}</td>
            </tr>
            <tr>
                <td><meta itemprop="recipeYield" content="{recipe['servings']} servings">{bilingual_text('servings_label')}</td>
                <td>{recipe['servings']}</td>
            </tr>
        </table>

        <h2>{bilingual_text('ingredients_heading')}</h2>

        <table class="ingredients-table">
            <thead>
                <tr>
                    <th>{bilingual_text('amount_label')}</th>
                    <th>{bilingual_text('ingredient_label')}</th>
                </tr>
            </thead>
            <tbody>
{chr(10).join(ingredients_rows)}
            </tbody>
        </table>

        <h2>{bilingual_text('instructions_heading')}</h2>
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

                // Trigger sync if available (weekly.html loads this on same device)
                // This will only work if user navigates to weekly page
                // Cross-device sync happens when opening weekly page on other device
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
                button.innerHTML = `<span class="lang-de">✓ In Wochenplan${{countText}}</span><span class="lang-en">✓ In Weekly Plan${{countText}}</span>`;
            }} else {{
                button.classList.remove('in-plan');
                button.innerHTML = '<span class="lang-de">📅 Diese Woche kochen</span><span class="lang-en">📅 Cook This Week</span>';
            }}

            // Apply current language
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);
        }}

        // Language toggle functionality
        function toggleLanguage() {{
            const currentLang = localStorage.getItem('language') || 'de';
            const newLang = currentLang === 'de' ? 'en' : 'de';
            localStorage.setItem('language', newLang);
            applyLanguage(newLang);
        }}

        function applyLanguage(lang) {{
            document.querySelectorAll('.lang-de, .lang-en').forEach(el => {{
                el.classList.remove('active');
            }});
            document.querySelectorAll('.lang-' + lang).forEach(el => {{
                el.classList.add('active');
            }});
        }}

        // Dark mode toggle functionality
        function toggleDarkMode() {{
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
            updateDarkModeButton(isDark);
        }}

        function updateDarkModeButton(isDark) {{
            document.querySelectorAll('.light-mode-text').forEach(el => {{
                el.style.display = isDark ? 'none' : 'inline';
            }});
            document.querySelectorAll('.dark-mode-text').forEach(el => {{
                el.style.display = isDark ? 'inline' : 'none';
            }});

            // Update dark mode toggle icon
            document.querySelectorAll('.light-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.remove('active');
                }} else {{
                    el.classList.add('active');
                }}
            }});
            document.querySelectorAll('.dark-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
        }}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Apply language
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);

            // Apply dark mode
            const darkMode = localStorage.getItem('darkMode');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = darkMode === 'enabled' || (darkMode === null && prefersDark);

            if (isDark) {{
                document.body.classList.add('dark-mode');
            }}
            updateDarkModeButton(isDark);

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
            <span class="servings">🍽️ {servings} {bilingual_text('servings')}</span> •
            <span class="time">⏱️ {total_time} {bilingual_text('min_total')}</span>
        </p>
        <a href="{escape(filename)}" class="view-recipe-btn">{bilingual_text('view_recipe')}</a>
    </div>'''
        recipe_entries.append(recipe_entry)

    # Generate footer with deployment time
    footer_html = ""
    if deployment_time:
        formatted_time = deployment_time.strftime("%d. %B %Y um %H:%M UTC")
        footer_html = f'''
    <footer class="deployment-info">
        <p>{bilingual_text('last_updated')} {formatted_time}</p>
    </footer>'''

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_text('overview_title')}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <style>
        {COMMON_CSS}
        {OVERVIEW_PAGE_CSS}
    </style>
</head>
<body>
    <div class="page-header">
        <h1>{bilingual_text('overview_title')}</h1>
        <div class="top-nav">
            <a href="weekly.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="stats.html" class="nav-link" aria-label="Statistics">📊</a>
            <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
                <span class="emoji lang-de">🇩🇪</span>
                <span class="emoji lang-en">🇬🇧</span>
            </button>
            <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
                <span class="emoji light-mode-icon">☀️</span>
                <span class="emoji dark-mode-icon">🌙</span>
            </button>
        </div>
    </div>

    <div class="filter-buttons">
        <button class="filter-btn active" data-filter="all" data-filter-type="category">{bilingual_text('filter_all')}</button>
        <button class="filter-btn" data-filter="🥩" data-filter-type="category">🥩 {bilingual_text('filter_meat')}</button>
        <button class="filter-btn" data-filter="🐟" data-filter-type="category">🐟 {bilingual_text('filter_fish')}</button>
        <button class="filter-btn" data-filter="🥦" data-filter-type="category">🥦 {bilingual_text('filter_vegetarian')}</button>
        <button class="filter-btn" data-filter="🍞" data-filter-type="category">🍞 {bilingual_text('filter_bread')}</button>
        <button class="filter-btn" data-filter="🥣" data-filter-type="category">🥣 {bilingual_text('filter_sweet')}</button>
        <button class="filter-btn" data-filter="fast" data-filter-type="time">⚡ {bilingual_text('filter_fast')}</button>
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

        // Language toggle functionality
        function toggleLanguage() {{
            const currentLang = localStorage.getItem('language') || 'de';
            const newLang = currentLang === 'de' ? 'en' : 'de';
            localStorage.setItem('language', newLang);
            applyLanguage(newLang);
        }}

        function applyLanguage(lang) {{
            document.querySelectorAll('.lang-de, .lang-en').forEach(el => {{
                el.classList.remove('active');
            }});
            document.querySelectorAll('.lang-' + lang).forEach(el => {{
                el.classList.add('active');
            }});
        }}

        // Dark mode toggle functionality
        function toggleDarkMode() {{
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
            updateDarkModeButton(isDark);
        }}

        function updateDarkModeButton(isDark) {{
            document.querySelectorAll('.light-mode-text').forEach(el => {{
                el.style.display = isDark ? 'none' : 'inline';
            }});
            document.querySelectorAll('.dark-mode-text').forEach(el => {{
                el.style.display = isDark ? 'inline' : 'none';
            }});

            // Update dark mode toggle icon
            document.querySelectorAll('.light-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.remove('active');
                }} else {{
                    el.classList.add('active');
                }}
            }});
            document.querySelectorAll('.dark-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
        }}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Apply language
            const savedLang = localStorage.getItem('language') || 'de';
            const languageToggle = document.getElementById('languageToggle');
            if (languageToggle) {{
                languageToggle.checked = (savedLang === 'en');
            }}
            applyLanguage(savedLang);

            // Apply dark mode
            const darkMode = localStorage.getItem('darkMode');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = darkMode === 'enabled' || (darkMode === null && prefersDark);

            const darkModeToggle = document.getElementById('darkModeToggle');
            if (darkModeToggle) {{
                darkModeToggle.checked = isDark;
            }}

            if (isDark) {{
                document.body.classList.add('dark-mode');
            }}
            updateDarkModeButton(isDark);

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

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_text('stats_title')}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <style>
        {COMMON_CSS}
        {OVERVIEW_PAGE_CSS}
        .stats-list {{
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
        }}
    </style>
</head>
<body>
    <div class="top-nav">
        <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="weekly.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="stats.html" class="nav-link" aria-label="Statistics">📊</a>
            <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
                <span class="emoji lang-de">🇩🇪</span>
                <span class="emoji lang-en">🇬🇧</span>
            </button>
            <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
                <span class="emoji light-mode-icon">☀️</span>
                <span class="emoji dark-mode-icon">🌙</span>
            </button>
        </div>
    </div>
    <h1>{bilingual_text('stats_title')}</h1>
    <p style="color: var(--text-secondary); margin-bottom: 15px;">{bilingual_text('stats_subtitle')}</p>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{bilingual_text('stats_disclaimer')}</p>

    <div id="stats-container">
        <p class="no-data">{bilingual_text('stats_no_data')}</p>
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
                container.innerHTML = '<p class="no-data">{bilingual_text("stats_no_data")}</p>';
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
                        <div class="view-count">${{count}} <span class="lang-de">Aufrufe</span><span class="lang-en">Views</span></div>
                    </li>
                `;
            }});
            html += '</ol>';

            container.innerHTML = html;

            // Apply current language to new content
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);
        }}

        // Language toggle functionality
        function toggleLanguage() {{
            const currentLang = localStorage.getItem('language') || 'de';
            const newLang = currentLang === 'de' ? 'en' : 'de';
            localStorage.setItem('language', newLang);
            applyLanguage(newLang);
        }}

        function applyLanguage(lang) {{
            document.querySelectorAll('.lang-de, .lang-en').forEach(el => {{
                el.classList.remove('active');
            }});
            document.querySelectorAll('.lang-' + lang).forEach(el => {{
                el.classList.add('active');
            }});
        }}

        // Dark mode toggle functionality
        function toggleDarkMode() {{
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
            updateDarkModeButton(isDark);
        }}

        function updateDarkModeButton(isDark) {{
            document.querySelectorAll('.light-mode-text').forEach(el => {{
                el.style.display = isDark ? 'none' : 'inline';
            }});
            document.querySelectorAll('.dark-mode-text').forEach(el => {{
                el.style.display = isDark ? 'inline' : 'none';
            }});

            // Update dark mode toggle icon
            document.querySelectorAll('.light-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.remove('active');
                }} else {{
                    el.classList.add('active');
                }}
            }});
            document.querySelectorAll('.dark-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
        }}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Display stats
            displayStats();

            // Apply language
            const savedLang = localStorage.getItem('language') || 'de';
            const languageToggle = document.getElementById('languageToggle');
            if (languageToggle) {{
                languageToggle.checked = (savedLang === 'en');
            }}
            applyLanguage(savedLang);

            // Apply dark mode
            const darkMode = localStorage.getItem('darkMode');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = darkMode === 'enabled' || (darkMode === null && prefersDark);

            const darkModeToggle = document.getElementById('darkModeToggle');
            if (darkModeToggle) {{
                darkModeToggle.checked = isDark;
            }}

            if (isDark) {{
                document.body.classList.add('dark-mode');
            }}
            updateDarkModeButton(isDark);
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

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_text('weekly_plan_title')}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <script src="https://accounts.google.com/gsi/client"></script>
    <script src="https://apis.google.com/js/api.js"></script>
    <style>
        {COMMON_CSS}
        {WEEKLY_PAGE_CSS}
    </style>
</head>
<body>
    <div class="top-nav">
        <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="weekly.html" class="nav-link" aria-label="Weekly Plan">🗓️</a>
            <a href="stats.html" class="nav-link" aria-label="Statistics">📊</a>
            <button id="googleSignInButton" class="nav-toggle-button google-sign-in-button" onclick="handleSignIn()" style="display: none;">
                <span>🔒</span>
            </button>
            <button id="googleSignOutButton" class="nav-toggle-button google-sign-in-button" onclick="handleSignOut()" style="display: none;">
                <span id="userEmail"></span>
            </button>
            <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
                <span class="emoji lang-de">🇩🇪</span>
                <span class="emoji lang-en">🇬🇧</span>
            </button>
            <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
                <span class="emoji light-mode-icon">☀️</span>
                <span class="emoji dark-mode-icon">🌙</span>
            </button>
        </div>
    </div>
    <h1>{bilingual_text('weekly_plan_title')}</h1>
    <div id="syncStatus" class="sync-status" style="display: none;"></div>

    <button id="clearAllButton" class="clear-all-button" onclick="clearAllRecipes()">
        <span class="lang-de">Alle löschen</span>
        <span class="lang-en">Clear All</span>
    </button>

    <div id="weeklyPlanContainer"></div>

    <script>
        const recipeData = {recipe_lookup_json};
        const GOOGLE_CLIENT_ID = '{GOOGLE_DRIVE_CLIENT_ID}';
        const SCOPES = 'https://www.googleapis.com/auth/drive.appdata';
        const SYNC_FILENAME = 'bring-wochenplan-sync.json';

        // Google Drive API state
        let gapiInitialized = false;
        let tokenClient;
        let accessToken = null;
        let userEmail = null;

        // ============ Google Drive API Functions ============

        // Initialize Google API
        function initGoogleDrive() {{
            gapi.load('client', initClient);
        }}

        // Initialize OAuth client with new Google Identity Services
        async function initClient() {{
            try {{
                await gapi.client.init({{
                    discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest']
                }});

                gapiInitialized = true;

                // Initialize the token client
                tokenClient = google.accounts.oauth2.initTokenClient({{
                    client_id: GOOGLE_CLIENT_ID,
                    scope: SCOPES,
                    callback: (response) => {{
                        if (response.error !== undefined) {{
                            console.error('Token response error:', response);
                            showSignedOutUI();
                            return;
                        }}
                        accessToken = response.access_token;
                        gapi.client.setToken({{ access_token: accessToken }});

                        // Get user info
                        getUserInfo();
                    }}
                }});

                // Check if we have a saved token
                const savedToken = localStorage.getItem('googleAccessToken');
                const savedEmail = localStorage.getItem('googleUserEmail');
                if (savedToken && savedEmail) {{
                    accessToken = savedToken;
                    userEmail = savedEmail;
                    gapi.client.setToken({{ access_token: accessToken }});
                    showSignedInUI(userEmail);
                    performSync();
                }} else {{
                    showSignedOutUI();
                }}
            }} catch (error) {{
                console.error('Error initializing Google API:', error);
                showSignedOutUI();
            }}
        }}

        // Get user info from Google
        async function getUserInfo() {{
            try {{
                const response = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {{
                    headers: {{
                        'Authorization': `Bearer ${{accessToken}}`
                    }}
                }});
                const data = await response.json();
                userEmail = data.email;

                // Save token and email
                localStorage.setItem('googleAccessToken', accessToken);
                localStorage.setItem('googleUserEmail', userEmail);

                showSignedInUI(userEmail);
                performSync();
            }} catch (error) {{
                console.error('Error getting user info:', error);
                showSignedOutUI();
            }}
        }}

        // Sign in
        function handleSignIn() {{
            if (!gapiInitialized || !tokenClient) {{
                console.error('Google API not initialized');
                return;
            }}

            // Request an access token
            tokenClient.requestAccessToken({{ prompt: 'consent' }});
        }}

        // Sign out
        function handleSignOut() {{
            if (accessToken) {{
                google.accounts.oauth2.revoke(accessToken, () => {{
                    console.log('Token revoked');
                }});
            }}

            accessToken = null;
            userEmail = null;
            gapi.client.setToken(null);
            localStorage.removeItem('googleAccessToken');
            localStorage.removeItem('googleUserEmail');

            showSignedOutUI();
        }}

        // Show signed-in UI
        function showSignedInUI(email) {{
            const signInButton = document.getElementById('googleSignInButton');
            const signOutButton = document.getElementById('googleSignOutButton');
            const userEmailSpan = document.getElementById('userEmail');

            if (signInButton) signInButton.style.display = 'none';
            if (signOutButton) {{
                signOutButton.style.display = 'flex';
                const shortEmail = email.length > 20 ? email.substring(0, 17) + '...' : email;
                userEmailSpan.textContent = '✓ ' + shortEmail;
            }}
        }}

        // Show signed-out UI
        function showSignedOutUI() {{
            const signInButton = document.getElementById('googleSignInButton');
            const signOutButton = document.getElementById('googleSignOutButton');
            const syncStatus = document.getElementById('syncStatus');

            if (signInButton) signInButton.style.display = 'flex';
            if (signOutButton) signOutButton.style.display = 'none';
            if (syncStatus) syncStatus.style.display = 'none';
        }}

        // Find the sync file in Drive
        async function findSyncFile() {{
            try {{
                const response = await gapi.client.drive.files.list({{
                    spaces: 'appDataFolder',
                    fields: 'files(id, name, modifiedTime)',
                    q: `name='${{SYNC_FILENAME}}'`
                }});

                return response.result.files.length > 0 ? response.result.files[0] : null;
            }} catch (error) {{
                console.error('Error finding sync file:', error);
                throw error;
            }}
        }}

        // Download data from Drive
        async function downloadFromDrive(fileId) {{
            try {{
                const response = await gapi.client.drive.files.get({{
                    fileId: fileId,
                    alt: 'media'
                }});

                return JSON.parse(response.body);
            }} catch (error) {{
                console.error('Error downloading from Drive:', error);
                throw error;
            }}
        }}

        // Upload data to Drive (create or update)
        async function uploadToDrive(data) {{
            try {{
                const file = await findSyncFile();
                const content = JSON.stringify(data);
                const boundary = '-------314159265358979323846';
                const delimiter = "\\r\\n--" + boundary + "\\r\\n";
                const close_delim = "\\r\\n--" + boundary + "--";

                const metadata = {{
                    name: SYNC_FILENAME,
                    mimeType: 'application/json'
                }};

                if (file) {{
                    // Update existing file
                    const multipartRequestBody =
                        delimiter +
                        'Content-Type: application/json\\r\\n\\r\\n' +
                        JSON.stringify(metadata) +
                        delimiter +
                        'Content-Type: application/json\\r\\n\\r\\n' +
                        content +
                        close_delim;

                    await gapi.client.request({{
                        path: `/upload/drive/v3/files/${{file.id}}`,
                        method: 'PATCH',
                        params: {{ uploadType: 'multipart' }},
                        headers: {{
                            'Content-Type': 'multipart/related; boundary="' + boundary + '"'
                        }},
                        body: multipartRequestBody
                    }});
                }} else {{
                    // Create new file in appDataFolder
                    metadata.parents = ['appDataFolder'];

                    const multipartRequestBody =
                        delimiter +
                        'Content-Type: application/json\\r\\n\\r\\n' +
                        JSON.stringify(metadata) +
                        delimiter +
                        'Content-Type: application/json\\r\\n\\r\\n' +
                        content +
                        close_delim;

                    await gapi.client.request({{
                        path: '/upload/drive/v3/files',
                        method: 'POST',
                        params: {{ uploadType: 'multipart' }},
                        headers: {{
                            'Content-Type': 'multipart/related; boundary="' + boundary + '"'
                        }},
                        body: multipartRequestBody
                    }});
                }}
            }} catch (error) {{
                console.error('Error uploading to Drive:', error);
                throw error;
            }}
        }}

        // Main sync function
        async function performSync() {{
            if (!isSignedInToGoogle()) {{
                return;
            }}

            try {{
                setSyncStatus('syncing');

                const localData = getLocalWeeklyPlan();
                const driveFile = await findSyncFile();

                if (!driveFile) {{
                    // No Drive data - upload local data if any
                    if (localData.recipes && localData.recipes.length > 0) {{
                        await uploadToDrive(addSyncMetadata(localData));
                    }} else {{
                        // Initialize empty plan in Drive
                        await uploadToDrive(addSyncMetadata({{ recipes: [] }}));
                    }}
                }} else {{
                    const driveData = await downloadFromDrive(driveFile.id);

                    // Compare timestamps
                    const localTime = localData.lastModified || 0;
                    const driveTime = driveData.lastModified || 0;

                    if (driveTime > localTime) {{
                        // Drive is newer - download
                        saveLocalWeeklyPlan(driveData);
                        loadWeeklyPlan(); // Refresh UI
                    }} else if (localTime > driveTime) {{
                        // Local is newer - upload
                        await uploadToDrive(addSyncMetadata(localData));
                    }}
                    // Else: equal timestamps - no action needed
                }}

                setSyncStatus('synced');
                localStorage.setItem('lastSyncTime', Date.now().toString());
            }} catch (error) {{
                console.error('Sync error:', error);
                setSyncStatus('error');
            }}
        }}

        // Add sync metadata to plan data
        function addSyncMetadata(planData) {{
            return {{
                ...planData,
                lastModified: Date.now(),
                deviceId: getDeviceId()
            }};
        }}

        // Get or create device ID
        function getDeviceId() {{
            let deviceId = localStorage.getItem('deviceId');
            if (!deviceId) {{
                deviceId = 'device-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('deviceId', deviceId);
            }}
            return deviceId;
        }}

        // Set sync status UI
        function setSyncStatus(status) {{
            const indicator = document.getElementById('syncStatus');
            if (!indicator) return;

            indicator.style.display = 'block';
            const lastSync = localStorage.getItem('lastSyncTime');

            switch (status) {{
                case 'syncing':
                    indicator.innerHTML = '<span class="lang-de">⟳ Synchronisiere...</span><span class="lang-en">⟳ Syncing...</span>';
                    indicator.className = 'sync-status syncing';
                    break;
                case 'synced':
                    const timeAgo = lastSync ? getTimeAgo(parseInt(lastSync)) : '<span class="lang-de">gerade eben</span><span class="lang-en">just now</span>';
                    indicator.innerHTML = `<span class="lang-de">✓ Zuletzt synchronisiert: ${{timeAgo}}</span><span class="lang-en">✓ Last synced: ${{timeAgo}}</span>`;
                    indicator.className = 'sync-status synced';
                    break;
                case 'error':
                    indicator.innerHTML = '<span class="lang-de">⚠ Sync-Fehler - <a href="#" onclick="performSync(); return false;">erneut versuchen?</a></span><span class="lang-en">⚠ Sync error - <a href="#" onclick="performSync(); return false;">retry?</a></span>';
                    indicator.className = 'sync-status error';
                    break;
                case 'offline':
                    indicator.innerHTML = '<span class="lang-de">📡 Offline - Änderungen lokal gespeichert</span><span class="lang-en">📡 Offline - changes saved locally</span>';
                    indicator.className = 'sync-status offline';
                    break;
            }}

            // Apply current language to new content
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);
        }}

        // Calculate time ago
        function getTimeAgo(timestamp) {{
            const currentLang = localStorage.getItem('language') || 'de';
            const seconds = Math.floor((Date.now() - timestamp) / 1000);

            if (seconds < 60) {{
                return currentLang === 'de' ? 'gerade eben' : 'just now';
            }}

            const minutes = Math.floor(seconds / 60);
            if (minutes < 60) {{
                if (currentLang === 'de') {{
                    return minutes === 1 ? '1 Minute her' : `${{minutes}} Minuten her`;
                }} else {{
                    return minutes === 1 ? '1 minute ago' : `${{minutes}} minutes ago`;
                }}
            }}

            const hours = Math.floor(minutes / 60);
            if (hours < 24) {{
                if (currentLang === 'de') {{
                    return hours === 1 ? '1 Stunde her' : `${{hours}} Stunden her`;
                }} else {{
                    return hours === 1 ? '1 hour ago' : `${{hours}} hours ago`;
                }}
            }}

            const days = Math.floor(hours / 24);
            if (currentLang === 'de') {{
                return days === 1 ? '1 Tag her' : `${{days}} Tagen her`;
            }} else {{
                return days === 1 ? '1 day ago' : `${{days}} days ago`;
            }}
        }}

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

        // Check if user is signed in to Google
        function isSignedInToGoogle() {{
            return gapiInitialized && accessToken !== null;
        }}

        // Trigger sync after data changes
        function syncIfSignedIn() {{
            if (isSignedInToGoogle()) {{
                performSync();
            }}
        }}

        // ============ Weekly Plan Functions ============

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
                        <h2><span class="lang-de">Noch keine Rezepte geplant</span><span class="lang-en">No Recipes Planned Yet</span></h2>
                        <p><span class="lang-de">Füge Rezepte aus den Detail-Seiten hinzu, um deinen Wochenplan zu erstellen!</span><span class="lang-en">Add recipes from detail pages to create your weekly meal plan!</span></p>
                    </div>
                `;
                clearButton.disabled = true;

                // Apply current language to new content
                const savedLang = localStorage.getItem('language') || 'de';
                applyLanguage(savedLang);
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
                const statusText = recipe.cooked
                    ? '<span class="lang-de">✓ Gekocht</span><span class="lang-en">✓ Cooked</span>'
                    : '<span class="lang-de">Nicht gekocht</span><span class="lang-en">Not cooked</span>';
                const dateAdded = formatDate(recipe.addedAt);

                const actionButton = recipe.cooked
                    ? `<button class="action-button uncook-button" onclick="toggleCooked('${{recipeId}}')">
                        <span class="lang-de">Als ungekocht markieren</span>
                        <span class="lang-en">Mark as Uncooked</span>
                       </button>`
                    : `<button class="action-button cook-button" onclick="toggleCooked('${{recipeId}}')">
                        <span class="lang-de">Als gekocht markieren</span>
                        <span class="lang-en">Mark as Cooked</span>
                       </button>`;

                html += `
                    <div class="weekly-recipe-card ${{cookedClass}}">
                        <div class="recipe-category">${{recipe.category}}</div>
                        <div class="recipe-details">
                            <h3><a href="${{recipeInfo.filename}}">${{recipeInfo.name}}</a></h3>
                            <div class="recipe-status">
                                ${{statusText}} • <span class="lang-de">Hinzugefügt:</span><span class="lang-en">Added:</span> ${{dateAdded}}
                            </div>
                        </div>
                        <div class="recipe-actions">
                            ${{actionButton}}
                            <button class="action-button remove-button" onclick="removeRecipe('${{recipeId}}')">
                                <span class="lang-de">Entfernen</span>
                                <span class="lang-en">Remove</span>
                            </button>
                        </div>
                    </div>
                `;
            }});
            html += '</div>';

            container.innerHTML = html;

            // Apply current language to new content
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);
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
                syncIfSignedIn();
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
                syncIfSignedIn();
            }}
        }}

        function clearAllRecipes() {{
            const currentLang = localStorage.getItem('language') || 'de';
            const confirmMessage = currentLang === 'de'
                ? 'Möchtest du wirklich alle Rezepte aus dem Wochenplan entfernen?'
                : 'Do you really want to remove all recipes from your weekly plan?';

            if (!confirm(confirmMessage)) {{
                return;
            }}

            const emptyPlan = {{
                recipes: [],
                lastModified: Date.now()
            }};

            saveLocalWeeklyPlan(emptyPlan);
            loadWeeklyPlan();
            syncIfSignedIn();
        }}

        // Language toggle functionality
        function toggleLanguage() {{
            const currentLang = localStorage.getItem('language') || 'de';
            const newLang = currentLang === 'de' ? 'en' : 'de';
            localStorage.setItem('language', newLang);
            applyLanguage(newLang);
        }}

        function applyLanguage(lang) {{
            document.querySelectorAll('.lang-de, .lang-en').forEach(el => {{
                el.classList.remove('active');
            }});
            document.querySelectorAll('.lang-' + lang).forEach(el => {{
                el.classList.add('active');
            }});
        }}

        // Dark mode toggle functionality
        function toggleDarkMode() {{
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
            updateDarkModeButton(isDark);
        }}

        function updateDarkModeButton(isDark) {{
            document.querySelectorAll('.light-mode-text').forEach(el => {{
                el.style.display = isDark ? 'none' : 'inline';
            }});
            document.querySelectorAll('.dark-mode-text').forEach(el => {{
                el.style.display = isDark ? 'inline' : 'none';
            }});

            // Update dark mode toggle icon
            document.querySelectorAll('.light-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.remove('active');
                }} else {{
                    el.classList.add('active');
                }}
            }});
            document.querySelectorAll('.dark-mode-icon').forEach(el => {{
                if (isDark) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
        }}

        // Apply saved preferences on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Load weekly plan
            loadWeeklyPlan();

            // Apply language
            const savedLang = localStorage.getItem('language') || 'de';
            applyLanguage(savedLang);

            // Apply dark mode
            const darkMode = localStorage.getItem('darkMode');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDark = darkMode === 'enabled' || (darkMode === null && prefersDark);

            if (isDark) {{
                document.body.classList.add('dark-mode');
            }}
            updateDarkModeButton(isDark);

            // Initialize Google Drive API
            initGoogleDrive();

            // Set up periodic sync (every 60 seconds when page is visible)
            setInterval(function() {{
                if (!document.hidden && isSignedInToGoogle()) {{
                    performSync();
                }}
            }}, 60000);
        }});
    </script>
</body>
</html>'''

    return html
