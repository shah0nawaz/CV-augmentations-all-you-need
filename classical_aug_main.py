import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import glob
from Bounding_box_adju import bbox
from classical_aug import classical_images_aug
import cv2
import os
import argparse
import shutil


class Classical:

    def __init__(self, dataset_imgs, aug_type):
        self.dataset_imgs = dataset_imgs
        self.aug_type = aug_type

    def main_(self, args):
        # classical_images_aug
        break_loop = True
        if self.aug_type in args.aug_types:
            break_loop = False
            output_path = args.aug_type.lower() + '/'
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
                os.mkdir(output_path)
            else:
                os.mkdir(output_path)
        else:
            print(f'Wrong augmentation type name: {args.aug_type} ')
            print(f'Augmentation name should be from the list {args.aug_types}')

        ia.seed(1)
        for img_path in dataset_imgs:
            if break_loop:
                break
            img_path_copy = img_path
            txt_file = os.path.splitext(img_path_copy)[0] +'.txt'

            img = cv2.imread(img_path)
            x1, y1, x2, y2 = bbox.image_info(img_path, txt_file)

            bbs = BoundingBoxesOnImage([
                BoundingBox(x1, y1, x2, y2),
                BoundingBox(x1, y1, x2, y2)
            ], shape=img.shape)

            if self.aug_type.lower() == 'affine':
                seq, aug_name = classical_images_aug.Affine()

            if self.aug_type.lower() == 'fliplr':
                seq, aug_name = classical_images_aug.Fliplr()

            if self.aug_type.lower() == 'crop':
                seq, aug_name = classical_images_aug.Crop()

            if self.aug_type.lower() == 'scaling':
                seq, aug_name = classical_images_aug.Scaling()

            if self.aug_type.lower() == 'translation':
                seq, aug_name = classical_images_aug.Translation()

            if self.aug_type.lower() == 'shear':
                seq, aug_name = classical_images_aug.Shear()


            image_aug, bbs_aug = seq(image=img, bounding_boxes=bbs)
            for i in range(len(bbs.bounding_boxes)):
                before = bbs.bounding_boxes[i]
                after = bbs_aug.bounding_boxes[i]
                height, width, _ = img.shape
                after.x1, after.y1, after.x2, after.y2 = bbox.xyxy_xywh(
                    after.x1, after.y1, after.x2, after.y2, height, width)
                print("BB %d: (%.4f, %.4f, %.4f, %.4f) -> (%.4f, %.4f, %.4f, %.4f)" % (
                    i,
                    before.x1, before.y1, before.x2, before.y2,
                    after.x1, after.y1, after.x2, after.y2)
                )
            image_before = bbs.draw_on_image(img, size=2)
            image_after = bbs_aug.draw_on_image(
                image_aug, size=2, color=[0, 0, 255])
            name = img_path.split('/')[-1].split('.')[0]
            cv2.imwrite(output_path + self.aug_type + "_" +
                        name + '.jpg', image_aug)

            with open(output_path  + self.aug_type + "_" + name + '.txt', 'w') as fout:
                fout.writelines((str(0), " ", str(after.x1), " ", str(after.y1), " ",
                                str(after.x2), " ", str(after.y2)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--imgs_path", help="Path to images for Augmenations", type=str, default='dataset/')
    parser.add_argument("--aug_type", type=str, default="Affine",  help='Affine Augmentation')
    parser.add_argument("--aug_types", type=str, default=["affine", 'shear', 'translation', 'crop', 'fliplr', 'scaling'] , help='Affine Augmentation')
    parser.add_argument('--main_dir', type=str, default='classical_aug/')
    args = parser.parse_args()
    dataset_imgs = glob.glob(args.imgs_path + '*.jpeg')
    arg_name = args.aug_type

    obj = Classical(dataset_imgs, str(arg_name))
    obj.main_(args)
