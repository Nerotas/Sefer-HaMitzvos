#!/usr/bin/env python3
"""
CSV to PDF Calendar Converter
Converts the Sefer HaMitzvos schedule CSV into a beautiful PDF calendar
"""

import csv
import calendar
from datetime import datetime, date
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

class MitzvosCalendarGenerator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.mitzvos_data = {}
        self.load_csv_data()

    def load_csv_data(self):
        """Load the CSV data and organize by date"""
        with open(self.csv_file, 'r', encoding='utf-8-sig') as file:  # utf-8-sig handles BOM
            reader = csv.DictReader(file)
            for row in reader:
                date_str = row['Date']
                self.mitzvos_data[date_str] = {
                    'mitzvah_type': row['Mitzvah_Type_Number'],
                    'summary': row['Summary'],
                    'biblical_source': row['Biblical_Source'],
                    'sefaria_link': row['Sefaria_Link']
                }

    def create_monthly_calendar(self, year, month):
        """Create a calendar layout for a specific month"""
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        # Create table data
        table_data = []

        # Header row with month and year
        header = [f"{month_name} {year}"]
        table_data.append([Paragraph(f"<b>{month_name} {year}</b>",
                                   ParagraphStyle('MonthHeader',
                                                fontSize=16,
                                                alignment=TA_CENTER,
                                                textColor=colors.darkblue))] + [''] * 6)

        # Days of week header
        days_header = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        table_data.append([Paragraph(f"<b>{day}</b>",
                                   ParagraphStyle('DayHeader',
                                                fontSize=10,
                                                alignment=TA_CENTER,
                                                textColor=colors.white)) for day in days_header])

        # Calendar weeks
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append('')
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    cell_content = f"<b>{day}</b>"

                    # Check if there's a mitzvah for this date
                    if date_str in self.mitzvos_data:
                        mitzvah_info = self.mitzvos_data[date_str]
                        mitzvah_type = mitzvah_info['mitzvah_type']
                        summary = mitzvah_info['summary']

                        # Escape HTML and truncate long summaries properly
                        summary = summary.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        if len(summary) > 80:
                            summary = summary[:80] + "..."

                        # Escape mitzvah type
                        mitzvah_type = mitzvah_type.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                        cell_content += f"<br/><font size=8><b>{mitzvah_type}</b></font>"
                        cell_content += f"<br/><font size=7>{summary}</font>"

                        if mitzvah_info['biblical_source']:
                            biblical_source = mitzvah_info['biblical_source'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                            cell_content += f"<br/><font size=6 color='blue'>{biblical_source}</font>"

                    week_data.append(Paragraph(cell_content,
                                             ParagraphStyle('DayCell',
                                                          fontSize=9,
                                                          alignment=TA_LEFT,
                                                          leftIndent=2,
                                                          rightIndent=2)))
            table_data.append(week_data)

        return table_data

    def generate_pdf_calendar(self, output_file="sefer_hamitzvos_calendar.pdf", start_year=2025, end_year=2026):
        """Generate the complete PDF calendar"""
        doc = SimpleDocTemplate(output_file, pagesize=A4,
                              rightMargin=0.5*inch, leftMargin=0.5*inch,
                              topMargin=0.5*inch, bottomMargin=0.5*inch)

        story = []
        styles = getSampleStyleSheet()

        # Title page
        title_style = ParagraphStyle('Title',
                                   fontSize=24,
                                   alignment=TA_CENTER,
                                   textColor=colors.darkblue,
                                   spaceAfter=20)

        story.append(Paragraph("<b>Sefer HaMitzvos</b>", title_style))
        story.append(Paragraph("<b>Daily Study Calendar</b>", title_style))
        story.append(Spacer(1, 0.5*inch))

        subtitle_style = ParagraphStyle('Subtitle',
                                      fontSize=14,
                                      alignment=TA_CENTER,
                                      textColor=colors.black,
                                      spaceAfter=30)

        story.append(Paragraph("A complete schedule for studying Maimonides' enumeration<br/>of the 613 commandments", subtitle_style))
        story.append(Spacer(1, 1*inch))

        # Add introduction text
        intro_style = ParagraphStyle('Intro',
                                   fontSize=11,
                                   alignment=TA_LEFT,
                                   leftIndent=20,
                                   rightIndent=20,
                                   spaceAfter=12)

        intro_text = """
        <b>About This Calendar:</b><br/><br/>

        This calendar provides a systematic approach to studying Maimonides' Sefer HaMitzvos
        (Book of Commandments), which enumerates and explains each of the 613 biblical commandments.<br/><br/>

        <b>Study Structure:</b><br/>
        • <b>Principles (Shorashim):</b> Fundamental rules for counting commandments<br/>
        • <b>Positive Commandments:</b> Actions we are commanded to perform<br/>
        • <b>Negative Commandments:</b> Actions we are forbidden from doing<br/><br/>

        Each day includes the mitzvah number, description, and biblical source when available.
        Sefaria links are provided for deeper study.<br/><br/>

        <b>How to Use:</b><br/>
        Follow the daily schedule to complete the entire Sefer HaMitzvos systematically.
        Each entry builds upon previous learning, creating a comprehensive understanding
        of the mitzvah system.
        """

        story.append(Paragraph(intro_text, intro_style))
        story.append(PageBreak())

        # Generate monthly calendars
        current_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        while current_date <= end_date:
            year = current_date.year
            month = current_date.month

            print(f"Generating calendar for {calendar.month_name[month]} {year}")

            table_data = self.create_monthly_calendar(year, month)

            # Create table
            table = Table(table_data, colWidths=[1.1*inch]*7)

            # Style the table
            table.setStyle(TableStyle([
                # Month header styling
                ('SPAN', (0, 0), (6, 0)),
                ('BACKGROUND', (0, 0), (6, 0), colors.lightblue),
                ('ALIGN', (0, 0), (6, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (6, 0), 16),
                ('BOTTOMPADDING', (0, 0), (6, 0), 12),

                # Days header styling
                ('BACKGROUND', (0, 1), (6, 1), colors.darkblue),
                ('TEXTCOLOR', (0, 1), (6, 1), colors.white),
                ('ALIGN', (0, 1), (6, 1), 'CENTER'),
                ('FONTSIZE', (0, 1), (6, 1), 10),
                ('BOTTOMPADDING', (0, 1), (6, 1), 6),

                # Calendar cells styling
                ('VALIGN', (0, 2), (-1, -1), 'TOP'),
                ('FONTSIZE', (0, 2), (-1, -1), 8),
                ('GRID', (0, 1), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, colors.lightgrey]),
                ('LEFTPADDING', (0, 2), (-1, -1), 3),
                ('RIGHTPADDING', (0, 2), (-1, -1), 3),
                ('TOPPADDING', (0, 2), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 2), (-1, -1), 8),
            ]))

            story.append(table)
            story.append(Spacer(1, 20))

            # Move to next month
            if month == 12:
                current_date = datetime(year + 1, 1, 1)
            else:
                current_date = datetime(year, month + 1, 1)

            # Add page break after every 2 months (except the last)
            if month % 2 == 0 and current_date <= end_date:
                story.append(PageBreak())

        # Build the PDF
        print(f"Building PDF: {output_file}")
        doc.build(story)
        print(f"Calendar saved as: {output_file}")

def main():
    """Main function to generate the calendar"""
    csv_file = "Schedule_Complete_Sefer_HaMitzvos_WithBiblical.csv"

    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        return

    print("Creating Sefer HaMitzvos PDF Calendar...")

    generator = MitzvosCalendarGenerator(csv_file)
    generator.generate_pdf_calendar("Sefer_HaMitzvos_Calendar_2025-2026.pdf")

    print("Calendar generation complete!")

if __name__ == "__main__":
    main()