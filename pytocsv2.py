import os
import csv

def save_py_to_csv(directory: str, csv_filename: str):
    """
    Goes through every .py file in the specified folder and saves their contents in CSV format.

    Parameters:
        directory (str): The folder to scan for .py files.
        csv_filename (str): The name of the output CSV file.
    """
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(["File Name", "Content"])

        # Walk through the directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, mode='r', encoding='utf-8') as py_file:
                            content = py_file.read()
                        # Modify file name and content
                        simple_file_name = '_'.join(file.split('_')[1:])
                        formatted_content = f"""```python
                        {content}```"""
                        csv_writer.writerow([simple_file_name, formatted_content])
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing .py files: ")
    output_csv = input("Enter the name of the output CSV file (e.g., output.csv): ")
    save_py_to_csv(folder_path, output_csv)
    print(f"Contents of .py files saved to {output_csv}.")
