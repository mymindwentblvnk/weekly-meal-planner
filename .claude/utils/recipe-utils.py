"""
Utility scripts for recipe validation and manipulation.

These scripts can be used by agents for common recipe operations.
"""

import yaml
from pathlib import Path


# ============ SORTING FUNCTIONS ============

def german_sort_key(s):
    """
    German alphabetical sorting key (DIN 5007-1).
    Treats ä as a, ö as o, ü as u, ß as ss for alphabetical ordering.

    Args:
        s: String to generate sort key for

    Returns:
        Normalized string for sorting
    """
    s = s.lower()
    s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('ß', 'ss')
    return s


# ============ TAG VALIDATION ============

def check_tag_sorting(recipe_file):
    """
    Check if tags in a recipe file are sorted alphabetically.

    Args:
        recipe_file: Path to recipe YAML file

    Returns:
        dict with 'sorted' (bool), 'current' (list), 'should_be' (list)
    """
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)

    if 'tags' not in recipe or not recipe['tags']:
        return {'sorted': True, 'current': [], 'should_be': []}

    tags = recipe['tags']
    sorted_tags = sorted(tags, key=german_sort_key)

    return {
        'sorted': tags == sorted_tags,
        'current': tags,
        'should_be': sorted_tags
    }


def find_unsorted_tags(recipes_dir='recipes'):
    """
    Find all recipe files with unsorted tags.

    Args:
        recipes_dir: Directory to search for recipe YAML files

    Returns:
        List of dicts with file path and tag info
    """
    recipe_files = list(Path(recipes_dir).rglob('*.yaml'))
    unsorted_files = []

    for recipe_file in recipe_files:
        try:
            result = check_tag_sorting(recipe_file)
            if not result['sorted']:
                unsorted_files.append({
                    'file': str(recipe_file),
                    'current': result['current'],
                    'sorted': result['should_be']
                })
        except Exception as e:
            print(f"Error checking {recipe_file}: {e}")

    return unsorted_files


def sort_recipe_tags(recipe_file):
    """
    Sort tags in a recipe file alphabetically and save.

    Args:
        recipe_file: Path to recipe YAML file

    Returns:
        bool indicating if file was modified
    """
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)

    if 'tags' not in recipe or not recipe['tags']:
        return False

    original_tags = recipe['tags']
    sorted_tags = sorted(original_tags, key=german_sort_key)

    if original_tags == sorted_tags:
        return False

    recipe['tags'] = sorted_tags

    with open(recipe_file, 'w', encoding='utf-8') as f:
        yaml.dump(recipe, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    return True


# ============ HIERARCHICAL TAG VALIDATION ============

# Hierarchical tag rules
HIERARCHICAL_TAGS = {
    'fish': {
        'generic': 'Fisch',
        'specific': ['Lachs', 'Thunfisch', 'Seelachs', 'Garnelen']
    },
    'meat': {
        'generic': 'Fleisch',
        'specific': ['Rind', 'Pute', 'Schinken', 'Hackfleisch']
    },
    'cheese': {
        'generic': 'Käse',
        'specific': ['Feta', 'Schafskäse', 'Parmesan', 'Bergkäse', 'Frischkäse']
    },
    'nuts': {
        'generic': 'Nüsse',
        'specific': ['Walnüsse', 'Haselnüsse', 'Mandeln']
    },
    'berries': {
        'generic': 'Beeren',
        'specific': ['Himbeeren', 'Erdbeeren']
    },
    'fruit': {
        'generic': 'Obst',
        'specific': ['Apfel', 'Kiwi', 'Weintrauben']
    },
    'seeds': {
        'generic': 'Kerne',
        'specific': ['Chiasamen', 'Leinsamen', 'Sesam']
    },
    'cabbage': {
        'generic': 'Kohl',
        'specific': ['Blumenkohl', 'Brokkoli']
    },
    'potatoes': {
        'generic': 'Kartoffeln',
        'specific': ['Süßkartoffel']
    }
}


def check_hierarchical_tags(recipe_file):
    """
    Check if recipe has proper hierarchical tags.

    Args:
        recipe_file: Path to recipe YAML file

    Returns:
        List of missing generic tags
    """
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)

    if 'tags' not in recipe or not recipe['tags']:
        return []

    tags = set(recipe['tags'])
    missing_generic = []

    for category, rules in HIERARCHICAL_TAGS.items():
        generic = rules['generic']
        specific_tags = rules['specific']

        # Check if recipe has any specific tag from this category
        has_specific = any(tag in tags for tag in specific_tags)
        has_generic = generic in tags

        if has_specific and not has_generic:
            # Find which specific tags are present
            present_specific = [tag for tag in specific_tags if tag in tags]
            missing_generic.append({
                'category': category,
                'generic': generic,
                'specific_found': present_specific
            })

    return missing_generic



