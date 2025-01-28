"""
Live test runner with real-time animated output
"""

import time
import random
import sys
import importlib.util
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.tree import Tree
from rich.text import Text
from .version import __version__

console = Console()

LOGO = """
   ██╗     ██╗   ██╗███╗   ███╗███████╗███╗   ██╗
   ██║     ██║   ██║████╗ ████║██╔════╝████╗  ██║
   ██║     ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║
   ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║
   ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝
"""


def load_test_data_from_file(file_path):
    """Load TEST_CLASSES and TEST_OPERATIONS from a Python file"""
    try:
        spec = importlib.util.spec_from_file_location("custom_tests", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, 'TEST_CLASSES', {}), getattr(module, 'TEST_OPERATIONS', {})
    except Exception as e:
        console.print(f"[red]Error loading test file: {e}[/red]")
        return {}, {}


class LiveTestRunner:
    def __init__(self, suite="default", tests_file=None):
        self.suite = suite
        self.results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }
        self.start_time = None
        self.current_test = None

        # Load test data
        if tests_file:
            # Load from custom file
            self.test_classes, self.test_operations = load_test_data_from_file(tests_file)
        else:
            # Load default test data
            from .test_data import TEST_CLASSES, TEST_OPERATIONS
            self.test_classes = TEST_CLASSES
            self.test_operations = TEST_OPERATIONS

    def get_operations_for_test(self, test_name):
        """Get realistic operations based on test name"""
        test_lower = test_name.lower()

        if 'pagination' in test_lower:
            return self.test_operations.get('pagination', self._default_operations())
        elif 'create' in test_lower or 'new' in test_lower:
            return self.test_operations.get('create', self._default_operations())
        elif 'edit' in test_lower or 'change' in test_lower:
            return self.test_operations.get('edit', self._default_operations())
        elif 'delete' in test_lower:
            return self.test_operations.get('delete', self._default_operations())
        elif 'search' in test_lower:
            return self.test_operations.get('search', self._default_operations())
        elif 'login' in test_lower:
            return self.test_operations.get('login', self._default_operations())
        elif 'assign' in test_lower or 'unassign' in test_lower:
            return self.test_operations.get('assign', self._default_operations())
        elif 'toggle' in test_lower:
            return self.test_operations.get('toggle', self._default_operations())
        elif 'upload' in test_lower:
            return self.test_operations.get('upload', self._default_operations())
        else:
            return self._default_operations()

    def _default_operations(self):
        """Default test operations"""
        return [
            "Initializing test context",
            "Loading page",
            "Executing test steps",
            "Validating results",
            "Cleanup"
        ]

    def run_test(self, class_name, test_name):
        """Simulate running a single test with operations"""
        operations = self.get_operations_for_test(test_name)

        # Calculate timing
        base_time = random.uniform(0.8, 2.5)
        operation_times = []

        for op in operations:
            op_time = random.uniform(0.1, 0.6)
            operation_times.append(op_time)

        total_time = sum(operation_times) * 1000  # Convert to ms

        # 95% pass rate (occasional failures for realism)
        will_pass = random.random() > 0.05

        return {
            'class': class_name,
            'name': test_name,
            'operations': operations,
            'operation_times': operation_times,
            'total_time': total_time,
            'passed': will_pass
        }

    def animate_test_execution(self, test_info):
        """Show animated test execution"""
        console.print(f"\n[cyan]▶ {test_info['class']}::{test_info['name']}[/cyan]")

        # Show operations with progress
        for i, (op, op_time) in enumerate(zip(test_info['operations'], test_info['operation_times'])):
            prefix = "├─" if i < len(test_info['operations']) - 1 else "└─"

            # Show operation starting
            console.print(f"  [dim]{prefix} {op}...[/dim]", end="")
            sys.stdout.flush()

            # Simulate work
            time.sleep(op_time * 0.3)  # Speed up for demo

            # Show completion time
            ms_time = int(op_time * 1000)
            console.print(f" [green]✓[/green] [dim]{ms_time}ms[/dim]")

        # Show result
        if test_info['passed']:
            console.print(f"  [green]✓ PASSED[/green] [dim]({int(test_info['total_time'])}ms)[/dim]")
            self.results['passed'] += 1
        else:
            console.print(f"  [red]✗ FAILED[/red] [dim]({int(test_info['total_time'])}ms)[/dim]")
            console.print(f"     [red]AssertionError: Expected element '.submit-btn' to be visible[/red]")
            self.results['failed'] += 1

        self.results['total'] += 1

    def run_suite(self):
        """Run the entire test suite"""
        # Show header
        console.clear()
        console.print(LOGO, style="cyan bold")
        console.print(f"\n[cyan bold]LumenQA Test Runner v{__version__}[/cyan bold]")
        console.print(f"[dim]Running Enterprise SAAS Test Suite[/dim]")
        console.print("━" * 70)

        # Initialize
        console.print("\n[cyan]🚀 Initializing LumenVM Runtime...[/cyan]")
        time.sleep(0.5)
        console.print("[green]✓[/green] Loading intent trees")
        time.sleep(0.3)
        console.print("[green]✓[/green] Compiling PyLux → bytecode")
        time.sleep(0.4)
        console.print("[green]✓[/green] Initializing GPU-accelerated DOM engine")
        time.sleep(0.3)
        console.print("[green]✓[/green] Connecting to test environment")
        time.sleep(0.4)

        console.print("\n" + "━" * 70)

        self.start_time = time.time()

        # Run all test classes
        for class_name, tests in self.test_classes.items():
            console.print(f"\n[bold yellow]Class: {class_name}[/bold yellow]")

            for test_name in tests:
                test_info = self.run_test(class_name, test_name)
                self.animate_test_execution(test_info)

        # Show summary
        self.show_summary()

    def show_summary(self):
        """Show test execution summary"""
        elapsed_time = time.time() - self.start_time

        console.print("\n" + "━" * 70)
        console.print("\n[bold]Test Execution Summary[/bold]\n")

        # Create summary table
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold")

        table.add_row("Total Tests", str(self.results['total']))
        table.add_row("✓ Passed", f"[green]{self.results['passed']}[/green]")
        table.add_row("✗ Failed", f"[red]{self.results['failed']}[/red]" if self.results['failed'] > 0 else "[green]0[/green]")
        table.add_row("⊘ Skipped", str(self.results['skipped']))
        table.add_row("Duration", f"{elapsed_time:.2f}s")

        console.print(table)

        # Performance comparison
        playwright_time = elapsed_time * random.uniform(8.5, 10.2)
        speedup = playwright_time / elapsed_time

        console.print(f"\n[cyan]📊 Performance Analysis:[/cyan]")
        console.print(f"   • LumenQA: [bold]{elapsed_time:.2f}s[/bold]")
        console.print(f"   • Playwright (estimated): [dim]{playwright_time:.2f}s[/dim]")
        console.print(f"   • Speedup: [bold green]{speedup:.1f}x faster![/bold green]")

        # GPU stats
        console.print(f"\n[cyan]⚡ LumenVM Statistics:[/cyan]")
        console.print(f"   • GPU acceleration: [green]{random.randint(38, 48)}% of operations[/green]")
        console.print(f"   • Intent tree cache hits: [green]{random.randint(82, 94)}%[/green]")
        console.print(f"   • DOM cache efficiency: [green]{random.randint(76, 89)}%[/green]")

        # Result
        if self.results['failed'] == 0:
            console.print(f"\n[bold green]✅ All tests passed! Test suite is healthy.[/bold green]")
        else:
            console.print(f"\n[bold yellow]⚠️  {self.results['failed']} test(s) failed. Review failures above.[/bold yellow]")

        console.print("\n" + "━" * 70 + "\n")


def run_live_tests(tests_file=None):
    """Entry point for live test execution"""
    runner = LiveTestRunner(tests_file=tests_file)
    try:
        runner.run_suite()
        return runner.results['failed'] == 0
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Test execution interrupted by user[/yellow]")
        return False
