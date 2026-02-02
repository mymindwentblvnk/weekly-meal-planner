# bring-recipes-adder

🛒 This is a HTML website generator that lets you add your favourite recipes with one click to Bring! app.

**[🚀 Try the live app](https://mymindwentblvnk.github.io/bring-recipes-adder/)**

## Demo

<p align="center">
  <img src="media/demo.gif" alt="Demo" width="400">
</p>

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
- `🥣` - Breakfast (Porridge, etc.)

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

## Google Drive Sync for Weekly Meal Plan

The weekly meal plan feature includes optional Google Drive synchronization, allowing you to sync your meal plans across multiple devices using your personal Google account.

### Features

- **Cross-device sync**: Access your weekly plan from any device
- **Automatic syncing**: Changes sync automatically in the background
- **Offline support**: Works offline, syncs when back online
- **Private storage**: Data stored in your Google Drive's private app data folder
- **No backend required**: All sync happens client-side using Google Drive API

### Setup Google Drive Sync (One-time)

To enable Google Drive sync for your deployment, you need to create OAuth credentials:

#### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the **Google Drive API**:
   - Go to **APIs & Services** → **Library**
   - Search for "Google Drive API"
   - Click **Enable**

#### 2. Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: Your recipe collection name
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: No additional scopes needed (only `drive.appdata` is used)
   - Test users: Add your Google account email
4. Create OAuth client ID:
   - Application type: **Web application**
   - Name: "Recipe Collection - Web"
   - Authorized JavaScript origins:
     - `http://localhost:8000` (for local testing)
     - `https://YOUR_USERNAME.github.io` (for production)
   - Authorized redirect URIs: Leave empty (popup flow doesn't need this)
5. Click **Create** and copy the **Client ID**

#### 3. Configure Client ID in Code

Open `recipe_generator/config.py` and replace the placeholder with your Client ID:

```python
GOOGLE_DRIVE_CLIENT_ID = "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com"
```

#### 4. Deploy

Commit and push your changes:

```bash
git add recipe_generator/config.py
git commit -m "Add Google Drive OAuth Client ID"
git push
```

The GitHub Actions workflow will deploy the updated site with Google Drive sync enabled.

### Using Google Drive Sync

1. Visit your weekly plan page (`weekly.html`)
2. Click the **🔒** button in the top navigation
3. Sign in with your Google account
4. Grant permission to access app data
5. Your weekly plan will automatically sync across all devices where you sign in

### Data Privacy

- Your recipe data is stored in Google Drive's **app data folder** (hidden from your regular Drive files)
- The app can only access its own data, not your other Drive files
- Data is automatically deleted if you revoke app access
- All data transmission is encrypted (HTTPS)
- No data is sent to any third-party servers

### Troubleshooting

**"Sign in" button doesn't appear:**
- Check that `GOOGLE_DRIVE_CLIENT_ID` is set correctly in `config.py`
- Verify the site is deployed and accessible
- Check browser console for errors

**Sync not working:**
- Ensure you're signed in (email shown in top navigation)
- Check your internet connection
- Try signing out and back in
- Check that the authorized JavaScript origins in Google Cloud Console match your site URL

**"Access blocked" error when signing in:**
- Your app is in testing mode - add your Google account as a test user in the OAuth consent screen
- Or publish your app (requires verification for production use)

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
