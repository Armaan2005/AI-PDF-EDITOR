import fitz

doc = fitz.open("input.pdf")
for page in doc:
    text_instances = page.search_for("Armaan Joshi")
    for inst in text_instances:
        page.insert_text(inst.tl, "Armaan", fontsize=11, overlay=True)
        page.delete_text(inst)
doc.save("output.pdf")