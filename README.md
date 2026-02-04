# bring-recipes-adder

🛒 This is a HTML website generator that lets you add your favourite recipes with one click to Bring! app.

**[🚀 Try the live app](https://mymindwentblvnk.github.io/bring-recipes-adder/)**

## Demo

<p align="center">
  <img src="media/demo.gif" alt="Demo" width="400">
</p>

## Features

- **YAML-based recipes**: Define recipes in simple YAML files organized by author
- **Bring! integration**: One-click ingredient import to your Bring! shopping list
- **Unified search**: Search by recipe name, tags, authors, or categories with autocomplete
- **Hierarchical tagging**: Smart tag system with both generic (fish, nuts) and specific (salmon, walnuts) tags
- **Weekly meal planner**: Plan your meals for the week with local storage sync
- **Recipe statistics**: Track and view your most-viewed recipes
- **Advanced filtering**: Multi-select search with support for tags, categories, authors, and recipe names
- **Auto-detection**: Categories, authors, and tags are automatically detected from recipe files
- **Quick recipes filter**: Find recipes that take 30 minutes or less
- **Dark mode**: Toggle between light and dark themes with automatic detection
- **Schema.org markup**: Properly structured recipe data for SEO and compatibility
- **Static site generation**: Generates clean HTML pages that can be hosted anywhere
- **Automatic deployment**: GitHub Actions workflow with tests deploys to GitHub Pages
- **German interface**: All UI text in German

## Local Development

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bring-recipes-adder.git
   cd bring-recipes-adder
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

5. Open `output/index.html` in your browser to view the recipe collection

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
  - eier
  - mehl

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
- Lowercase German words
- Sorted alphabetically
- Include BOTH generic category AND specific ingredient

**Hierarchical Tag Examples:**
```yaml
tags:
  - fisch           # Generic: fish
  - lachs           # Specific: salmon
  - käse            # Generic: cheese
  - feta            # Specific: feta
  - nüsse           # Generic: nuts
  - walnüsse        # Specific: walnuts
  - kerne           # Generic: seeds
  - chiasamen       # Specific: chia seeds
```

**Tag Hierarchies:**
- **Fish**: `fisch` + (`lachs` | `thunfisch` | `seelachs` | `garnelen`)
- **Meat**: `fleisch` + (`rind` | `pute` | `schinken` | `hackfleisch`)
- **Cheese**: `käse` + (`feta` | `schafskäse` | `parmesan` | `bergkäse` | `frischkäse`)
- **Nuts**: `nüsse` + (`walnüsse` | `haselnüsse` | `mandeln`)
- **Berries**: `beeren` + (`himbeeren` | `erdbeeren`)
- **Fruit**: `obst` + (`apfel` | `kiwi` | `weintrauben`)
- **Seeds**: `kerne` + (`chiasamen` | `leinsamen` | `sesam`)
- **Cabbage**: `kohl` + (`blumenkohl` | `brokkoli`)

**Important Rules:**
- ✓ Use both levels: "Wildlachsfilet" → `fisch` + `lachs`
- ✗ Don't go deeper: "Wildlachsfilet" → NOT `wildlachs`
- ✓ Always sort tags alphabetically
- ✓ Use singular German forms: "Äpfel" → `apfel`

This allows users to search broadly (all fish recipes) or specifically (only salmon recipes).

## GitHub Pages Deployment

The project includes a GitHub Actions workflow that automatically:
1. Runs unit tests with pytest
2. Generates HTML files from your YAML recipes (only if tests pass)
3. Deploys them to GitHub Pages

### Setup GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push changes to the `main` branch
4. Your recipes will be available at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

The workflow runs automatically on every push to `main`, or can be triggered manually from the Actions tab. Deployment will only occur if all tests pass.

## Search & Filtering

The overview page provides a powerful unified search with autocomplete:

### Unified Search
- **Recipe names** (🍽️): Search for specific recipes like "Fischpfanne" or "Gulasch"
- **Tags** (🏷️): Search by ingredients like "lachs", "käse", or "nüsse"
- **Authors** (👤): Filter by recipe creators (VitaMoment, HelloFresh, Chefkoch, etc.)
- **Categories** (📁): Filter by meal type (Brot, Fisch, Fleisch, Frühstück, etc.)

### Additional Filters
- **Fast recipes**: Checkbox to show only recipes that take 30 minutes or less
- **Multi-select**: Combine multiple search criteria (e.g., "lachs" + "frühstück" + VitaMoment)
- **Persistent state**: Filter selections are saved in local storage and restored on page reload

### How It Works
Start typing in the search box to see autocomplete suggestions. All searchable items are automatically detected from your recipe files - no configuration needed! Select any combination of recipe names, tags, authors, or categories to filter the recipe list.

## Weekly Meal Plan

The weekly meal plan feature allows you to organize recipes for the upcoming week:

- **Add recipes**: Click "📅 Diese Woche kochen" on any recipe detail page
- **Mark as cooked**: Track which meals you've already prepared
- **Local storage**: All data is stored in your browser's local storage
- **No sync**: Weekly plans are device-specific and not synced across browsers

## Project Structure

```
bring-recipes-adder/
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