def check_description(recipe_file):
    """
    Check if a recipe has a valid description.

    Args:
        recipe_file: Path to recipe YAML file

    Returns:
        dict with 'has_description' (bool) and 'description' (str or None)
    """
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)

    has_description = 'description' in recipe
    description = recipe.get('description', None)

    # Check if description is empty or placeholder
    is_valid = (has_description and
                description and
                description.strip() and
                description.lower() not in ['tbd', 'todo', 'placeholder'])

    return {
        'has_description': is_valid,
        'description': description
    }


def check_tags_exist(recipe_file):
    """
    Check if a recipe has tags field.

    Args:
        recipe_file: Path to recipe YAML file

    Returns:
        dict with 'has_tags' (bool) and 'tags' (list or None)
    """
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = yaml.safe_load(f)

    has_tags = 'tags' in recipe and recipe['tags']

    return {
        'has_tags': has_tags,
        'tags': recipe.get('tags', None)
    }


def validate_all_recipes(recipes_dir='recipes'):
    """
    Validate all recipes for quality issues (tags, hierarchical tags, costs, descriptions).

    Args:
        recipes_dir: Directory to search for recipe YAML files

    Returns:
        dict with validation results
    """
    recipe_files = list(Path(recipes_dir).rglob('*.yaml'))
    results = {
        'total': len(recipe_files),
        'missing_description': [],
        'missing_tags': [],
        'unsorted_tags': [],
        'missing_hierarchical': [],
        'valid': []
    }

    for recipe_file in recipe_files:
        try:
            # Check description
            desc_check = check_description(recipe_file)
            if not desc_check['has_description']:
                results['missing_description'].append(str(recipe_file))

            # Check tags exist
            tags_check = check_tags_exist(recipe_file)
            if not tags_check['has_tags']:
                results['missing_tags'].append(str(recipe_file))

            # Check tag sorting (only if tags exist)
            sort_check = check_tag_sorting(recipe_file)
            if tags_check['has_tags'] and not sort_check['sorted']:
                results['unsorted_tags'].append({
                    'file': str(recipe_file),
                    'current': sort_check['current'],
                    'should_be': sort_check['should_be']
                })

            # Check hierarchical tags (only if tags exist)
            if tags_check['has_tags']:
                missing = check_hierarchical_tags(recipe_file)
                if missing:
                    results['missing_hierarchical'].append({
                        'file': str(recipe_file),
                        'missing': missing
                    })
            else:
                missing = []

            # If all checks pass, add to valid
            if (desc_check['has_description'] and
                tags_check['has_tags'] and
                sort_check['sorted'] and
                not missing):
                results['valid'].append(str(recipe_file))

        except Exception as e:
            print(f"Error validating {recipe_file}: {e}")

    return results


# ============ USAGE EXAMPLES ============

if __name__ == '__main__':
    # Example 1: Check tag sorting for all recipes
    print("=== Checking tag sorting ===")
    unsorted = find_unsorted_tags()
    if unsorted:
        print(f"Found {len(unsorted)} recipes with unsorted tags:")
        for item in unsorted:
            print(f"  {item['file']}")
    else:
        print("✓ All recipes have properly sorted tags!")

    # Example 2: Validate all recipes
    print("\n=== Full validation ===")
    results = validate_all_recipes()
    print(f"Total recipes: {results['total']}")
    print(f"Valid recipes: {len(results['valid'])}")
    print(f"Recipes missing description: {len(results['missing_description'])}")
    print(f"Recipes missing tags: {len(results['missing_tags'])}")
    print(f"Recipes with unsorted tags: {len(results['unsorted_tags'])}")
    print(f"Recipes missing hierarchical tags: {len(results['missing_hierarchical'])}")

    if results['missing_description']:
        print("\nMissing description:")
        for file in results['missing_description']:
            print(f"  {file}")

    if results['missing_tags']:
        print("\nMissing tags:")
        for file in results['missing_tags']:
            print(f"  {file}")

    if results['missing_hierarchical']:
        print("\nMissing hierarchical tags:")
        for item in results['missing_hierarchical']:
            print(f"  {item['file']}:")
            for missing in item['missing']:
                print(f"    - Missing '{missing['generic']}' (has {missing['specific_found']})")
