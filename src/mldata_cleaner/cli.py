import click
from rich.console import Console
from rich.table import Table
from .inspector import DataInspector

console = Console()

@click.group()
def cli():
    """ML Data Cleaning Toolkit - Inspect and clean your datasets with ease"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--detailed', '-d', is_flag=True, help='Show detailed statistics')
def inspect(file_path, detailed):
    """Analyze dataset for quality issues and missing values"""
    inspector = DataInspector(file_path)
    report = inspector.generate_report(detailed=detailed)
    
    # Display missing values
    table = Table(title="Missing Values Summary")
    table.add_column("Column")
    table.add_column("Missing Count")
    table.add_column("Missing Percentage")
    
    for col, stats in report['missing_values'].items():
        table.add_row(
            col,
            str(stats['count']),
            f"{stats['percentage']:.2f}%"
        )
    
    console.print(table)

if __name__ == '__main__':
    cli()