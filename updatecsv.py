import csv
import re

def process_csv(input_csv: str, output_csv: str):
    """
    Processes each row in the 'Response' column of a CSV file to:
    1. Extract the filename from `#filename: filename.py`.
    2. Replace 'from ocp_vscode import show' with 'from ocp_vscode import *'.
    3. Replace 'show(result)' with 'show_object(result)'.
    4. Append export lines inside the triple backticks using the extracted filename.

    Parameters:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
    """
    updated_rows = []

    with open(input_csv, mode='r', encoding='utf-8') as infile:
        csv_reader = csv.DictReader(infile)
        fieldnames = csv_reader.fieldnames  # Preserve original headers
        for row in csv_reader:
            if "Response" in row:
                content = row["Response"]

                # Extract the filename from #filename line
                match = re.search(r"#filename: (.+?\.py)", content)
                if match:
                    filename = match.group(1).replace('.py', '')

                    # Perform replacements in the content
                    content = content.replace("from ocp_vscode import show", "from ocp_vscode import *")
                    content = content.replace("show(result)", "show_object(result)")

                    # Check for and append export lines within the triple backticks
                    if content.strip().endswith("```"):
                        export_lines = f'\ncq.exporters.export(result, "{filename}.stl")\n'
                        export_lines += f'cq.exporters.export(result, "{filename}.step")\n'
                        content = content.rstrip("```") + export_lines + "```"

                # Update the row with modified content
                row["Response"] = content

            updated_rows.append(row)

    # Write the updated content back to a new CSV file
    with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(updated_rows)

if __name__ == "__main__":
    input_csv = input("Enter the input CSV file name (e.g., input.csv): ")
    output_csv = input("Enter the output CSV file name (e.g., updated_output.csv): ")
    process_csv(input_csv, output_csv)
    print(f"Processed CSV file saved to {output_csv}.")
