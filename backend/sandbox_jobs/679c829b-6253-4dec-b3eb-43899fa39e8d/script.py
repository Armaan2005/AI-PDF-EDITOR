import fitz

doc = fitz.open("input.pdf")

search_text = "armaan joshi"
replace_text = "armaan"

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # Search for all instances of the text to be replaced
    text_instances = page.search_for(search_text)
    
    # Store original rectangles before redaction to use for text insertion
    original_rects = []
    for inst in text_instances:
        original_rects.append(inst)
        # Add redaction annotation over the found text with white fill to hide it
        page.add_redact_annot(inst, fill=(1, 1, 1)) 
        
    # If any text was found and marked for redaction, apply redactions
    if original_rects:
        page.apply_redactions()
        
        # After redaction, insert the new text at the original positions
        for original_rect in original_rects:
            # Insert new text at the top-left corner of the original rectangle
            # Use a default font size and black color for the new text
            page.insert_text(fitz.Point(original_rect.x0, original_rect.y0), replace_text, fontsize=12, color=(0, 0, 0))

doc.save("output.pdf")
doc.close()