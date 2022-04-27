## MODIFIED FROM: https://github.com/Ovyerus/deeppyer


from collections import namedtuple
from io import BytesIO
import math
import pkgutil
from typing import Tuple

from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import cv2
import numpy
import skimage

__all__ = ('Colour', 'ColourTuple', 'DefaultColours', 'deepfry')

Colour = Tuple[int, int, int]
ColourTuple = Tuple[Colour, Colour]


class DefaultColours:
    """Default colours provided for deepfrying"""
    red = ((254, 0, 2), (255, 255, 15))
    blue = ((36, 113, 229), (255,) * 3)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

FlarePosition = namedtuple('FlarePosition', ['x', 'y', 'size'])

def add_salt_and_pepper(image, amount):

    output = numpy.copy(numpy.array(image))

    # add salt
    nb_salt = numpy.ceil(amount * output.size * 0.5)
    coords = [numpy.random.randint(0, i - 1, int(nb_salt)) for i in output.shape[:2]]
    output[coords] = 1

    # add pepper
    nb_pepper = numpy.ceil(amount* output.size * 0.5)
    coords = [numpy.random.randint(0, i - 1, int(nb_pepper)) for i in output.shape[:2]]
    output[coords] = 0

    return Image.fromarray(output)

async def deepfry(img: Image, *, colours: ColourTuple = DefaultColours.red, flares: bool = False) -> Image:
    """
    Deepfry a given image.

    Parameters
    ----------
    img : `Image`
        Image to manipulate.
    colours : `ColourTuple`, optional
        A tuple of the colours to apply on the image.
    flares : `bool`, optional
        Whether or not to try and detect faces for applying lens flares.

    Returns
    -------
    `Image`
        Deepfried image.
    """
    # SHARPNESS = 3
    CONTRAST = 1.4
    BRIGHTNESS = 1.6
    SATURATION = 0.7
    NOISE = 2
 
    img = img.copy().convert('RGB')

    # CONTRAST
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(CONTRAST)

    # BRIGHTNESS
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(BRIGHTNESS)

    # SATURATION
    saturation = ImageEnhance.Color(img)
    img = saturation.enhance(SATURATION)

    img = img.filter(ImageFilter.UnsharpMask(radius = 2, percent = 150, threshold = 3))
    # NOISE
    skimg = numpy.asarray(img)
    for i in range(NOISE):
        skimg = skimage.util.random_noise(skimg, mode="gaussian")
    skimg = (255*skimg).astype(numpy.uint8)
    img = Image.fromarray(skimg)

    # Crush image to hell and back
    img = img.convert('RGB')
    width, height = img.width, img.height
    img = img.resize((int(width ** .95), int(height ** .95)), resample=Image.LANCZOS)
    img = img.resize((int(width ** .95), int(height ** .95)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    # img = ImageOps.posterize(img, 4)
    
    return img
