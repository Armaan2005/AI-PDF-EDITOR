import fitz

doc = fitz.open("input.pdf")

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # Search for "armaan joshi"
    text_instances = page.search_for("armaan joshi")
    
    # If instances are found, redact and replace
    if text_instances:
        # First, add redaction annotations for all found instances
        for rect in text_instances:
            # Redact with a white fill to hide the original text
            page.add_redact_annot(rect, fill=(1, 1, 1))
        
        # Apply all redactions on the page
        page.apply_redactions()
        
        # Now, insert the new text at the approximate original positions
        # Using a fontsize of 12 as a reasonable default for "same font size"
        # The y-offset (+10) is based on the PyMuPDF critical rule example for replacement.
        for rect in text_instances:
            page.insert_text(fitz.Point(rect.x0, rect.y0 + 10), "armaan", fontsize=12)

doc.save("output.pdf")