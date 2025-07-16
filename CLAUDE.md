# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project named "lowson" that appears to be related to scraping or analyzing Lawson convenience store data. The project uses uv for dependency management and includes pandas for data processing.

## Development Commands

### Package Management
- `uv sync` - Install/update dependencies and sync environment
- `uv add <package>` - Add new dependencies
- `uv remove <package>` - Remove dependencies
- `uv lock` - Update lockfile

### Running the Application
- `uv run python main.py` - Run the main application
- `uv run <command>` - Run any command within the project environment

### Project Structure
- `main.py` - Main application entry point (currently a simple "Hello from lowson!" script)
- `dataset/source.json` - Contains URLs for Lawson convenience store product categories
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Dependency lockfile managed by uv

## Dependencies

The project currently depends on:
- `pandas>=2.3.1` - For data manipulation and analysis
- Python 3.13+ required

## Data Sources

The `dataset/source.json` file contains URLs for various Lawson product categories:
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

This suggests the project may be intended for scraping or analyzing Lawson convenience store product data.