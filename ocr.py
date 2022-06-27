from PIL import Image

import pytesseract

def ResizeImage(img, magnification):
    ImgWidth = img.width * magnification
    ImgHeight = img.height * magnification
    img_resize = img.resize((int(ImgWidth), int(ImgHeight)), Image.LANCZOS)
    return img_resize

I = Image.open('test.png')
I = I.crop((0,50,400,450))
# I = I.crop((0,50,300,150))
I = ResizeImage(I, 0.3)
I.save("test-cropped.png")
# print(pytesseract.image_to_string(I))
# print(pytesseract.image_to_string(I, lang="jpn"))
print(pytesseract.image_to_string(I, lang="jpn", config="-c tessedit_char_whitelist=0123456789m.").split("\n"))