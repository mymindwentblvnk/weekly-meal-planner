"""Tests for configuration module."""

from pathlib import Path
from recipe_generator.config import (
    RECIPES_DIR,
    OUTPUT_DIR,
    COMMON_CSS,
    DETAIL_PAGE_CSS,
    OVERVIEW_PAGE_CSS,
)


class TestConfiguration:
    """Test cases for configuration constants."""

    def test_recipes_dir_is_path(self):
        """Test that RECIPES_DIR is a Path object."""
        assert isinstance(RECIPES_DIR, Path)
        assert str(RECIPES_DIR) == "recipes"

    def test_output_dir_is_path(self):
        """Test that OUTPUT_DIR is a Path object."""
        assert isinstance(OUTPUT_DIR, Path)
        assert str(OUTPUT_DIR) == "output"

    def test_common_css_is_string(self):
        """Test that COMMON_CSS is a non-empty string."""
        assert isinstance(COMMON_CSS, str)
        assert len(COMMON_CSS) > 0
        assert 'font-family' in COMMON_CSS
        assert 'body' in COMMON_CSS

    def test_detail_page_css_is_string(self):
        """Test that DETAIL_PAGE_CSS is a non-empty string."""
        assert isinstance(DETAIL_PAGE_CSS, str)
        assert len(DETAIL_PAGE_CSS) > 0
        assert '.amount' in DETAIL_PAGE_CSS
        assert '.ingredient' in DETAIL_PAGE_CSS

    def test_overview_page_css_is_string(self):
        """Test that OVERVIEW_PAGE_CSS is a non-empty string."""
        assert isinstance(OVERVIEW_PAGE_CSS, str)
        assert len(OVERVIEW_PAGE_CSS) > 0
        assert '.recipe-card' in OVERVIEW_PAGE_CSS
        assert 'h1' in OVERVIEW_PAGE_CSS

    def test_css_contains_valid_properties(self):
        """Test that CSS contains valid CSS properties."""
        all_css = COMMON_CSS + DETAIL_PAGE_CSS + OVERVIEW_PAGE_CSS
        assert 'color:' in all_css or 'color :' in all_css
        assert '{' in all_css
        assert '}' in all_css
