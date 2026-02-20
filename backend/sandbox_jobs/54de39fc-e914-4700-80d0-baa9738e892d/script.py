doc = fitz.open("input.pdf")
for page in doc:
    page.replace_string("armaan joshi", "armaan")
doc.save("output.pdf")