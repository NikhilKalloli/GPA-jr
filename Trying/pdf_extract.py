import PyPDF2

# Open the PDF file in read binary mode
with open("CSE_Core.pdf", "rb") as pdf_file:
    # Create a PdfFileReader object
    read_pdf = PyPDF2.PdfReader(pdf_file)
    
    # Get the total number of pages in the PDF
    number_of_pages = len(read_pdf.pages)

    
    # Initialize an empty string to store the content of all pages
    all_page_content = ""
    
    # Loop through each page in the PDF
    for page_number in range(number_of_pages):
        # Extract the text content of the current page
        page = read_pdf.pages[page_number]
        page_content = page.extract_text()
        
        # Append the text content of the current page to the string
        all_page_content += page_content

# Save the extracted text to a text file
with open("cse.txt", "w", encoding="utf-8") as text_file:
    text_file.write(all_page_content)

print("Text extracted from PDF and saved to extracted_text.txt")
