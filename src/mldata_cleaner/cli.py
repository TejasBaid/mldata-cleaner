import click
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint
from .inspector import DataInspector
from .cleaner import DataCleaner
import pandas as pd

console = Console()

HELP_TEXT = """
# ML Data Cleaner Commands

## Basic Commands
* `inspect <file>` - Show basic dataset information
* `clean <file> <output>` - Clean dataset with specified options
* `interactive <file>` - Start interactive cleaning session

## Inspection Commands
* `missing <file>` - Show missing value analysis
* `duplicates <file>` - Show duplicate records
* `stats <file>` - Show basic statistics
* `types <file>` - Show column data types

## Cleaning Commands
* `fix-missing <file> <output> --strategy <strategy>` - Fix missing values
* `remove-duplicates <file> <output>` - Remove duplicate records
* `handle-outliers <file> <output> --column <col> --method <method>` - Remove outliers
* `convert-type <file> <output> --column <col> --type <type>` - Convert column type

## Options
* `--strategy`: mean, median, mode, constant, drop
* `--method`: iqr, zscore
* `--type`: int, float, str, datetime, category
"""

def display_missing_values(missing_values):
    """Display missing values in a tabular format"""
    table = Table(title="Missing Value Analysis")
    table.add_column("Column", style="cyan", justify="left")
    table.add_column("Missing Count", style="magenta", justify="right")
    
    for column, missing_count in missing_values.items():
        table.add_row(column, str(missing_count))
    
    console.print(table)

def display_data_types(data_types):
    """Display column data types"""
    table = Table(title="Data Types")
    table.add_column("Column", style="cyan", justify="left")
    table.add_column("Data Type", style="magenta", justify="left")
    
    for column, dtype in data_types.items():
        table.add_row(column, str(dtype))
    
    console.print(table)

def display_duplicates(duplicate_stats):
    """Display duplicate analysis"""
    table = Table(title="Duplicate Analysis")
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Value", style="magenta", justify="right")
    
    table.add_row("Total Duplicates", str(duplicate_stats['total_duplicates']))
    table.add_row("Percentage of Duplicates", f"{duplicate_stats['percentage']:.2f}%")
    
    console.print(table)

def display_statistics(statistics):
    """Display dataset statistics"""
    table = Table(title="Dataset Statistics")
    table.add_column("Statistic", style="cyan", justify="left")
    for column in statistics.keys():
        table.add_column(column, style="magenta", justify="right")
    
    stats_to_show = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    
    for stat in stats_to_show:
        row = [stat]
        for column, column_stats in statistics.items():
            row.append(f"{column_stats.get(stat, 'N/A'):.2f}" if isinstance(column_stats.get(stat), (int, float)) else "N/A")
        table.add_row(*row)
    
    console.print(table)


def print_menu(title, options):
    """Print a numbered menu"""
    console.print(f"\n[bold blue]{title}[/bold blue]")
    for idx, (key, label) in enumerate(options.items(), 1):
        console.print(f"{idx}. {label}")
    return {str(idx): key for idx, (key, _) in enumerate(options.items(), 1)}

def get_menu_choice(menu_map):
    """Get user choice from menu"""
    while True:
        choice = Prompt.ask("Enter your choice (number or command)")
        if choice in menu_map:
            return menu_map[choice]
        if choice in menu_map.values():
            return choice
        console.print("[red]Invalid choice. Please try again.[/red]")
def print_column_types(cleaner, columns):
        """Print column types and relevant metadata"""
        from rich.table import Table
        from rich.console import Console

        console = Console()
        table = Table(title="Column Data Types")

        table.add_column("Column", style="cyan", justify="left")
        table.add_column("Type", style="magenta", justify="left")
        table.add_column("Sample Value", style="green", justify="left")

        for column in columns:
            col_type = cleaner.get_column_type(column)
            sample_value = cleaner.get_column_sample(column)
            table.add_row(column, str(col_type), str(sample_value))

        console.print(table)

@click.group()
def cli():
    """ML Data Cleaning Toolkit - Clean and prepare your data with ease"""
    pass

