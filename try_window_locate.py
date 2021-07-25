import win32gui


class Win:
    def __init__(self):
        self.hwnd = None
        win32gui.EnumWindows(self.enumHandler, None)

    def enumHandler(self, hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            if 'Total Commander' in win32gui.GetWindowText(hwnd):
                # print(123)
                self.hwnd = hwnd

    def callback(self, hwnd, extra):
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

    def get_window_box(self):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return x, y, w, h

if __name__ == "__main__":
    print(11111111111)
    w = Win()
    hwnd = w.hwnd
    print(w.get_window_box())
