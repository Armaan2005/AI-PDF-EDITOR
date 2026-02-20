doc = fitz.open("input.pdf")
for page in doc:
    page.draw_rect(page.rect, color=None, fill=(0, 0, 1), overlay=False)
doc.save("output.pdf")