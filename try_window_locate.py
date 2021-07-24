import win32gui


def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if 'Total Commander' in win32gui.GetWindowText(hwnd):
            return hwnd
def get_total_com_box():


def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    if "Total Commander" in win32gui.GetWindowText(hwnd):
        print(f"Window {win32gui.GetWindowText(hwnd)}:")
        print(f"\tLocation: ({x}, {y})")
        print(f"\t    Size: ({w}, {h})")
        return (x,y),(w,h)


hwnd = win32gui.EnumWindows(enumHandler, None)

print(win32gui.EnumWindows(callback, None))
# print(callback(hwnd, None))
