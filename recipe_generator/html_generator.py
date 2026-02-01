"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS, WEEKLY_PAGE_CSS, get_text, TEXTS


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
        <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span class="emoji lang-de">🇩🇪</span>
            <span class="emoji lang-en">🇬🇧</span>
        </button>
        <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
            <span class="emoji light-mode-icon">☀️</span>
            <span class="emoji dark-mode-icon">🌙</span>
        </button>
        <div class="burger-menu">
            <button class="burger-icon" onclick="toggleBurgerMenu()" aria-label="Menu">☰</button>
            <div class="burger-dropdown" id="burgerDropdown">
                <div class="burger-item">
                    <a href="weekly.html">{bilingual_text('view_weekly_plan')}</a>
                </div>
                <div class="burger-item">
                    <a href="stats.html">{bilingual_text('view_stats')}</a>
                </div>
            </div>
        </div>
    </div>
    <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{escape(recipe['name'])}</h1>

        <p itemprop="description">{escape(recipe.get('description', ''))}</p>

        <div itemprop="author" itemscope itemtype="https://schema.org/Person">
            <meta itemprop="name" content="{escape(recipe.get('author', 'Unknown'))}">
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

        <button id="weeklyPlanButton" class="weekly-plan-button" onclick="toggleWeeklyPlan()">
            <span class="lang-de">📅 Diese Woche kochen</span>
            <span class="lang-en">📅 Cook This Week</span>
        </button>

        <h2>{bilingual_text('ingredients_heading')}</h2>

        {generate_bring_widget()}

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

            // Save back to localStorage
            try {{
                localStorage.setItem(planKey, JSON.stringify(plan));
                updateWeeklyPlanButton();
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

        // Burger menu functionality
        function toggleBurgerMenu() {{
            const dropdown = document.getElementById('burgerDropdown');
            dropdown.classList.toggle('open');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.querySelector('.burger-menu');
            const dropdown = document.getElementById('burgerDropdown');
            if (!menu.contains(event.target) && dropdown.classList.contains('open')) {{
                dropdown.classList.remove('open');
            }}
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
    <div class="top-nav">
        <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span class="emoji lang-de">🇩🇪</span>
            <span class="emoji lang-en">🇬🇧</span>
        </button>
        <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
            <span class="emoji light-mode-icon">☀️</span>
            <span class="emoji dark-mode-icon">🌙</span>
        </button>
        <div class="burger-menu">
            <button class="burger-icon" onclick="toggleBurgerMenu()" aria-label="Menu">☰</button>
            <div class="burger-dropdown" id="burgerDropdown">
                <div class="burger-item">
                    <a href="weekly.html">{bilingual_text('view_weekly_plan')}</a>
                </div>
                <div class="burger-item">
                    <a href="stats.html">{bilingual_text('view_stats')}</a>
                </div>
            </div>
        </div>
    </div>
    <h1>{bilingual_text('overview_title')}</h1>

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
        // Burger menu functionality
        function toggleBurgerMenu() {{
            const dropdown = document.getElementById('burgerDropdown');
            dropdown.classList.toggle('open');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.querySelector('.burger-menu');
            const dropdown = document.getElementById('burgerDropdown');
            if (!menu.contains(event.target) && dropdown.classList.contains('open')) {{
                dropdown.classList.remove('open');
            }}
        }});

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
        <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span class="emoji lang-de">🇩🇪</span>
            <span class="emoji lang-en">🇬🇧</span>
        </button>
        <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
            <span class="emoji light-mode-icon">☀️</span>
            <span class="emoji dark-mode-icon">🌙</span>
        </button>
        <div class="burger-menu">
            <button class="burger-icon" onclick="toggleBurgerMenu()" aria-label="Menu">☰</button>
            <div class="burger-dropdown" id="burgerDropdown">
                <div class="burger-item">
                    <a href="weekly.html">{bilingual_text('view_weekly_plan')}</a>
                </div>
                <div class="burger-item">
                    <a href="stats.html">{bilingual_text('view_stats')}</a>
                </div>
            </div>
        </div>
    </div>
    <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
    <h1>{bilingual_text('stats_title')}</h1>
    <p style="color: var(--text-secondary); margin-bottom: 15px;">{bilingual_text('stats_subtitle')}</p>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{bilingual_text('stats_disclaimer')}</p>

    <div id="stats-container">
        <p class="no-data">{bilingual_text('stats_no_data')}</p>
    </div>

    <script>
        // Burger menu functionality
        function toggleBurgerMenu() {{
            const dropdown = document.getElementById('burgerDropdown');
            dropdown.classList.toggle('open');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.querySelector('.burger-menu');
            const dropdown = document.getElementById('burgerDropdown');
            if (!menu.contains(event.target) && dropdown.classList.contains('open')) {{
                dropdown.classList.remove('open');
            }}
        }});

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
    <style>
        {COMMON_CSS}
        {WEEKLY_PAGE_CSS}
    </style>
</head>
<body>
    <div class="top-nav">
        <button class="nav-toggle-button" id="languageToggle" onclick="toggleLanguage()" aria-label="Toggle language">
            <span class="emoji lang-de">🇩🇪</span>
            <span class="emoji lang-en">🇬🇧</span>
        </button>
        <button class="nav-toggle-button" id="darkModeToggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
            <span class="emoji light-mode-icon">☀️</span>
            <span class="emoji dark-mode-icon">🌙</span>
        </button>
        <div class="burger-menu">
            <button class="burger-icon" onclick="toggleBurgerMenu()" aria-label="Menu">☰</button>
            <div class="burger-dropdown" id="burgerDropdown">
                <div class="burger-item">
                    <a href="weekly.html">{bilingual_text('view_weekly_plan')}</a>
                </div>
                <div class="burger-item">
                    <a href="stats.html">{bilingual_text('view_stats')}</a>
                </div>
            </div>
        </div>
    </div>
    <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
    <h1>{bilingual_text('weekly_plan_title')}</h1>

    <button id="clearAllButton" class="clear-all-button" onclick="clearAllRecipes()">
        <span class="lang-de">Alle löschen</span>
        <span class="lang-en">Clear All</span>
    </button>

    <div id="weeklyPlanContainer"></div>

    <script>
        const recipeData = {recipe_lookup_json};

        function formatDate(timestamp) {{
            const date = new Date(timestamp);
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            return `${{day}}.${{month}}.${{year}}`;
        }}

        function loadWeeklyPlan() {{
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
            const planKey = 'weeklyMealPlan';
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem(planKey);
                if (stored) {{
                    plan = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading weekly plan:', e);
                return;
            }}

            // Find recipe by ID (or fallback to slug+addedAt for backwards compatibility)
            const recipe = plan.recipes.find(r => {{
                const id = String(r.id || `${{r.slug}}-${{r.addedAt}}`);
                return id === String(recipeId);
            }});

            if (recipe) {{
                recipe.cooked = !recipe.cooked;

                try {{
                    localStorage.setItem(planKey, JSON.stringify(plan));
                    loadWeeklyPlan();
                }} catch (e) {{
                    console.error('Error saving weekly plan:', e);
                }}
            }}
        }}

        function removeRecipe(recipeId) {{
            const planKey = 'weeklyMealPlan';
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem(planKey);
                if (stored) {{
                    plan = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading weekly plan:', e);
                return;
            }}

            // Find and remove recipe by ID (or fallback to slug+addedAt for backwards compatibility)
            const index = plan.recipes.findIndex(r => {{
                const id = String(r.id || `${{r.slug}}-${{r.addedAt}}`);
                return id === String(recipeId);
            }});

            if (index >= 0) {{
                plan.recipes.splice(index, 1);

                try {{
                    localStorage.setItem(planKey, JSON.stringify(plan));
                    loadWeeklyPlan();
                }} catch (e) {{
                    console.error('Error saving weekly plan:', e);
                }}
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

            const planKey = 'weeklyMealPlan';
            const emptyPlan = {{ recipes: [] }};

            try {{
                localStorage.setItem(planKey, JSON.stringify(emptyPlan));
                loadWeeklyPlan();
            }} catch (e) {{
                console.error('Error clearing weekly plan:', e);
            }}
        }}

        // Burger menu functionality
        function toggleBurgerMenu() {{
            const dropdown = document.getElementById('burgerDropdown');
            dropdown.classList.toggle('open');
        }}

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {{
            const menu = document.querySelector('.burger-menu');
            const dropdown = document.getElementById('burgerDropdown');
            if (!menu.contains(event.target) && dropdown.classList.contains('open')) {{
                dropdown.classList.remove('open');
            }}
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
        }});
    </script>
</body>
</html>'''

    return html
