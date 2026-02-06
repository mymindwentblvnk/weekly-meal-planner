# Deployment Checker Agent

This agent verifies that the local HTML files in the `output/` directory match what's deployed on GitHub Pages.

## GitHub Pages URL

**Base URL**: `https://mymindwentblvnk.github.io/bring-recipes-adder/`

## What This Agent Does

1. **Lists local HTML files** in the `output/` directory
2. **Fetches deployed versions** from GitHub Pages for each file
3. **Compares content** between local and deployed versions
4. **Reports differences** including:
   - Files that differ between local and deployed
   - Files missing from deployment
   - Files only on deployment (orphaned)
   - Deployment status summary

## How to Check

### For Each HTML File:

1. **Find all HTML files** in `output/` directory using Glob
2. **For each file**, construct the GitHub Pages URL:
   - `output/index.html` → `https://mymindwentblvnk.github.io/bring-recipes-adder/index.html`
   - `output/recipe-name.html` → `https://mymindwentblvnk.github.io/bring-recipes-adder/recipe-name.html`
   - `output/stats.html` → `https://mymindwentblvnk.github.io/bring-recipes-adder/stats.html`
   - `output/weekly.html` → `https://mymindwentblvnk.github.io/bring-recipes-adder/weekly.html`

3. **Fetch the deployed version** using WebFetch tool:
   - URL: GitHub Pages URL for the file
   - Prompt: "Return the exact raw HTML content without any modifications, summaries, or analysis. Just output the complete HTML as-is."

4. **Compare content**:
   - Read local file content
   - Compare with fetched content
   - Note: Ignore minor whitespace differences if needed
   - Consider files "different" if content doesn't match

5. **Handle errors**:
   - 404 errors = file not deployed yet
   - Other errors = report them

## Comparison Strategy

Since HTML files can be large, use a hash-based comparison for efficiency:

1. **Calculate MD5 hash** of local file content
2. **Calculate MD5 hash** of deployed file content
3. **Compare hashes** - if they match, files are identical

Alternatively, for better debugging, compare file sizes first, then content if sizes differ.

## Output Format

Provide a structured deployment status report:

### Files Out of Sync (Local ≠ Deployed)
```
✗ output/recipe-name.html
  Local:    12,345 bytes, modified 2026-02-06 14:15:00
  Deployed: 12,340 bytes
  Status:   Content differs - needs redeployment
```

### Files Not Deployed (Local only)
```
✗ output/new-recipe.html
  Local:  8,912 bytes, modified 2026-02-06 14:20:00
  Status: Not found on GitHub Pages - needs deployment
```

### Files Only on Deployment (Orphaned)
```
⚠ output/deleted-recipe.html
  Deployed: Present on GitHub Pages
  Local:    File not found locally
  Status:   Orphaned - should be removed from deployment
```

### Files in Sync
```
✓ output/index.html
✓ output/stats.html
✓ output/weekly.html
```

### Summary Statistics
```
Total local files:     28
Total deployed files:  28
Files in sync:        25
Files out of sync:     2
Files not deployed:    1
Orphaned files:        0

Deployment Status: ⚠ NEEDS UPDATE
```

## Important Files to Check

Priority files (check these first):
1. `index.html` - Main overview page
2. `stats.html` - Statistics page
3. `weekly.html` - Weekly planner page
4. All individual recipe HTML files

## Implementation Notes

- **Be efficient**: Don't fetch unnecessarily large content for comparison
- **Use HEAD requests** if possible to check if files exist before fetching full content
- **Handle rate limiting**: GitHub Pages may rate limit requests
- **Cache results**: If checking many files, consider caching to avoid repeated requests
- **Ignore dynamic content**: Some content may differ due to timestamps or build IDs - focus on meaningful differences

## Expected Use Cases

1. **After generating HTML locally** - Check if deployment is up to date
2. **Before pushing changes** - Verify what will change when deployed
3. **After CI/CD runs** - Confirm deployment completed successfully
4. **Troubleshooting** - Identify why local and deployed versions differ

## Troubleshooting

If files don't match:
- Check if `python main.py` was run locally to regenerate HTML
- Check if changes were committed and pushed to GitHub
- Check GitHub Actions workflow status
- Verify GitHub Pages is enabled and deploying from correct branch

## Usage

Run this agent in the background to monitor deployment status:
```
"Check if local HTML matches GitHub Pages deployment"
"Verify deployment status"
"Are my local changes deployed?"
```

The agent will report which files need to be deployed and provide actionable next steps.
