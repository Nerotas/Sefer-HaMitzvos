import csv
from datetime import datetime

def create_corrected_schedule():
    """Create a corrected Schedule.csv that follows the Master List order."""
    
    # Read the master list to get the correct mitzvot
    master_list = {}
    with open('MitzvosMasterList.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                number = int(row['Number'])
                master_list[number] = {
                    'mitzvah': row['Mitzvah'].strip(),
                    'reference': row['Biblical Reference'].strip()
                }
            except ValueError:
                continue
    
    # Read the current schedule to get dates and structure
    schedule_entries = []
    with open('Schedule.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            schedule_entries.append({
                'date': row['Date'].strip(),
                'mitzvos': row['Mitzvos'].strip(),
                'title': row['English Title(s)'].strip(),
                'source': row['Source'].strip()
            })
    
    # Create corrected entries
    corrected_entries = []
    
    for entry in schedule_entries:
        mitzvos_field = entry['mitzvos']
        
        # Keep intro entries unchanged
        if mitzvos_field.startswith('Intro'):
            corrected_entries.append(entry)
            continue
        
        # Extract numbers from the Mitzvos field
        numbers = []
        if ',' in mitzvos_field:
            # Multiple numbers like "66, 67"
            parts = mitzvos_field.split(',')
            for part in parts:
                part = part.strip()
                if part.isdigit():
                    numbers.append(int(part))
        else:
            # Single number
            if mitzvos_field.isdigit():
                numbers.append(int(mitzvos_field))
        
        if numbers:
            # Create corrected title and source based on master list
            if len(numbers) == 1:
                # Single mitzvah
                num = numbers[0]
                if num in master_list:
                    corrected_title = master_list[num]['mitzvah']
                    corrected_source = master_list[num]['reference']
                else:
                    corrected_title = f"ERROR: Mitzvah {num} not found"
                    corrected_source = "ERROR"
            else:
                # Multiple mitzvot - combine titles and sources
                titles = []
                sources = []
                for num in numbers:
                    if num in master_list:
                        titles.append(master_list[num]['mitzvah'])
                        sources.append(master_list[num]['reference'])
                    else:
                        titles.append(f"ERROR: Mitzvah {num} not found")
                        sources.append("ERROR")
                
                corrected_title = " & ".join(titles)
                corrected_source = " & ".join(sources)
            
            corrected_entries.append({
                'date': entry['date'],
                'mitzvos': mitzvos_field,  # Keep original numbering
                'title': corrected_title,
                'source': corrected_source
            })
        else:
            # Keep non-numeric entries unchanged
            corrected_entries.append(entry)
    
    # Write the corrected schedule
    with open('Schedule_Corrected.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Date', 'Mitzvos', 'English Title(s)', 'Source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in corrected_entries:
            writer.writerow({
                'Date': entry['date'],
                'Mitzvos': entry['mitzvos'],
                'English Title(s)': entry['title'],
                'Source': entry['source']
            })
    
    print(f"Created Schedule_Corrected.csv with {len(corrected_entries)} entries")
    print(f"Corrected {len([e for e in corrected_entries if not e['mitzvos'].startswith('Intro')])} mitzvah entries")

if __name__ == "__main__":
    create_corrected_schedule()