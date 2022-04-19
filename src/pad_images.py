import os
import cv2
import numpy as np


def find_largest_dim(image_dir):
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

    max_dim = find_largest_dim(src_dir)

    filenames = os.listdir(src_dir)

    for filename in filenames:
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


if __name__ == '__main__':

    pad_images('/home/andy/Documents/6.869/final_project/memes', '/home/andy/Documents/6.869/final_project/padded_memes')