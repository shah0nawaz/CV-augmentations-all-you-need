import glob
import os
images = glob.glob('0_degree/*.jpg')

for fil in images:
    path = fil
    name = fil.split('/')[-1].split('.')[0]
    name_copy = name
    new_name = name_copy.split('.')
    if '.' in new_name:

        new_name = '_'.join(new_name)
        os.rename(name + '.jpg', new_name + '.jpg')
        os.rename(name + '.txt', new_name + '.txt')