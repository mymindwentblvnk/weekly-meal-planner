# Shrink Recipe Images

This skill optimizes oversized recipe images to ensure consistent size and faster page load times.

## Usage

```
/shrink-images
```

No arguments needed - automatically scans and optimizes all oversized images.

**IMPORTANT**: Do NOT ask for permission before scanning and optimizing images. This skill is designed to run autonomously - just scan the directory and replace oversized files with the optimized versions automatically.

## What This Skill Does

**Automatically optimizes all recipe images that exceed the maximum dimension of 800px.**

1. **Scans images directory** - Checks all images in `images/recipes/`
2. **Measures dimensions** - Uses `sips` to get width and height of each image
3. **Identifies oversized images** - Flags any image with width OR height > 800px
4. **Optimizes in-place** - Resizes oversized images using `sips -Z 800`
5. **Reports results** - Shows which images were optimized and file size savings

## Image Optimization Standard

All recipe images should follow this standard (same as `/import-recipe`):

- **Max dimension**: 800px (width or height)
- **Aspect ratio**: Preserved (not stretched)
- **Format**: JPG preferred for photos, PNG for graphics
- **In-place optimization**: Original files are replaced (no broken links)

## How It Works

### Step 1: Find All Images

```bash
find images/recipes/ -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) ! -name "placeholder.svg"
```

### Step 2: Check Dimensions

For each image:
```bash
sips -g pixelWidth -g pixelHeight [filename]
```

### Step 3: Optimize If Needed

If width > 800 OR height > 800:
```bash
# Get original file size
ls -lh [filename]

# Resize to max 800px (maintains aspect ratio)
sips -Z 800 [filename]

# Get new file size
ls -lh [filename]

# Report optimization
echo "Optimized [filename]: [WxH] → 800px max, [old_size] → [new_size]"
```

Else:
```bash
echo "✓ [filename] - already optimized ([width]x[height])"
```

## Output Format

### Optimized Image Example:
```
Optimized kartoffelpuffer-mit-apfelkompott.png: 2006x1222 → 800px max, 5.2M → 845K
```

### Already Optimized Example:
```
✓ bircher-muesli.jpg - already optimized (800x533)
```

### Summary:
```
## Summary Statistics
- Optimized: 1 image
- Already optimized: 23 images
- Total processed: 24 images
```

## When to Use This Skill

- **After manual image uploads** - When images are added directly to `images/recipes/`
- **After bulk imports** - When importing multiple recipes at once
- **Regular maintenance** - Periodic checks to ensure all images are optimized
- **Before deployment** - Optimize images before pushing to production

**Note**: The `/import-recipe` skill automatically optimizes images during import, so this skill is mainly for:
- Images added manually
- Images that were added before optimization was implemented
- Verifying all images meet the standard

## Technical Details

### Tool: sips (macOS built-in)

`sips` (Scriptable Image Processing System) is built into macOS and requires no installation.

**Key command**: `sips -Z 800 [filename]`
- `-Z`: Resize maintaining aspect ratio
- `800`: Maximum dimension (width or height)
- Operates in-place (replaces original file)

### Supported Formats

- **JPG/JPEG**: Standard format for recipe photos
- **PNG**: For graphics or images requiring transparency
- **Skipped**: placeholder.svg (vector graphic, doesn't need optimization)

### Safety

- **Non-destructive for correct images**: Images already ≤800px are not modified
- **Preserves filenames**: No broken links in YAML files or HTML
- **Maintains aspect ratio**: Images are not stretched or distorted
- **Reports changes**: Clear output shows what was modified

## Example Workflow

```bash
# 1. Add new recipe images manually
cp ~/Downloads/new-recipe.png images/recipes/

# 2. Run optimization
/shrink-images

# Output:
# Optimized new-recipe.png: 1920x1080 → 800px max, 2.1M → 450K

# 3. Verify optimization
ls -lh images/recipes/new-recipe.png
# -rw-r--r--  1 user  staff   450K Feb 24 15:30 new-recipe.png

# 4. Image is now optimized and ready to use
```

## Integration with Other Skills

### Complementary to `/import-recipe`

- `/import-recipe`: Automatically optimizes images during recipe import
- `/shrink-images`: Optimizes existing images that were added manually

### Workflow:

1. **Import recipes**: Use `/import-recipe <URL>` for new recipes
   - Images are automatically optimized during import
2. **Manual images**: When adding images directly, run `/shrink-images`
3. **Verification**: Periodically run `/shrink-images` to ensure all images are optimized

## Benefits

1. **Faster page loads**: Smaller images load significantly faster
2. **Reduced bandwidth**: Lower file sizes save bandwidth for users
3. **Consistent quality**: All images at same max resolution (800px)
4. **No broken links**: In-place optimization preserves file paths
5. **Easy maintenance**: Single command optimizes entire directory

## Performance Impact

### Example Results:
- **Before**: 2006x1222px, 5.2MB
- **After**: 800x487px, 845KB
- **Savings**: 84% file size reduction

### Typical Savings:
- Large photos (2000px+): 70-90% reduction
- Medium photos (1200-2000px): 50-70% reduction
- Already optimized (≤800px): 0% (not modified)

## Error Handling

- **Missing directory**: Reports error if `images/recipes/` doesn't exist
- **Corrupted images**: Skips images that `sips` cannot process
- **Permission errors**: Reports if files cannot be modified
- **No images found**: Reports success with 0 images processed

## Notes

- **macOS only**: Uses `sips` which is macOS-specific
- **Irreversible**: Original oversized images are replaced (keep backups if needed)
- **Quick execution**: Typical runtime for 24 images: ~2-5 seconds
- **Safe to run multiple times**: Already optimized images are skipped
