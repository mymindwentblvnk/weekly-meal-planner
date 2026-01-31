"""Configuration and constants for the recipe generator."""

from pathlib import Path


# Directory configuration
RECIPES_DIR = Path("recipes")
OUTPUT_DIR = Path("output")

# CSS Styles
COMMON_CSS = """
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
"""

DETAIL_PAGE_CSS = """
.amount {
    font-weight: bold;
    min-width: 80px;
    display: inline-block;
    color: #2c5282;
}
.ingredient {
    color: #333;
}
ul {
    list-style-type: none;
    padding-left: 0;
}
li {
    padding: 5px 0;
}
"""

OVERVIEW_PAGE_CSS = """
h1 {
    color: #2c5282;
}
.recipe-card {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #f7fafc;
}
.recipe-card h2 {
    margin-top: 0;
    color: #2d3748;
}
.recipe-card a {
    color: #2c5282;
    text-decoration: none;
}
.recipe-card a:hover {
    text-decoration: underline;
}
.ingredients {
    color: #4a5568;
    line-height: 1.6;
}
"""
