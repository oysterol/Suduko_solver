from sudukoFinder import find_suduko,find_digits
import cv2
import pytesseract
import numpy as np
from sudoku import Sudoku



def Solve(img):
    ###import tesseract
    pytesseract.pytesseract.tesseract_cmd='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    config=r'--oem 3 --psm 6 outputbase digits'
    #img=cv2.imread('Resources\Sudukoimage_test.jpg')
    #print(pytesseract.image_to_string(img))
    print('Finding Board')
    puzzleImg,warp=find_suduko(img)
    board=np.zeros((9,9),dtype="int")
    stepX=warp.shape[1] //9
    stepY=warp.shape[0]//9
    filled=[]
    empty=[]
    print("Finding cells and digits")
    for y in range(0,9):
        row=[]
        for x in range(0,9):
            startX=x*stepX
            startY=y*stepY
            endX=(x+1)*stepX
            endY=(y+1)*stepY
            #row.append((startX,startY,endX,endY))
            cell=warp[startY:endY,startX:endX]
            digit=find_digits(cell)
            if digit is not None:
                digit=cv2.bitwise_not(digit)
                nr=pytesseract.image_to_string(digit,config=config)
                board[y,x]=int(nr)
                filled.append([x,y])
            else:
                empty.append([x,y])
    print('Solving Soduko')
    puzzle=Sudoku(3,3,board=board.tolist())
    #puzzle.show()
    solution=puzzle.solve()
    brett=solution.board
    imOut=puzzleImg.copy()

    for i in range(len(empty)):
            textX = int(stepX*empty[i][0]+0.33*stepX)
            textY = int(stepY*empty[i][1]+0.75*stepY)
            digits=brett[empty[i][0]][empty[i][1]]
            print(digits)
            # draw the result digit on the Sudoku puzzle image
            cv2.putText(imOut, str(digits), (textX, textY),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("res",imOut)
    cv2.waitKey(0) 

def webcam_suduko_locator():
    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    kernel=np.ones((5,5))

    sud_img= np.zeros((480,480,3),np.uint8)


    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    kernel=np.ones((5,5))


    while True:
        success, img= cap.read()
       # cv2.resize(img,(widthImg,heightImg))
        imgCount=img.copy()
        temp_img=find_suduko(imgCount)
        if temp_img!=None:
            sud_img=img[0]

        cv2.imshow("OGimage",img)
        cv2.imshow("thresh",sud_img)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        elif cv2.waitKey(1)& 0xFF==ord('s'):
            Solve(sud_img)


webcam_suduko_locator()