#!/usr/bin/env python3
"""
Convert the new Schedule_Complete_Sefer_HaMitzvos.csv format to embedded Python code
for the lambda bot
"""
import csv
from collections import defaultdict

def convert_csv_to_embedded_format():
    """Convert the new CSV format to the format expected by the lambda bot"""
    
    # Read the new CSV
    schedule_data = []
    daily_entries = defaultdict(list)
    
    print("Reading Schedule_Complete_Sefer_HaMitzvos.csv...")
    
    with open('Schedule_Complete_Sefer_HaMitzvos.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            daily_entries[row['Date']].append({
                'Sequential_Number': row['Sequential_Number'],
                'Mitzvah_Type_Number': row['Mitzvah_Type_Number'],
                'Summary': row['Summary'],
                'Sefaria_Link': row['Sefaria_Link']
            })
    
    print(f"Processed {len(daily_entries)} unique dates")
    
    # Convert to the format expected by lambda bot
    embedded_data = []
    
    for date, entries in sorted(daily_entries.items()):
        # Create consolidated entry for this date
        mitzvos_numbers = []
        titles = []
        sources = []
        sefaria_links = []
        
        for entry in entries:
            mitzvos_numbers.append(entry['Mitzvah_Type_Number'])
            titles.append(entry['Summary'])
            sefaria_links.append(entry['Sefaria_Link'])
            
            # Extract source from Sefaria link
            if 'Shorashim' in entry['Sefaria_Link']:
                sources.append('Sefer HaMitzvos Introduction')
            elif 'Positive_Commandments' in entry['Sefaria_Link']:
                sources.append('Sefer HaMitzvos Positive')
            elif 'Negative_Commandments' in entry['Sefaria_Link']:
                sources.append('Sefer HaMitzvos Negative')
            elif 'Conclusion' in entry['Sefaria_Link']:
                sources.append('Sefer HaMitzvos Conclusion')
            else:
                sources.append('Sefer HaMitzvos')
        
        # Consolidate for the day
        embedded_entry = {
            'Date': date,
            'Mitzvos': ', '.join(mitzvos_numbers),
            'English Title(s)': ' & '.join(titles),
            'Source': ' & '.join(set(sources)),  # Remove duplicates
            'Sefaria_Link': sefaria_links[0] if len(sefaria_links) == 1 else sefaria_links  # Keep all links if multiple
        }
        
        embedded_data.append(embedded_entry)
    
    return embedded_data

def generate_embedded_code(schedule_data):
    """Generate the Python code for embedding in the lambda function"""
    
    code_lines = [
        "    def get_embedded_schedule(self):",
        "        \"\"\"",
        "        Embed complete Sefer HaMitzvot schedule data directly in Lambda function",
        "        Updated with the complete 628-entry schedule including proper conclusion positioning",
        "        \"\"\"",
        "        return ["
    ]
    
    for i, entry in enumerate(schedule_data):
        code_lines.append("            {")
        code_lines.append(f"                'Date': '{entry['Date']}',")
        code_lines.append(f"                'Mitzvos': '{entry['Mitzvos']}',")
        
        # Handle long titles by truncating if needed
        title = entry['English Title(s)']
        if len(title) > 200:  # Truncate very long combined titles
            title = title[:200] + "..."
        
        code_lines.append(f"                'English Title(s)': '{title}',")
        code_lines.append(f"                'Source': '{entry['Source']}',")
        
        if isinstance(entry['Sefaria_Link'], list):
            code_lines.append(f"                'Sefaria_Links': {entry['Sefaria_Link']}")
        else:
            code_lines.append(f"                'Sefaria_Link': '{entry['Sefaria_Link']}'")
        
        if i < len(schedule_data) - 1:
            code_lines.append("            },")
        else:
            code_lines.append("            }")
    
    code_lines.append("        ]")
    
    return '\n'.join(code_lines)

if __name__ == "__main__":
    print("Converting CSV to embedded format...")
    
    # Convert CSV
    schedule_data = convert_csv_to_embedded_format()
    
    print(f"Generated {len(schedule_data)} daily entries")
    print(f"Date range: {schedule_data[0]['Date']} to {schedule_data[-1]['Date']}")
    
    # Generate Python code
    embedded_code = generate_embedded_code(schedule_data)
    
    # Write to file
    with open('embedded_schedule_code.py', 'w', encoding='utf-8') as f:
        f.write("# Generated embedded schedule code for lambda bot\n")
        f.write("# Replace the get_embedded_schedule method with this code\n\n")
        f.write(embedded_code)
    
    print("Embedded code generated in: embedded_schedule_code.py")
    print("You can now copy this code into the lambda bot's get_embedded_schedule method")