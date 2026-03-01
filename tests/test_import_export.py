"""Tests for import/export functionality across all pages."""

import pytest
from recipe_generator import (
    generate_settings_page_html,
    generate_weekly_html,
    generate_overview_html,
    generate_shopping_list_html,
)


class TestImportExportFunctionality:
    """Test that import/export functionality is consistent across all pages."""

    def test_settings_page_has_export_button(self):
        """Settings page should have export data button."""
        html = generate_settings_page_html()
        assert 'onclick="exportData()"' in html
        assert '📤 Daten als Link exportieren' in html

    def test_settings_page_has_import_modal(self):
        """Settings page should have import modal."""
        html = generate_settings_page_html()
        assert 'id="importModal"' in html
        assert 'Daten importieren' in html
        assert 'onclick="confirmImport()"' in html

    def test_settings_page_has_lzstring_library(self):
        """Settings page should include LZ-String compression library."""
        html = generate_settings_page_html()
        assert 'var LZString=' in html
        assert 'compressToEncodedURIComponent' in html
        assert 'decompressFromEncodedURIComponent' in html

    def test_settings_page_uses_query_parameter_format(self):
        """Settings page should use ?import= query parameter format (not hash)."""
        html = generate_settings_page_html()
        # Check that export creates URL with query parameter
        assert '?import=' in html
        # Check that import reads from query parameter
        assert 'URLSearchParams' in html
        assert "urlParams.get('import')" in html

    def test_settings_page_uses_weeks_data_structure(self):
        """Settings page should use new {weeks: ...} data structure."""
        html = generate_settings_page_html()
        # Check that export creates weeks structure
        assert 'weeks: plans' in html
        # Check that import expects weeks structure
        assert 'data.weeks' in html

    def test_settings_page_has_pending_import_data(self):
        """Settings page should use pendingImportData variable (not window.importData)."""
        html = generate_settings_page_html()
        assert 'let pendingImportData' in html
        assert 'pendingImportData =' in html
        assert 'if (!pendingImportData)' in html

    def test_weekly_page_has_export_functionality(self):
        """Weekly plan page should have export functionality."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]
        html = generate_weekly_html(recipes_data)

        assert 'function exportData()' in html
        assert 'let pendingImportData' in html
        assert 'function checkForImportData()' in html
        assert 'function confirmImport()' in html

    def test_weekly_page_uses_lzstring_compression(self):
        """Weekly plan page should use LZ-String for compression."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]
        html = generate_weekly_html(recipes_data)

        # Check LZ-String library is included
        assert 'var LZString=' in html
        # Check compression is used in export
        assert 'LZString.compressToEncodedURIComponent' in html
        # Check decompression is used in import
        assert 'LZString.decompressFromEncodedURIComponent' in html

    def test_overview_page_has_import_functionality(self):
        """Overview/recipes page should have import functionality."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]
        html = generate_overview_html(recipes_data)

        assert 'let pendingImportData' in html
        assert 'function checkForImportData()' in html
        assert 'function confirmImport()' in html

    def test_shopping_list_page_has_import_functionality(self):
        """Shopping list page should have import functionality."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]
        html = generate_shopping_list_html(recipes_data)

        assert 'let pendingImportData' in html
        assert 'function checkForImportData()' in html
        assert 'function confirmImport()' in html

    def test_all_pages_have_import_modal(self):
        """All pages should have the import modal."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]

        pages = [
            generate_settings_page_html(),
            generate_weekly_html(recipes_data),
            generate_overview_html(recipes_data),
            generate_shopping_list_html(recipes_data),
        ]

        for html in pages:
            assert 'id="importModal"' in html
            assert 'importPreview' in html

    def test_export_data_structure_consistency(self):
        """All pages should export consistent data structure."""
        recipes_data = [
            ('test.html', {
                'name': 'Test Recipe',
                'description': 'Test',
                'category': '🍲',
                'servings': 4,
                'prep_time': 10,
                'cook_time': 20,
                'ingredients': [{'name': 'Test', 'amount': '1'}],
                'instructions': ['Test instruction'],
            })
        ]

        pages = [
            generate_settings_page_html(),
            generate_weekly_html(recipes_data),
            generate_overview_html(recipes_data),
            generate_shopping_list_html(recipes_data),
        ]

        for html in pages:
            # All pages should use the same export structure
            assert 'version: 1' in html
            assert 'exportDate:' in html
            assert 'weeks:' in html

    def test_import_handles_compressed_and_base64(self):
        """Import should handle both LZ-String compressed and base64 fallback."""
        html = generate_settings_page_html()

        # Check for LZ-String handling
        assert "typeof LZString !== 'undefined'" in html
        assert 'LZString.decompressFromEncodedURIComponent' in html

        # Check for base64 fallback
        assert "importParam.startsWith('b64:')" in html
        assert 'atob(base64Data)' in html

    def test_export_creates_valid_url_format(self):
        """Export should create URL in correct format."""
        # Only settings page has export functionality
        html = generate_settings_page_html()

        # Check URL is properly formatted
        assert 'window.location.origin' in html
        assert 'window.location.pathname' in html
        assert '?import=' in html

        # Settings page should redirect to index.html
        assert "replace('settings.html', 'index.html')" in html

    def test_import_clears_url_parameter_after_import(self):
        """Import should clear URL parameter after successful import."""
        html = generate_settings_page_html()

        # Check that URL parameter is removed after import
        assert 'url.searchParams.delete' in html
        assert "delete('import')" in html

    def test_error_handling_for_invalid_import(self):
        """Import should handle errors gracefully."""
        html = generate_settings_page_html()

        # Check error handling
        assert 'try {' in html
        assert 'catch (e)' in html
        assert 'Ungültiger Import-Link' in html or 'Fehler beim Importieren' in html
