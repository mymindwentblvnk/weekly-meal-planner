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

        // Track cumulative "add to plan" clicks
        function incrementAddToPlanCounter(recipeName) {{
            const counterKey = 'recipeAddToPlanCount';
            let counts = {{}};

            try {{
                const stored = localStorage.getItem(counterKey);
                if (stored) {{
                    counts = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading add-to-plan counts:', e);
            }}

            // Increment counter for this recipe
            counts[recipeName] = (counts[recipeName] || 0) + 1;

            // Save back to localStorage
            try {{
                localStorage.setItem(counterKey, JSON.stringify(counts));
            }} catch (e) {{
                console.error('Error saving add-to-plan counts:', e);
            }}
        }}

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

            // Increment add-to-plan counter
            incrementAddToPlanCounter(recipeData.name);

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
            <button class="weekly-plan-button-card" data-slug="{slug}" data-name="{escape(recipe['name'])}" data-category="{category}" onclick="toggleWeeklyPlanFromCard(this)">📅 Diese Woche kochen</button>
        </div>
    </div>'''
        recipe_entries.append(recipe_entry)

    # Generate footer with deployment time
    footer_html = ""
    if deployment_time:
        formatted_time = deployment_time.strftime("%d. %B %Y um %H:%M %Z")
        footer_html = f'''
    <footer class="deployment-info">
        <p>{get_text('last_updated')} {formatted_time}</p>
    </footer>'''

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

    html = f'''{generate_page_header(get_text('overview_title'), OVERVIEW_PAGE_CSS)}
    <div class="page-header">
        <h1>{get_text('overview_title')}</h1>
        {generate_navigation(show_back_button=False)}
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
{footer_html}

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
        function incrementAddToPlanCounter(recipeName) {{
            const counterKey = 'recipeAddToPlanCount';
            let counts = {{}};

            try {{
                const stored = localStorage.getItem(counterKey);
                if (stored) {{
                    counts = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading add-to-plan counts:', e);
            }}

            // Increment counter for this recipe
            counts[recipeName] = (counts[recipeName] || 0) + 1;

            // Save back to localStorage
            try {{
                localStorage.setItem(counterKey, JSON.stringify(counts));
            }} catch (e) {{
                console.error('Error saving add-to-plan counts:', e);
            }}
        }}

        // Weekly plan functionality for overview page
        function toggleWeeklyPlanFromCard(button) {{
            const slug = button.dataset.slug;
            const name = button.dataset.name;
            const category = button.dataset.category;
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
                id: String(Date.now() + Math.random()),
                name: name,
                slug: slug,
                category: category,
                addedAt: Date.now(),
                cooked: false
            }});

            // Update lastModified timestamp
            plan.lastModified = Date.now();

            // Increment add-to-plan counter
            incrementAddToPlanCounter(name);

            // Save back to localStorage
            try {{
                localStorage.setItem(planKey, JSON.stringify(plan));
                updateAllWeeklyPlanButtons();

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

        function updateAllWeeklyPlanButtons() {{
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

            document.querySelectorAll('.weekly-plan-button-card').forEach(button => {{
                const slug = button.dataset.slug;
                const count = plan.recipes.filter(r => r.slug === slug).length;

                if (count > 0) {{
                    button.classList.add('in-plan');
                    const countText = count > 1 ? ` (${{count}}×)` : '';
                    button.textContent = `✓ In Wochenplan${{countText}}`;
                }} else {{
                    button.classList.remove('in-plan');
                    button.textContent = '📅 Diese Woche kochen';
                }}
            }});
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
    recipe_lookup_by_name = {recipe['name']: (filename, recipe) for filename, recipe in recipes_data}

    # Stats-specific CSS
    stats_css = '''.stats-list {
            list-style: none;
            padding: 0;
            margin: 20px 0;
        }
        .stats-item {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            transition: box-shadow 0.2s;
        }
        .stats-item:hover {
            box-shadow: 0 4px 6px var(--shadow);
        }
        .rank {
            font-size: 2em;
            font-weight: bold;
            color: var(--primary-color);
            min-width: 60px;
            text-align: center;
        }
        .recipe-info {
            flex: 1;
            margin-left: 20px;
        }
        .recipe-info h3 {
            margin: 0 0 5px 0;
            color: var(--text-color);
        }
        .recipe-info a {
            color: var(--primary-color);
            text-decoration: none;
            font-size: 1.2em;
        }
        .recipe-info a:hover {
            text-decoration: underline;
        }
        .view-count {
            font-size: 0.9em;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-style: italic;
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

        /* Mobile optimizations */
        @media (max-width: 600px) {
            .stats-item {
                padding: 15px 10px;
                gap: 10px;
            }
            .rank {
                font-size: 1.3em;
                min-width: 40px;
            }
            .recipe-info {
                margin-left: 10px;
            }
            .recipe-info a {
                font-size: 1em;
                line-height: 1.3;
            }
            .view-count {
                font-size: 0.85em;
            }
        }'''

    html = f'''{generate_page_header(get_text('stats_title'), OVERVIEW_PAGE_CSS, stats_css)}
    {generate_navigation(show_back_button=True)}
    <h1>{get_text('stats_title')}</h1>
    <p style="color: var(--text-secondary); margin-bottom: 15px;">{get_text('stats_subtitle')}</p>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{get_text('stats_disclaimer')}</p>

    <div id="stats-container">
        <p class="no-data">{get_text('stats_no_data')}</p>
    </div>

    <script>
        const recipeData = {{{','.join(f'"{recipe["name"]}": {{"filename": "{filename}", "category": "{recipe.get("category", "")}"}}' for filename, recipe in recipes_data)}}};

        function displayStats() {{
            const counterKey = 'recipeAddToPlanCount';
            let counts = {{}};

            try {{
                const stored = localStorage.getItem(counterKey);
                if (stored) {{
                    counts = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading add-to-plan counts:', e);
            }}

            // Filter to only include recipes that exist
            const validCounts = {{}};
            for (const [name, count] of Object.entries(counts)) {{
                if (recipeData[name]) {{
                    validCounts[name] = count;
                }}
            }}

            // Sort by count and take top 10
            const sortedRecipes = Object.entries(validCounts)
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
                            <div class="view-count">${{count}} {get_text("stats_count")}</div>
                        </div>
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
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{get_text('weekly_plan_disclaimer')}</p>

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
