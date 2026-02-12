#!/usr/bin/env python3
"""Update ingredient prices by scanning recipes and finding missing prices."""

import sys
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Tuple


RECIPES_DIR = Path("recipes")
PRICES_FILE = Path("ingredient_prices.yaml")


def normalize_ingredient_name(name: str) -> str:
    """Normalize ingredient name for matching.

    Args:
        name: Raw ingredient name from recipe

    Returns:
        Normalized name for lookup
    """
    # Remove content in parentheses
    if '(' in name:
        name = name.split('(')[0].strip()

    # Remove common qualifiers
    qualifiers = ['frisch', 'gefroren', 'bio', 'klein', 'groß', 'große', 'kleine']
    words = name.split()
    filtered_words = [w for w in words if w.lower() not in qualifiers]

    if filtered_words:
        name = ' '.join(filtered_words)

    return name.strip()


def load_prices() -> Dict[str, Dict]:
    """Load ingredient prices from YAML file."""
    if not PRICES_FILE.exists():
        return {}

    with open(PRICES_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def scan_recipes() -> Tuple[Set[str], Dict[str, List[str]]]:
    """Scan all recipes and extract unique ingredients.

    Returns:
        Tuple of (unique_ingredients, ingredient_usage_map)
    """
    all_ingredients = set()
    ingredient_usage = defaultdict(list)  # ingredient -> list of recipes

    for yaml_file in RECIPES_DIR.glob("**/*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                recipe = yaml.safe_load(f)

            recipe_name = recipe.get('name', yaml_file.stem)
            ingredients = recipe.get('ingredients', [])

            for ingredient in ingredients:
                name = ingredient.get('name', '')
                if name:
                    normalized = normalize_ingredient_name(name)
                    all_ingredients.add(normalized)
                    ingredient_usage[normalized].append(recipe_name)

        except Exception as e:
            print(f"Warning: Could not process {yaml_file.name}: {e}")

    return all_ingredients, dict(ingredient_usage)


def find_missing_ingredients(recipe_ingredients: Set[str], prices: Dict) -> Set[str]:
    """Find ingredients that don't have prices.

    Args:
        recipe_ingredients: Set of ingredient names from recipes
        prices: Price database

    Returns:
        Set of missing ingredient names
    """
    price_keys = set(prices.keys())
    missing = set()

    for ingredient in recipe_ingredients:
        # Check exact match
        if ingredient in price_keys:
            continue

        # Check variations (singular/plural)
        found = False
        for price_key in price_keys:
            # Simple check: if one is substring of other
            if (ingredient.lower() in price_key.lower() or
                price_key.lower() in ingredient.lower()):
                found = True
                break

        if not found:
            missing.add(ingredient)

    return missing


def generate_report(recipe_ingredients: Set[str], prices: Dict,
                   ingredient_usage: Dict[str, List[str]], missing: Set[str]) -> str:
    """Generate coverage report.

    Args:
        recipe_ingredients: All ingredients from recipes
        prices: Price database
        ingredient_usage: Map of ingredient to recipes using it
        missing: Missing ingredients

    Returns:
        Formatted report string
    """
    total_ingredients = len(recipe_ingredients)
    with_prices = total_ingredients - len(missing)
    coverage_pct = (with_prices / total_ingredients * 100) if total_ingredients > 0 else 0

    # Count recipe files
    recipe_count = len(list(RECIPES_DIR.glob("**/*.yaml")))

    # Find most expensive
    price_items = [(name, info['price']) for name, info in prices.items()
                   if isinstance(info, dict) and 'price' in info]
    most_expensive = sorted(price_items, key=lambda x: x[1], reverse=True)[:5]

    report = []
    report.append("╔════════════════════════════════════════╗")
    report.append("║   BIO Price Database Coverage Report   ║")
    report.append("╠════════════════════════════════════════╣")
    report.append(f"║ Total unique ingredients:   {total_ingredients:>8} ║")
    report.append(f"║ With prices:                {with_prices:>8} ║")
    report.append(f"║ Missing prices:             {len(missing):>8} ║")
    report.append(f"║ Coverage:                  {coverage_pct:>6.1f}% ║")
    report.append("╠════════════════════════════════════════╣")
    report.append(f"║ Total recipes:              {recipe_count:>8} ║")
    report.append("╠════════════════════════════════════════╣")

    if most_expensive:
        report.append("║ Most expensive ingredients:            ║")
        for name, price in most_expensive:
            unit = prices[name].get('unit', 'kg')
            report.append(f"║   - {name:20s} {price:>6.2f} €/{unit:5s} ║")
        report.append("╠════════════════════════════════════════╣")

    if missing:
        report.append("║ Missing ingredients (first 20):        ║")
        for ingredient in sorted(missing)[:20]:
            usage = ingredient_usage.get(ingredient, [])
            usage_str = f"({len(usage)} recipes)"
            display_name = ingredient[:25] + "..." if len(ingredient) > 25 else ingredient
            report.append(f"║   - {display_name:32s} {usage_str:>6s} ║")

    report.append("╚════════════════════════════════════════╝")

    return '\n'.join(report)


def check_mode():
    """Run in check mode - show missing ingredients."""
    print("Scanning recipes...")
    recipe_ingredients, ingredient_usage = scan_recipes()

    print(f"Found {len(recipe_ingredients)} unique ingredients across recipes\n")

    prices = load_prices()
    missing = find_missing_ingredients(recipe_ingredients, prices)

    with_prices = len(recipe_ingredients) - len(missing)
    coverage_pct = (with_prices / len(recipe_ingredients) * 100) if recipe_ingredients else 0

    print(f"Price database coverage: {coverage_pct:.1f}% ({with_prices}/{len(recipe_ingredients)})\n")

    if missing:
        print(f"Missing ingredients ({len(missing)}):")
        for ingredient in sorted(missing)[:30]:  # Show first 30
            usage = ingredient_usage.get(ingredient, [])
            usage_str = ', '.join(usage[:3])
            if len(usage) > 3:
                usage_str += f", ... ({len(usage)} total)"
            print(f"  - {ingredient:30s} (used in: {usage_str})")

        if len(missing) > 30:
            print(f"\n  ... and {len(missing) - 30} more")

        print("\n" + "="*60)
        print("Recommendations:")
        print("  1. Run 'python update_prices.py add' to add missing ingredients")
        print("  2. Manually edit ingredient_prices.yaml")
        print("  3. Check REWE Bio / Edeka Bio for current prices")
    else:
        print("✓ All ingredients have prices!")

    return 0


def report_mode():
    """Run in report mode - generate full coverage report."""
    print("Generating coverage report...\n")

    recipe_ingredients, ingredient_usage = scan_recipes()
    prices = load_prices()
    missing = find_missing_ingredients(recipe_ingredients, prices)

    report = generate_report(recipe_ingredients, prices, ingredient_usage, missing)
    print(report)

    return 0


def add_mode():
    """Run in add mode - add missing ingredients with estimated prices."""
    print("Scanning recipes...")
    recipe_ingredients, ingredient_usage = scan_recipes()

    prices = load_prices()
    missing = find_missing_ingredients(recipe_ingredients, prices)

    if not missing:
        print("✓ All ingredients already have prices!")
        return 0

    print(f"\nFound {len(missing)} missing ingredients")
    print("\nNote: This mode requires online price research.")
    print("For now, adding placeholders. Please update with actual BIO prices.\n")

    # Add placeholders for missing ingredients
    added = []
    for ingredient in sorted(missing):
        # Determine likely unit based on ingredient name
        unit = "kg"  # default
        if any(word in ingredient.lower() for word in ['milch', 'öl', 'essig', 'brühe', 'saft', 'wasser']):
            unit = "L"
        elif any(word in ingredient.lower() for word in ['ei', 'gurke', 'zitrone', 'zwiebel', 'knoblauch']):
            unit = "piece"
        elif any(word in ingredient.lower() for word in ['petersilie', 'koriander', 'basilikum', 'minze']):
            unit = "bunch"

        prices[ingredient] = {
            'price': 5.00,  # placeholder
            'unit': unit,
            'notes': f'PLACEHOLDER - needs price research (added {Path(__file__).stem})'
        }
        added.append(ingredient)
        print(f"  + {ingredient:30s} ({unit}) - PLACEHOLDER")

    # Save updated prices
    with open(PRICES_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(prices, f, allow_unicode=True, sort_keys=True, default_flow_style=False)

    print(f"\n✓ Added {len(added)} placeholder entries to {PRICES_FILE}")
    print("\n⚠️  IMPORTANT: These are PLACEHOLDERS with 5.00 € default price")
    print("Please research actual BIO prices and update:")
    print(f"  - Edit {PRICES_FILE}")
    print("  - Check REWE Bio: https://www.rewe.de/bio")
    print("  - Check Edeka Bio: https://www.edeka.de")

    return 0


def main():
    """Main entry point."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"

    if mode not in ['check', 'add', 'report']:
        print(f"Unknown mode: {mode}")
        print("Usage: python update_prices.py [check|add|report]")
        return 1

    if mode == "check":
        return check_mode()
    elif mode == "add":
        return add_mode()
    elif mode == "report":
        return report_mode()


if __name__ == "__main__":
    sys.exit(main())
