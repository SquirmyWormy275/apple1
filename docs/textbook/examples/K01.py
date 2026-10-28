from tools.card_book import compile_books, decode_book

payloads, pages, manifest = compile_books()
assert len(pages) == 50
for record in manifest["books"]:
    decoded, answer = decode_book(payloads[record["name"]])
    assert decoded == pages[record["name"]]
    assert answer == record["answer_page"]
print("Original lesson books: 42")
print("All reading books:", len(pages))
print("Display pages:", sum(len(p) for p in pages.values()))
print("Largest book bytes:", max(len(payloads[name]) for name in pages))
print("Display: prose <=39x23; atlas <=40x24, uppercase SPACE-$5F")
print("RAM reader: $0800; book buffer: $1000-$7FFF")
print("Physical acceptance: pending")
