import fitz

doc = fitz.open("input.pdf")
page = doc[0]
text = "hello"
page.insert_text(fitz.Point(0, 0), text, fontsize=11)
doc.save("output.pdf")