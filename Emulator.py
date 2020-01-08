import win32gui


class Emulator:
    #def __init__(self, Screen_Size, Emulator, Emu_Index):
    def __init__(self):
        # 儲存所有窗口名稱
        self.windowsNames = set()
        #self.Screen_Size = Screen_Size
        #self.Emulator = Emulator
        #self.Hwnd = Hwnd # 實際操作的模擬器 Hwnd Number

    # 取得模擬器索引編號
    def getEmulator_Index(self, Emulator):
        return win32gui.FindWindow(None, Emulator)

    def getWindow(self):
        win32gui.EnumWindows(self.checkWindow, 0)

    def checkWindow(self, hwnd, mouse):
        # 去掉下面這句就所有都輸出了，但是我不需要那麼多
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.windowsNames.add(win32gui.GetWindowText(hwnd))

    def Get_Self_Hawd(self, Emulator, Emu_Index):
        parentHawd = win32gui.FindWindow(None, Emulator)
        win32gui.EnumChildWindows(parentHawd, self.checkWindow, Emu_Index)
        lt = [t for t in self.windowsNames if t]
        lt.sort()
        for t in lt:
            hawd = win32gui.FindWindowEx(parentHawd, 0, None, t)
            if hawd != 0:
                return hawd


