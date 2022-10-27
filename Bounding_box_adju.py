import os
import glob
import cv2


class bbox:

    def xyxy_xywh(x1, y1, x2, y2, height, width):
        dw = 1./width
        dh = 1./height
        x = (x1 + x2)/2.0
        y = (y1 + y2)/2.0
        w = x2 - x1
        h = y2 - y1
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return x, y, w, h

    def xywh_xyxy(x, y, w, h, height, width):

        x1 = int((x - (w/2))*width)
        y1 = int((y - (h/2))*height)

        x2 = int((x + (w/2))*width)
        y2 = int((y + (h/2))*height)

        #print(x1, y1, x2, y2)
        return x1, y1, x2, y2

    def image_info(image, txt_file):
        print(txt_file)

        # images = glob.glob('./images_dataset/*.jpg')
        # for imgs in images:
        #     base_name = os.path.basename(imgs)
        img_read = cv2.imread(image)
        height, width, c = img_read.shape
        with open(txt_file, 'r') as f:
            cls, x, y, w, h = f.readline().split(' ')
            x1, y1, x2, y2 = bbox.xywh_xyxy(float(x), float(
                y), float(w), float(h), height, width)

            return x1, y1, x2, y2

            # X, Y, W, H = xyxy_xywh(x1, y1, x2, y2, height, width)

            # cv2.imwrite('./results_images_dataset/'+base_name, resize_img)
            # with open('./results_images_dataset/'+base_name[:-4]+'.txt', 'w') as g:
            #     label = int(cls), X, Y, W, H
            #     g.write((str(label)[1:-1]).replace(',', ''))

            # cv2.rectangle(resize_img, (int(x1), int(y1)),
            #               (int(x2), int(y2)), (255, 0, 0), 3)
            # cv2.imshow('image'+str(x1), resize_img)
            # cv2.waitKey(0)
