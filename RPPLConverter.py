import csv
import os
import random
import argparse
from datetime import datetime

def generate_unique_id():
    """Generate a unique ID."""
    return f"ID_{random.randint(100000, 999999)}"

def is_numeric(value):
    """Check if a value is numeric (int or float)."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def final_tagging(file_path):
    """Tag headers with 'c' for categorical and 'n' for numerical data."""
    # Read the data to check each column's type
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        headers = reader[0]
        data = reader[1:]

        # Determine type for each column based on the first few rows of data
        tagged_headers = []
        for i, header in enumerate(headers):
            if i == 0 or i == 1:  # Unique ID and Timestamp are always categorical
                tagged_headers.append(f"c {header}")
                continue

            column_data = [row[i] for row in data if row[i]]
            col_type = "n" if all(is_numeric(value) for value in column_data) else "c"
            tagged_headers.append(f"{col_type} {header}")

    # Write the updated headers with tags
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(tagged_headers)
        writer.writerows(data)

def clean_row(row, headers, remove_columns, paired_columns, timestamp_index, is_googleforms):
    """Clean each row by removing unwanted columns, handling TRUE/FALSE pairs, and simplifying responses."""
    cleaned_row = []
    unique_id = generate_unique_id()
    cleaned_row.append(unique_id)

    # Handle Timestamp only if it's not a GoogleForms file
    if not is_googleforms:
        timestamp = row[timestamp_index] if timestamp_index is not None else datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cleaned_row.append(timestamp)
    
    for i, cell in enumerate(row):
        if any(unwanted in headers[i] for unwanted in remove_columns):
            continue
        if headers[i] in paired_columns:
            if headers[i].endswith("True"):
                cleaned_row.append("TRUE" if cell == "1" else "FALSE")
            continue
        cleaned_row.append(cell)
    return cleaned_row

def convert_datasets(input_folder, output_folder, separate):
    remove_columns = [
        "IP Address", "Recipient Last Name", "Recipient First Name", 
        "Recipient Email", "External Data Reference", "Response Type", 
        "Progress", "Duration (in seconds)", "Finished", "Recorded Date", 
        "Response ID", "Location Latitude", "Location Longitude", 
        "Distribution Channel", "User Language", "Start Date", "End Date"
    ]
    paired_columns = [
        "(Teacher-facing) Would you recommend this professional learning workshop to a colleague or friend? - True",
        "(Teacher-facing) Would you recommend this professional learning workshop to a colleague or friend? - False",
        "(Teacher-facing) I intend to utilize what I learned in my classroom as I believe the things that I learned will positively impact my teaching practice - True",
        "(Teacher-facing) I intend to utilize what I learned in my classroom as I believe the things that I learned will positively impact my teaching practice - False"
    ]

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            all_data = []
            headers_written = False

            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)

                # Determine if it's a Qualtrics or GoogleForms file
                is_qualtrics = "Qualtrics" in filename
                is_googleforms = "GoogleForms" in filename
                
                if is_qualtrics:
                    next(reader)

                headers = next(reader)  # Get the actual headers
                timestamp_index = headers.index("End Date") if "End Date" in headers else None
                cleaned_headers = ["Unique ID", "Timestamp"] if not is_googleforms else ["Unique ID"]
                
                for i, header in enumerate(headers):
                    if any(unwanted in header for unwanted in remove_columns):
                        continue
                    if header in paired_columns:
                        if header.endswith("True"):
                            cleaned_headers.append(header.rsplit(' - ', 1)[0].strip())
                        continue
                    cleaned_headers.append(header)

                all_data.append(cleaned_headers)

                # Process all rows
                for row in reader:
                    cleaned_row = clean_row(row, headers, remove_columns, paired_columns, timestamp_index, is_googleforms)
                    all_data.append(cleaned_row)

            # Write initial data to output file without tagging
            output_file = os.path.join(output_folder, f"converted_{filename}") if separate == "yes" else os.path.join(output_folder, "converted_combined.csv")
            write_mode = 'w' if separate == "yes" else 'a'
            with open(output_file, mode=write_mode, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if separate == "yes" or not headers_written:
                    writer.writerow(cleaned_headers)
                    headers_written = True
                writer.writerows(all_data[1:])

            # Apply final tagging to the file
            final_tagging(output_file)

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert and clean CSV datasets.")
    parser.add_argument("input_folder", help="Folder with CSV files to convert")
    parser.add_argument("output_folder", help="Folder to save converted CSV files")
    parser.add_argument("--separate", choices=["yes", "no"], default="no", help="Save datasets separately or combined")
    args = parser.parse_args()

    convert_datasets(args.input_folder, args.output_folder, args.separate)
