import fitz
doc = fitz.open("input.pdf")

for page_num in range(len(doc)):
    page = doc[page_num]
    
    old_text = "armaan joshi"
    new_text = "armaan"
    
    text_instances = page.search_for(old_text)
    
    for inst in text_instances:
        # Hide the old text by redacting it with a white fill
        page.add_redact_annot(inst, fill=(1, 1, 1))
    
    # Apply all redactions on the page
    page.apply_redactions()
    
    # Now insert the new text
    for inst in text_instances:
        # Calculate font size dynamically based on the height of the original text instance
        # Use a factor like 0.85 to make it fit well within the original height
        dynamic_size = inst.height * 0.85
        
        # Calculate the baseline for the new text.
        # insert_text places text starting at the given point (x, y) where y is the baseline.
        # inst.y1 is the bottom of the rectangle. Adjust it slightly upwards for the baseline.
        baseline_y = inst.y1 - (inst.height * 0.2)
        
        # Insert the new text. PyMuPDF's default font (usually Helvetica) is used here,
        # which is the closest we can get to "same font style" without specific font detection
        # and embedding which is beyond simple text insertion.
        page.insert_text(fitz.Point(inst.x0, baseline_y), new_text, 
                         fontsize=dynamic_size, 
                         color=(0, 0, 0)) # Black color for the new text

doc.save("output.pdf")
doc.close()