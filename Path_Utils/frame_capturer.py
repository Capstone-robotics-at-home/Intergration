import win32gui
import win32ui
import win32con
import win32api
import numpy as np 
import cv2 
from PIL import Image 

def window_capture():
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    w = int(w * 1.5)
    h = int(h * 1.5)
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, 'temp.jpg')

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)
    img_pil = Image.fromarray(img).convert('RGB')
    x, y = img_pil.size
    img_pil.thumbnail((x//2,y//2))
    
    return np.array(img_pil)



if __name__ == '__main__':
    
    # while True:
    for i in range(1):
        frame = window_capture()
        # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        cv2.imshow('video', frame)
        c= cv2.waitKey(30) & 0xff 
        if c==27:
            # capture.release()
            break


