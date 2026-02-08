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
            <a href="shopping.html" class="nav-link" aria-label="Shopping List">🛒</a>
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
            <button class="weekly-plan-button-card" data-slug="{slug}" data-name="{escape(recipe['name'])}" data-category="{category}" data-servings="{servings}" onclick="toggleWeeklyPlanFromCard(this)">📅 Diese Woche kochen</button>
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
                    <label for="daySelect">{get_text('select_day')}</label>
                    <select id="daySelect" class="plan-select">
                        <option value="montag">{get_text('monday')}</option>
                        <option value="dienstag">{get_text('tuesday')}</option>
                        <option value="mittwoch">{get_text('wednesday')}</option>
                        <option value="donnerstag">{get_text('thursday')}</option>
                        <option value="freitag">{get_text('friday')}</option>
                        <option value="samstag">{get_text('saturday')}</option>
                        <option value="sonntag">{get_text('sunday')}</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="mealSelect">{get_text('select_meal')}</label>
                    <select id="mealSelect" class="plan-select">
                        <option value="breakfast">{get_text('breakfast')}</option>
                        <option value="lunch">{get_text('lunch')}</option>
                        <option value="dinner">{get_text('dinner')}</option>
                    </select>
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
            document.getElementById('daySelect').value = dayMap[today];

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

            const day = document.getElementById('daySelect').value;
            const meal = document.getElementById('mealSelect').value;
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

                // Increment counter
                incrementAddToPlanCounter(currentRecipeForPlan.name);

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
    """Generate week-based meal planner page.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)

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
    {generate_navigation(show_back_button=True)}
    <h1>{get_text('weekly_plan_title')}</h1>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{get_text('weekly_plan_disclaimer')}</p>

    <div class="week-navigation">
        <div class="week-nav-buttons">
            <button class="week-nav-btn" onclick="previousWeek()">{get_text('previous_week')}</button>
            <button class="week-nav-btn current-week-btn" onclick="goToCurrentWeek()">{get_text('current_week')}</button>
            <button class="week-nav-btn" onclick="nextWeek()">{get_text('next_week')}</button>
        </div>
        <div class="week-info" id="weekInfo"></div>
    </div>

    <div id="daysContainer" class="days-container"></div>

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

        // Week navigation
        function previousWeek() {{
            const dates = getWeekDates(currentWeek);
            const prevMonday = new Date(dates[0]);
            prevMonday.setDate(prevMonday.getDate() - 7);
            currentWeek = getISOWeek(prevMonday);
            renderWeek();
        }}

        function nextWeek() {{
            const dates = getWeekDates(currentWeek);
            const nextMonday = new Date(dates[0]);
            nextMonday.setDate(nextMonday.getDate() + 7);
            currentWeek = getISOWeek(nextMonday);
            renderWeek();
        }}

        function goToCurrentWeek() {{
            currentWeek = getISOWeek(new Date());
            renderWeek();
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

        // Render week view
        function renderWeek() {{
            const dates = getWeekDates(currentWeek);
            const dayNames = ['{get_text('monday')}', '{get_text('tuesday')}', '{get_text('wednesday')}', '{get_text('thursday')}', '{get_text('friday')}', '{get_text('saturday')}', '{get_text('sunday')}'];
            const mealTypes = ['breakfast', 'lunch', 'dinner'];
            const mealLabels = ['{get_text('breakfast')}', '{get_text('lunch')}', '{get_text('dinner')}'];

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
            renderWeek();
            initializeDarkMode();
        }});
    </script>
</body>
</html>'''

    return html


def generate_shopping_list_html(recipes_data: list[tuple[str, dict[str, Any]]]) -> str:
    """Generate shopping list page based on weekly meal plan.

    Args:
        recipes_data: List of tuples containing (filename, recipe_dict)

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
    {generate_navigation(show_back_button=True)}
    <h1>{get_text('shopping_list_title')}</h1>
    <p style="color: var(--text-tertiary); font-size: 0.9em; margin-bottom: 10px;">{get_text('shopping_list_subtitle')}</p>
    <p style="color: var(--text-tertiary); font-size: 0.9em; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: var(--bg-secondary); border-radius: 4px; border-left: 3px solid var(--primary-color);">{get_text('shopping_list_disclaimer')}</p>

    <div id="shoppingListContainer"></div>

    <script>
        const recipeData = {recipe_lookup_json};

        {generate_dark_mode_script()}

        // ============ Shopping List Functions ============

        // Get current week's meal plan (aggregated from mealPlansV2)
        function getLocalWeeklyPlan() {{
            // Get current week
            function getISOWeek(date) {{
                const d = new Date(date);
                d.setHours(0, 0, 0, 0);
                d.setDate(d.getDate() + 4 - (d.getDay() || 7));
                const yearStart = new Date(d.getFullYear(), 0, 1);
                const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
                return d.getFullYear() + '-W' + String(weekNo).padStart(2, '0');
            }}

            const currentWeek = getISOWeek(new Date());
            let plan = {{ recipes: [] }};

            try {{
                const stored = localStorage.getItem('mealPlansV2');
                if (stored) {{
                    const mealPlans = JSON.parse(stored);
                    const weekData = mealPlans[currentWeek] || {{}};

                    // Aggregate all meals from the week with servings
                    const meals = [];
                    Object.values(weekData).forEach(dayMeals => {{
                        Object.entries(dayMeals).forEach(([mealType, mealData]) => {{
                            // Skip 'todo' entries
                            if (mealType === 'todo' || !mealData) return;

                            // Support both old format (string) and new format (object)
                            if (typeof mealData === 'string') {{
                                meals.push({{ slug: mealData, servings: 2 }});
                            }} else if (mealData.slug) {{
                                meals.push({{ slug: mealData.slug, servings: mealData.servings || 2 }});
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

        // Get checked items from localStorage
        function getCheckedItems() {{
            const checkedKey = 'shoppingListChecked';
            let checked = {{}};

            try {{
                const stored = localStorage.getItem(checkedKey);
                if (stored) {{
                    checked = JSON.parse(stored);
                }}
            }} catch (e) {{
                console.error('Error reading checked items:', e);
            }}

            return checked;
        }}

        // Save checked items to localStorage
        function saveCheckedItems(checked) {{
            const checkedKey = 'shoppingListChecked';
            try {{
                localStorage.setItem(checkedKey, JSON.stringify(checked));
            }} catch (e) {{
                console.error('Error saving checked items:', e);
            }}
        }}

        // Update servings and sync back to weekly plan
        function updateServings(recipeSlug, newServings) {{
            newServings = Math.max(1, Math.min(20, parseInt(newServings) || 2));

            // Get current week's meal plan
            function getISOWeek(date) {{
                const d = new Date(date);
                d.setHours(0, 0, 0, 0);
                d.setDate(d.getDate() + 4 - (d.getDay() || 7));
                const yearStart = new Date(d.getFullYear(), 0, 1);
                const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
                return d.getFullYear() + '-W' + String(weekNo).padStart(2, '0');
            }}

            const currentWeek = getISOWeek(new Date());
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

            // Update localStorage
            let checked = getCheckedItems();
            checked[itemId] = isChecked;
            saveCheckedItems(checked);
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

        function loadShoppingList() {{
            let plan = getLocalWeeklyPlan();
            const container = document.getElementById('shoppingListContainer');

            if (plan.recipes.length === 0) {{
                container.innerHTML = `
                    <div class="no-shopping-items">
                        <h2>{get_text('no_shopping_list')}</h2>
                        <p>{get_text('no_shopping_list_message')}</p>
                    </div>
                `;
                // Clear all checked items when no recipes
                saveCheckedItems({{}});
                return;
            }}

            // Load checked state
            let checked = getCheckedItems();
            let currentItemIds = new Set();

            // Aggregate servings for duplicate recipes
            const recipeServingsMap = {{}};
            plan.recipes.forEach((recipe) => {{
                if (recipeServingsMap[recipe.slug]) {{
                    recipeServingsMap[recipe.slug] += recipe.servings || 2;
                }} else {{
                    recipeServingsMap[recipe.slug] = recipe.servings || 2;
                }}
            }});

            let html = '<div class="shopping-list-container">';

            Object.entries(recipeServingsMap).forEach(([slug, weeklyServings]) => {{
                const recipeInfo = recipeData[slug];
                if (!recipeInfo) return; // Skip if recipe not found

                const originalServings = recipeInfo.servings || 2;
                // Always use servings from weekly plan
                const targetServings = weeklyServings;

                html += `
                    <div class="recipe-shopping-section">
                        <div class="recipe-header">
                            <h2 class="recipe-title">${{recipeInfo.category}} ${{recipeInfo.name}}</h2>
                            <div class="servings-control">
                                <label for="servings-${{slug}}">{get_text('servings_label_short')}</label>
                                <div class="servings-buttons">
                                    <button
                                        class="servings-btn"
                                        onclick="decrementServings('${{slug}}', ${{targetServings}})"
                                        aria-label="Portionen verringern"
                                        ${{targetServings <= 1 ? 'disabled' : ''}}
                                    >−</button>
                                    <input
                                        type="number"
                                        id="servings-${{slug}}"
                                        class="servings-input"
                                        min="1"
                                        max="20"
                                        value="${{targetServings}}"
                                        onchange="updateServings('${{slug}}', this.value)"
                                        aria-label="Anzahl Portionen"
                                    >
                                    <button
                                        class="servings-btn"
                                        onclick="incrementServings('${{slug}}', ${{targetServings}})"
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
                        const itemId = `${{slug}}-${{index}}`;
                        currentItemIds.add(itemId);
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

            // Clean up checked items that are no longer in the list
            let cleanedChecked = {{}};
            for (let itemId of currentItemIds) {{
                if (checked[itemId]) {{
                    cleanedChecked[itemId] = true;
                }}
            }}
            saveCheckedItems(cleanedChecked);
        }}

        // Load shopping list on page load
        document.addEventListener('DOMContentLoaded', function() {{
            loadShoppingList();
            initializeDarkMode();

            // Listen for storage changes from other tabs (when weekly plan is modified)
            window.addEventListener('storage', function(e) {{
                if (e.key === 'weeklyMealPlan' || e.key === 'weeklyPlanNeedsSync') {{
                    loadShoppingList(); // Refresh shopping list
                }}
            }});
        }});
    </script>
</body>
</html>'''

    return html
