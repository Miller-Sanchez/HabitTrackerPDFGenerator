import os
import requests
import re
import subprocess
from PyPDF2 import PdfMerger

# Number of habit trackers to create
n = int(input("Enter the number of habit trackers to create: "))


# List to keep track of generated PDF filenames
pdf_filenames = []

for i in range(n):
    # Fetch a random quote from Quotes REST API
    response = requests.get("https://api.quotable.io/random")
    quote_data = response.json()

    quote = quote_data['content']
    author = quote_data['author']
    formatted_quote = f"{quote} - {author}"

    # Read the LaTeX file
    with open('habit_traker.tex', 'r') as file:
        latex_content = file.read()

    # Escape special characters in the formatted_quote
    escaped_quote = re.escape(formatted_quote)

    # Replace the existing \changefooter{} content with the new quote
    new_latex_content = re.sub(r'\\changefooter\{.*\}', r'\\changefooter{' + escaped_quote + '}', latex_content)

    # Write the updated content back to a new LaTeX file
    tex_filename = f'document_{i}.tex'
    with open(tex_filename, 'w') as file:
        file.write(new_latex_content)

    # Compile the updated LaTeX document into a PDF
    #subprocess.run(['pdflatex', tex_filename])
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])


    # Append the generated PDF filename to the list
    pdf_filenames.append(f'document_{i}.pdf')

    # Clean up auxiliary files
    os.remove(f'document_{i}.aux')
    os.remove(f'document_{i}.log')
    os.remove(tex_filename)

# Merge all generated PDFs into a single PDF
merger = PdfMerger()

for pdf_filename in pdf_filenames:
    merger.append(pdf_filename)

output_filename = 'merged_habit_tracker.pdf'
merger.write(output_filename)
merger.close()

# Clean up the individual PDF files
for pdf_filename in pdf_filenames:
    os.remove(pdf_filename)

print(f"All habit trackers merged into {output_filename}")
