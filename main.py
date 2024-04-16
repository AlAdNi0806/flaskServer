from textRecogniton.doc2text.reader import Reader


reader = Reader()
result = reader.doc2text("test.png")

print(result[0])