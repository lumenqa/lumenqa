"""
PyLux Parser - Parses .lux test files
"""

import re
from pathlib import Path


def parse_lux_file(file_path):
    """
    Parse a .lux file and extract test definitions

    Returns a list of test objects with name and steps
    """
    try:
        content = Path(file_path).read_text()
    except Exception as e:
        return [{"name": f"Failed to read {file_path}", "steps": []}]

    tests = []

    # Simple regex to find test blocks
    # Format: test "Test Name":
    test_pattern = r'test\s+"([^"]+)":\s*\n((?:    .+\n?)*)'
    matches = re.finditer(test_pattern, content, re.MULTILINE)

    for match in matches:
        test_name = match.group(1)
        test_body = match.group(2)

        # Extract steps (lines with indentation)
        steps = []
        for line in test_body.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract the command (first word)
                steps.append(line)

        tests.append({
            'name': test_name,
            'steps': steps
        })

    return tests if tests else [{"name": Path(file_path).stem, "steps": []}]
