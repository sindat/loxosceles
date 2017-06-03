import win32gui
import win32ui
import win32con
import win32api

# establish a handle to the desktop window, includes multiple monitors
hdesktop = win32gui.GetDesktopWindow()

# determine size of all handled monitors in pixels
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# get the device context passing in the desktop handle
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device context to store screenshot before saving
mem_dc = img_dc.CreateCompatibleDC()

# create a bitmap object that will be saved to a file
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy the screenshot into our memory based context using bit-for-bit
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# save the bitmap to a file
screenshot.SaveBitmapFile(mem_dc, 'c:\\users\\Radka-PC\Desktop\screenshot.bmp')

# release the desktop handle and memory based device context
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())

