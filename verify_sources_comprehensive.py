#!/usr/bin/env python3
"""
Comprehensive source verification to identify problematic biblical references.
This will check for:
1. Mismatched sources between summary and source column
2. Suspicious patterns like many entries using the same generic source
3. Sources that don't align with the mitzvah content
"""

import csv
import re
from collections import Counter
from datetime import datetime

def verify_sources_comprehensive():
    """Comprehensive verification of biblical sources in CSV"""
    
    input_file = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
    
    print("=== COMPREHENSIVE SOURCE VERIFICATION ===\n")
    
    # Read the CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    issues = []
    source_counter = Counter()
    summary_sources = []
    
    print("🔍 Analyzing all entries...")
    
    for i, row in enumerate(rows):
        if i == 0:  # Skip header
            continue
            
        if len(row) < 5:  # Skip incomplete rows
            continue
            
        entry_id = row[2]  # Mitzvah ID
        summary = row[3]  # Summary text
        source = row[4]   # Biblical source
        
        # Skip introduction/conclusion entries
        if "Intro" in entry_id or "Conclusion" in entry_id:
            continue
            
        # Count source frequency
        source_counter[source] += 1
        
        # Extract sources mentioned in summary text using regex
        hebrew_books = ['Bereishis', 'Shemos', 'Vayikra', 'Bamidbar', 'Devarim']
        summary_source_pattern = r'(' + '|'.join(hebrew_books) + r')\s+\d+[:\d\-]*'
        summary_matches = re.findall(summary_source_pattern, summary)
        
        if summary_matches:
            summary_sources.append({
                'line': i + 1,
                'entry': entry_id,
                'summary_sources': summary_matches,
                'column_source': source,
                'summary': summary[:100] + "..." if len(summary) > 100 else summary
            })
            
            # Check if summary source matches column source
            summary_books = [match for match in summary_matches]
            column_book = source.split()[0] if source else ""
            
            if summary_books and column_book not in summary_books:
                issues.append({
                    'type': 'MISMATCH',
                    'line': i + 1,
                    'entry': entry_id,
                    'issue': f"Summary mentions {summary_books} but source column has {source}",
                    'severity': 'HIGH'
                })
    
    # Identify suspicious frequent sources
    print(f"\n📊 SOURCE FREQUENCY ANALYSIS:")
    print("=" * 50)
    for source, count in source_counter.most_common(10):
        print(f"{source}: {count} occurrences")
        if count > 20:  # Flag sources used more than 20 times
            issues.append({
                'type': 'OVERUSE',
                'entry': 'MULTIPLE',
                'issue': f"Source '{source}' used {count} times - possibly generic/incorrect",
                'severity': 'MEDIUM'
            })
    
    # Print all issues
    print(f"\n🚨 ISSUES FOUND:")
    print("=" * 50)
    
    high_issues = [issue for issue in issues if issue['severity'] == 'HIGH']
    medium_issues = [issue for issue in issues if issue['severity'] == 'MEDIUM']
    
    if high_issues:
        print(f"\n❌ HIGH PRIORITY ISSUES ({len(high_issues)}):")
        for issue in high_issues[:20]:  # Show first 20 high priority
            print(f"   Line {issue.get('line', 'N/A')}: {issue['entry']} - {issue['issue']}")
    
    if medium_issues:
        print(f"\n⚠️ MEDIUM PRIORITY ISSUES ({len(medium_issues)}):")
        for issue in medium_issues:
            print(f"   {issue['issue']}")
    
    # Show entries with sources mentioned in summaries
    if summary_sources:
        print(f"\n📋 ENTRIES WITH SOURCES IN SUMMARY TEXT ({len(summary_sources)}):")
        print("=" * 60)
        for entry in summary_sources[:10]:  # Show first 10
            print(f"Line {entry['line']}: {entry['entry']}")
            print(f"   Summary sources: {entry['summary_sources']}")  
            print(f"   Column source: {entry['column_source']}")
            if entry['summary_sources']:
                summary_book = entry['summary_sources'][0]
                column_book = entry['column_source'].split()[0] if entry['column_source'] else ""
                if summary_book != column_book:
                    print(f"   ⚠️ MISMATCH!")
            print()
    
    print(f"\n📈 SUMMARY:")
    print(f"Total entries analyzed: {len(rows) - 1}")
    print(f"High priority issues: {len(high_issues)}")  
    print(f"Medium priority issues: {len(medium_issues)}")
    print(f"Entries with sources in summary: {len(summary_sources)}")
    
    return issues, source_counter, summary_sources

if __name__ == "__main__":
    verify_sources_comprehensive()