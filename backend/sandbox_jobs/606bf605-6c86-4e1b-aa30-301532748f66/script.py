import fitz

doc = fitz.open("input.pdf")
for page in doc:
    rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
    page.draw_rect(rect, color=(0, 0, 1), fill=(0, 0, 1), overlay=False)
doc.save("output.pdf")