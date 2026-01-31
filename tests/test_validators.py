"""Tests for recipe validation functions."""

import pytest
from recipe_generator.validators import validate_recipe


class TestValidateRecipe:
    """Test cases for validate_recipe function."""

    @pytest.fixture
    def valid_recipe(self):
        """Return a valid recipe for testing."""
        return {
            'name': 'Test Recipe',
            'servings': 4,
            'prep_time': 15,
            'cook_time': 30,
            'ingredients': [
                {'name': 'flour', 'amount': '2 cups'},
                {'name': 'sugar', 'amount': '1 cup'},
            ],
            'instructions': [
                'Mix ingredients',
                'Bake at 350F',
            ],
        }

    def test_valid_recipe_passes(self, valid_recipe):
        """Test that a valid recipe passes validation."""
        validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_name_raises_error(self, valid_recipe):
        """Test that missing name field raises ValueError."""
        del valid_recipe['name']
        with pytest.raises(ValueError, match="Missing required field 'name'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_servings_raises_error(self, valid_recipe):
        """Test that missing servings field raises ValueError."""
        del valid_recipe['servings']
        with pytest.raises(ValueError, match="Missing required field 'servings'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_prep_time_raises_error(self, valid_recipe):
        """Test that missing prep_time field raises ValueError."""
        del valid_recipe['prep_time']
        with pytest.raises(ValueError, match="Missing required field 'prep_time'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_cook_time_raises_error(self, valid_recipe):
        """Test that missing cook_time field raises ValueError."""
        del valid_recipe['cook_time']
        with pytest.raises(ValueError, match="Missing required field 'cook_time'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_ingredients_raises_error(self, valid_recipe):
        """Test that missing ingredients field raises ValueError."""
        del valid_recipe['ingredients']
        with pytest.raises(ValueError, match="Missing required field 'ingredients'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_missing_instructions_raises_error(self, valid_recipe):
        """Test that missing instructions field raises ValueError."""
        del valid_recipe['instructions']
        with pytest.raises(ValueError, match="Missing required field 'instructions'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_empty_ingredients_list_raises_error(self, valid_recipe):
        """Test that empty ingredients list raises ValueError."""
        valid_recipe['ingredients'] = []
        with pytest.raises(ValueError, match="'ingredients' must be a non-empty list"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_non_list_ingredients_raises_error(self, valid_recipe):
        """Test that non-list ingredients raises ValueError."""
        valid_recipe['ingredients'] = "not a list"
        with pytest.raises(ValueError, match="'ingredients' must be a non-empty list"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_ingredient_not_dict_raises_error(self, valid_recipe):
        """Test that ingredient that is not a dict raises ValueError."""
        valid_recipe['ingredients'] = ['string ingredient']
        with pytest.raises(ValueError, match="Ingredient 0 must be a dictionary"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_ingredient_missing_name_raises_error(self, valid_recipe):
        """Test that ingredient missing name raises ValueError."""
        valid_recipe['ingredients'] = [{'amount': '2 cups'}]
        with pytest.raises(ValueError, match="Ingredient 0 missing 'name' or 'amount'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_ingredient_missing_amount_raises_error(self, valid_recipe):
        """Test that ingredient missing amount raises ValueError."""
        valid_recipe['ingredients'] = [{'name': 'flour'}]
        with pytest.raises(ValueError, match="Ingredient 0 missing 'name' or 'amount'"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_empty_instructions_list_raises_error(self, valid_recipe):
        """Test that empty instructions list raises ValueError."""
        valid_recipe['instructions'] = []
        with pytest.raises(ValueError, match="'instructions' must be a non-empty list"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_non_list_instructions_raises_error(self, valid_recipe):
        """Test that non-list instructions raises ValueError."""
        valid_recipe['instructions'] = "not a list"
        with pytest.raises(ValueError, match="'instructions' must be a non-empty list"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_zero_servings_raises_error(self, valid_recipe):
        """Test that zero servings raises ValueError."""
        valid_recipe['servings'] = 0
        with pytest.raises(ValueError, match="'servings' must be a positive integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_negative_servings_raises_error(self, valid_recipe):
        """Test that negative servings raises ValueError."""
        valid_recipe['servings'] = -1
        with pytest.raises(ValueError, match="'servings' must be a positive integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_non_integer_servings_raises_error(self, valid_recipe):
        """Test that non-integer servings raises ValueError."""
        valid_recipe['servings'] = "4"
        with pytest.raises(ValueError, match="'servings' must be a positive integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_negative_prep_time_raises_error(self, valid_recipe):
        """Test that negative prep_time raises ValueError."""
        valid_recipe['prep_time'] = -1
        with pytest.raises(ValueError, match="'prep_time' must be a non-negative integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_non_integer_prep_time_raises_error(self, valid_recipe):
        """Test that non-integer prep_time raises ValueError."""
        valid_recipe['prep_time'] = "15"
        with pytest.raises(ValueError, match="'prep_time' must be a non-negative integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_zero_prep_time_is_valid(self, valid_recipe):
        """Test that zero prep_time is valid."""
        valid_recipe['prep_time'] = 0
        validate_recipe(valid_recipe, 'test.yaml')

    def test_negative_cook_time_raises_error(self, valid_recipe):
        """Test that negative cook_time raises ValueError."""
        valid_recipe['cook_time'] = -1
        with pytest.raises(ValueError, match="'cook_time' must be a non-negative integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_non_integer_cook_time_raises_error(self, valid_recipe):
        """Test that non-integer cook_time raises ValueError."""
        valid_recipe['cook_time'] = "30"
        with pytest.raises(ValueError, match="'cook_time' must be a non-negative integer"):
            validate_recipe(valid_recipe, 'test.yaml')

    def test_zero_cook_time_is_valid(self, valid_recipe):
        """Test that zero cook_time is valid."""
        valid_recipe['cook_time'] = 0
        validate_recipe(valid_recipe, 'test.yaml')

    def test_multiple_ingredients_valid(self, valid_recipe):
        """Test that multiple ingredients are validated correctly."""
        valid_recipe['ingredients'] = [
            {'name': 'flour', 'amount': '2 cups'},
            {'name': 'sugar', 'amount': '1 cup'},
            {'name': 'eggs', 'amount': '3'},
        ]
        validate_recipe(valid_recipe, 'test.yaml')
