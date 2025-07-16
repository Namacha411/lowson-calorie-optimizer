import pandas as pd
import sys


def load_food_data(csv_file="lawson_food_data.csv"):
    """Load food data from CSV file"""
    try:
        df = pd.read_csv(csv_file)

        # Clean the data - remove any invalid entries
        df = df.dropna()
        df = df[df["calories"] > 0]
        df = df[df["price"] > 0]

        return df
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please run the scraper first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def knapsack_dp(items, budget):
    """
    Solve knapsack problem using dynamic programming

    Args:
        items: List of tuples (name, calories, price)
        budget: Maximum budget (price limit)

    Returns:
        Tuple of (max_calories, selected_items)
    """
    n = len(items)

    # Create DP table: dp[i][w] = max calories using first i items with budget w
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        name, calories, price = items[i - 1]

        for w in range(budget + 1):
            # Don't take current item
            dp[i][w] = dp[i - 1][w]

            # Take current item if it fits in budget
            if price <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - price] + calories)

    # Backtrack to find which items were selected
    selected_items = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1][2]  # Subtract price

    return dp[n][budget], selected_items


def optimize_calories_for_budget(df, budget):
    """
    Find the optimal combination of food items to maximize calories within budget

    Args:
        df: DataFrame with food data
        budget: Maximum budget in yen

    Returns:
        Dictionary with optimization results
    """
    # Convert dataframe to list of tuples
    items = [(row["name"], row["calories"], row["price"]) for _, row in df.iterrows()]

    # Solve knapsack problem
    max_calories, selected_items = knapsack_dp(items, budget)

    # Calculate total cost
    total_cost = sum(item[2] for item in selected_items)

    # Sort selected items by calories per yen ratio (efficiency)
    selected_items.sort(key=lambda x: x[1] / x[2], reverse=True)

    return {
        "budget": budget,
        "max_calories": max_calories,
        "total_cost": total_cost,
        "remaining_budget": budget - total_cost,
        "selected_items": selected_items,
        "num_items": len(selected_items),
        "avg_calories_per_yen": max_calories / total_cost if total_cost > 0 else 0,
    }


def print_results(results):
    """Print optimization results in a formatted way"""
    print("\n" + "=" * 60)
    print("CALORIE OPTIMIZATION RESULTS")
    print("=" * 60)
    print(f"Budget: {results['budget']:,}円")
    print(f"Maximum Calories: {results['max_calories']:,} kcal")
    print(f"Total Cost: {results['total_cost']:,}円")
    print(f"Remaining Budget: {results['remaining_budget']:,}円")
    print(f"Number of Items: {results['num_items']}")
    print(f"Average Calories per Yen: {results['avg_calories_per_yen']:.2f}")

    print("\nSelected Items:")
    print("-" * 90)
    print(f"{'Item Name':<40}\t{'Calories':>10}\t{'Price':>10}\t{'Cal/¥':>10}")
    print("-" * 90)

    for name, calories, price in results["selected_items"]:
        cal_per_yen = calories / price
        print(f"{name:<40}\t{calories:>10}\t{price:>10}円\t{cal_per_yen:>10.2f}")

    print("-" * 90)
    print(f"{'TOTAL':<40} {results['max_calories']:>10} {results['total_cost']:>10}円")


def analyze_budget_scenarios(df, budgets):
    """Analyze multiple budget scenarios"""
    print("\nBUDGET SCENARIO ANALYSIS")
    print("=" * 80)
    print(
        f"{'Budget':<10} {'Max Calories':<12} {'Items':<8} {'Cost':<10} {'Remaining':<12} {'Cal/¥':<10}"
    )
    print("-" * 80)

    for budget in budgets:
        results = optimize_calories_for_budget(df, budget)
        print(
            f"{budget:<10}円 {results['max_calories']:<12} {results['num_items']:<8} "
            f"{results['total_cost']:<10}円 {results['remaining_budget']:<12}円 "
            f"{results['avg_calories_per_yen']:<10.2f}"
        )


def find_most_efficient_items(df, top_n=10):
    """Find the most calorie-efficient items (calories per yen)"""
    df["calories_per_yen"] = df["calories"] / df["price"]
    top_items = df.nlargest(top_n, "calories_per_yen")

    print(f"\nTOP {top_n} MOST CALORIE-EFFICIENT ITEMS")
    print("=" * 70)
    print(f"{'Item Name':<40} {'Calories':<10} {'Price':<10} {'Cal/¥':<10}")
    print("-" * 70)

    for _, row in top_items.iterrows():
        print(
            f"{row['name']:<40} {row['calories']:<10} {row['price']:<10}円 {row['calories_per_yen']:<10.2f}"
        )


def main():
    """Main function to run the calorie optimizer"""
    print("Lawson Food Calorie Optimizer")
    print("Using Dynamic Programming Knapsack Algorithm")

    # Load data
    df = load_food_data()
    print(f"\nLoaded {len(df)} food items from CSV")

    # Show most efficient items
    find_most_efficient_items(df, 10)

    # Analyze different budget scenarios
    budgets = [500, 1000, 1500, 2000, 3000, 5000]
    analyze_budget_scenarios(df, budgets)

    # Interactive budget input
    print("\n" + "=" * 60)
    print("INTERACTIVE BUDGET OPTIMIZER")
    print("=" * 60)

    while True:
        try:
            budget_input = input(
                "\nEnter your budget in yen (or 'quit' to exit): "
            ).strip()

            if budget_input.lower() in ["quit", "q", "exit"]:
                break

            budget = int(budget_input)

            if budget <= 0:
                print("Please enter a positive budget amount.")
                continue

            if budget > 50000:
                print("Budget seems quite high. Are you sure? (y/n)")
                confirm = input().strip().lower()
                if confirm != "y":
                    continue

            results = optimize_calories_for_budget(df, budget)
            print_results(results)

        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

