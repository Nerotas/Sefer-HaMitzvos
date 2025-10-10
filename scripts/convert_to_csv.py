import re
import csv

def parse_mitzvot_file(input_file, output_file):
    """Parse the mitzvot text file and convert to CSV format."""

    mitzvot_data = []

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines and process each line
    lines = content.strip().split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Check if this is the start of a numbered entry
        if re.match(r'^\d+\.', line):
            current_entry = line

            # Check if the entry continues on the next line(s)
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # If next line starts with a number, it's a new entry
                if re.match(r'^\d+\.', next_line) or not next_line:
                    break
                # Otherwise, it's part of the current entry
                current_entry += " " + next_line
                j += 1

            # Now parse the complete entry
            patterns = [
                r'^(\d+)\.\s*(.+?)—(.+)$',  # em dash
                r'^(\d+)\.\s*(.+?)--(.+)$', # double hyphen
                r'^(\d+)\.\s*(.+?)[-–—](.+)$'  # various dash types
            ]

            matched = False
            for pattern in patterns:
                match = re.match(pattern, current_entry)
                if match:
                    number = int(match.group(1))
                    mitzvah = match.group(2).strip()
                    reference = match.group(3).strip()

                    mitzvot_data.append([number, mitzvah, reference])
                    matched = True
                    break

            if not matched:
                print(f"Warning: Could not parse entry: {current_entry}")

            # Move to the next unprocessed line
            i = j
        else:
            i += 1

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(['Number', 'Mitzvah', 'Biblical Reference'])

        # Write data
        writer.writerows(mitzvot_data)

    print(f"Successfully converted {len(mitzvot_data)} mitzvot to CSV format")
    return len(mitzvot_data)

if __name__ == "__main__":
    input_file = "MitzvosMasterList.txt"
    output_file = "MitzvosMasterList.csv"

    count = parse_mitzvot_file(input_file, output_file)
    print(f"Created {output_file} with {count} entries")