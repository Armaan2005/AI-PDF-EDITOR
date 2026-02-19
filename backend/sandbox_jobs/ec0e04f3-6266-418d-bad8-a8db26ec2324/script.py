import fitz

doc = fitz.open("input.pdf")
new_doc = fitz.open()

for page_num in range(len(doc)):
    page = doc[page_num]
    
    page_rect = page.rect
    
    new_page = new_doc.new_page(width=page_rect.width, height=page_rect.height)
    
    background_rect = fitz.Rect(0, 0, page_rect.width, page_rect.height)
    blue_color = (0, 0, 1) # RGB color for blue
    
    new_page.draw_rect(background_rect, color=blue_color, fill=blue_color)
    
    new_page.show_pdf_page(new_page.rect, doc, page_num) 

new_doc.save("output.pdf")
new_doc.close()
doc.close()