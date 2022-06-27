from PIL import Image
import pytesseract


I = Image.open('test.png')
# I = I.convert("L").point(lambda x: 255 if x < 255 else 0, mode="1")
# I = I.crop((0,50,500,400))
I = I.crop((0,50,500,300))
# I = ResizeImage(I)
I.save("test-cropped.png")
print(pytesseract.image_to_string(I, config="digits"))
print(pytesseract.image_to_string(I, lang="jpn", config="digits"))