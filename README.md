# Lowson - Lawson Food Data Scraper & Calorie Optimizer

A Python project that scrapes Lawson convenience store food data and provides calorie optimization tools to help you maximize calories within your budget.

## Features

- **Web Scraping**: Automatically scrapes Lawson's website for food items with prices and calorie information
- **Calorie Optimization**: Uses dynamic programming to find the optimal combination of foods that maximizes calories within a budget
- **Interactive Analysis**: Provides interactive budget optimization and scenario analysis
- **Efficiency Analysis**: Shows the most calorie-efficient items (calories per yen)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Make sure you have Python 3.13+ installed.

```bash
# Install dependencies
uv sync
```

## Usage

### 1. Data Collection

First, run the scraper to collect food data from Lawson's website:

```bash
uv run python scraping.py
```

This will:
- Scrape all product categories defined in `dataset/source.json`
- Extract product names, calories, and prices
- Save the data to `dataset/lawson_food_data.csv`

### 2. Calorie Optimization

Run the optimizer to find the best food combinations:

```bash
uv run python knapsack_optimizer.py
```

This will:
- Show the top 10 most calorie-efficient items
- Analyze multiple budget scenarios (500円, 1000円, 1500円, etc.)
- Provide interactive budget optimization where you can input your own budget

## Project Structure

```txt
|--dataset
|  |--lawson_food_data.csv  # Scraped food data (generated)
|  |--source.json           # URLs for Lawson product categories
|--scraping.py              # Web scraper for Lawson food data
|--knapsack_optimizer.py    # Calorie optimization using dynamic programming
|--pyproject.toml           # Project configuration
|--.python-version
|--uv.lock                  # Dependency lockfile
|--README.md                # This file
```

## Dependencies

- `pandas>=2.3.1` - Data manipulation and analysis
- `requests` - HTTP requests for web scraping
- `beautifulsoup4` - HTML parsing
- Python 3.13+

## Algorithm

The calorie optimization uses a dynamic programming approach to solve the knapsack problem:
- **Objective**: Maximize calories within a budget constraint
- **Constraints**: Total cost must not exceed the budget
- **Method**: Bottom-up dynamic programming with backtracking to find selected items

## Data Sources

The scraper targets various Lawson product categories:
- Gateau (cakes)
- Desserts
- Rice dishes
- Sandwiches
- Bakery items
- Pasta
- Noodles
- Salads
- Fried items
- Frozen select items

## License

This project is for educational and research purposes only. Please be respectful when scraping and follow the website's robots.txt and terms of service.

