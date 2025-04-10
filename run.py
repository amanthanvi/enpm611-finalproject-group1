"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse
import importlib
import os
import inspect

import config


def list_module_functions():
    """
    Dynamically lists all callable functions in the 'modules' folder.
    """
    modules_folder = os.path.join(os.getcwd(), 'modules')
    module_files = sorted([f for f in os.listdir(modules_folder) if f.endswith('.py') and f != '__init__.py'])  # Sort files alphabetically
    
    functions = {}
    for module_file in module_files:
        module_name = module_file[:-3]  # Remove the .py extension
        module = importlib.import_module(f'modules.{module_name}')
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            # Use the full file name for display
            functions[module_file] = obj
    return functions


def main():
    """
    Main entry point for the application.
    """
    functions = list_module_functions()
    if not functions:
        print("No functions found in the 'modules' folder.")
        return

    while True:
        print("Available modules:")
        for idx, module_name in enumerate(functions.keys(), start=1):
            print(f"{idx}: {module_name}")
        print("\nR: Refresh list of modules")
        print("Q: Exit")

        selection = input("Select a module to run by number (or R to refresh, Q to exit): ").strip().upper()

        if selection == "Q":
            print("Exiting the program.")
            break
        elif selection == "R":
            print("Refreshing the list of modules...")
            functions = list_module_functions()
            continue

        try:
            selected_func = list(functions.values())[int(selection) - 1]
            print(f"Running: {list(functions.keys())[int(selection) - 1]}")
            selected_func()
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")


if __name__ == '__main__':
    main()
