import os
import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
import textwrap

from wonderwords import RandomSentence


fonts = ['/home/andy/Documents/6.869/final_project/comic-sans-ms/comic_sans.ttf',
         '/home/andy/Documents/6.869/final_project/Impact-Font/impact.ttf']


def find_largest_dim(image_dir):
    """
    Find the largest image dimension out of a set of images inside of image_dir
    """
    filenames = os.listdir(image_dir)


    largest_dim = 0
    for filename in filenames:
        img = cv2.imread(os.path.join(image_dir, filename))
        if img.shape[0] > largest_dim:
            largest_dim = img.shape[0]
        if img.shape[1] > largest_dim:
            largest_dim = img.shape[1]

    return largest_dim


def pad_images(src_dir, output_dir):
    """
    Pads the images in src_dir with zeros in order to match the size of the largest image
    dimensions out of all of the images. The output are square images with the same filenames in
    output_dir
    """

    max_dim = find_largest_dim(src_dir)

    filenames = os.listdir(src_dir)

    print(f'Padding {len(filenames)} memes...')
    for filename in tqdm(filenames):
        img = cv2.imread(os.path.join(src_dir, filename))
        result = np.full((max_dim, max_dim, 3), (0, 0, 0), dtype=np.uint8)

        # compute center offset
        x_center = (max_dim - img.shape[0]) // 2
        y_center = (max_dim - img.shape[1]) // 2

        # copy img image into center of result image
        result[x_center:x_center+img.shape[0],
               y_center:y_center+img.shape[1]] = img

        save_file = os.path.join(output_dir, filename)
        cv2.imwrite(save_file, result)


def generate_text_imgs(output_dir, size, num=1000):
    """
    Generate num amount of images of shape (size, size) with random text. The size and font of the
    texts varies randomly for each image. Images are saved to output_dir
    """
    fill = (255, 255, 255)  #TextColor
    stroke_fill = (0,0,0)   #Color of the text outline

    generator = RandomSentence()
    print(f'Generating {1000} random text images...')
    for i in tqdm(range(num)):
        np_img = np.full((size, size, 3), (255, 255, 255), dtype=np.uint8)
        img = Image.fromarray(np_img)
        d = ImageDraw.Draw(img)

        

        # Pick the parameters randomly
        font_size = np.random.randint(200, 400)
        line_spacing = int(font_size / 10)  #Space between lines
        font_file = fonts[1]
        font = ImageFont.truetype(font_file, size=font_size)

        height = 0
        while height <= size - 150:
            caption = generator.sentence().upper()

            starting_x = np.random.randint(0, size // 4)
            char_width = font.getsize('A')[0]
            split_caption = textwrap.wrap(caption, width=(size - starting_x) / char_width)

            text_height = d.textsize(split_caption[0], font=font)

            # just draw first part of caption
            for line in split_caption:
                x, y = starting_x, height
                for char in line:
                    w, h = font.getsize(char)
                    d.text((x, y), char,
                           fill=fill, stroke_width=5,
                           font=font, stroke_fill=stroke_fill)
                    x += w + 10
                height += h + 100
                if height > size - 150:
                    break


        img.save(os.path.join(output_dir, f'text_{i}.png'))


if __name__ == '__main__':

    # pad_images('/home/andy/Documents/6.869/final_project/memes',
    #            '/home/andy/Documents/6.869/final_project/padded_memes')

    generate_text_imgs('/home/andy/Documents/6.869/final_project/text',
                       find_largest_dim('/home/andy/Documents/6.869/final_project/memes'),
                       num=1)