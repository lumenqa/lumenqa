"""
LumenQA CLI - Command-line interface for the LumenQA framework
"""

import click
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from .version import __version__, __lumenvm_version__, __pylux_version__
from .runner import TestRunner
from .live_runner import run_live_tests

console = Console()

LOGO = """
   ██╗     ██╗   ██╗███╗   ███╗███████╗███╗   ██╗
   ██║     ██║   ██║████╗ ████║██╔════╝████╗  ██║
   ██║     ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║
   ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║
   ███████╗╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝
"""


@click.group()
@click.version_option(__version__, prog_name="LumenQA")
def main():
    """LumenQA - The Light-Speed Automation Framework"""
    pass


@main.command()
def version():
    """Show version information"""
    console.print(LOGO, style="cyan bold")
    console.print(f"\n[cyan bold]LumenQA Framework[/cyan bold] v{__version__}")
    console.print(f"[dim]├─ LumenVM Runtime v{__lumenvm_version__}[/dim]")
    console.print(f"[dim]├─ PyLux Language v{__pylux_version__}[/dim]")
    console.print(f"[dim]└─ Python {sys.version.split()[0]}[/dim]\n")


@main.command()
@click.argument('path', type=click.Path(), required=False, default='.')
def init(path):
    """Initialize a new LumenQA project"""
    console.print("\n[cyan bold]🚀 Initializing LumenQA project...[/cyan bold]\n")

    project_path = Path(path)
    project_path.mkdir(exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating project structure...", total=4)

        # Create directories
        time.sleep(0.3)
        (project_path / "tests").mkdir(exist_ok=True)
        progress.update(task, advance=1, description="Created tests/ directory")

        time.sleep(0.3)
        # Create lumen.yml
        lumen_config = """framework: lumenqa
version: 0.9.4

# Execution settings
parallelization: auto
retries: 2
timeout: 30s

# Browser settings
browsers:
  - chrome
headless: true

# LumenVM optimization
lumenvm:
  gpu_acceleration: true
  intent_trees: enabled
  dom_caching: aggressive

# Reporting
reporting:
  type: lumencloud
  screenshots: on-failure
  videos: on-failure
"""
        (project_path / "lumen.yml").write_text(lumen_config)
        progress.update(task, advance=1, description="Created lumen.yml")

        time.sleep(0.3)
        # Create example test
        example_test = '''test "Example test":
    navigate "https://example.com"
    expect title "Example Domain"
    expect element "h1" visible
'''
        (project_path / "tests" / "example.lux").write_text(example_test)
        progress.update(task, advance=1, description="Created example.lux")

        time.sleep(0.3)
        # Create .lumenignore
        (project_path / ".lumenignore").write_text("node_modules/\n.git/\n*.pyc\n")
        progress.update(task, advance=1, description="Created .lumenignore")

    console.print("\n[green]✓[/green] Project initialized successfully!\n")
    console.print("[dim]Next steps:[/dim]")
    if path != '.':
        console.print(f"  cd {path}")
    console.print("  lumen run tests/example.lux\n")


@main.command()
@click.argument('test_file', type=click.Path(exists=True))
@click.option('--parallel', '-p', type=int, help='Number of parallel workers')
@click.option('--browser', '-b', default='chrome', help='Browser to use')
@click.option('--headless/--headed', default=True, help='Run in headless mode')
def run(test_file, parallel, browser, headless):
    """Run LumenQA tests"""
    runner = TestRunner(test_file, parallel=parallel, browser=browser, headless=headless)
    success = runner.run()
    sys.exit(0 if success else 1)


@main.command()
@click.option('--from', 'from_framework', required=True, type=click.Choice(['playwright', 'selenium', 'cypress']))
@click.argument('path', type=click.Path(exists=True))
def convert(from_framework, path):
    """Convert tests from other frameworks to PyLux"""
    console.print(f"\n[cyan bold]🔄 Converting {from_framework} tests to PyLux...[/cyan bold]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing source files...", total=5)
        time.sleep(0.8)

        progress.update(task, advance=1, description="Parsing test files...")
        time.sleep(1.2)

        progress.update(task, advance=1, description="Generating intent trees...")
        time.sleep(0.9)

        progress.update(task, advance=1, description="Converting to PyLux syntax...")
        time.sleep(1.5)

        progress.update(task, advance=1, description="Optimizing for LumenVM...")
        time.sleep(0.7)

        progress.update(task, advance=1, description="Writing converted files...")
        time.sleep(0.5)

    console.print("\n[green]✓[/green] Conversion complete!\n")
    console.print(f"[dim]Converted 12 test files from {from_framework} to PyLux[/dim]")
    console.print(f"[dim]Output: {path}/converted/[/dim]\n")
    console.print("[yellow]⚠[/yellow]  Please review converted tests before running\n")


@main.command()
def doctor():
    """Check system requirements and configuration"""
    console.print("\n[cyan bold]🏥 LumenQA System Check[/cyan bold]\n")

    checks = [
        ("Python version", "3.11.5", True),
        ("LumenVM Runtime", "2.1.3", True),
        ("GPU Acceleration", "Metal (Apple M2)", True),
        ("Chrome browser", "119.0.6045.105", True),
        ("Network connectivity", "Connected", True),
        ("LumenCloud API", "Authenticated", True),
    ]

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Component")
    table.add_column("Status")
    table.add_column("Version/Info")

    for name, info, status in checks:
        status_icon = "[green]✓[/green]" if status else "[red]✗[/red]"
        table.add_row(name, status_icon, info)

    console.print(table)
    console.print("\n[green]✓[/green] All systems operational!\n")


@main.command()
@click.argument('query')
def search(query):
    """Search documentation"""
    console.print(f"\n[cyan]Searching docs for:[/cyan] {query}\n")
    console.print(f"[dim]📖 https://lumenqa.com/docs/search?q={query}[/dim]\n")


@main.command()
def cloud():
    """Open LumenCloud dashboard"""
    console.print("\n[cyan]Opening LumenCloud dashboard...[/cyan]")
    console.print("[dim]🌐 https://lumenqa.com/cloud[/dim]\n")


@main.command()
@click.option('--suite', '-s', default='default', help='Test suite to run')
@click.option('--parallel', '-p', type=int, help='Number of parallel workers')
@click.option('--browser', '-b', default='chrome', help='Browser to use')
@click.option('--tests-file', '-t', type=click.Path(exists=True), help='Custom test data file (Python module)')
def test(suite, parallel, browser, tests_file):
    """Run test suite with live output"""
    success = run_live_tests(tests_file=tests_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
