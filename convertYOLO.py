# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015
Convert BBlabel tool box txt annotation files to appropriate format needed by YOLO
Adapted from original script by Guanghan Ning (gnxr9@mail.missouri.edu) to allow multiple classes
"""

import os
from os import walk, getcwd
from PIL import Image

classes = ["Squirtle", "Charmander", "Pikachu", "Bulbasaur"]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


"""-------------------------------------------------------------------"""

""" Configure Paths"""
mypath = "data/labeled_pokemon/Images/%s"
outpath = "data/labeled_pokemon/Images/%s"

wd = getcwd()
for cls in classes:

    cls_id = classes.index(cls)

    list_file = open('%s/%s_list.txt' % (wd, cls), 'w')

    """ Get input text file list """
    txt_name_list = []
    for (dirpath, dirnames, filenames) in walk(mypath % cls):
        txt_name_list.extend(filenames)
        break
    print(txt_name_list)

    """ Process """
    for txt_name in txt_name_list:
        if ".txt" not in txt_name:
            continue

        """ Open input text files """
        txt_path = mypath % cls + "/" + txt_name
        print("Input:" + txt_path)
        txt_file = open(txt_path, "r")
        lines = txt_file.read().split('\n')  # for ubuntu, use "\r\n" instead of "\n"

        """ Open output text files """
        txt_outpath = outpath % cls + "/" + txt_name
        print("Output:" + txt_outpath)
        txt_outfile = open(txt_outpath, "w")

        """ Convert the data to YOLO format """
        ct = 0
        for line in lines:
            # print('lenth of line is: ')
            # print(len(line))
            # print('\n')
            if (len(line) >= 2):
                ct = ct + 1
                print(line + "\n")
                elems = line.split(' ')
                print(elems)
                xmin = elems[0]
                xmax = elems[2]
                ymin = elems[1]
                ymax = elems[3]
                #
                img_path = str('%s/data/labeled_pokemon/Images/%s/%s.jpg' % (wd, cls, os.path.splitext(txt_name)[0]))
                # t = magic.from_file(img_path)
                # wh= re.search('(\d+) x (\d+)', t).groups()
                im = Image.open(img_path)
                w = int(im.size[0])
                h = int(im.size[1])
                # w = int(xmax) - int(xmin)
                # h = int(ymax) - int(ymin)
                # print(xmin)
                print(w, h)
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w, h), b)
                print(bb)
                txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        """ Save those images with bb into list"""
        if (ct != 0):
            list_file.write('%s/data/labeled_pokemon/Images/%s/%s.jpg\n' % (wd, cls, os.path.splitext(txt_name)[0]))

    list_file.close()