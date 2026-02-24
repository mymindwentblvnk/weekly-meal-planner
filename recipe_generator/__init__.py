"""Recipe generator package for creating HTML pages from YAML recipes."""

from .config import RECIPES_DIR, OUTPUT_DIR
from .validators import validate_recipe
from .html_generator import (
    generate_recipe_detail_html,
    generate_overview_html,
    generate_weekly_html,
    generate_shopping_list_html,
    generate_settings_page_html,
)

__all__ = [
    'RECIPES_DIR',
    'OUTPUT_DIR',
    'validate_recipe',
    'generate_recipe_detail_html',
    'generate_overview_html',
    'generate_weekly_html',
    'generate_shopping_list_html',
    'generate_settings_page_html',
]
