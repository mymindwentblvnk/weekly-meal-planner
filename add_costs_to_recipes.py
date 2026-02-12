#!/usr/bin/env python3
"""Add estimated_cost field to all existing recipe YAML files."""

import yaml
from pathlib import Path
from recipe_generator.cost_calculator import load_prices, calculate_recipe_cost


RECIPES_DIR = Path("recipes")


def add_cost_to_recipe(yaml_file: Path) -> bool:
    """Add estimated_cost to a recipe YAML file.

    Args:
        yaml_file: Path to recipe YAML file

    Returns:
        True if cost was added/updated, False if skipped
    """
    try:
        # Read recipe
        with open(yaml_file, 'r', encoding='utf-8') as f:
            recipe = yaml.safe_load(f)

        # Check if already has estimated_cost
        if 'estimated_cost' in recipe:
            print(f"  ⊙ {yaml_file.name} - already has cost: {recipe['estimated_cost']:.2f} €")
            return False

        # Calculate cost
        prices = load_prices()
        total_cost, priced_count, total_count = calculate_recipe_cost(recipe, prices)

        # Add cost to recipe (insert after cook_time)
        recipe['estimated_cost'] = round(total_cost, 2)

        # Write back to file with proper ordering
        ordered_recipe = {}
        key_order = ['name', 'description', 'author', 'category', 'servings',
                     'prep_time', 'cook_time', 'estimated_cost', 'tags',
                     'ingredients', 'instructions']

        for key in key_order:
            if key in recipe:
                ordered_recipe[key] = recipe[key]

        # Add any remaining keys
        for key in recipe:
            if key not in ordered_recipe:
                ordered_recipe[key] = recipe[key]

        # Write to file using proper YAML formatting
        with open(yaml_file, 'w', encoding='utf-8') as f:
            # Write metadata fields with comments
            yaml.dump({'name': ordered_recipe['name']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            yaml.dump({'description': ordered_recipe['description']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            yaml.dump({'author': ordered_recipe['author']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            yaml.dump({'category': ordered_recipe['category']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            yaml.dump({'servings': ordered_recipe['servings']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            f.write(f"prep_time: {ordered_recipe.get('prep_time', 0)}  # minutes\n")
            f.write(f"cook_time: {ordered_recipe.get('cook_time', 0)}  # minutes\n")

            # Add estimated cost with coverage info
            coverage = f"{priced_count}/{total_count}" if total_count > 0 else "0/0"
            f.write(f"estimated_cost: {ordered_recipe['estimated_cost']:.2f}  # EUR - {coverage} ingredients priced\n")

            # Tags
            if 'tags' in ordered_recipe and ordered_recipe['tags']:
                yaml.dump({'tags': ordered_recipe['tags']}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            f.write("\n")

            # Ingredients
            yaml.dump({'ingredients': ordered_recipe.get('ingredients', [])}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            f.write("\n")

            # Instructions
            yaml.dump({'instructions': ordered_recipe.get('instructions', [])}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"  + {yaml_file.name} - added cost: {total_cost:.2f} € ({coverage} ingredients)")
        return True

    except Exception as e:
        print(f"  ✗ {yaml_file.name} - error: {e}")
        return False


def main():
    """Add costs to all recipes."""
    print("Adding estimated_cost to recipe YAML files...\n")

    all_recipes = list(RECIPES_DIR.glob("**/*.yaml"))
    added_count = 0
    skipped_count = 0
    error_count = 0

    for yaml_file in sorted(all_recipes):
        result = add_cost_to_recipe(yaml_file)
        if result is True:
            added_count += 1
        elif result is False:
            skipped_count += 1
        else:
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total recipes: {len(all_recipes)}")
    print(f"  Added cost: {added_count}")
    print(f"  Already had cost: {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"\nNext steps:")
    print(f"  1. Review the added costs in recipe YAML files")
    print(f"  2. Manually adjust costs where needed")
    print(f"  3. Run 'python main.py' to regenerate HTML")
    print(f"  4. Commit changes to git")


if __name__ == "__main__":
    main()
