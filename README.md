# weekly-meal-planner

🗓️ A static HTML website generator for weekly meal planning with integrated shopping lists. Plan your meals for the week and generate ingredient lists automatically.

**[🚀 Try the live app](https://mymindwentblvnk.github.io/weekly-meal-planner/)** - Feel free to play around with all features! Search, filter, plan your weekly meals, and explore the interface. All changes are stored locally in your browser.

## Features

### Meal Planning
- **Weekly meal planner**: Plan breakfast, lunch, and dinner for each day of the week
- **Week navigation**: Browse and plan meals for current, past, and future weeks
- **Servings control**: Adjust servings for each meal individually
- **Daily notes**: Add TODO notes and reminders for each day
- **Local storage**: All meal plans are saved in your browser automatically
- **Smart cleanup**: Automatically removes meal plans older than 2 weeks to save space

### Shopping List
- **Automatic generation**: Shopping list is generated from your weekly meal plan
- **Two views**: Toggle between "Nach Rezept" (by recipe) and "Alphabetisch" (alphabetical)
- **Checkboxes**: Mark ingredients as purchased, synced across both views
- **Individual instances**: Recipes added multiple times appear separately with their own servings
- **Week-specific**: Each week has its own shopping list

### Recipe Management
- **YAML-based recipes**: Define recipes in simple YAML files organized by author
- **Unified search**: Search by recipe name, tags, authors, or categories with autocomplete
- **Hierarchical tagging**: Smart tag system with both generic (fish, nuts) and specific (salmon, walnuts) tags
- **Recipe catalog**: Browse all available recipes with advanced filtering
- **Quick recipes filter**: Find recipes that take 30 minutes or less
- **Schema.org markup**: Properly structured recipe data for SEO and compatibility

### User Interface
- **Dark mode**: Toggle between light and dark themes with automatic detection
- **German interface**: All UI text in German
- **Responsive design**: Works on desktop and mobile devices
- **Static site generation**: Generates clean HTML pages that can be hosted anywhere

### Deployment
- **Automatic deployment**: GitHub Actions workflow with tests deploys to GitHub Pages
- **100% test coverage**: Comprehensive test suite ensures reliability

## Local Development

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/weekly-meal-planner.git
   cd weekly-meal-planner
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Add your recipes to the `recipes/` folder organized by author (e.g., `recipes/YourName/recipe.yaml`)

4. Generate HTML files:
   ```bash
   uv run python main.py
   ```

5. Open `output/index.html` in your browser to view the meal planner

### Running Tests

The project includes comprehensive unit tests with 100% code coverage.

Run the tests:
```bash
uv run pytest
```

Run tests with coverage report:
```bash
uv run pytest --cov=recipe_generator --cov-report=term-missing
```

The test suite includes:
- Recipe validation tests
- HTML generation tests
- Configuration tests

Tests are automatically run on every push via GitHub Actions.

### Development Commands

The project includes Claude Code commands for managing recipe metadata:

- **`/fill-metadata`**: Comprehensive metadata validation and improvement
  - Fills missing descriptions
  - Adds missing tags
  - Validates hierarchical tag completeness
  - Ensures all required fields are present
  - Auto-regenerates HTML and commits changes

- **`/fill-descriptions`**: Generate descriptions for recipes without them
- **`/fill-tags`**: Add tags to recipes that don't have them

Use these commands to maintain high-quality recipe metadata across all files.

## Recipe Format

Recipes are organized by author in subdirectories under `recipes/`. For example:
```
recipes/
├── VitaMoment/
│   └── recipe1.yaml
├── HelloFresh/
│   └── recipe2.yaml
└── YourName/
    └── recipe3.yaml
```

Create YAML files with the following structure:

```yaml
name: Simple Pasta Dough
description: A basic pasta dough recipe with just three ingredients.
author: Your Name
category: 🍞  # See allowed categories below
servings: 4
prep_time: 15  # minutes
cook_time: 0   # minutes
tags:
  - Eier
  - Mehl

ingredients:
  - name: flour
    amount: 500g
  - name: eggs
    amount: 2
  - name: salt
    amount: 1 spoon

instructions:
  - Mix flour and salt in a large bowl.
  - Create a well in the center and add the eggs.
  - Mix until a dough forms, then knead for 10 minutes.
  - Rest for 30 minutes before rolling out.
```

### Categories

Categories are automatically detected from your recipe files. Use emoji icons to categorize your recipes. Common categories include:

- `🍞` - Bread & Baked Goods (Brot)
- `🥩` - Meat Dishes (Fleisch)
- `🐟` - Fish & Seafood (Fisch)
- `🥦` - Vegetable Dishes (Vegetarisch)
- `🥣` - Breakfast (Frühstück)

You can use any emoji as a category - it will automatically appear in the filter dropdown. Known categories will display with German labels, while new categories will show just the emoji.

### Tags

Tags enable powerful ingredient-based search and filtering. The system uses a **hierarchical tagging structure** with both generic and specific tags:

**Tag Format:**
- Capitalized German words (start with uppercase letter)
- Sorted alphabetically
- Include BOTH generic category AND specific ingredient

**Hierarchical Tag Examples:**
```yaml
tags:
  - Fisch           # Generic: fish
  - Lachs           # Specific: salmon
  - Käse            # Generic: cheese
  - Feta            # Specific: feta
  - Nüsse           # Generic: nuts
  - Walnüsse        # Specific: walnuts
  - Kerne           # Generic: seeds
  - Chiasamen       # Specific: chia seeds
```

**Tag Hierarchies:**
- **Fish**: `Fisch` + (`Lachs` | `Thunfisch` | `Seelachs` | `Garnelen`)
- **Meat**: `Fleisch` + (`Rind` | `Pute` | `Schinken` | `Hackfleisch`)
- **Cheese**: `Käse` + (`Feta` | `Schafskäse` | `Parmesan` | `Bergkäse` | `Frischkäse`)
- **Nuts**: `Nüsse` + (`Walnüsse` | `Haselnüsse` | `Mandeln`)
- **Berries**: `Beeren` + (`Himbeeren` | `Erdbeeren`)
- **Fruit**: `Obst` + (`Apfel` | `Kiwi` | `Weintrauben`)
- **Seeds**: `Kerne` + (`Chiasamen` | `Leinsamen` | `Sesam`)
- **Cabbage**: `Kohl` + (`Blumenkohl` | `Brokkoli`)

**Important Rules:**
- ✓ Use both levels: "Wildlachsfilet" → `Fisch` + `Lachs`
- ✗ Don't go deeper: "Wildlachsfilet" → NOT `Wildlachs`
- ✓ Always sort tags alphabetically
- ✓ Use singular German forms: "Äpfel" → `Apfel`

This allows users to search broadly (all fish recipes) or specifically (only salmon recipes).

## How to Use

### Planning Your Week

1. Open the **Wochenplan** (weekly plan) page
2. Navigate to the desired week using the week navigation buttons
3. For each day and meal slot, click **Rezept zuweisen** to search and select a recipe
4. Adjust servings for each meal using the +/- buttons
5. Add notes or reminders in the **Notizen & TODOs** section for each day

### Creating Shopping Lists

1. Your shopping list is automatically generated from your weekly meal plan
2. Open the **Einkaufsliste** (shopping list) page
3. Switch between weeks using the week navigation
4. Toggle between **Nach Rezept** (grouped by recipe) and **Alphabetisch** (sorted alphabetically)
5. Check off ingredients as you shop - checkmarks are synced across both views
6. Adjust servings for individual recipe instances if needed

### Browsing Recipes

1. Open the **Rezeptkatalog** (recipe catalog) page
2. Use the search box to find recipes by name, ingredient, author, or category
3. Filter by quick recipes (≤30 minutes) using the checkbox
4. Click on any recipe to view details and add it to your weekly plan

## GitHub Pages Deployment

The project includes a GitHub Actions workflow that automatically:
1. Runs unit tests with pytest
2. Generates HTML files from your YAML recipes (only if tests pass)
3. Deploys them to GitHub Pages

### Setup GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push changes to the `main` branch
4. Your meal planner will be available at: `https://YOUR_USERNAME.github.io/weekly-meal-planner/`

The workflow runs automatically on every push to `main`, or can be triggered manually from the Actions tab. Deployment will only occur if all tests pass.

## Data Storage

All meal plans, shopping list checkmarks, and preferences are stored locally in your browser using localStorage:

- **Meal plans**: Stored for current week ± 2 weeks (5 weeks total)
- **Shopping list checkmarks**: Tracked per ingredient instance
- **Dark mode preference**: Remembered across sessions
- **Old data cleanup**: Automatically removes data older than 2 weeks

**Note**: Data is device-specific and not synced across browsers or devices.

## Project Structure

```
weekly-meal-planner/
├── main.py                      # Entry point
├── recipe_generator/            # Core package
│   ├── __init__.py             # Package exports
│   ├── config.py               # Configuration & CSS
│   ├── html_generator.py       # HTML generation
│   └── validators.py           # Recipe validation
├── tests/                       # Unit tests
│   ├── test_config.py
│   ├── test_html_generator.py
│   └── test_validators.py
├── recipes/                     # YAML recipe files organized by author
│   ├── VitaMoment/
│   │   └── *.yaml
│   ├── HelloFresh/
│   │   └── *.yaml
│   └── Chefkoch/
│       └── *.yaml
├── output/                      # Generated HTML (gitignored)
├── .claude/                     # Claude Code commands
│   └── commands/
│       ├── fill-metadata.md    # Comprehensive metadata validation
│       ├── fill-descriptions.md # Generate descriptions
│       └── fill-tags.md        # Hierarchical tagging rules
├── .github/workflows/
│   ├── deploy.yml              # Deploy to GitHub Pages
│   └── test.yml                # Run tests on push
└── pyproject.toml              # Python dependencies
```

## License

This project is open source and available under the MIT License.
