#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import time
import scipy.misc



number = ['0','1','2','3','4','5','6','7','8','9']
alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHA = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

char_set = number + ALPHA + alpha
# def gen_text_image(char_set = number):
#     random.shuffle(char_set)
#     captcha_text = char_set[0] + char_set[1] + char_set[2] + char_set[3]
#     img = ImageCaptcha()
#     captcha = img.generate(captcha_text)
#     captcha_image = Image.open(captcha)
#     captcha_image.save(captcha_text + '.jpg')
    # return captcha_text, captcha_image
# text, image = gen_text_image()

# color image to black and white
def process_img(charn, rows = 30, cols = 20):
    char_ori = charn
    # if the pixel is a island, erase it
    for i in range(rows)[1: rows - 1]:
        for j in range(cols)[1: cols - 1]:
            sum = 0
            if char_ori[i][j] == 255:
                break
            if char_ori[i - 1][j] == 0:
                sum = sum + 1
            if char_ori[i + 1][j] == 0:
                sum = sum + 1
            if char_ori[i][j - 1] == 0:
                sum = sum + 1
            if char_ori[i][j + 1] == 0:
                sum = sum + 1
            if sum < 2:
                charn[ i ][ j ] = 255

    # black to white and white to black
    for i in range(rows):
        for j in range(cols):
            charn[i][j] = ~charn[i][j]

    # crop the image along the char's edge
    begin_x, begin_y, end_x, end_y = 0, 0, 0, 0
    for i in range(rows):
        sum = 0
        for j in range(cols):
            if charn[i][j] == True:
                sum = sum + 1
        if sum >= 3:
            begin_y = i
            break
    for i in range(rows)[::-1]:
        sum = 0
        for j in range(cols):
            if charn[i][j] == True:
                sum = sum + 1
        if sum >= 3:
            end_y = i + 1
            break
    for i in range(cols):
        sum = 0
        for j in range(rows):
            if charn[j][i] == True:
                sum = sum + 1
        if sum >= 4:
            begin_x = i
            break
    for i in range(cols)[::-1]:
        sum = 0
        for j in range(rows):
            if charn[j][i] == True:
                sum = sum + 1
        if sum >= 3:
            end_x = i + 1
            break
    charn = charn[begin_y: end_y, begin_x: end_x]

    return charn

def generate_img():
    size = (20, 30)
    fg_color = (0, 0, 255)
    bg_color = (255, 255, 255)
    captcha_image = Image.new('RGB', (80, 30), bg_color)
    captcha_text = ''
    params = [
                1 - float(random.randint(1, 2)) / 100,
                0,
                0,
                0,
                1 - float(random.randint(1, 10)) / 100,
                float(random.randint(1, 2)) / 500,
                0.001,
                float(random.randint(1, 2)) / 500
             ]
    for i in range(4):
        r = np.random.randint(62)
        captcha_text = captcha_text + char_set[r]
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        font_size = np.random.randint(22, 28)
        font = ImageFont.truetype('RobotoCondensed-Bold', font_size)
        draw.text((5, -5), char_set[r], fill = fg_color, font = font)
        img = img.transform(size, Image.PERSPECTIVE, params)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        captcha_image.paste(img, (i * 20, 0))
        path = './train_chars/'
        path = path + str(r) + time.strftime('_%H%M%S') + str(np.random.randint(100)) +'.jpg'
        img = img.convert('1')
        c = np.array(img)
        c = process_img(c)
        old_row, old_col = c.shape
        result = np.zeros((26, 26))
        row_w = old_row / 26
        col_w = old_col / 26
        for i in range(26):
            for j in range(26):
                new_row = (round(row_w * i), old_row - 1)[round(row_w * i) >= old_row]
                new_col = (round(col_w * j), old_col - 1)[round(col_w * j) >= old_col]
                result[i][j] = c[new_row][new_col]
        scipy.misc.imsave(path, result)
    captcha_draw = ImageDraw.Draw(captcha_image)
    for i in range(50):
        point_x = np.random.randint(80)
        point_y = np.random.randint(30)
        captcha_draw.point((point_x, point_y), fill = (0, 0, 0))
    line_begin = (random.randint(0, 40), random.randint(0, 30))
    line_end = (random.randint(40, 80), random.randint(0, 30))
    captcha_draw.line((line_begin, line_end), fill = (0, 0, 0))
    captcha_path = './captcha/' + captcha_text + '.jpg'
    captcha_image.save(captcha_path)
for i in range(200):
    generate_img()
