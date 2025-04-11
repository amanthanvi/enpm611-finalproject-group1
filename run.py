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

    last_selected_func = None  # Store the last selected function

    while True:
        print("\nAvailable modules:")
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
            last_selected_func = selected_func  # Remember the last selected function
            result = post_execution_menu(last_selected_func)
            if result == "SKIP_MAIN_MENU":
                continue  # Skip re-displaying the main menu
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

def post_execution_menu(last_selected_func):
    """
    Displays a menu after executing a module to allow the user to return to the main menu,
    select another data file, or quit the program.
    """
    while True:
        print("\n1. Main menu")
        print("2. Select another data file")
        print("Q. Quit")

        selection = input("Choose an option: ").strip().upper()

        if selection == "1":
            return  # Return to the main menu
        elif selection == "2":
            reset_data_file_selection()
            if last_selected_func:
                print("Re-running the previously selected module...")
                last_selected_func()  # Re-execute the last selected function
            # Loop back to the post-execution menu instead of returning to the main menu
            continue
        elif selection == "Q":
            print("Exiting the program.")
            exit(0)
        else:
            print("Invalid selection. Please try again.")

def reset_data_file_selection():
    """
    Resets the data file selection and prompts the user to select a new JSON file.
    """
    from data_loader import DataLoader
    data_folder = os.path.join(os.getcwd(), 'data')
    json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]

    if not json_files:
        print("No JSON files found in the 'data' folder.")
        return

    print("\nAvailable JSON files:")
    for idx, file_name in enumerate(json_files, start=1):
        print(f"{idx}: {file_name}")

    while True:
        try:
            selection = int(input("Select a file by number: ").strip())
            if 1 <= selection <= len(json_files):
                DataLoader._data_path = os.path.join(data_folder, json_files[selection - 1])
                print(f"Data file set to: {json_files[selection - 1]}")  # Show only the file name
                return
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == '__main__':
    main()