@cli.command()
def help():
    """Show detailed help and all available commands"""
    console.print(Markdown(HELP_TEXT))

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def interactive(file_path):
    """Start interactive data cleaning session"""
    console.print("[bold green]Welcome to Interactive Data Cleaning! 🎉[/bold green]")
    
    try:
        inspector = DataInspector(file_path)
        cleaner = DataCleaner(file_path)
    except Exception as e:
        console.print(f"[red]Error loading file: {e}[/red]")
        return

    show_data_overview(inspector)

    while True:
        main_menu = {
            "inspect": "Inspect Data",
            "clean": "Clean Data",
            "save": "Save Dataset",
            "help": "Show Help",
            "exit": "Exit"
        }
        menu_map = print_menu("Main Menu", main_menu)
        choice = get_menu_choice(menu_map)

        if choice == "inspect":
            handle_inspection(inspector)
        elif choice == "clean":
            handle_cleaning(cleaner)
        elif choice == "save":
            output_path = Prompt.ask("Enter path to save cleaned dataset")
            try:
                cleaner.save(output_path)
                console.print(f"[green]Dataset saved to {output_path}[/green]")
            except Exception as e:
                console.print(f"[red]Error saving file: {e}[/red]")
        elif choice == "help":
            console.print(Markdown(HELP_TEXT))
        elif choice == "exit":
            if Confirm.ask("Are you sure you want to exit?"):
                break

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def missing(file_path):
    """Show missing value analysis"""
    try:
        inspector = DataInspector(file_path)
        display_missing_values(inspector.analyze_missing_values())
    except Exception as e:
        console.print(f"[red]Error analyzing missing values: {e}[/red]")

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def duplicates(file_path):
    """Show duplicate records analysis"""
    try:
        inspector = DataInspector(file_path)
        display_duplicates(inspector.analyze_duplicates())
    except Exception as e:
        console.print(f"[red]Error analyzing duplicates: {e}[/red]")

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--strategy', type=click.Choice(['mean', 'median', 'mode', 'constant', 'drop']), required=True)
@click.option('--columns', '-c', multiple=True)
@click.option('--value', help='Constant value for filling missing data')
def fix_missing(file_path, output_file, strategy, columns, value):
    """Fix missing values in the dataset"""
    try:
        cleaner = DataCleaner(file_path)
        cleaner.handle_missing_values(strategy, columns, value)
        cleaner.save(output_file)
        console.print("[green]Missing values handled successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error fixing missing values: {e}[/red]")

def handle_inspection(inspector):
    """Handle inspection menu options"""
    inspection_menu = {
        "missing": "Check Missing Values",
        "types": "View Data Types",
        "dupes": "Find Duplicates",
        "stats": "View Statistics",
        "back": "Back to Main Menu"
    }

    while True:
        menu_map = print_menu("Inspection Options", inspection_menu)
        choice = get_menu_choice(menu_map)

        if choice == "missing":
            display_missing_values(inspector.analyze_missing_values())
        elif choice == "types":
            display_data_types(inspector.get_data_types())
        elif choice == "dupes":
            display_duplicates(inspector.analyze_duplicates())
        elif choice == "stats":
            display_statistics(inspector.get_statistics())
        elif choice == "back":
            break

def handle_cleaning(cleaner):
    """Handle cleaning menu options"""
    cleaning_menu = {
        "missing": "Handle Missing Values",
        "dupes": "Remove Duplicates",
        "outliers": "Handle Outliers",
        "types": "Convert Data Types",
        "back": "Back to Main Menu"
    }

    while True:
        menu_map = print_menu("Cleaning Options", cleaning_menu)
        choice = get_menu_choice(menu_map)

        if choice == "missing":
            handle_missing_values_cleaning(cleaner)
        elif choice == "dupes":
            handle_duplicates_cleaning(cleaner)
        elif choice == "outliers":
            handle_outliers_cleaning(cleaner)
        elif choice == "types":
            handle_datatype_conversion(cleaner)
        elif choice == "back":
            break

