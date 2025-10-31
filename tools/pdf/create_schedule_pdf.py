#!/usr/bin/env python3
"""
Simple CSV to PDF Schedule Converter
Creates a clean, readable schedule from the Sefer HaMitzvos CSV
"""

import csv
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
from pathlib import Path

class MitzvosScheduleGenerator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.mitzvos_data = []
        self.load_csv_data()

    def load_csv_data(self):
        """Load and group CSV data by date"""
        grouped_data = {}
        with open(self.csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse date
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%A, %B %d, %Y')
                date_key = row['Date']  # Keep original date as key for grouping

                mitzvah_entry = {
                    'mitzvah_type': row['Mitzvah_Type_Number'],
                    'summary': row['Summary'],
                    'biblical_source': row['Biblical_Source'],
                    'sefaria_link': row['Sefaria_Link']
                }

                if date_key not in grouped_data:
                    grouped_data[date_key] = {
                        'formatted_date': formatted_date,
                        'date_obj': date_obj,
                        'mitzvot': []
                    }

                grouped_data[date_key]['mitzvot'].append(mitzvah_entry)

        # Convert to sorted list
        self.mitzvos_data = []
        for date_key in sorted(grouped_data.keys()):
            self.mitzvos_data.append(grouped_data[date_key])

    def generate_schedule_pdf(self, output_file="Sefer_HaMitzvos_Schedule.pdf"):
        """Generate a simple schedule PDF"""
        doc = SimpleDocTemplate(output_file, pagesize=A4,
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=1*inch, bottomMargin=1*inch)

        story = []
        styles = getSampleStyleSheet()

        # Title page
        title_style = ParagraphStyle('Title',
                                   fontSize=28,
                                   alignment=TA_CENTER,
                                   textColor=colors.darkblue,
                                   spaceAfter=30,
                                   fontName='Helvetica-Bold')

        story.append(Paragraph("Sefer HaMitzvos", title_style))
        story.append(Paragraph("Daily Study Schedule", title_style))
        story.append(Spacer(1, 0.5*inch))

        subtitle_style = ParagraphStyle('Subtitle',
                                      fontSize=16,
                                      alignment=TA_CENTER,
                                      textColor=colors.black,
                                      spaceAfter=40)

        story.append(Paragraph("Complete Schedule for Studying Maimonides'<br/>Enumeration of the 613 Commandments", subtitle_style))

        # Add introduction
        intro_style = ParagraphStyle('Intro',
                                   fontSize=12,
                                   alignment=TA_JUSTIFY,
                                   leftIndent=30,
                                   rightIndent=30,
                                   spaceAfter=15,
                                   leading=16)

        intro_paragraphs = [
            "<b>About This Schedule:</b> This document provides a systematic daily study plan for Maimonides' Sefer HaMitzvos, which enumerates and explains each of the 613 biblical commandments.",

            "<b>Structure:</b> The study begins with fundamental principles (Shorashim) for understanding how commandments are counted, followed by the positive commandments (248) and negative commandments (365).",

            "<b>Daily Study:</b> Each entry includes the mitzvah number, a concise description, biblical sources when available, and links to Sefaria.org for deeper study.",

            "<b>Duration:</b> This schedule spans approximately 1.7 years of daily study, providing a comprehensive foundation in Jewish law and ethics."
        ]

        for para in intro_paragraphs:
            story.append(Paragraph(para, intro_style))

        story.append(PageBreak())

        # Create the schedule table
        total_mitzvot = sum(len(entry['mitzvot']) for entry in self.mitzvos_data)
        print(f"Creating schedule with {len(self.mitzvos_data)} dates containing {total_mitzvot} mitzvot...")

        # Table headers
        headers = ['Date', 'Mitzvot & Descriptions', 'Biblical Sources']
        table_data = [headers]

        for entry in self.mitzvos_data:
            date_text = entry['formatted_date']
            mitzvot_list = entry['mitzvot']

            # Build combined mitzvot content
            mitzvot_content = ""
            sources_content = ""

            for i, mitzvah in enumerate(mitzvot_list):
                mitzvah_text = mitzvah['mitzvah_type']
                description_text = mitzvah['summary']
                source_text = mitzvah['biblical_source'] if mitzvah['biblical_source'] else "Traditional Sources"

                # Limit description length for better formatting
                if len(description_text) > 150:
                    description_text = description_text[:150] + "..."

                # Add to mitzvot content
                if i > 0:
                    mitzvot_content += "<br/><br/>"
                    sources_content += "<br/><br/>"

                mitzvot_content += f"<b>{mitzvah_text}</b><br/>{description_text}"
                sources_content += source_text

            row = [
                Paragraph(f"<font size=9><b>{date_text}</b></font>",
                         ParagraphStyle('DateCell', fontSize=9, alignment=TA_LEFT)),
                Paragraph(f"<font size=9>{mitzvot_content}</font>",
                         ParagraphStyle('MitzvotCell', fontSize=9, alignment=TA_LEFT)),
                Paragraph(f"<font size=8>{sources_content}</font>",
                         ParagraphStyle('SourceCell', fontSize=8, alignment=TA_LEFT))
            ]
            table_data.append(row)

        # Create the table with appropriate column widths
        table = Table(table_data, colWidths=[1.8*inch, 4.0*inch, 1.7*inch])

        # Style the table
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),

            # Grid lines
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        story.append(table)

        # Build the PDF
        print(f"Building PDF: {output_file}")
        doc.build(story)
        print(f"Schedule saved as: {output_file}")

def main():
    """Main function to generate the schedule"""
    repo_root = Path(__file__).resolve().parents[2]
    csv_path = repo_root / 'data' / 'Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv'

    if not csv_path.exists():
        print(f"Error: CSV file '{csv_path}' not found!")
        return

    print("Creating Sefer HaMitzvos PDF Schedule...")

    generator = MitzvosScheduleGenerator(str(csv_path))
    generator.generate_schedule_pdf("Sefer_HaMitzvos_Daily_Schedule.pdf")

    print("Schedule generation complete!")

if __name__ == "__main__":
    main()