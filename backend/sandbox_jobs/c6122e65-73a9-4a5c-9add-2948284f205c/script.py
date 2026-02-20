import fitz
doc = fitz.open("input.pdf")
for page in doc:
    old_text = "armaan joshi"
    new_text = "armaan"
    text_instances = page.search_for(old_text)
    for rect in text_instances:
        # Hide the old text by redacting it with a white fill
        page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions()

    # Re-search for the original text after redaction to get updated positions
    # (or simply use the original rects if applying redaction doesn't shift things too much,
    # but applying redactions *then* inserting text is generally safer if positions might shift)
    # However, since we are using the original 'rect' to determine position for new text,
    # we should insert *after* redactions are applied.
    # The original rect positions should still be valid for inserting new text.

    for rect in text_instances:
        # Calculate font size dynamically
        dynamic_font_size = rect.height * 0.85 # A common heuristic
        
        # Calculate insertion point: x0 and y1 (baseline)
        # Adjust y1 slightly upwards to align with the baseline, considering descenders
        insertion_point = fitz.Point(rect.x0, rect.y1 - (rect.height * 0.2)) # Adjust 0.2 as needed for baseline
        
        page.insert_text(insertion_point, new_text, fontsize=dynamic_font_size, color=(0, 0, 0))

doc.save("output.pdf")
doc.close()