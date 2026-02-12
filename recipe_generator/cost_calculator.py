"""Cost calculation module for recipes."""

import yaml
import re
from pathlib import Path
from typing import Dict, Tuple, Optional


# Load ingredient prices
PRICES_FILE = Path("ingredient_prices.yaml")


def load_prices() -> Dict[str, Dict]:
    """Load ingredient prices from YAML file."""
    if not PRICES_FILE.exists():
        return {}

    with open(PRICES_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def parse_amount(amount_str: str) -> Tuple[Optional[float], Optional[str]]:
    """Parse amount string to extract number and unit.

    Args:
        amount_str: Amount string like "200 g", "2 EL", "3", "1-2 TL"

    Returns:
        Tuple of (number, unit) or (None, None) if parsing fails
    """
    if not amount_str or amount_str == "nach Geschmack":
        return None, None

    amount_str = str(amount_str).strip()

    # Handle ranges like "1-2" - take the average
    if '-' in amount_str and not amount_str.startswith('-'):
        parts = amount_str.split('-')
        if len(parts) == 2:
            try:
                num1 = float(parts[0].strip())
                # Extract number from second part (might have unit)
                num2_match = re.match(r'(\d+(?:[.,]\d+)?)', parts[1].strip())
                if num2_match:
                    num2 = float(num2_match.group(1).replace(',', '.'))
                    avg = (num1 + num2) / 2
                    # Get unit from second part
                    unit_match = re.search(r'[a-zA-ZäöüÄÖÜß]+', parts[1].strip())
                    unit = unit_match.group(0) if unit_match else None
                    return avg, unit
            except (ValueError, AttributeError):
                pass

    # Extract number (handles decimals with comma or dot)
    number_match = re.match(r'(\d+(?:[.,]\d+)?)', amount_str)
    if not number_match:
        return None, None

    number = float(number_match.group(1).replace(',', '.'))

    # Extract unit (everything after the number)
    unit_match = re.search(r'[a-zA-ZäöüÄÖÜß]+', amount_str)
    unit = unit_match.group(0) if unit_match else None

    return number, unit


def normalize_unit(unit: Optional[str], number: float) -> Tuple[float, str]:
    """Normalize unit to standard units (kg, L, piece).

    Args:
        unit: Unit string like "g", "ml", "TL", etc.
        number: Amount number

    Returns:
        Tuple of (normalized_number, normalized_unit)
    """
    if not unit:
        return number, "piece"

    unit_lower = unit.lower()

    # Weight conversions to kg
    if unit_lower in ['g', 'gr', 'gramm']:
        return number / 1000, "kg"
    elif unit_lower in ['kg', 'kilo', 'kilogramm']:
        return number, "kg"

    # Volume conversions to L
    elif unit_lower in ['ml', 'milliliter']:
        return number / 1000, "L"
    elif unit_lower in ['l', 'liter']:
        return number, "L"

    # Tablespoons and teaspoons (approximate)
    elif unit_lower in ['el', 'esl', 'esslöffel']:
        return number * 0.015, "L"  # ~15ml per tablespoon
    elif unit_lower in ['tl', 'teel', 'teelöffel']:
        return number * 0.005, "L"  # ~5ml per teaspoon

    # Pieces/items
    elif unit_lower in ['stück', 'st', 'st.', 'stuck', 'stücke']:
        return number, "piece"
    elif unit_lower in ['dose', 'dosen', 'can', 'cans']:
        return number, "piece"
    elif unit_lower in ['bund', 'bunch']:
        return number, "bunch"
    elif unit_lower in ['prise', 'messerspitze']:
        return 0, "piece"  # negligible cost

    # Default to piece if unknown
    else:
        return number, "piece"


def calculate_ingredient_cost(ingredient_name: str, amount_str: str, prices: Dict) -> Optional[float]:
    """Calculate cost for a single ingredient.

    Args:
        ingredient_name: Name of the ingredient
        amount_str: Amount string (e.g., "200 g")
        prices: Price database

    Returns:
        Cost in EUR or None if price not found
    """
    # Handle "nach Geschmack" (to taste)
    if not amount_str or amount_str == "nach Geschmack":
        return 0.0

    # Parse amount
    number, unit = parse_amount(amount_str)
    if number is None:
        return None

    # Normalize unit
    normalized_number, normalized_unit = normalize_unit(unit, number)

    # Look up price - try exact match first, then variations
    price_info = None
    search_names = [
        ingredient_name,
        ingredient_name.split('(')[0].strip(),  # Remove parentheses
        ingredient_name.split()[0],  # First word only
    ]

    for search_name in search_names:
        if search_name in prices:
            price_info = prices[search_name]
            break

    if not price_info:
        return None

    # Get price per unit
    price_per_unit = price_info.get('price', 0)
    price_unit = price_info.get('unit', 'kg')

    # Convert if units don't match
    if normalized_unit != price_unit:
        # Try to convert
        if price_unit == "piece" and normalized_unit in ["kg", "L"]:
            # Can't convert weight/volume to pieces
            return None
        elif normalized_unit == "piece" and price_unit in ["kg", "L"]:
            # Use piece price as-is
            return price_per_unit * normalized_number
        elif price_unit in ["kg", "L"] and normalized_unit in ["kg", "L"]:
            # Both are compatible units, use normalized
            pass
        else:
            # Unknown conversion
            return None

    # Calculate cost
    cost = price_per_unit * normalized_number
    return round(cost, 2)


def calculate_recipe_cost(recipe: Dict, prices: Dict) -> Tuple[float, int, int]:
    """Calculate total cost for a recipe.

    Args:
        recipe: Recipe dictionary
        prices: Price database

    Returns:
        Tuple of (total_cost, priced_ingredients_count, total_ingredients_count)
    """
    total_cost = 0.0
    priced_count = 0
    total_count = 0

    ingredients = recipe.get('ingredients', [])
    for ingredient in ingredients:
        total_count += 1
        name = ingredient.get('name', '')
        amount = ingredient.get('amount', '')

        cost = calculate_ingredient_cost(name, str(amount), prices)
        if cost is not None:
            total_cost += cost
            priced_count += 1

    return round(total_cost, 2), priced_count, total_count


def format_cost(cost: float) -> str:
    """Format cost as currency string.

    Args:
        cost: Cost in EUR

    Returns:
        Formatted string like "2,50 €"
    """
    return f"{cost:.2f} €".replace('.', ',')
