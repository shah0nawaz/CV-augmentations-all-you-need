
aug = iaa.imgcorruptlike.MotionBlur(severity=5)
        blur_image = aug(image=self.image[0])
        hsv_images = cv2.cvtColor(blur_image, cv2.COLOR_BGR2RGB)





   def random_flip(self):

        random_flip_images = am.random_flip(self.image[0])
        random_flip_images = cv2.cvtColor(
            random_flip_images, cv2.COLOR_BGR2RGB)
        # print(bright_images)
        cv2.imwrite('./random_flip/'+'random_flip' + '_'+base_name_image[:-4] +
                    '.png', random_flip_images)

        # for i in self.txt_file:
        # print("hello....", str(self.txt_file))
        with open(self.txt_file, 'r') as f:
            label = f.readlines()
            #print(label)

        with open('./random_flip/'+'random_flip' + '_'+base_name_image[:-4] +
                  '.txt', 'a') as fout:
            # label = fout.readlines()
            fout.writelines(label)



    def augment_random(self):

        bright_images = am.darken(self.image[0], brightness_coeff=0.7)
        # print(bright_images)
        cv2.imwrite('./brightness/'+'brighness_images' + '_'+base_name_image[:-4] +
                    '.png', bright_images)

        # for i in self.txt_file:
        # print("hello....", str(self.txt_file))
        with open(self.txt_file, 'r') as f:
            label = f.readlines()
            print(label)

        with open('./brightness/'+'brighness_images' + '_'+base_name_image[:-4] +
                  '.txt', 'a') as fout:
            # label = fout.readlines()
            fout.writelines(label)

    def augment_random(self):

        bright_images = am.darken(self.image[0], brightness_coeff=0.7)
        # print(bright_images)
        cv2.imwrite('./brightness/'+'brighness_images' + '_'+base_name_image[:-4] +
                    '.png', bright_images)

        # for i in self.txt_file:
        # print("hello....", str(self.txt_file))
        with open(self.txt_file, 'r') as f:
            label = f.readlines()
            #print(label)

        with open('./brightness/'+'brighness_images' + '_'+base_name_image[:-4] +
                  '.txt', 'a') as fout:
            # label = fout.readlines()
            fout.writelines(label)
