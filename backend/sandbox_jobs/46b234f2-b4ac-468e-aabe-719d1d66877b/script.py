import fitz

doc = fitz.open("input.pdf")

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # List to store original rectangle details for later text insertion
    replacements_data = []

    old_text_to_find = "armaan joshi"
    new_text_to_insert = "armaan"
    
    # Search for all instances of the old text on the page
    text_instances = page.search_for(old_text_to_find)
    
    for rect in text_instances:
        # Store the original rectangle information before redaction
        replacements_data.append({
            "rect": rect,
            "new_text": new_text_to_insert
        })
        # Add a redaction annotation over the found text.
        # fill=(1,1,1) makes the redaction white, effectively hiding the text.
        page.add_redact_annot(rect, fill=(1, 1, 1))

    # Apply all redactions added to the current page.
    # This permanently removes the text content and replaces it with the redaction fill.
    page.apply_redactions()

    # Now, iterate through the stored data to insert the new text
    for item in replacements_data:
        original_rect = item["rect"]
        text_content = item["new_text"]

        # Dynamically calculate the font size based on the original text's height
        dynamic_font_size = original_rect.height * 0.85
        
        # Calculate the insertion point for the new text's baseline.
        # (rect.x0, rect.y1 - (rect.height * 0.2)) aligns with the original text's baseline.
        insert_point = fitz.Point(original_rect.x0, original_rect.y1 - (original_rect.height * 0.2))
        
        # Insert the new text. Color is set to black (0,0,0) as original color cannot be extracted securely.
        page.insert_text(insert_point, text_content, fontsize=dynamic_font_size, color=(0, 0, 0))

doc.save("output.pdf")
doc.close()