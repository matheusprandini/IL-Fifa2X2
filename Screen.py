import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import time

class Screen():
    
    def __init__(self, region=None):
        self.region = region      
    
    def GrabScreenBGR(self):
        # Done by Frannecklp
    
        hwin = win32gui.GetDesktopWindow()
    
        if self.region:
                left,top,x2,y2 = self.region
                width = x2 - left + 1
                height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
        
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)
    
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
    
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

if __name__ == '__main__':
    screen = Screen(region=())
    last_time = time.time()
    i = 0
    while (True):
        new_screen = screen.GrabScreenBGR()
        #crop_img = new_screen[150:700,:]        
        #new_screen = cv2.resize(crop_img, (240,180))
        cv2.imshow('window', new_screen)
        cv2.imwrite('window' + str(i) + '.png', new_screen)
        i += 1
        print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        