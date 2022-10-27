
from ast import arg
from distutils import text_file
from os.path import exists
from tkinter import Label
import Augmentation_backend as am
import Helpers_ as hp
import cv2
from helpers import *
import glob
import os
import argparse
import math
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np
import PIL.Image
import torch
from torchvision import transforms
import os
import shutil

def augment(image, output_path, txt_path, image_name, args):

    if args.aug_type == 'brightness':
        image = am.brighten(image, brightness_coeff=0.3)

    if args.aug_type == 'darken':
        am.darken(image, darkness_coeff=0.1)

    if args.aug_type == 'add_shadow':
        image = am.add_shadow(image, no_of_shadows=2, shadow_dimension=8)

    if args.aug_type == 'add_rain':
        image = am.add_rain(image, rain_type='heavy', slant=20)

    if args.aug_type == 'add_fog':
        image = am.add_fog(image, fog_coeff=0.3)

    if args.aug_type == 'add_gravel':
        image = am.add_gravel(image, rectangular_roi=(700, 550, 1280, 720), no_of_patches=20)

    if args.aug_type == 'add_sun_flare':
        image = am.add_sun_flare(image, flare_center=(100, 100), angle=-math.pi / 4)

    if args.aug_type == 'add_apeed':
        image = am.add_speed(image, speed_coeff=0.9)

    if args.aug_type == 'add_autumn':
        image = am.add_autumn(image)

    if args.aug_type == 'hsv':
        image1 = image.copy()
        aug = iaa.imgcorruptlike.Saturate(severity=3)
        image = aug(image=image1)

    if args.aug_type=='green':
        img = image
        row, col, plane = img.shape
        temp = np.zeros((row, col, plane), np.uint8)
        temp[:, :, 1] = img[:, :, 1]
        image = temp.copy()

    if args.aug_type=='blue':
        img = image
        row, col, plane = img.shape
        temp = np.zeros((row, col, plane), np.uint8)
        temp[:, :, 1] = img[:, :, 0]
        image = temp.copy()

    if args.aug_type=='red':
        img = image
        row, col, plane = img.shape
        temp = np.zeros((row, col, plane), np.uint8)
        temp[:, :, 1] = img[:, :, 2]
        image = temp.copy()

    if args.aug_type=='add_blur':
        aug = iaa.imgcorruptlike.MotionBlur(severity=5)
        image = aug(image=image)

    if args.aug_type=='hue':
        aug = iaa.AddToHue((-50, 50))
        image = aug(image=image)

    if args.aug_type=='gaussian_noise':
        aug = iaa.imgcorruptlike.GaussianNoise(severity=5)
        image = aug(image=image)

    if args.aug_type=='linearcontrast':
        aug = iaa.LinearContrast((0.75, 1.5))
        image = aug(image=image)

    if args.aug_type=='change_temperature':
        aug = iaa.ChangeColorTemperature((1100, 10000))
        image = aug(image=image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(output_path + args.aug_type + '_' + image_name)
    cv2.imwrite(output_path + args.aug_type + '_' + image_name, image)
    name = image_name.split('.')[0]
    shutil.copy(txt_path, output_path + name + '.txt')
    os.rename(output_path + name + '.txt', output_path + args.aug_type + '_' + name + '.txt')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--images', type=str, default='', help='path to input images')
    parser.add_argument('--labels', type=str, default='', help='path to input images')
    parser.add_argument('--aug_type', type=str, default= '' , help='augmentation type')
    args = parser.parse_args()
    aug_types = ['brightness', 'darken', 'add_shadow', 'add_rain', 'add_graval', 'add_speed', 'hsv', 'green', 'blue',
                 'red', 'hue', 'linearconstrast', 'gaussian_noise','change', 'add_blur', 'add_sun_flare', 'add_fog', 'hsv',
                 'add_autumn']

    if args.aug_type in aug_types:
        output_path = args.aug_type + '/'
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            os.mkdir(output_path)
        else:
            os.mkdir(output_path)

        images_list = glob.glob(args.images + '*.jpg')
        for img_path in images_list:
            image_name = os.path.basename(img_path)
            txt_name = image_name.split('.')[0]
            txt_path = args.images + txt_name + '.txt'
            image = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
            augment(image, output_path, txt_path, image_name, args)

    else:
        print(f'Invalid argument: "{args.aug_type}" augmentation type should be from the list "{aug_types}"')
