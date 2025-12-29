"""Script to add pytest markers to test files."""
import re

# Define which tests are core for each file
CORE_TESTS = {
    "test_03_matrix_structure.py": [
        "test_create_base_matrix_size",
        "test_finder_patterns_intact",
        "test_timing_pattern_horizontal",
        "test_timing_pattern_vertical",
        "test_place_data_preserves_reserved",
        "test_is_reserved_dark_module",
        "test_format_bits_length",
        "test_format_coords_primary_length",
    ],
    "test_04_data_placement.py": [
        "test_place_data_shape",
        "test_place_data_starts_bottom_right",
        "test_place_data_skips_reserved",
        "test_place_data_fills_all_available",
        "test_place_data_correct_order",
    ],
    "test_05_masking.py": [
        "test_finalize_matrix_returns_0_1",
        "test_finalize_matrix_shape",
        "test_finalize_matrix_applies_mask",
        "test_apply_mask0_shape",
        "test_apply_mask0_pattern_correct",
        "test_mask_doesnt_corrupt_finders",
        "test_format_bits_written_correctly",
    ],
    "test_06_integration.py": [
        "test_pipeline_hello_produces_valid_matrix",
        "test_pipeline_reproducible",
        "test_format_bits_at_primary_coordinates",
        "test_data_starts_at_bottom_right",
        "test_masking_doesnt_corrupt_finders",
    ],
    "test_07_quality_and_scannability.py": [
        "test_no_uninitialized_cells_in_final_matrix",
        "test_all_required_patterns_present",
        "test_entire_matrix_is_valid_binary",
        "test_same_text_same_output",
    ],
    "test_08_webapp.py": [
        "test_home_page_loads",
        "test_generate_single_qr",
    ],
}

def mark_tests(filename):
    """Add pytest markers to tests in a file."""
    filepath = f"tests/{filename}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    core_tests = CORE_TESTS.get(filename, [])
    
    # Find all test functions
    pattern = r'(^def (test_\w+)\()'
    
    def replace_func(match):
        test_name = match.group(2)
        if test_name in core_tests:
            return f"@pytest.mark.core\n{match.group(1)}"
        else:
            return f"@pytest.mark.optional\n{match.group(1)}"
    
    new_content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
    
    # Also mark class-based tests
    class_pattern = r'(\n    def (test_\w+)\()'
    
    def replace_class_func(match):
        test_name = match.group(2)
        if test_name in core_tests:
            return f"\n    @pytest.mark.core\n    def {test_name}("
        else:
            return f"\n    @pytest.mark.optional\n    def {test_name}("
    
    new_content = re.sub(class_pattern, replace_class_func, new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    core_count = len([t for t in core_tests])
    print(f"✓ {filename}: {core_count} core tests marked")

if __name__ == "__main__":
    for filename in CORE_TESTS.keys():
        mark_tests(filename)
    print("\n✓ All test files marked!")
