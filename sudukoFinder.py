import cv2
import numpy as np
from skimage.segmentation import clear_border
from imutils.perspective import four_point_transform
import imutils

img=cv2.imread('Resources\Sudukoimage_test.jpg')


def find_suduko(image, debug=False):
    imgGrey=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    imgBlur=cv2.GaussianBlur(imgGrey, (3,3), 2)
    thresh=cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    thresh=cv2.bitwise_not(thresh)

    ####Find countours and sort them by size 
    cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    cnts=sorted(cnts,key=cv2.contourArea,reverse=True)
    puzzleCnt=None
    for c in cnts:
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.02*peri,True)
        if len(approx)==4:
            puzzleCnt=approx
            break
        if puzzleCnt is None:
            raise Exception(("Could nt find suduko outline,Debugg?"))
    if debug:
        output=image.copy()
        cv2.drawContours(output,[puzzleCnt],-1,(0,255,0),2)
        cv2.imshow("puzzle OUtline",output)
        cv2.waitKey(0)
    imgWarped=four_point_transform(image, puzzleCnt.reshape(4,2))
    imgWgrey=four_point_transform(imgGrey,puzzleCnt.reshape(4,2))
    if debug:
        cv2.imshow("pustrans",imgWarped)
        cv2.waitKey(0)
    return imgWarped, imgWgrey


def find_digits(cell, debug=False):
    thresh=cv2.threshold(cell,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    thresh=clear_border(thresh)
    if debug:
        cv2.imshow("CellThresh",thresh)
        cv2.waitKey(0)
    cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    if len(cnts)==0:
        return None
    c=max(cnts, key=cv2.contourArea)
    mask=np.zeros(thresh.shape,dtype="uint8")
    cv2.drawContours(mask,[c],-1,255,-1)
    (h,w)=thresh.shape
    percentFilled=cv2.countNonZero(mask)/float(w*h)
    if percentFilled<0.015:
        return None

    digit=cv2.bitwise_and(thresh,thresh,mask=mask)
    if debug==True:
        cv2.imshow("digit",digit)
        cv2.waitKey(0)
    return digit



