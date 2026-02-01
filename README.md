# bring-recipes-adder

🛒 This is a HTML website generator that lets you add your favourite recipes with one click to Bring! app.

## Features

- **YAML-based recipes**: Define recipes in simple YAML files
- **Bring! integration**: One-click ingredient import to your Bring! shopping list
- **Schema.org markup**: Properly structured recipe data for SEO and compatibility
- **Static site generation**: Generates clean HTML pages that can be hosted anywhere
- **Automatic deployment**: GitHub Actions workflow deploys to GitHub Pages

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

3. Add your recipes to the `recipes/` folder (see recipe format below)

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

## Recipe Format

Create YAML files in the `recipes/` directory with the following structure:

```yaml
name: Simple Pasta Dough
description: A basic pasta dough recipe with just three ingredients.
author: Your Name
category: 🍞  # See allowed categories below
servings: 4
prep_time: 15  # minutes
cook_time: 0   # minutes

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

### Allowed Categories

Use one of the following emoji categories for your recipe:

- `🍞` - Bread & Baked Goods
- `🥩` - Meat Dishes
- `🐟` - Fish & Seafood
- `🥦` - Vegetable Dishes
- `🥣` - Sweet Breakfast (Porridge, etc.)

## GitHub Pages Deployment

The project includes a GitHub Actions workflow that automatically:
1. Generates HTML files from your YAML recipes
2. Deploys them to GitHub Pages

### Setup GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Push changes to the `main` branch
4. Your recipes will be available at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

The workflow runs automatically on every push to `main`, or can be triggered manually from the Actions tab.

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
├── recipes/                     # YAML recipe files
│   └── *.yaml
├── output/                      # Generated HTML (gitignored)
├── .github/workflows/
│   ├── deploy.yml              # Deploy to GitHub Pages
│   └── test.yml                # Run tests on push
└── pyproject.toml              # Python dependencies
```

## License

This project is open source and available under the MIT License.
