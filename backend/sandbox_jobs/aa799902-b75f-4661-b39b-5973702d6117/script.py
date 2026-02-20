import fitz

doc = fitz.open("input.pdf")
for page in doc:
    page.insert_text(fitz.Point(50, 50), "hello", fontsize=12, color=(0, 0, 0))
doc.save("output.pdf")