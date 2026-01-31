"""Main script to generate HTML recipe pages from YAML files."""

import yaml
from datetime import datetime, timezone
from PIL import Image, ImageDraw

from recipe_generator import (
    RECIPES_DIR,
    OUTPUT_DIR,
    validate_recipe,
    generate_recipe_detail_html,
    generate_overview_html,
)


def create_logo(size):
    """Create a chef hat logo at the specified size."""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (44, 82, 130)  # #2c5282
    white = (255, 255, 255)

    # Draw circular background
    margin = size * 0.05
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=bg_color,
        outline=(30, 58, 95),
        width=max(1, size // 60)
    )

    # Chef hat proportions (scaled to image size)
    center_x = size / 2
    center_y = size / 2

    # Hat dimensions scaled by size
    scale = size / 200

    # Hat band
    band_width = 90 * scale
    band_height = 15 * scale
    band_y = center_y - 10 * scale
    draw.rounded_rectangle(
        [
            center_x - band_width/2,
            band_y,
            center_x + band_width/2,
            band_y + band_height
        ],
        radius=3 * scale,
        fill=white
    )

    # Hat top (puffy circles)
    puff_radius = 18 * scale
    draw.ellipse(
        [
            center_x - puff_radius,
            center_y - 50 * scale - puff_radius,
            center_x + puff_radius,
            center_y - 50 * scale + puff_radius
        ],
        fill=white
    )

    # Side puffs
    for x_offset in [-30 * scale, 30 * scale]:
        draw.ellipse(
            [
                center_x + x_offset - puff_radius,
                center_y - 40 * scale - puff_radius,
                center_x + x_offset + puff_radius,
                center_y - 40 * scale + puff_radius
            ],
            fill=white
        )

    # Center large ellipse
    draw.ellipse(
        [
            center_x - 50 * scale,
            center_y - 60 * scale,
            center_x + 50 * scale,
            center_y - 10 * scale
        ],
        fill=white
    )

    # Hat bottom (trapezoid as polygon)
    hat_bottom = [
        (center_x - 45 * scale, band_y + band_height),
        (center_x - 50 * scale, center_y + 20 * scale),
        (center_x + 50 * scale, center_y + 20 * scale),
        (center_x + 45 * scale, band_y + band_height),
    ]
    draw.polygon(hat_bottom, fill=white)

    # Fork on left
    fork_x = center_x - 25 * scale
    fork_y = center_y + 10 * scale
    fork_width = 4 * scale
    fork_height = 35 * scale

    # Fork handle
    draw.rounded_rectangle(
        [fork_x - fork_width/2, fork_y, fork_x + fork_width/2, fork_y + fork_height],
        radius=max(1, scale),
        fill=bg_color
    )

    # Fork tines
    tine_width = 2 * scale
    for x_offset in [-6 * scale, 0, 4 * scale]:
        draw.rounded_rectangle(
            [
                fork_x + x_offset,
                fork_y,
                fork_x + x_offset + tine_width,
                fork_y + 15 * scale
            ],
            radius=max(1, scale),
            fill=bg_color
        )

    # Spoon on right
    spoon_x = center_x + 25 * scale
    spoon_y = center_y + 10 * scale

    # Spoon handle
    draw.rounded_rectangle(
        [
            spoon_x - fork_width/2,
            spoon_y + 10 * scale,
            spoon_x + fork_width/2,
            spoon_y + 35 * scale
        ],
        radius=max(1, scale),
        fill=bg_color
    )

    # Spoon bowl
    draw.ellipse(
        [
            spoon_x - 5 * scale,
            spoon_y,
            spoon_x + 5 * scale,
            spoon_y + 14 * scale
        ],
        fill=bg_color
    )

    return img


def generate_icons():
    """Generate favicon and apple-touch-icon."""
    print("Generating icons...")

    # Generate apple-touch-icon (180x180 PNG)
    apple_touch_icon_path = OUTPUT_DIR / "apple-touch-icon.png"
    logo_180 = create_logo(180)
    logo_180.save(apple_touch_icon_path, 'PNG')
    print(f"  → Created {apple_touch_icon_path}")

    # Generate favicon.ico with multiple sizes
    sizes = [16, 32, 48]
    images = [create_logo(size) for size in sizes]

    favicon_path = OUTPUT_DIR / "favicon.ico"
    images[0].save(
        favicon_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print(f"  → Created {favicon_path}")


def main():
    """Generate HTML files from YAML recipes."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate favicon and apple-touch-icon
    generate_icons()

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

    # Print summary
    print(f"\nDone! Generated {len(recipes_data)} recipe(s) in the 'output' directory.")
    if errors:
        print(f"\n⚠ {len(errors)} error(s) occurred:")
        for error in errors:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
