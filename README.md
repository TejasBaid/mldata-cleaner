# ML Data Cleaning Toolkit

The ML Data Cleaning Toolkit is a command-line tool designed to simplify and automate the process of cleaning and preparing datasets for machine learning projects. It provides a rich set of features for inspecting, handling missing values, managing duplicates, and handling outliers in datasets.

---

## Features

### Inspection
- View dataset statistics and structure.
- Analyze missing values.
- Detect and remove duplicate rows.
- Examine column data types and unique values.

### Cleaning
- Handle missing values using various strategies: `mean`, `median`, `mode`, `constant`, or `drop`.
- Remove duplicate rows.
- Handle outliers using `IQR` or `Z-Score` methods.
- Convert column data types.

### Interactive Session
- Start an interactive session to explore and clean datasets using a user-friendly menu.

---

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Steps
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the CLI tool:
   ```bash
   python cli.py
   ```

---

## Usage

### Command-Line Interface (CLI)

```bash
python cli.py [COMMAND] [OPTIONS]
```

### Commands

#### 1. `inspect`
Display basic dataset statistics.
```bash
python cli.py inspect <file_path>
```

#### 2. `missing`
Analyze missing values in the dataset.
```bash
python cli.py missing <file_path>
```

#### 3. `duplicates`
Find duplicate rows in the dataset.
```bash
python cli.py duplicates <file_path>
```

#### 4. `fix-missing`
Handle missing values using specified strategies.
```bash
python cli.py fix-missing <file_path> <output_file> --strategy <strategy> --columns <columns> [--value <constant_value>]
```
- Strategies: `mean`, `median`, `mode`, `constant`, `drop`.

#### 5. `interactive`
Start an interactive session for data cleaning.
```bash
python cli.py interactive <file_path>
```

---

## Examples

### Inspect Dataset
```bash
python cli.py inspect data.csv
```

### Handle Missing Values
Replace missing values with the column mean:
```bash
python cli.py fix-missing data.csv cleaned_data.csv --strategy mean --columns column1,column2
```

### Remove Duplicates
```bash
python cli.py duplicates data.csv
```

### Start Interactive Session
```bash
python cli.py interactive data.csv
```

---

## Development

### Code Structure
- **`cli.py`**: Entry point for the CLI application.
- **`cleaner.py`**: Handles dataset cleaning operations.
- **`inspector.py`**: Provides dataset inspection functionalities.
- **`tests/`**: Unit tests for the toolkit.

### Running Tests
To run tests, execute:
```bash
pytest tests/
```

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgements

- **Rich Library**: For creating beautiful and interactive console outputs.
- **Pandas**: For data manipulation and analysis.
- **Scikit-learn**: For data preprocessing utilities.

---

Happy Cleaning! 🚀

