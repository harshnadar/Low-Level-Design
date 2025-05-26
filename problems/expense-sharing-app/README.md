# Expense Sharing Application

## Overview
The Expense Sharing Application allows users to manage and split expenses among multiple participants. Users can add expenses, choose how to split them (equally, exactly, or by percentage), and view balances to see who owes whom.

## Features
- User management with unique identifiers, names, emails, and mobile numbers.
- Expense management with different splitting strategies: EQUAL, EXACT, and PERCENT.
- Validation for expense splitting to ensure correctness.
- Group functionality for smart settlements among users.
- Display of individual user expenses and balances.

## Project Structure
```
expense-sharing-app
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── expense.py
│   │   ├── group.py
│   │   └── balance.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── expense_service.py
│   │   ├── balance_service.py
│   │   └── group_service.py
│   ├── strategies
│   │   ├── __init__.py
│   │   ├── split_strategy.py
│   │   ├── equal_split.py
│   │   ├── exact_split.py
│   │   └── percent_split.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── validators.py
│   └── exceptions
│       ├── __init__.py
│       └── custom_exceptions.py
├── tests
│   ├── __init__.py
│   ├── test_expense_service.py
│   ├── test_balance_service.py
│   └── test_split_strategies.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/expense-sharing-app.git
   ```
2. Navigate to the project directory:
   ```
   cd expense-sharing-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Follow the prompts to add users, expenses, and view balances.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.