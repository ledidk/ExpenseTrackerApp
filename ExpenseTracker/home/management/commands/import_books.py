# books/management/commands/import_books.py

import pandas as pd
from django.core.management.base import BaseCommand
from home.models import Book

class Command(BaseCommand):
    help = 'Import books from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        df = pd.read_excel(file_path)
        
        # Specify the exact date format to ensure proper conversion
        """
        df['published_date'] = pd.to_datetime(df['published_date'], format='%d/%m/%Y', errors='coerce').dt.date
        """
        df['published_date'] = pd.to_datetime(df['published_date'].astype(str).str.strip(), format='%d/%m/%Y', errors='coerce').dt.date


        print(df)

        
        for _, row in df.iterrows():
            if pd.isna(row['published_date']):
                print(f"Skipping row with invalid date: {row}")
                continue

            if pd.isna(row['published_date']):
                print(f"Skipping row with invalid date: {row}")
                continue
            
            Book.objects.create(
                isbn=row['id'],  # Assuming 'id' corresponds to 'isbn'
                title=row['title'],
                subtitle=row['subtitle'],
                authors=row['authors'],
                publisher=row['publisher'],
                publish_date=row['published_date'],
                category=row['category'],
                distribution_expense=row['distribution_expense']
            )
        self.stdout.write(self.style.SUCCESS('Books imported successfully'))



""" 
import pandas as pd
from django.core.management.base import BaseCommand
from home.models import Book

class Command(BaseCommand):
    help = 'Import book data from an Excel or CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel or CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        # Read Excel or CSV file using pandas
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        
        # Iterate through the data and save each row to the database
        for _, row in data.iterrows():
            book = Book(
                isbn=row['ISBN'],
                title=row['Title'],
                subtitle=row.get('Subtitle', ''),  # Handle missing subtitles
                authors=row['Authors'],
                publisher=row['Publisher'],
                publish_date=row['Published Date'],
                category=row['Category'],
                distribution_expense=row['Distribution Expense ($)']
            )
            book.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully imported book data'))

        
"""