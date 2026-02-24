# Claude's Learnings: Recipe Generator Project

This document captures key insights, patterns, and lessons learned during the development of the bring-recipes-adder project.

## Project Overview

Built a static site generator that transforms YAML recipe files into HTML pages with integrated Bring! shopping list widgets, enabling one-click ingredient import to the Bring! mobile app.

## Technical Learnings

### 1. Bring! Widget Integration

**Key Discovery**: The Bring! widget uses Schema.org Recipe microdata for parsing ingredients.

- **Widget Script**: `//platform.getbring.com/widgets/import.js`
- **Activation**: Add `data-bring-import` attribute to a container div
- **Data Source**: Can point to a URL or parse the current page
- **Critical**: Requires proper Schema.org markup with `itemscope`, `itemprop` attributes

**Best Practice**: For overview pages, we initially tried using `data-bring-import="recipe.html"` to point to detail pages, but this proved unreliable. The cleaner approach is to only include the widget on detail pages where users can interact with it directly.

### 2. Schema.org Structured Data

**Learned Pattern**: Use microdata format (not JSON-LD) for maximum compatibility:

```html
<div itemscope itemtype="https://schema.org/Recipe">
  <h1 itemprop="name">Recipe Name</h1>
  <meta itemprop="recipeIngredient" content="500g flour">
  <time itemprop="prepTime" datetime="PT15M">15 minutes</time>
</div>
```

**Important**:
- Times must be in ISO 8601 duration format: `PT{minutes}M`
- Ingredients need both amount and name in a single string
- Can use `<meta>` tags for machine-readable data

### 3. Code Organization Evolution

**Journey**: Single file → Refactored modules → Package structure

**Final Structure**:
```
main.py                    # Entry point (orchestration only)
recipe_generator/          # Package
  ├── config.py           # Constants & CSS
  ├── validators.py       # Input validation
  ├── html_generator.py   # HTML generation logic
  └── __init__.py         # Public API
```

**Why This Matters**:
- Separation of concerns
- Easier testing
- Reusable components
- Clean imports via `__init__.py`

### 4. Security: HTML Escaping

**Critical Learning**: Always escape user-provided content to prevent XSS.

```python
from html import escape

# Good
f"<h1>{escape(recipe['name'])}</h1>"

# Bad (vulnerable to XSS)
f"<h1>{recipe['name']}</h1>"
```

**Applied to**: Recipe names, descriptions, ingredients, instructions, filenames

### 5. GitHub Actions for Static Sites

**Pattern Learned**: Modern GitHub Pages deployment flow

```yaml
jobs:
  build:
    - Checkout code
    - Setup environment (Python + uv)
    - Generate static files
    - Upload artifact

  deploy:
    - Deploy artifact to GitHub Pages
```

**Key Points**:
- Use `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4`
- Requires proper permissions: `pages: write`, `id-token: write`
- Must enable GitHub Actions as source in repo settings
- Use relative paths for project sites (not absolute paths)

### 6. GitHub Pages URL Patterns

**Learned the Hard Way**: Project sites include repo name in URL.

- **User/Org site**: `username.github.io/` → use absolute paths `/path/`
- **Project site**: `username.github.io/repo-name/` → use relative paths `path/`

**Fix Applied**: Changed redirects from `/bring/` to `bring/` (relative)

### 7. Progressive Enhancement

**Evolution of Overview Page**:
1. **v1**: Full Schema.org + Bring! widget per recipe (too heavy)
2. **v2**: Schema.org metadata + widget (still cluttered)
3. **v3**: Clean cards with description, link to detail page (final)

**Lesson**: Not every page needs every feature. The overview should preview, the detail page should provide full functionality.

### 8. Python Packaging Best Practices

**Pattern**: Create a proper package structure even for small projects

```python
# recipe_generator/__init__.py
from .config import RECIPES_DIR, OUTPUT_DIR
from .validators import validate_recipe
from .html_generator import generate_recipe_detail_html

__all__ = [...]  # Explicit exports
```

**Benefits**:
- Clear public API
- Easy imports: `from recipe_generator import validate_recipe`
- Professional structure
- Extensible design

### 9. Validation First, Generate Second

**Pattern**: Validate YAML structure before attempting to generate HTML

```python
try:
    recipe = yaml.safe_load(f)
    validate_recipe(recipe, filename)  # Fail fast
    html = generate_html(recipe)
except ValueError as e:
    # Clear error message
    print(f"Validation error: {e}")
```

