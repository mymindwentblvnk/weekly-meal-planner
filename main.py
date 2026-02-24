"""Main script to generate HTML recipe pages from YAML files."""

import yaml
import shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from recipe_generator import (
    RECIPES_DIR,
    OUTPUT_DIR,
    validate_recipe,
    generate_recipe_detail_html,
    generate_overview_html,
    generate_weekly_html,
    generate_shopping_list_html,
)


def main():
    """Generate HTML files from YAML recipes."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy images directory to output
    images_src = Path("images")
    images_dst = OUTPUT_DIR / "images"
    if images_src.exists():
        if images_dst.exists():
            shutil.rmtree(images_dst)
        shutil.copytree(images_src, images_dst)

    # Get deployment time for all pages
    deployment_time = datetime.now(ZoneInfo("Europe/Berlin"))

    # Store recipes for overview generation
    recipes_data = []
    errors = []

    # Process all YAML files in recipes directory (including subdirectories)
    # Sort by modification time (oldest first, so newest get highest index)
    yaml_files = sorted(RECIPES_DIR.glob("**/*.yaml"), key=lambda p: p.stat().st_mtime)

    for yaml_file in yaml_files:
        print(f"Processing {yaml_file.name}...")

        try:
            # Read YAML recipe
            with open(yaml_file, 'r', encoding='utf-8') as f:
                recipe = yaml.safe_load(f)

            # Validate recipe structure
            validate_recipe(recipe, yaml_file.name)

            # Generate recipe detail HTML
            html = generate_recipe_detail_html(recipe, yaml_file.stem, deployment_time)

            # Write HTML file
            output_filename = f"{yaml_file.stem}.html"
            output_file = OUTPUT_DIR / output_filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  → Generated {output_file}")

            # Store recipe data for overview
            recipes_data.append((output_filename, recipe))

        except yaml.YAMLError as e:
            error_msg = f"Error parsing YAML in {yaml_file.name}: {e}"
            print(f"  ✗ {error_msg}")
            errors.append(error_msg)
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            print(f"  ✗ {error_msg}")
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error processing {yaml_file.name}: {e}"
            print(f"  ✗ {error_msg}")
            errors.append(error_msg)

    # Generate pages if we have at least one valid recipe
    if recipes_data:
        # Generate weekly plan page as the main index
        print("Generating weekly plan page (index)...")
        weekly_html = generate_weekly_html(recipes_data, deployment_time)
        index_file = OUTPUT_DIR / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(weekly_html)
        print(f"  → Generated {index_file}")

        # Generate recipe catalog page
        print("Generating recipe catalog page...")
        catalog_html = generate_overview_html(recipes_data, deployment_time)
        catalog_file = OUTPUT_DIR / "recipes.html"
        with open(catalog_file, 'w', encoding='utf-8') as f:
            f.write(catalog_html)
        print(f"  → Generated {catalog_file}")

        # Generate shopping list page
        print("Generating shopping list page...")
        shopping_html = generate_shopping_list_html(recipes_data, deployment_time)
        shopping_file = OUTPUT_DIR / "shopping.html"
        with open(shopping_file, 'w', encoding='utf-8') as f:
            f.write(shopping_html)
        print(f"  → Generated {shopping_file}")

    # Print summary
    print(f"\nDone! Generated {len(recipes_data)} recipe(s) in the 'output' directory.")
    if errors:
        print(f"\n⚠ {len(errors)} error(s) occurred:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
