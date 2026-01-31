"""Tests for HTML generation functions."""

import pytest
from recipe_generator.html_generator import (
    format_time,
    generate_bring_widget,
    generate_schema_metadata,
    generate_recipe_detail_html,
    generate_overview_html,
)


class TestFormatTime:
    """Test cases for format_time function."""

    def test_zero_minutes(self):
        """Test formatting zero minutes."""
        assert format_time(0) == "PT0M"

    def test_single_digit_minutes(self):
        """Test formatting single digit minutes."""
        assert format_time(5) == "PT5M"

    def test_double_digit_minutes(self):
        """Test formatting double digit minutes."""
        assert format_time(45) == "PT45M"

    def test_large_minutes(self):
        """Test formatting large number of minutes."""
        assert format_time(120) == "PT120M"


class TestGenerateBringWidget:
    """Test cases for generate_bring_widget function."""

    def test_widget_without_url(self):
        """Test widget generation without URL."""
        widget = generate_bring_widget()
        assert 'data-bring-import' in widget
        assert 'data-bring-import="' not in widget
        assert 'platform.getbring.com/widgets/import.js' in widget

    def test_widget_with_url(self):
        """Test widget generation with URL."""
        url = "https://example.com/recipe"
        widget = generate_bring_widget(url)
        assert f'data-bring-import="{url}"' in widget
        assert 'platform.getbring.com/widgets/import.js' in widget

    def test_widget_with_special_characters_in_url(self):
        """Test widget generation with special characters in URL."""
        url = 'https://example.com/recipe?id=1&name="test"'
        widget = generate_bring_widget(url)
        assert 'data-bring-import="https://example.com/recipe?id=1&amp;name=&quot;test&quot;"' in widget


class TestGenerateSchemaMetadata:
    """Test cases for generate_schema_metadata function."""

    @pytest.fixture
    def sample_recipe(self):
        """Return a sample recipe for testing."""
        return {
            'name': 'Test Recipe',
            'description': 'A delicious test recipe',
            'servings': 4,
            'prep_time': 15,
            'cook_time': 30,
            'ingredients': [
                {'name': 'flour', 'amount': '2 cups'},
                {'name': 'sugar', 'amount': '1 cup'},
            ],
        }

    def test_metadata_includes_description(self, sample_recipe):
        """Test that metadata includes description."""
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="description"' in metadata
        assert 'A delicious test recipe' in metadata

    def test_metadata_includes_servings(self, sample_recipe):
        """Test that metadata includes servings."""
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="recipeYield"' in metadata
        assert '4 servings' in metadata

    def test_metadata_includes_prep_time(self, sample_recipe):
        """Test that metadata includes prep time."""
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="prepTime"' in metadata
        assert 'PT15M' in metadata

    def test_metadata_includes_cook_time(self, sample_recipe):
        """Test that metadata includes cook time."""
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="cookTime"' in metadata
        assert 'PT30M' in metadata

    def test_metadata_includes_ingredients(self, sample_recipe):
        """Test that metadata includes ingredients."""
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="recipeIngredient"' in metadata
        assert '2 cups flour' in metadata
        assert '1 cup sugar' in metadata

    def test_metadata_without_description(self, sample_recipe):
        """Test metadata generation without description."""
        del sample_recipe['description']
        metadata = generate_schema_metadata(sample_recipe)
        assert 'itemprop="description"' in metadata

    def test_metadata_escapes_html(self, sample_recipe):
        """Test that metadata escapes HTML characters."""
        sample_recipe['description'] = 'Recipe with <script>alert("xss")</script>'
        sample_recipe['ingredients'] = [{'name': 'ingredient&name', 'amount': '1 <cup>'}]
        metadata = generate_schema_metadata(sample_recipe)
        assert '<script>' not in metadata
        assert '&lt;script&gt;' in metadata
        assert '&amp;' in metadata


