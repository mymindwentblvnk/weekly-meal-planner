"""HTML generation functions for recipes."""

from typing import Any
from html import escape
from datetime import datetime

from .config import COMMON_CSS, DETAIL_PAGE_CSS, OVERVIEW_PAGE_CSS, get_text, TEXTS


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


def generate_recipe_detail_html(recipe: dict[str, Any]) -> str:
    """Generate HTML with Schema.org microdata and Bring! widget from recipe data.

    Args:
        recipe: Recipe dictionary containing name, ingredients, instructions, etc.

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
    <button class="language-toggle" onclick="toggleLanguage()">
        <span class="lang-de">🇬🇧 English</span>
        <span class="lang-en">🇩🇪 Deutsch</span>
    </button>
    <button class="dark-mode-toggle" onclick="toggleDarkMode()">
        <span class="light-mode-indicator">🌙</span>
        <span class="dark-mode-indicator">☀️</span>
    </button>
    <a href="index.html" class="back-button">{bilingual_text('back_to_recipes')}</a>
    <div itemscope itemtype="https://schema.org/Recipe">
        <h1 itemprop="name">{category} {escape(recipe['name'])}</h1>

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
            const lightIndicator = document.querySelector('.light-mode-indicator');
            const darkIndicator = document.querySelector('.dark-mode-indicator');
            if (isDark) {{
                lightIndicator.style.display = 'none';
                darkIndicator.style.display = 'inline';
            }} else {{
                lightIndicator.style.display = 'inline';
                darkIndicator.style.display = 'none';
            }}
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
    category_order = {'🥩': 0, '🐟': 1, '🥦': 2, '🥣': 3}
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
        <h2><a href="{escape(filename)}">{category} {escape(recipe['name'])}</a></h2>
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
    <button class="language-toggle" onclick="toggleLanguage()">
        <span class="lang-de">🇬🇧 English</span>
        <span class="lang-en">🇩🇪 Deutsch</span>
    </button>
    <button class="dark-mode-toggle" onclick="toggleDarkMode()">
        <span class="light-mode-indicator">🌙</span>
        <span class="dark-mode-indicator">☀️</span>
    </button>
    <h1>{bilingual_text('overview_title')}</h1>

    <div class="filter-buttons">
        <button class="filter-btn active" data-filter="all">{bilingual_text('filter_all')}</button>
        <button class="filter-btn" data-filter="🥩">🥩 {bilingual_text('filter_meat')}</button>
        <button class="filter-btn" data-filter="🐟">🐟 {bilingual_text('filter_fish')}</button>
        <button class="filter-btn" data-filter="🥦">🥦 {bilingual_text('filter_vegetarian')}</button>
        <button class="filter-btn" data-filter="🥣">🥣 {bilingual_text('filter_sweet')}</button>
        <button class="filter-btn" data-filter="fast">⚡ {bilingual_text('filter_fast')}</button>
    </div>

{chr(10).join(recipe_entries)}{footer_html}

    <script>
        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        const recipeCards = document.querySelectorAll('.recipe-card');

        function applyFilter(filterValue) {{
            // Update active button
            filterButtons.forEach(btn => {{
                if (btn.dataset.filter === filterValue) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});

            // Filter recipes
            recipeCards.forEach(card => {{
                if (filterValue === 'all') {{
                    card.classList.remove('hidden');
                }} else if (filterValue === 'fast') {{
                    // Filter by time
                    if (card.dataset.time === 'fast') {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }} else {{
                    // Filter by category
                    if (card.dataset.category === filterValue) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }}
            }});
        }}

        filterButtons.forEach(button => {{
            button.addEventListener('click', () => {{
                const filterValue = button.dataset.filter;
                localStorage.setItem('recipeFilter', filterValue);
                applyFilter(filterValue);
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
            const lightIndicator = document.querySelector('.light-mode-indicator');
            const darkIndicator = document.querySelector('.dark-mode-indicator');
            if (isDark) {{
                lightIndicator.style.display = 'none';
                darkIndicator.style.display = 'inline';
            }} else {{
                lightIndicator.style.display = 'inline';
                darkIndicator.style.display = 'none';
            }}
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

            // Apply saved filter
            const savedFilter = localStorage.getItem('recipeFilter') || 'all';
            applyFilter(savedFilter);
        }});
    </script>
</body>
</html>'''

    return html
