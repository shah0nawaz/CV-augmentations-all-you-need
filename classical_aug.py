import imgaug.augmenters as iaa


class classical_images_aug:

    def Affine():
        seq = iaa.Sequential([
            iaa.Multiply((1.2, 1.5)),  # change brightness, doesn't affect BBs
            iaa.Affine(
                translate_px={"x": 40, "y": 60},
                # scale=(0.5, 0.7)
            )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        ])

        return seq, str('Affine_')

    def Fliplr():
        seq = iaa.Sequential([
            iaa.Fliplr(0.5),  # horizontally flip 50% of the images

        ])

        return seq, str('Fliplr_')

    def Crop():
        seq = iaa.Sequential([
            iaa.Crop(px=(0, 116))
        ])

        return seq, str('Crop_')

    def Scaling():
        seq = iaa.Sequential([

            iaa.Affine(
                translate_px={"x": 0, "y": 0},
                scale=(0.5, 0.7)
            )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        ])

        return seq, str('Scaling_')

    def Translation():
        seq = iaa.Sequential([

            iaa.Affine(
                # translate_px={"x": 0, "y": 0},
                translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}
                # scale=(0.5, 0.7)
            )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        ])

        return seq, str('Translation_')

    def Shear():
        seq = iaa.Sequential([

            iaa.Affine(
                translate_px={"x": 0, "y": 0},
                shear=(-8, 8)
            )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        ])

        return seq, str('Shear_')
