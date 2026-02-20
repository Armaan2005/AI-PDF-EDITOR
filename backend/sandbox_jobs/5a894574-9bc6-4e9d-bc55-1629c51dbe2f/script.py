import fitz

def add_text_top_left(input_pdf_path, output_pdf_path, text_to_add="hello"):
    doc = fitz.open(input_pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Define the position for "top left" (e.g., x=50, y=50 for some padding)
        # Assuming origin (0,0) is top-left
        point = fitz.Point(50, 50) 
        
        # Add the text
        page.insert_text(point, text_to_add, fontsize=12, color=(0, 0, 0)) # Black color
        
    doc.save(output_pdf_path)
    doc.close()

if __name__ == '__main__':
    # This is example usage and will not be executed in the final environment.
    # Replace 'input.pdf' with your actual input file name.
    # Replace 'output.pdf' with your desired output file name.
    # A dummy PDF creation for testing purposes if run standalone
    try:
        doc = fitz.open()
        doc.new_page()
        doc[0].insert_text(fitz.Point(100, 100), "Original content")
        doc.save("input.pdf")
        doc.close()
    except Exception as e:
        pass # Ignore if file creation fails in restricted environment

    add_text_top_left("input.pdf", "output.pdf", "hello")