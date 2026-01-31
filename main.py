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
    """Create a restaurant-style logo with 'R' for Rezepte."""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (44, 82, 130)  # #2c5282
    border_color = (30, 58, 95)  # darker blue
    white = (255, 255, 255)
    gold = (212, 175, 55)  # restaurant gold accent

    center_x = size / 2
    center_y = size / 2

    # Draw circular background with elegant border
    margin = size * 0.03
    border_width = max(2, size // 40)

    # Outer gold ring
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=gold,
        outline=None
    )

    # Inner blue circle
    inner_margin = margin + border_width
    draw.ellipse(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        fill=bg_color,
        outline=None
    )

    # Try to use a font for the R
    try:
        from PIL import ImageFont
        # Try to load a serif font - these are common on macOS
        font_size = int(size * 0.6)
        font = None

        # Try different serif fonts
        for font_name in ['/System/Library/Fonts/Supplemental/Times New Roman.ttf',
                         '/System/Library/Fonts/Supplemental/Georgia.ttf',
                         '/Library/Fonts/Times New Roman.ttf',
                         '/System/Library/Fonts/SupplementalSerif.ttf']:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue

        if font is None:
            # Fallback to default font
            font = ImageFont.load_default()
            # Scale up the default font usage
            font_size = int(size * 0.5)
    except:
        font = None
        font_size = int(size * 0.5)

    # Draw the letter R
    text = "R"

    if font:
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center the text
        text_x = center_x - text_width / 2
        text_y = center_y - text_height / 2 - bbox[1]

        # Draw text with slight shadow for depth
        shadow_offset = max(1, size // 80)
        draw.text((text_x + shadow_offset, text_y + shadow_offset), text, fill=(0, 0, 0, 100), font=font)
        draw.text((text_x, text_y), text, fill=white, font=font)
    else:
        # Fallback: draw a simple serif-style R using shapes
        scale = size / 200

        # Vertical stem
        stem_width = 20 * scale
        stem_height = 100 * scale
        draw.rectangle(
            [
                center_x - stem_width/2,
                center_y - stem_height/2,
                center_x + stem_width/2,
                center_y + stem_height/2
            ],
            fill=white
        )

        # Top bowl (rounded rectangle for P-like top)
        bowl_width = 45 * scale
        bowl_height = 45 * scale
        draw.rounded_rectangle(
            [
                center_x - stem_width/2,
                center_y - stem_height/2,
                center_x + bowl_width,
                center_y - stem_height/2 + bowl_height
            ],
            radius=22 * scale,
            fill=white
        )

        # Inner cutout for bowl
        inner_radius = 15 * scale
        draw.rounded_rectangle(
            [
                center_x + stem_width/2,
                center_y - stem_height/2 + 7 * scale,
                center_x + bowl_width - 7 * scale,
                center_y - stem_height/2 + bowl_height - 7 * scale
            ],
            radius=inner_radius,
            fill=bg_color
        )

        # Diagonal leg
        leg_points = [
            (center_x + stem_width/2, center_y),
            (center_x + bowl_width + 5 * scale, center_y + stem_height/2),
            (center_x + bowl_width + 15 * scale, center_y + stem_height/2),
            (center_x + stem_width/2 + 15 * scale, center_y),
        ]
        draw.polygon(leg_points, fill=white)

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
