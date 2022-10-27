import glob
import numpy as np
import cv2
import os
import argparse
import Augmentation_backend as am
import Helpers_ as hp
from PIL import Image
from helpers import *
import shutil


class YoloRotateBBox:

    def __init__(self, args, angle, file_name, image):
        self.args = args
        self.image = image
        self.angle = angle
        self.file_name = file_name
        rotation_angle = self.angle * np.pi / 180
        self.rot_matrix = np.array(
            [[np.cos(rotation_angle), -np.sin(rotation_angle)], [np.sin(rotation_angle), np.cos(rotation_angle)]])


    def rotateYolobbox(self):
        new_height, new_width = self.rotate_image().shape[:2]
        f = open(self.args.input + self.file_name + '.txt', 'r')
        f1 = f.readlines()
        new_bbox = []
        H, W = self.image.shape[:2]
        for x in f1:
            bbox = x.strip('\n').split(' ')
            if len(bbox) > 1:
                (center_x, center_y, bbox_width, bbox_height) = yoloFormattocv(float(bbox[1]), float(bbox[2]),
                                                                               float(bbox[3]), float(bbox[4]), H, W)
                upper_left_corner_shift = (center_x - W / 2, -H / 2 + center_y)
                upper_right_corner_shift = (
                    bbox_width - W / 2, -H / 2 + center_y)
                lower_left_corner_shift = (
                    center_x - W / 2, -H / 2 + bbox_height)
                lower_right_corner_shift = (
                    bbox_width - W / 2, -H / 2 + bbox_height)

                new_lower_right_corner = [-1, -1]
                new_upper_left_corner = []

                for i in (upper_left_corner_shift, upper_right_corner_shift, lower_left_corner_shift,
                          lower_right_corner_shift):
                    new_coords = np.matmul(
                        self.rot_matrix, np.array((i[0], -i[1])))
                    x_prime, y_prime = new_width / 2 + \
                        new_coords[0], new_height / 2 - new_coords[1]
                    if new_lower_right_corner[0] < x_prime:
                        new_lower_right_corner[0] = x_prime
                    if new_lower_right_corner[1] < y_prime:
                        new_lower_right_corner[1] = y_prime

                    if len(new_upper_left_corner) > 0:
                        if new_upper_left_corner[0] > x_prime:
                            new_upper_left_corner[0] = x_prime
                        if new_upper_left_corner[1] > y_prime:
                            new_upper_left_corner[1] = y_prime
                    else:
                        new_upper_left_corner.append(x_prime)
                        new_upper_left_corner.append(y_prime)
                new_bbox.append([bbox[0], new_upper_left_corner[0], new_upper_left_corner[1],
                                 new_lower_right_corner[0], new_lower_right_corner[1]])

        return new_bbox

    def rotate_image(self):
        """
        Rotates an image (angle in degrees) and expands image to avoid cropping
        """
        height, width = self.image.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origin) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(
            image, rotation_mat, (bound_w, bound_h))
        return rotated_mat


if __name__ == "__main__":

    # Create the parser
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--input', type=str, default='dataset/', help='input images path')
    my_parser.add_argument('--output', type=str, default='rotated/', help='output images path')
    my_parser.add_argument('--rotation_angle', type=int, default=7, help='angle of rotation')
    args = my_parser.parse_args()

    if os.path.exists(args.output):
        shutil.rmtree(args.output)
        os.mkdir(args.output)
    else:
        os.mkdir(args.output)

    img_paths = glob.glob(args.input + '*.jpeg')
    angle_range = []
    for img_path in img_paths:
        print(img_path)
        for angle in range(0, 360 - args.rotation_angle, args.rotation_angle):
            copy = img_path
            file_name = copy.split('/')[-1].split('.')[0]
            image = cv2.imread(img_path)
            org_height, org_width, _ = image.shape
            im = YoloRotateBBox(args, angle, file_name, image)

            bbox = im.rotateYolobbox()
            image = im.rotate_image()
            image = np.array(image)
            hh,ww,c = image.shape
            ratio_w = org_width/ww
            ratio_h = org_height/hh
            dims = (org_width, org_height)
            image = cv2.resize(image, (dims))
            # to write rotateed image to disk
            cv2.imwrite(args.output + file_name +
                        '_' + str(angle) + '.jpg', image)

            txt_path = args.output + file_name + '_' + str(angle) + '.txt'
            if os.path.exists(file_name):
                os.remove(file_name)
            for i in bbox:
                with open(txt_path, 'a') as fout:
                    fout.writelines(
                        ' '.join(map(str, cvFormattoYolo(i, im.rotate_image().shape[0], im.rotate_image().shape[1], ratio_w,ratio_w))) + '\n')
