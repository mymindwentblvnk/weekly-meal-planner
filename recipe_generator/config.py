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
    transition: box-shadow 0.2s;
}
.recipe-card:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.recipe-card h2 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #2d3748;
}
.recipe-card h2 a {
    color: #2c5282;
    text-decoration: none;
}
.recipe-card h2 a:hover {
    text-decoration: underline;
}
.description {
    color: #4a5568;
    line-height: 1.6;
    margin-bottom: 12px;
}
.meta {
    color: #718096;
    font-size: 0.9em;
    margin-bottom: 15px;
}
.view-recipe-btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: #2c5282;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s;
}
.view-recipe-btn:hover {
    background-color: #1e3a5f;
    text-decoration: none;
}
"""
