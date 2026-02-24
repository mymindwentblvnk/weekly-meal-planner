# Recipe Images

This directory contains images for recipe cards displayed on the overview page.

## Adding Images to Recipes

1. **Place your image** in this directory (`images/recipes/`)
   - Supported formats: JPG, PNG, SVG, WebP
   - Recommended size: 800x600px or similar aspect ratio
   - File naming: Use lowercase, hyphens for spaces (e.g., `lasagne.jpg`)

2. **Update the recipe YAML** file to reference the image:
   ```yaml
   name: Lasagne
   description: ...
   image: images/recipes/lasagne.jpg
   # ... rest of recipe
   ```

3. **Regenerate HTML** by running:
   ```bash
   python main.py
   ```

## Placeholder Image

If a recipe doesn't have an `image` field in its YAML file, the `placeholder.svg` will be displayed instead.

## Image Display

- Images are displayed at **200px height** on recipe cards
- Images use `object-fit: cover` for consistent cropping
- Images are clickable and link to the recipe detail page
- Images have rounded top corners matching the card design

## Tips

- Use high-quality, well-lit food photography
- Ensure images are properly cropped and centered on the food
- Keep file sizes reasonable (< 500KB) for faster loading
- Use descriptive filenames matching the recipe name
