"""
LumenQA Test Reporter - Generates test reports
"""

import json
from datetime import datetime
from pathlib import Path


class TestReporter:
    """Handles test result reporting in various formats"""

    def __init__(self, output_dir='lumen-results'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []

    def add_result(self, test_name, status, duration, error=None):
        """Add a test result"""
        self.results.append({
            'test': test_name,
            'status': status,
            'duration': duration,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })

    def generate_json(self):
        """Generate JSON report"""
        report = {
            'framework': 'LumenQA',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': sum(1 for r in self.results if r['status'] == 'passed'),
                'failed': sum(1 for r in self.results if r['status'] == 'failed'),
            },
            'tests': self.results
        }

        output_file = self.output_dir / 'results.json'
        output_file.write_text(json.dumps(report, indent=2))
        return output_file

    def generate_html(self):
        """Generate HTML report"""
        # Simplified HTML report
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>LumenQA Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .passed { color: green; }
                .failed { color: red; }
            </style>
        </head>
        <body>
            <h1>LumenQA Test Results</h1>
            <p>Generated: {timestamp}</p>
            <ul>
        """

        for result in self.results:
            status_class = result['status']
            html += f"""
                <li class="{status_class}">
                    {result['test']} - {result['status']} ({result['duration']}ms)
                </li>
            """

        html += """
            </ul>
        </body>
        </html>
        """

        output_file = self.output_dir / 'results.html'
        output_file.write_text(html.format(timestamp=datetime.now().isoformat()))
        return output_file
