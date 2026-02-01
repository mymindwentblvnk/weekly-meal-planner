"""Main script to generate HTML recipe pages from YAML files."""

import yaml
from datetime import datetime, timezone

from recipe_generator import (
    RECIPES_DIR,
    OUTPUT_DIR,
    validate_recipe,
    generate_recipe_detail_html,
    generate_overview_html,
    generate_stats_html,
)


def main():
    """Generate HTML files from YAML recipes."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Store recipes for overview generation
    recipes_data = []
    errors = []

    # Process all YAML files in recipes directory
    for yaml_file in RECIPES_DIR.glob("*.yaml"):
        print(f"Processing {yaml_file.name}...")

        try:
            # Read YAML recipe
            with open(yaml_file, 'r', encoding='utf-8') as f:
                recipe = yaml.safe_load(f)

            # Validate recipe structure
            validate_recipe(recipe, yaml_file.name)

            # Generate recipe detail HTML
            html = generate_recipe_detail_html(recipe)

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

    # Generate overview page if we have at least one valid recipe
    if recipes_data:
        print("Generating overview page...")
        deployment_time = datetime.now(timezone.utc)
        overview_html = generate_overview_html(recipes_data, deployment_time)
        overview_file = OUTPUT_DIR / "index.html"
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write(overview_html)
        print(f"  → Generated {overview_file}")

        # Generate stats page
        print("Generating stats page...")
        stats_html = generate_stats_html(recipes_data)
        stats_file = OUTPUT_DIR / "stats.html"
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(stats_html)
        print(f"  → Generated {stats_file}")

    # Print summary
    print(f"\nDone! Generated {len(recipes_data)} recipe(s) in the 'output' directory.")
    if errors:
        print(f"\n⚠ {len(errors)} error(s) occurred:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
