import os
import glob
import pandas
import torch

def iou(box1, box2):
    box1_x1 = box1[0]
    box1_y1 = box1[1]
    box1_x2 = box1[2]
    box1_y2 = box1[3]
    box2_x1 = box2[0]
    box2_y1 = box2[1]
    box2_x2 = box2[2]
    box2_y2 = box2[3]
    x1 = max(box1_x1, box2_x1)
    y1 = max(box1_y1, box2_y1)
    x2 = min(box1_x2, box2_x2)
    y2 = min(box1_y2, box2_y2)
    intersection = (x2 - x1).clamp(0) * (y2 - y1).clamp(0)
    box1_area = abs((box1_x2 - box1_x1) * (box1_y2 - box1_y1))
    box2_area = abs((box2_x2 - box2_x1) * (box2_y2 - box2_y1))
    return intersection / (box1_area + box2_area - intersection + 1e-6)

def conversion(line):
    l = line.strip('\n').split(' ')
    dim = 608
    label = l[0]
    w = int(float(l[3])*dim)
    h = int(float(l[4])*dim)

    x1 = int((float(l[1])*dim) - w//2)
    y1 = int((float(l[2])*dim) - w//2)

    x2 = int((float(l[1]) * dim) + w // 2)
    y2 = int((float(l[2]) * dim) + w // 2)

    lis = torch.tensor([x1,y1,x2,y2])
    return lis


images_list = glob.glob('valid/rotate/*.txt')

for fil in images_list:
    cp = fil
    name = cp.split('/')[-1]
    print(name)

    with open('valid/rotations_new/' + name, 'w') as f3:
        with open(fil, 'r') as f1:
            for line1 in f1.readlines():
                flag = True
                l1 = line1
                label = l1.split(' ')[0]
                #print(line1)
                box1 = conversion(line1)
                with open('valid/rotate_images/' + name, 'r') as f2:
                    for line2 in f2.readlines():
                        l2 = line2
                        #print(l1)
                        box2 = conversion(line2)
                        line2_list = l2.split(' ')
                        iu = iou(box1,box2)
                        if iu>=0.4:
                            flag = False
                            print('here')
                            #print(line2_list)
                            line2_list[0] = label
                            #print(line2_list)
                            line1_new = ' '.join(line2_list)
                            f3.write(line1_new)
                    if flag:
                        print(flag)
                        line1_new = ' '.join(l1)
                        f3.write(line1_new)


