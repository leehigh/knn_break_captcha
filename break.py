#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import scipy.misc
from sklearn import neighbors
from scipy import interpolate
from os import listdir

# image to vector for training
def img2vector(fileName):
    retMat = np.zeros([676], int)
    img = np.array(Image.open(fileName).convert('1'))
    for i in range(26):
        for j in range(26):
            retMat[i*26 + j] = img[i][j]
    return retMat

# read train data
def readDataSet(path):
    fileList = listdir(path)
    numFiles = len(fileList)
    dataSet = np.zeros([numFiles, 676], int)
    hwLabels = np.zeros([numFiles])
    for i in range(numFiles):
        filePath = fileList[i]
        digit = int(filePath.split('_')[0])
        hwLabels[i] = digit
        dataSet[i] = img2vector(path + '/' + filePath)
    return dataSet, hwLabels
train_dataSet, train_hwLabels = readDataSet('./train_chars')

knn = neighbors.KNeighborsClassifier(algorithm='kd_tree', n_neighbors=1)
knn.fit(train_dataSet, train_hwLabels)


def array2vector(charn):
    retMat = np.zeros([676], int)
    for i in range(26):
        for j in range(26):
            retMat[i * 26 + j] = charn[i][j]
    return retMat

def char2int(digit):
    if ord('9') >= ord(digit) >= ord('0'):
        return int(digit)
    elif ord('z') >= ord(digit) >= ord('a'):
        return ord(digit) - ord('a') + 36
    else:
        return ord(digit) - ord('A') + 10

def int2char(digit):
    if 9 >= digit >= 0:
        return str(int(digit))
    elif 61 >= digit >= 36:
        return chr(int(digit) - 36 + ord('a'))
    else:
        return chr(int(digit) - 10 + ord('A'))

def compare(a, b):
    if a == b:
        return True
    elif ord(a) - ord(b) == ord('a') - ord('A'):
        return True
    elif ord(a) - ord(b) == ord('A') - ord('a'):
        return True
    else:
        return False

def data_and_label(fileName):
    img = Image.open('/Users/lijia/LearningFiles/MachineLearning/endcaptcha/captcha/' + fileName).convert('1')
    region0 = (0, 0, 20, 30)
    region1 = (20, 0, 40, 30)
    region2 = (40, 0, 60, 30)
    region3 = (60, 0, 80, 30)
    char0 = np.array(img.crop(region0))
    char1 = np.array(img.crop(region1))
    char2 = np.array(img.crop(region2))
    char3 = np.array(img.crop(region3))
    char0 = process_img(char0)
    char1 = process_img(char1)
    char2 = process_img(char2)
    char3 = process_img(char3)
    dataSet = np.zeros([4, 676], int)
    hwLabels = np.zeros([4])
    digit0 = fileName.split('.')[0][0]
    digit1 = fileName.split('.')[0][1]
    digit2 = fileName.split('.')[0][2]
    digit3 = fileName.split('.')[0][3]
    dataSet[0] = array2vector(char0)
    dataSet[1] = array2vector(char1)
    dataSet[2] = array2vector(char2)
    dataSet[3] = array2vector(char3)
    hwLabels[0] = char2int(digit0)
    hwLabels[1] = char2int(digit1)
    hwLabels[2] = char2int(digit2)
    hwLabels[3] = char2int(digit3)
    return dataSet, hwLabels

def process_img(charn, rows = 30, cols = 20):
    char_ori = charn
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
    for i in range(rows):
        for j in range(cols):
            charn[i][j] = ~charn[i][j]
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
    result = np.zeros((26, 26))
    old_row, old_col = charn.shape
    row_w = old_row / 26
    col_w = old_col / 26
    for i in range(26):
        for j in range(26):
            new_row = (round(row_w * i), old_row - 1)[round(row_w * j) >= old_row]
            new_col = (round(col_w * j), old_col - 1)[round(col_w * j) >= old_col]
            result[i][j] = charn[new_row][new_col]
    return result

dataSet, hwLabels = readDataSet('/Users/lijia/LearningFiles/MachineLearning/endcaptcha/testnums')
res = knn.predict(dataSet)
error_num = np.sum(res != hwLabels)
num = len(dataSet)
# print("Total num:", num, " Wrong num:", error_num)
f = open('a', 'w')
f.write('Total num:' + str(num) + 'Wrong num:' + str(error_num) + 'recognition rate:' + str(1 - error_num / num) + '\n')


fileList = listdir('/Users/lijia/LearningFiles/MachineLearning/endcaptcha/captcha')
numFiles = len(fileList)
sum = 0

for i in range(numFiles):
    c_dataSet, c_hwLabels = data_and_label(fileList[i])
    res = knn.predict(c_dataSet)
    f.write('result:' + int2char(res[0]) + int2char(res[1]) + int2char(res[2]) + int2char(res[3]) + ' supposed to be:' + fileList[i][0] + fileList[i][1] + fileList[i][2] + fileList[i][3])
    if compare(int2char(res[0]), fileList[i][0]) and compare(int2char(res[1]), fileList[i][1]) and compare(int2char(res[2]), fileList[i][2]) and compare(int2char(res[3]), fileList[i][3]):
        sum = sum + 1
        f.write(' right')
    else:
        f.write(' wrong')
    f.write('\n')
f.write(str(sum / numFiles))
f.close()
