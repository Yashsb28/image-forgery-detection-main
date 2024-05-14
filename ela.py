from PIL import Image, ImageChops, ImageEnhance
from io import BytesIO

def convert_toJPEGandQuality(new_img, quality):
    with BytesIO() as f:
        new_img.save(f, "JPEG", quality=quality)
        return f.getvalue()

# converts input image to ela applied image
def convert_to_ela_image(img, quality = 90):

    original_image = img.convert("RGB")
    resaved_image = Image.open(BytesIO(convert_toJPEGandQuality(img, quality)))

    # pixel difference between original and resaved image
    ela_image = ImageChops.difference(original_image, resaved_image)

    # scaling factors are calculated from pixel extremas
    extrema = ela_image.getextrema()
    max_difference = max([pix[1] for pix in extrema])
    if max_difference == 0:
        max_difference = 1
    scale = 350.0 / max_difference

    # enhancing elaimage to brighten the pixels
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image