"""Recipe validation functions."""

from typing import Any


def validate_recipe(recipe: dict[str, Any], filename: str) -> None:
    """Validate recipe has required fields.

    Args:
        recipe: Recipe dictionary to validate
        filename: Name of the file being validated (for error messages)

    Raises:
        ValueError: If required fields are missing or invalid
    """
    required_fields = ['name', 'servings', 'prep_time', 'cook_time', 'ingredients', 'instructions']

    for field in required_fields:
        if field not in recipe:
            raise ValueError(f"Missing required field '{field}' in {filename}")

    # Validate ingredients structure
    if not isinstance(recipe['ingredients'], list) or not recipe['ingredients']:
        raise ValueError(f"'ingredients' must be a non-empty list in {filename}")

    for idx, ingredient in enumerate(recipe['ingredients']):
        if not isinstance(ingredient, dict):
            raise ValueError(f"Ingredient {idx} must be a dictionary in {filename}")
        if 'name' not in ingredient or 'amount' not in ingredient:
            raise ValueError(f"Ingredient {idx} missing 'name' or 'amount' in {filename}")

    # Validate instructions structure
    if not isinstance(recipe['instructions'], list) or not recipe['instructions']:
        raise ValueError(f"'instructions' must be a non-empty list in {filename}")

    # Validate numeric fields
    if not isinstance(recipe['servings'], int) or recipe['servings'] <= 0:
        raise ValueError(f"'servings' must be a positive integer in {filename}")
    if not isinstance(recipe['prep_time'], int) or recipe['prep_time'] < 0:
        raise ValueError(f"'prep_time' must be a non-negative integer in {filename}")
    if not isinstance(recipe['cook_time'], int) or recipe['cook_time'] < 0:
        raise ValueError(f"'cook_time' must be a non-negative integer in {filename}")
