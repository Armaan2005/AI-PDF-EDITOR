import fitz

doc = fitz.open("input.pdf")

search_term = "armaan joshi"
replace_term = "armaan"

for page_num, page in enumerate(doc):
    text_blocks = page.get_text("rawdict")["blocks"]
    
    # Store replacements found on this page to apply them after extraction is complete.
    # This prevents issues where modifying the page affects subsequent text extraction.
    replacements_to_apply = [] # Stores (rect_to_erase, insertion_point, font_size, text_color)

    for block in text_blocks:
        if block['type'] == 0:  # This is a text block
            for line in block['lines']:
                for span in line['spans']:
                    span_text = span['text']
                    
                    # We need character-level bounding boxes for precise substring replacement.
                    # If 'chars' is missing, we cannot guarantee precise placement and size,
                    # so we skip this span for exact replacement.
                    if not span.get('chars'):
                        continue

                    start_index_in_span_text = 0
                    while True:
                        # Find the search_term within the span's text
                        match_start_idx = span_text.find(search_term, start_index_in_span_text)
                        if match_start_idx == -1:
                            break # No more occurrences in this span

                        match_end_idx = match_start_idx + len(search_term)

                        char_details = span['chars']
                        
                        current_char_text_pos = 0
                        start_char_array_idx = -1 # Index in char_details for the first char of search_term
                        end_char_array_idx = -1   # Index in char_details for the char after search_term

                        # Map text index to char_details array index
                        for i, char_info in enumerate(char_details):
                            if current_char_text_pos == match_start_idx:
                                start_char_array_idx = i
                            if current_char_text_pos == match_end_idx:
                                end_char_array_idx = i
                                break # Found both start and end character array indices
                            current_char_text_pos += len(char_info['c'])

                        # If the match extends to the end of the span's characters
                        if end_char_array_idx == -1:
                            end_char_array_idx = len(char_details)

                        # If for some reason we couldn't find the start character index (shouldn't happen if match_start_idx is valid)
                        if start_char_array_idx == -1 or start_char_array_idx >= end_char_array_idx:
                            start_index_in_span_text = match_end_idx
                            continue

                        # Extract the character bounding boxes relevant to the search_term
                        matched_char_boxes = char_details[start_char_array_idx : end_char_array_idx]
                        
                        # Calculate the overall bounding box for the search_term
                        x0 = min(c['bbox'][0] for c in matched_char_boxes)
                        y0 = min(c['bbox'][1] for c in matched_char_boxes)
                        x1 = max(c['bbox'][2] for c in matched_char_boxes)
                        y1 = max(c['bbox'][3] for c in matched_char_boxes)
                        
                        rect_to_erase = fitz.Rect(x0, y0, x1, y1)

                        # Convert integer color (0xRRGGBB) to (R, G, B) tuple for PyMuPDF drawing
                        color_int = span['color']
                        text_color = (
                            ((color_int >> 16) & 0xFF) / 255.0,
                            ((color_int >> 8) & 0xFF) / 255.0,
                            (color_int & 0xFF) / 255.0
                        )

                        # Determine the insertion point for the new text.
                        # Using the bottom-left of the original text's bounding box as the baseline
                        # for the new text typically provides good vertical alignment.
                        insertion_point = fitz.Point(rect_to_erase.x0, rect_to_erase.y1)

                        replacements_to_apply.append((rect_to_erase, insertion_point, span['size'], text_color))
                        
                        start_index_in_span_text = match_end_idx # Continue searching after this match

    # After gathering all replacement details for the current page, apply them.
    for rect_to_erase, insertion_point, font_size, text_color in replacements_to_apply:
        # Erase the old text by drawing a white rectangle over its bounding box.
        # `overlay=False` is critical to draw *underneath* existing content if it were drawn later,
        # but in this case, it ensures the rectangle fills the space without affecting text stream.
        # Assumes a white background for effective 'erasing'.
        page.draw_rect(rect_to_erase, fill=(1, 1, 1), overlay=False)

        # Insert the new text using the exact font size and color of the original text.
        # PyMuPDF will use a default font (e.g., Helvetica) if 'fontname' is not specified or registered.
        # The user only requested "same font size", not specific font family.
        page.insert_text(insertion_point, replace_term, fontsize=font_size, color=text_color)

doc.save("output.pdf")