def handle_missing_values_cleaning(cleaner):
    """Interactive missing values handling"""
    strategy_menu = {
        "mean": "Replace with Mean (numeric only)",
        "median": "Replace with Median (numeric only)",
        "mode": "Replace with Mode",
        "constant": "Replace with Constant Value",
        "drop": "Drop Rows with Missing Values",
        "back": "Back to Cleaning Menu"
    }

    menu_map = print_menu("Select Missing Values Strategy", strategy_menu)
    strategy = get_menu_choice(menu_map)

    if strategy == "back":
        return

    columns = cleaner.get_columns_with_missing()
    if not columns:
        console.print("[yellow]No missing values found![/yellow]")
        return

    print_column_stats(cleaner, columns)
    selected_cols = select_columns(columns)

    if strategy == "constant":
        value = Prompt.ask("Enter value to fill missing data")
        cleaner.handle_missing_values(strategy, selected_cols, value)
    else:
        cleaner.handle_missing_values(strategy, selected_cols)

    console.print("[green]Missing values handled successfully![/green]")

def handle_duplicates_cleaning(cleaner):
    """Interactive duplicate handling"""
    count = cleaner.count_duplicates()
    if count == 0:
        console.print("[yellow]No duplicates found![/yellow]")
        return

    console.print(f"Found {count} duplicate rows")
    if Confirm.ask("Would you like to remove them?"):
        cleaner.remove_duplicates()
        console.print("[green]Duplicates removed successfully![/green]")

def handle_outliers_cleaning(cleaner):
    """Interactive outlier handling"""
    columns = cleaner.get_numerical_columns()
    if not columns:
        console.print("[yellow]No numerical columns found![/yellow]")
        return

    print_column_stats(cleaner, columns)
    selected_col = select_columns(columns, single=True)

    method_menu = {
        "iqr": "IQR Method (1.5 * IQR)",
        "zscore": "Z-Score Method (3 std dev)",
        "back": "Back to Cleaning Menu"
    }

    menu_map = print_menu("Select Outlier Detection Method", method_menu)
    method = get_menu_choice(menu_map)

    if method == "back":
        return

    threshold = float(Prompt.ask(
        "Enter threshold value",
        default="1.5" if method == "iqr" else "3"
    ))

    removed = cleaner.handle_outliers(selected_col, method, threshold)
    console.print(f"[green]Removed {removed} outliers from {selected_col}[/green]")

def handle_datatype_conversion(cleaner):
    """Interactive data type conversion"""
    columns = cleaner.get_columns()
    print_column_types(cleaner, columns)
    selected_col = select_columns(columns, single=True)

    type_menu = {
        "int": "Integer",
        "float": "Float",
        "str": "String",
        "datetime": "DateTime",
        "category": "Categorical",
        "back": "Back to Column Selection"
    }

    menu_map = print_menu("Select New Data Type", type_menu)
    new_type = get_menu_choice(menu_map)

    if new_type == "back":
        return

    try:
        cleaner.convert_dtype(selected_col, new_type)
        console.print(f"[green]Successfully converted {selected_col} to {new_type}[/green]")
    except Exception as e:
        console.print(f"[red]Error converting type: {str(e)}[/red]")

def print_column_stats(cleaner, columns):
    """Print column statistics"""
    table = Table(title="Column Statistics")
    table.add_column("Column")
    table.add_column("Type")
    table.add_column("Missing")
    table.add_column("Unique Values")

    for col in columns:
        stats = cleaner.get_column_stats(col)
        table.add_row(
            col,
            str(stats['type']),
            str(stats['missing']),
            str(stats['unique'])
        )

    console.print(table)

def select_columns(columns, single=False):
    """Interactive column selection"""
    if single:
        return Prompt.ask(
            "Select column",
            choices=columns
        )
    else:
        selected = Prompt.ask(
            "Enter column names (comma-separated) or 'all'",
        )
        return columns if selected.lower() == 'all' else [c.strip() for c in selected.split(',')]

def show_data_overview(inspector):
    """Show dataset overview"""
    stats = inspector.get_basic_stats()
    console.print(Panel.fit(
        f"[bold]Dataset Overview[/bold]\n"
        f"Rows: {stats['rows']}\n"
        f"Columns: {stats['columns']}\n"
        f"Missing Values: {stats['total_missing']}\n"
        f"Memory Usage: {stats['memory_usage']}\n",
        title="📊 Summary",
        border_style="blue"
    ))

if __name__ == '__main__':
    cli()
