#!/usr/bin/env python3
"""
Comprehensive Mitzvah Analysis Tool
1. Web search for existing comparisons between Rambam's 613 mitzvot order and Sefer HaMitzvot
2. Compare all schedule summaries to master list entries to find semantic matches
3. Identify mismatched sources even when mitzvot content matches
"""

import csv
import re
import time
from datetime import datetime
from difflib import SequenceMatcher
import requests
from urllib.parse import quote_plus

def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_text_for_comparison(text):
    """Normalize text for better comparison by removing common variations."""
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove common prefixes/patterns
    text = re.sub(r'^(to|we are commanded to|not to)', '', text)
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = text.strip()

    # Replace common variations
    replacements = {
        'g-d': 'god',
        'g‑d': 'god',
        'tzitzit': 'fringes',
        'tefillin': 'phylacteries',
        'shabbat': 'sabbath',
        'sukkot': 'tabernacles',
        'mezuzah': 'doorpost',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

def extract_key_concepts(text):
    """Extract key concepts from mitzvah text."""
    normalized = normalize_text_for_comparison(text)

    # Key concept patterns
    concepts = []

    # Religious concepts
    if any(word in normalized for word in ['god', 'lord', 'almighty', 'divine']):
        concepts.append('deity')

    if any(word in normalized for word in ['pray', 'prayer', 'worship', 'serve']):
        concepts.append('worship')

    if any(word in normalized for word in ['fringes', 'tzitzit', 'four-cornered', 'garment']):
        concepts.append('tzitzit')

    if any(word in normalized for word in ['tefillin', 'phylacteries', 'head', 'arm', 'hand']):
        concepts.append('tefillin')

    if any(word in normalized for word in ['mezuzah', 'doorpost', 'door']):
        concepts.append('mezuzah')

    if any(word in normalized for word in ['sabbath', 'seventh day', 'rest']):
        concepts.append('sabbath')

    if any(word in normalized for word in ['sukkot', 'tabernacles', 'booth']):
        concepts.append('sukkot')

    if any(word in normalized for word in ['lulav', 'etrog', 'four species']):
        concepts.append('four_species')

    if any(word in normalized for word in ['circumcis', 'brit', 'eighth day']):
        concepts.append('circumcision')

    if any(word in normalized for word in ['kasher', 'kosher', 'eat', 'food']):
        concepts.append('dietary')

    if any(word in normalized for word in ['temple', 'sanctuary', 'house', 'build']):
        concepts.append('temple')

    if any(word in normalized for word in ['priest', 'kohen', 'blessing', 'bless']):
        concepts.append('priestly')

    return concepts

def web_search_mitzvah_comparison():
    """Search for existing scholarly work comparing different mitzvah lists."""
    print("=== WEB SEARCH: Existing Scholarly Comparisons ===\n")

    search_terms = [
        "Rambam Sefer HaMitzvot 613 mitzvot order comparison",
        "Maimonides mitzvot enumeration differences scholarly analysis",
        "Sefer HaMitzvot vs traditional 613 list academic study",
        "Rambam mitzvot numbering system comparison research"
    ]

    findings = []

    for term in search_terms:
        print(f"Searching: {term}")
        try:
            # Create a search URL (using DuckDuckGo)
            url = f"https://duckduckgo.com/?q={quote_plus(term)}&t=h_&ia=web"
            print(f"Search URL: {url}")

            # Note: In a full implementation, you'd parse search results
            # For this analysis, we document the search approach
            findings.append({
                'search_term': term,
                'search_url': url,
                'note': 'Manual review required - automated parsing of search results not implemented'
            })

            time.sleep(2)  # Be respectful to search engines

        except Exception as e:
            print(f"Error searching for {term}: {e}")

    print(f"Created {len(findings)} search queries for manual review\n")
    return findings

def load_schedule_data():
    """Load the main schedule CSV file."""
    schedule_data = []
    try:
        with open('Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                schedule_data.append(row)
        print(f"Loaded {len(schedule_data)} schedule entries")
    except Exception as e:
        print(f"Error loading schedule: {e}")

    return schedule_data

def load_master_list():
    """Load the master list CSV file."""
    master_data = []
    try:
        with open('archive/MitzvosMasterList.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                master_data.append(row)
        print(f"Loaded {len(master_data)} master list entries")
    except Exception as e:
        print(f"Error loading master list: {e}")

    return master_data

def analyze_concept_matches(schedule_data, master_data):
    """Find potential matches based on key concepts."""
    print("\n=== CONCEPT-BASED ANALYSIS ===\n")

    matches = []

    for sched_entry in schedule_data:
        # Skip intro entries
        if 'Intro' in sched_entry.get('Mitzvah_Type_Number', ''):
            continue

        sched_summary = sched_entry.get('Summary', '')
        sched_source = sched_entry.get('Biblical_Source', '')
        sched_concepts = extract_key_concepts(sched_summary)

        if not sched_concepts:  # Skip entries without clear concepts
            continue

        best_matches = []

        for master_entry in master_data:
            master_mitzvah = master_entry.get('Mitzvah', '')
            master_source = master_entry.get('Biblical Reference', '')
            master_concepts = extract_key_concepts(master_mitzvah)

            # Check for concept overlap
            concept_overlap = set(sched_concepts) & set(master_concepts)

            if concept_overlap:
                # Calculate text similarity
                text_sim = similarity(sched_summary, master_mitzvah)

                match_info = {
                    'schedule_num': sched_entry.get('Sequential_Number'),
                    'schedule_type': sched_entry.get('Mitzvah_Type_Number'),
                    'schedule_summary': sched_summary,
                    'schedule_source': sched_source,
                    'master_num': master_entry.get('Number'),
                    'master_mitzvah': master_mitzvah,
                    'master_source': master_source,
                    'shared_concepts': list(concept_overlap),
                    'text_similarity': text_sim,
                    'source_match': sched_source == master_source
                }

                best_matches.append(match_info)

        # Sort by similarity and keep top matches
        best_matches.sort(key=lambda x: x['text_similarity'], reverse=True)

        # Report high-confidence matches
        for match in best_matches[:3]:  # Top 3 matches
            if match['text_similarity'] > 0.3 or len(match['shared_concepts']) > 1:
                matches.append(match)

    return matches

def identify_source_mismatches(matches):
    """Identify cases where mitzvot match but sources differ."""
    print("=== SOURCE MISMATCH ANALYSIS ===\n")

    source_mismatches = []
    high_confidence_matches = []

    for match in matches:
        # High confidence matches (similar content)
        if match['text_similarity'] > 0.5 or len(match['shared_concepts']) >= 2:
            high_confidence_matches.append(match)

            # Check for source mismatches
            if not match['source_match'] and match['schedule_source'] and match['master_source']:
                source_mismatches.append(match)

    print(f"Found {len(high_confidence_matches)} high-confidence content matches")
    print(f"Found {len(source_mismatches)} source mismatches among high-confidence matches\n")

    return source_mismatches, high_confidence_matches

def generate_detailed_report(web_findings, source_mismatches, high_confidence_matches, all_matches):
    """Generate a comprehensive analysis report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comprehensive_mitzvah_analysis_{timestamp}.csv"

    print(f"Generating detailed report: {filename}")

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Analysis_Type',
            'Schedule_Num', 'Schedule_Type', 'Schedule_Summary', 'Schedule_Source',
            'Master_Num', 'Master_Mitzvah', 'Master_Source',
            'Shared_Concepts', 'Text_Similarity', 'Source_Match', 'Notes'
        ])

        # Web search findings
        writer.writerow(['=== WEB SEARCH FINDINGS ==='])
        for finding in web_findings:
            writer.writerow([
                'Web_Search',
                '', '', finding['search_term'], '',
                '', '', '',
                '', '', '', finding['search_url']
            ])

        writer.writerow([''])  # Blank row

        # Source mismatches (highest priority)
        writer.writerow(['=== SOURCE MISMATCHES (Same Mitzvah, Different Source) ==='])
        for match in source_mismatches:
            writer.writerow([
                'Source_Mismatch',
                match['schedule_num'], match['schedule_type'],
                match['schedule_summary'], match['schedule_source'],
                match['master_num'], match['master_mitzvah'], match['master_source'],
                '; '.join(match['shared_concepts']), f"{match['text_similarity']:.3f}",
                match['source_match'], 'NEEDS VERIFICATION'
            ])

        writer.writerow([''])  # Blank row

        # High confidence matches
        writer.writerow(['=== HIGH CONFIDENCE MATCHES ==='])
        for match in high_confidence_matches:
            notes = 'Good Match'
            if not match['source_match']:
                notes += ' - CHECK SOURCE'

            writer.writerow([
                'High_Confidence',
                match['schedule_num'], match['schedule_type'],
                match['schedule_summary'], match['schedule_source'],
                match['master_num'], match['master_mitzvah'], match['master_source'],
                '; '.join(match['shared_concepts']), f"{match['text_similarity']:.3f}",
                match['source_match'], notes
            ])

        writer.writerow([''])  # Blank row

        # All other matches
        writer.writerow(['=== ALL OTHER POTENTIAL MATCHES ==='])
        other_matches = [m for m in all_matches if m not in high_confidence_matches]
        for match in other_matches[:50]:  # Limit to avoid huge file
            writer.writerow([
                'Potential_Match',
                match['schedule_num'], match['schedule_type'],
                match['schedule_summary'], match['schedule_source'],
                match['master_num'], match['master_mitzvah'], match['master_source'],
                '; '.join(match['shared_concepts']), f"{match['text_similarity']:.3f}",
                match['source_match'], 'Review Needed'
            ])

    print(f"Report saved: {filename}")
    return filename

def print_summary_report(web_findings, source_mismatches, high_confidence_matches):
    """Print a summary to console."""
    print("\n" + "="*60)
    print("COMPREHENSIVE MITZVAH ANALYSIS SUMMARY")
    print("="*60)

    print(f"\n1. WEB SEARCH QUERIES CREATED: {len(web_findings)}")
    for finding in web_findings:
        print(f"   - {finding['search_term']}")

    print(f"\n2. SOURCE MISMATCHES FOUND: {len(source_mismatches)}")
    if source_mismatches:
        print("   Examples:")
        for i, match in enumerate(source_mismatches[:3], 1):
            print(f"   {i}. Schedule #{match['schedule_num']}: {match['schedule_summary'][:60]}...")
            print(f"      Schedule Source: {match['schedule_source']}")
            print(f"      Master Source:   {match['master_source']}")
            print(f"      Similarity: {match['text_similarity']:.3f}")
            print()

    print(f"\n3. HIGH CONFIDENCE MATCHES: {len(high_confidence_matches)}")

    # Example: The tzitzit case you mentioned
    tzitzit_found = False
    for match in high_confidence_matches:
        if 'tzitzit' in match['shared_concepts'] or 'fringes' in match['schedule_summary'].lower():
            print(f"   TZITZIT EXAMPLE FOUND:")
            print(f"   Schedule: {match['schedule_summary']}")
            print(f"   Schedule Source: {match['schedule_source']}")
            print(f"   Master: {match['master_mitzvah']}")
            print(f"   Master Source: {match['master_source']}")
            print(f"   Source Match: {match['source_match']}")
            tzitzit_found = True
            break

    if not tzitzit_found:
        print("   Tzitzit example not found in high confidence matches - may need manual review")

    print(f"\n4. NEXT STEPS:")
    print("   - Review web search results manually")
    print("   - Verify source mismatches against authoritative texts")
    print("   - Update schedule with correct biblical sources")
    print("   - Consider creating mapping between Sefer HaMitzvot and traditional order")

def main():
    """Main analysis function."""
    print("Starting Comprehensive Mitzvah Analysis...")
    print("="*50)

    # 1. Web search for existing scholarly work
    web_findings = web_search_mitzvah_comparison()

    # 2. Load data
    schedule_data = load_schedule_data()
    master_data = load_master_list()

    if not schedule_data or not master_data:
        print("Error: Could not load required data files")
        return

    # 3. Analyze concept matches
    all_matches = analyze_concept_matches(schedule_data, master_data)
    print(f"Found {len(all_matches)} potential matches")

    # 4. Identify source mismatches
    source_mismatches, high_confidence_matches = identify_source_mismatches(all_matches)

    # 5. Generate detailed report
    report_filename = generate_detailed_report(web_findings, source_mismatches, high_confidence_matches, all_matches)

    # 6. Print summary
    print_summary_report(web_findings, source_mismatches, high_confidence_matches)

    print(f"\nAnalysis complete. Detailed results saved to: {report_filename}")

if __name__ == "__main__":
    main()