**Validation Checks**:
- Required fields exist
- Correct data types (int for servings, list for ingredients)
- Nested structure (ingredients have name + amount)
- Reasonable values (servings > 0)

### 10. CSS Organization

**Pattern**: Extract CSS constants for reusability

```python
COMMON_CSS = "..."      # Shared across all pages
DETAIL_PAGE_CSS = "..." # Detail page specific
OVERVIEW_PAGE_CSS = "..." # Overview specific
```

**Benefits**:
- Single source of truth
- Easy to modify styles
- No duplication
- Can be moved to external files later

## Design Decisions

### Why YAML Over JSON?
- More human-readable
- Supports comments
- Less syntax (no quotes needed for strings)
- Better for non-technical users

### Why Static Generation Over Dynamic?
- No backend required
- Fast page loads
- Easy to host (GitHub Pages, Netlify, etc.)
- Works offline once loaded
- Simple deployment

### Why Microdata Over JSON-LD?
- Inline with HTML (easier to maintain)
- Better tool support (especially for Bring!)
- More explicit relationship between markup and data

## Design Targets

### Mobile vs Desktop Design

**Important**: This project maintains **two separate design targets**:

1. **Mobile Design**: Optimized for mobile devices and small screens
2. **Desktop Design**: Optimized for desktop browsers and large screens

**When implementing design changes**:
- If the user requests a design change and it's **not clear** whether it applies to:
  - Mobile only
  - Desktop only
  - Both platforms
- **Always ask for clarification** before implementing

**Examples**:
- "Should this change apply to mobile, desktop, or both?"
- "I can implement this for [mobile/desktop/both]. Which would you prefer?"

This ensures design changes are intentional and platform-appropriate, preventing unintended breakage of responsive layouts.

## Gotchas & Solutions

### Problem: `escape()` doesn't work on integers
```python
# Error: 'int' object has no attribute 'replace'
escape(ingredient['amount'])

# Solution: Convert to string first
escape(str(ingredient['amount']))
```

### Problem: 404 on GitHub Pages
**Cause**: Absolute paths in project site URLs
**Solution**: Use relative paths or construct full URLs with base path

### Problem: Widget not working on overview
**Cause**: Widget parsing external URLs is unreliable
**Solution**: Remove widget from overview, only show on detail pages

## Future Enhancements Considered

1. **Recipe images**: Add optional image field to YAML
2. **Categories/tags**: Filter recipes by type (dessert, main, etc.)
3. **Search functionality**: Client-side search with JavaScript
4. **Print styling**: CSS for printer-friendly recipe pages
5. **Nutrition info**: Optional Schema.org nutrition data
6. **Multiple languages**: i18n support for recipe text
7. **Theme customization**: User-configurable color schemes

## Development Workflow

### Running Tests

The project uses pytest for testing. Always run tests after making changes to ensure nothing breaks.

**Command**:
```bash
source .venv/bin/activate && pytest tests/ -v
```

**Important Notes**:
- Must activate virtual environment first (`.venv`)
- Tests located in `tests/` directory
- Use `-v` flag for verbose output showing all test names
- All tests should pass before committing

**Test Coverage**:
- `test_config.py`: Configuration validation
- `test_html_generator.py`: HTML generation, formatting, escaping
- `test_validators.py`: Recipe YAML validation

### Pre-Commit Rules

**ALWAYS run `/fill-descriptions` before committing**
- This ensures all recipe descriptions are filled in before code is committed
- Prevents recipes with "tbd." descriptions from being deployed
- Should be run as the last step before any git commit

## Key Takeaways

1. **Start simple, refactor when needed**: Single file → modules → package
2. **Validate early**: Catch errors before generation
3. **Security matters**: Always escape user content
4. **Read the docs**: Bring! widget docs showed the Schema.org requirement
5. **Iterate based on feedback**: Overview page went through 3 iterations
6. **Test deployment early**: URL structure issues appear only after deploy
7. **Document as you go**: This file captures what would otherwise be lost

## Tools & Technologies Used

- **Python 3.13**: Latest stable Python
- **uv**: Fast Python package manager
- **PyYAML**: YAML parsing
- **GitHub Actions**: CI/CD pipeline
- **GitHub Pages**: Static hosting
- **Schema.org**: Structured data markup
- **Bring! Widget**: Third-party integration

---

*Generated during the development of bring-recipes-adder with Claude Code*
*Date: January 2025*
