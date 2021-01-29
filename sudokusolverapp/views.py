from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from keras.models import load_model
import tensorflow as tf
import os
import cv2
import numpy as np
# from pylab import *
import glob

import argparse
import random as rng
import math
# Create your views here.
# Create your views here.
model = settings.MODEL
# media root
mr = settings.MEDIA_ROOT
num_data_dir = settings.NUM_DATA
backtracks = 0

def clean_up(num_data_dir):
    for img in sorted(os.listdir(num_data_dir)):
        os.remove(img)

def hougher(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 100)
    # change 100 to 200, so that diagonal isn't detected
    lines= cv2.HoughLines(dst, 1, math.pi/180.0, 180, np.array([]), 0, 0)
    a,b,c = lines.shape
    for i in range(a):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0, y0 = a*rho, b*rho
        pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
        pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
        cv2.line(img, pt1, pt2, (0, 0, 255), 7, cv2.LINE_AA)
    cv2.imwrite('houghed.jpg',img)

def squares(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen,160,255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    img = cv2.drawContours(img, cnts, -1, (0,0,0), 3)
    cv2.imwrite("con.jpg", img)
    min_area = 4000
    max_area = 11000
    image_number = 0
    
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area and area < max_area:
            x,y,w,h = cv2.boundingRect(c)
            ROI = img[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(num_data_dir, 'boxes_{}.jpg'.format(str(80-image_number).zfill(2))), ROI)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), 4)
            image_number += 1

def pic_to_sudoku():
    sudoku = ""
    for img in sorted(os.listdir(num_data_dir)):
        # print(os.path.join(num_data_dir, img))
        img = cv2.imread(os.path.join(num_data_dir, img))
        img = cv2.resize(img, (28, 28))
        test_image = np.array(img).astype('float32')
        test_image = np.expand_dims(test_image, axis=0)/255
        test_image = tf.image.resize_with_pad(test_image, 28, 28)
        f = model.predict(test_image)
        index = np.argmax(f)
        d = index.item()
        d = f'{d}'
        sudoku += d
    return sudoku

def find_next_cell(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def is_valid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3 *(i//3), 3 *(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False
            return True
    return False

def solve_sudoku(grid, i=0, j=0):
    global backtracks
    i, j = find_next_cell(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        if is_valid(grid, i, j, e):
            grid[i][j] = e
            if solve_sudoku(grid, i, j):
                return True
            backtracks += 1
            grid[i][j] = 0
    return False

def index(request):
    context={'a': 'Hello'}
    return render(request, 'index.html', context)

def sudokuSolver(request):
    # clean_up(num_data_dir)
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathDisplay = fs.url(filePathName)
    # remember what context you're trying to send
    print(filePathDisplay)
    # term = "'" + filePathDisplay + "'"
    print(os.path.join(mr, filePathName))
    img = cv2.imread(os.path.join(mr, filePathName))
    print(img.shape)
    img = cv2.resize(img, (900, 900))
    hougher(img)
    file_path = 'houghed.jpg'
    img = cv2.imread(file_path)
    img = cv2.resize(img, (900, 900))
    squares(img)
    # gray_all()
    puzzle = pic_to_sudoku()
    print(len(puzzle))
    l = list(puzzle)
    i = np.reshape(l, (-1, 9))
    if i.size == 90:
        i = np.delete(i, (0), axis=0)
    if i.size == 81:
        a = i.astype('int')
        g = a.tolist()
        solve_sudoku(g)
    else:
        g = False
    context={'filePathDisplay': filePathDisplay,
    'puzzle': puzzle, 
    'solution': g}
    return render(request, 'index.html', context)