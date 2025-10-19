#!/usr/bin/env python3
"""
Web Search Biblical Source Verification
This script will search for each mitzvah summary and find its biblical source
using web searches to create a verified reference CSV.
"""

import csv
import time
import requests
from datetime import datetime
import re

class BiblicalSourceWebVerifier:
    def __init__(self):
        """Initialize the web verification system."""

        # Hebrew book name mappings for consistency
        self.book_mappings = {
            'genesis': 'Bereishis',
            'exodus': 'Shemos',
            'leviticus': 'Vayikra',
            'numbers': 'Bamidbar',
            'deuteronomy': 'Devarim'
        }

        # Results storage
        self.results = []

    def search_mitzvah_source(self, summary, mitzvah_type):
        """Search for biblical source of a specific mitzvah"""

        print(f"🔍 Searching: {mitzvah_type} - {summary[:60]}...")

        # Create search queries
        queries = [
            f'"{summary}" biblical source torah verse',
            f'Rambam "{summary}" biblical source',
            f'Sefer HaMitzvot "{summary}" source verse',
            f'mitzvah "{summary}" torah source'
        ]

        # Try each query
        for query in queries:
            try:
                # Use DuckDuckGo search (no API key needed)
                search_url = f"https://duckduckgo.com/html/?q={query}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    # Look for biblical references in the response
                    biblical_refs = self.extract_biblical_references(response.text)

                    if biblical_refs:
                        print(f"   ✅ Found potential sources: {biblical_refs[:3]}")
                        return biblical_refs[0] if biblical_refs else None

                # Rate limiting
                time.sleep(2)

            except Exception as e:
                print(f"   ⚠️ Search error: {e}")
                continue

        print(f"   ❌ No source found for {mitzvah_type}")
        return None

    def extract_biblical_references(self, html_content):
        """Extract biblical references from HTML content"""

        references = []

        # Common patterns for biblical references
        patterns = [
            # Hebrew book names with chapters/verses
            r'(Bereishis|Shemos|Vayikra|Bamidbar|Devarim)\s+(\d+):(\d+)',
            r'(Genesis|Exodus|Leviticus|Numbers|Deuteronomy)\s+(\d+):(\d+)',
            r'(Bereshit|Shemot|Vayikra|Bamidbar|Devarim)\s+(\d+):(\d+)',
            # Abbreviated forms
            r'(Gen|Ex|Lev|Num|Deut)\.?\s+(\d+):(\d+)',
            r'(Ber|Shem|Vay|Bam|Dev)\.?\s+(\d+):(\d+)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)

            for match in matches:
                book, chapter, verse = match

                # Normalize to Hebrew names
                book_lower = book.lower()
                if book_lower in ['genesis', 'gen', 'ber', 'bereshit']:
                    normalized_book = 'Bereishis'
                elif book_lower in ['exodus', 'ex', 'shem', 'shemot']:
                    normalized_book = 'Shemos'
                elif book_lower in ['leviticus', 'lev', 'vay']:
                    normalized_book = 'Vayikra'
                elif book_lower in ['numbers', 'num', 'bam']:
                    normalized_book = 'Bamidbar'
                elif book_lower in ['deuteronomy', 'deut', 'dev']:
                    normalized_book = 'Devarim'
                else:
                    normalized_book = book

                reference = f"{normalized_book} {chapter}:{verse}"
                if reference not in references:
                    references.append(reference)

        return references

    def verify_all_mitzvot(self, csv_file):
        """Verify biblical sources for all mitzvot in the CSV"""

        print("=== BIBLICAL SOURCE WEB VERIFICATION ===\n")

        # Load the CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"📊 Processing {len(rows)} entries...")

        processed = 0

        for i, row in enumerate(rows, 1):
            mitzvah_type = row['Mitzvah_Type_Number']
            summary = row['Summary']
            current_source = row['Biblical_Source']

            # Skip intro/conclusion entries (no biblical sources)
            if mitzvah_type.startswith(('Intro', 'Conclusion')):
                self.results.append({
                    'Sequential_Number': row['Sequential_Number'],
                    'Mitzvah_Type_Number': mitzvah_type,
                    'Summary': summary,
                    'Current_Source': current_source,
                    'Web_Search_Source': 'N/A - Introduction/Conclusion',
                    'Search_Status': 'Skipped',
                    'Confidence': 'N/A'
                })
                continue

            print(f"\n[{i}/{len(rows)}] Processing {mitzvah_type}...")

            # Search for biblical source
            web_source = self.search_mitzvah_source(summary, mitzvah_type)

            # Determine confidence level
            confidence = 'Not Found'
            if web_source:
                if current_source == web_source:
                    confidence = 'High - Matches Current'
                elif current_source and current_source != web_source:
                    confidence = 'Medium - Differs from Current'
                else:
                    confidence = 'Low - New Source Found'

            # Store result
            self.results.append({
                'Sequential_Number': row['Sequential_Number'],
                'Mitzvah_Type_Number': mitzvah_type,
                'Summary': summary,
                'Current_Source': current_source,
                'Web_Search_Source': web_source or 'NOT FOUND',
                'Search_Status': 'Found' if web_source else 'Not Found',
                'Confidence': confidence
            })

            processed += 1

            # Progress update
            if processed % 10 == 0:
                print(f"\n📈 Progress: {processed}/{len([r for r in rows if not r['Mitzvah_Type_Number'].startswith(('Intro', 'Conclusion'))])} mitzvot processed")

            # Rate limiting for web searches
            time.sleep(3)

        return self.results

    def save_results(self, output_file):
        """Save verification results to CSV"""

        fieldnames = [
            'Sequential_Number',
            'Mitzvah_Type_Number',
            'Summary',
            'Current_Source',
            'Web_Search_Source',
            'Search_Status',
            'Confidence'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

        print(f"\n✅ Results saved to: {output_file}")

    def generate_summary_report(self):
        """Generate a summary of the verification results"""

        total = len(self.results)
        found = len([r for r in self.results if r['Search_Status'] == 'Found'])
        skipped = len([r for r in self.results if r['Search_Status'] == 'Skipped'])
        not_found = len([r for r in self.results if r['Search_Status'] == 'Not Found'])

        matches = len([r for r in self.results if r['Confidence'] == 'High - Matches Current'])
        differs = len([r for r in self.results if r['Confidence'] == 'Medium - Differs from Current'])

        print(f"\n📊 VERIFICATION SUMMARY:")
        print(f"   • Total entries: {total}")
        print(f"   • Sources found: {found}")
        print(f"   • Not found: {not_found}")
        print(f"   • Skipped (intro/conclusion): {skipped}")
        print(f"   • Matches current source: {matches}")
        print(f"   • Differs from current: {differs}")
        print(f"   • Success rate: {(found/(total-skipped)*100):.1f}%")

def main():
    """Main execution function"""

    verifier = BiblicalSourceWebVerifier()

    input_file = 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'
    output_file = f'Web_Verified_Biblical_Sources_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    print(f"🔍 Starting web verification of biblical sources...")
    print(f"📖 Input: {input_file}")
    print(f"💾 Output: {output_file}")

    try:
        # Perform verification
        results = verifier.verify_all_mitzvot(input_file)

        # Save results
        verifier.save_results(output_file)

        # Generate summary
        verifier.generate_summary_report()

        print(f"\n🎉 WEB VERIFICATION COMPLETE!")
        print(f"   📁 Results file: {output_file}")

    except Exception as e:
        print(f"\n❌ Verification failed: {e}")

if __name__ == "__main__":
    main()