class TestGenerateRecipeDetailHtml:
    """Test cases for generate_recipe_detail_html function."""

    @pytest.fixture
    def sample_recipe(self):
        """Return a sample recipe for testing."""
        return {
            'name': 'Chocolate Cake',
            'description': 'A rich chocolate cake',
            'author': 'Test Chef',
            'servings': 8,
            'prep_time': 20,
            'cook_time': 40,
            'ingredients': [
                {'name': 'flour', 'amount': '2 cups'},
                {'name': 'cocoa powder', 'amount': '3/4 cup'},
            ],
            'instructions': [
                'Preheat oven to 350F',
                'Mix dry ingredients',
                'Bake for 40 minutes',
            ],
        }

    def test_html_includes_doctype(self, sample_recipe):
        """Test that HTML includes DOCTYPE."""
        html = generate_recipe_detail_html(sample_recipe)
        assert html.startswith('<!DOCTYPE html>')

    def test_html_includes_recipe_name(self, sample_recipe):
        """Test that HTML includes recipe name."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'Chocolate Cake' in html
        assert '<title>Chocolate Cake Recipe</title>' in html

    def test_html_includes_description(self, sample_recipe):
        """Test that HTML includes description."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'A rich chocolate cake' in html

    def test_html_includes_author(self, sample_recipe):
        """Test that HTML includes author."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'Test Chef' in html

    def test_html_includes_servings(self, sample_recipe):
        """Test that HTML includes servings."""
        html = generate_recipe_detail_html(sample_recipe)
        assert '8 servings' in html

    def test_html_includes_prep_time(self, sample_recipe):
        """Test that HTML includes prep time."""
        html = generate_recipe_detail_html(sample_recipe)
        assert '20 minutes' in html
        assert 'PT20M' in html

    def test_html_includes_cook_time(self, sample_recipe):
        """Test that HTML includes cook time."""
        html = generate_recipe_detail_html(sample_recipe)
        assert '40 minutes' in html
        assert 'PT40M' in html

    def test_html_includes_ingredients(self, sample_recipe):
        """Test that HTML includes all ingredients."""
        html = generate_recipe_detail_html(sample_recipe)
        assert '2 cups' in html
        assert 'flour' in html
        assert '3/4 cup' in html
        assert 'cocoa powder' in html

    def test_html_includes_instructions(self, sample_recipe):
        """Test that HTML includes all instructions."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'Preheat oven to 350F' in html
        assert 'Mix dry ingredients' in html
        assert 'Bake for 40 minutes' in html

    def test_html_includes_schema_org_microdata(self, sample_recipe):
        """Test that HTML includes Schema.org microdata."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'itemscope' in html
        assert 'itemtype="https://schema.org/Recipe"' in html
        assert 'itemprop="name"' in html
        assert 'itemprop="recipeIngredient"' in html
        assert 'itemprop="recipeInstructions"' in html

    def test_html_includes_bring_widget(self, sample_recipe):
        """Test that HTML includes Bring! widget."""
        html = generate_recipe_detail_html(sample_recipe)
        assert 'platform.getbring.com/widgets/import.js' in html
        assert 'data-bring-import' in html

    def test_html_escapes_special_characters(self, sample_recipe):
        """Test that HTML escapes special characters."""
        sample_recipe['name'] = 'Recipe with <script>alert("xss")</script>'
        sample_recipe['ingredients'][0]['name'] = 'ingredient&name'
        html = generate_recipe_detail_html(sample_recipe)
        assert '<script>' not in html
        assert '&lt;script&gt;' in html
        assert '&amp;' in html

    def test_html_without_optional_fields(self, sample_recipe):
        """Test HTML generation without optional fields."""
        del sample_recipe['description']
        del sample_recipe['author']
        html = generate_recipe_detail_html(sample_recipe)
        assert 'Chocolate Cake' in html
        assert 'Unknown' in html

    def test_html_has_valid_structure(self, sample_recipe):
        """Test that generated HTML has valid structure."""
        html = generate_recipe_detail_html(sample_recipe)
        assert '<html lang="en">' in html
        assert '<head>' in html
        assert '</head>' in html
        assert '<body>' in html
        assert '</body>' in html
        assert '</html>' in html


class TestGenerateOverviewHtml:
    """Test cases for generate_overview_html function."""

    @pytest.fixture
    def sample_recipes_data(self):
        """Return sample recipes data for testing."""
        return [
            ('recipe1.html', {
                'name': 'Recipe One',
                'description': 'First recipe description',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
            }),
            ('recipe2.html', {
                'name': 'Recipe Two',
                'description': 'Second recipe description',
                'servings': 6,
                'prep_time': 15,
                'cook_time': 30,
            }),
        ]

    def test_html_includes_doctype(self, sample_recipes_data):
        """Test that HTML includes DOCTYPE."""
        html = generate_overview_html(sample_recipes_data)
        assert html.startswith('<!DOCTYPE html>')

    def test_html_includes_title(self, sample_recipes_data):
        """Test that HTML includes title."""
        html = generate_overview_html(sample_recipes_data)
        assert '<title>Recipe Collection</title>' in html
        assert '<h1>Recipe Collection</h1>' in html

    def test_html_includes_all_recipes(self, sample_recipes_data):
        """Test that HTML includes all recipes."""
        html = generate_overview_html(sample_recipes_data)
        assert 'Recipe One' in html
        assert 'Recipe Two' in html

    def test_html_includes_recipe_descriptions(self, sample_recipes_data):
        """Test that HTML includes recipe descriptions."""
        html = generate_overview_html(sample_recipes_data)
        assert 'First recipe description' in html
        assert 'Second recipe description' in html

    def test_html_includes_recipe_links(self, sample_recipes_data):
        """Test that HTML includes links to recipe pages."""
        html = generate_overview_html(sample_recipes_data)
        assert 'href="recipe1.html"' in html
        assert 'href="recipe2.html"' in html

    def test_html_includes_servings_info(self, sample_recipes_data):
        """Test that HTML includes servings information."""
        html = generate_overview_html(sample_recipes_data)
        assert '4 servings' in html
        assert '6 servings' in html

    def test_html_includes_total_time(self, sample_recipes_data):
        """Test that HTML includes total time."""
        html = generate_overview_html(sample_recipes_data)
        assert '30 min total' in html  # 10 + 20
        assert '45 min total' in html  # 15 + 30

    def test_html_escapes_special_characters(self, sample_recipes_data):
        """Test that HTML escapes special characters."""
        sample_recipes_data[0] = ('test.html', {
            'name': 'Recipe with <script>alert("xss")</script>',
            'description': 'Description & special chars',
            'servings': 4,
            'prep_time': 10,
            'cook_time': 20,
        })
        html = generate_overview_html(sample_recipes_data)
        assert '<script>' not in html
        assert '&lt;script&gt;' in html
        assert '&amp;' in html

    def test_html_without_descriptions(self, sample_recipes_data):
        """Test HTML generation when recipes lack descriptions."""
        sample_recipes_data[0] = ('test.html', {
            'name': 'Recipe Without Description',
            'servings': 4,
            'prep_time': 10,
            'cook_time': 20,
        })
        html = generate_overview_html(sample_recipes_data)
        assert 'Recipe Without Description' in html

    def test_html_has_valid_structure(self, sample_recipes_data):
        """Test that generated HTML has valid structure."""
        html = generate_overview_html(sample_recipes_data)
        assert '<html lang="en">' in html
        assert '<head>' in html
        assert '</head>' in html
        assert '<body>' in html
        assert '</body>' in html
        assert '</html>' in html

    def test_single_recipe(self):
        """Test overview with a single recipe."""
        recipes_data = [
            ('single.html', {
                'name': 'Single Recipe',
                'description': 'Only recipe',
                'servings': 2,
                'prep_time': 5,
                'cook_time': 10,
            }),
        ]
        html = generate_overview_html(recipes_data)
        assert 'Single Recipe' in html
        assert 'href="single.html"' in html
