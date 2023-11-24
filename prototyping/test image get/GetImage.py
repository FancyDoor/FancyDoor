import cv2

def getImage():
    cam = cv2.VideoCapture(0)
    while True:
        ret, image = cam.read()
        cv2.imshow('Imagetest',image)
        k = cv2.waitKey(1)
        if k != -1:
            break
    cv2.imwrite('testimage.jpg', image)
    cam.release()
    cv2.destroyAllWindows()
    
def main():
    getImage()    

if __name__=='__main__':
    main()