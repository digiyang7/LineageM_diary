import subprocess
import time
import os

import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab
from PIL import Image
from threading import Thread


class ADB:
    #def __init__(self, Device_Name, Screen_Size, ADB_Path, Emulator, LD_Path):
    def __init__(self, Device_Name, Screen_Size, ADB_Path, Emulator):
        #self.ADB_Path = "vmTool/dnplayer_tw/adb.exe"  # run main.py 要用此路徑
        self.ADB_Path = ADB_Path  # run main.py 要用此路徑
        # self.ADB_Path = "../Tool/adb.exe"  # run LineageM.py 要用此路徑
        self.Screen_Size = Screen_Size
        self.Device_Name = Device_Name

        # 找到模擬器視窗 => 指定雷電模擬器目錄(為了可以使用ldconsole list, ldconsole list2, 需要在模擬器目錄下才能正常執行)
        #self.LD_Path = r"D:\Changzhi\dnplayer-tw\\"
        #self.LD_Path = LD_Path
        # Store all windows name
        self.windowsNames = set()
        self.Emulator = Emulator

        self.Hwnd = 0  # 指定預設索引為0的模擬器
        self.ScreenHot = None  # 預設截圖為None

    # 建立一個執行緒(流水線)
    # 每經過一段時間 => 載取整個遊戲畫面 => 此動作指派給一個執行緒去做
    def Keep_Game_ScreenHot(self, Emu_Index, file_name):
        # target = 執行載取畫面的函數
        th = Thread(target=self.Keep_Game_ScreenHot_fn, args=[Emu_Index, file_name])
        th.start()
    # 載取整個遊戲畫面  => Emu_Index(模擬器索引) ,  file_name(載圖存檔的檔案名稱)
    def Keep_Game_ScreenHot_fn(self, Emu_Index, file_name):
        self.Hwnd = self.Get_Self_Hawd(Emu_Index)
        print("hwnd:", self.Hwnd)
        # 持續執行 => 需加個delay 才不會卡住
        while 1:
            self.window_capture(hwnd=self.Hwnd, filename=file_name)
            #self.windowCapture(hwnd=self.Hwnd, filename=file_name)
            time.sleep(2)

    def checkWindow(self, hwnd, mouse):
        # 去掉下面這句就所有都輸出了，但是我不需要那麼多
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.windowsNames.add(win32gui.GetWindowText(hwnd))
    def Get_Self_Hawd(self, Index_Num):
        parentHawd = win32gui.FindWindow(None, self.Emulator)
        win32gui.EnumChildWindows(parentHawd, self.checkWindow, Index_Num)
        lt = [t for t in self.windowsNames if t]
        lt.sort()
        for t in lt:
            hawd = win32gui.FindWindowEx(parentHawd, 0, None, t)
            if hawd != 0:
                return hawd
    # 使用 ldconsole.exe 指令(function LD_Call) => 取得目前在運行中的模擬器 => 找到 綁定視窗的Hwnd
    # return 綁定視窗的Hwnd
    #def Get_Self_Hawd(self, Index_Num):
    #    if self.Emulator == 'BlueStacks':
    #        return self.Get_BlueStacks_Hawd()
    #    if self.Emulator == '雷電模擬器':
    #        return self.Get_BlueStacks_Hawd()
    #    Device_List = self.LD_Call()
    #    for k, Device_Data in enumerate(Device_List):
    #        if k != Index_Num:
    #            continue
    #        hawd = Device_Data[3]
    #        # print(hawd)
    #        return hawd
    # ldconsole list2 => 查看正在運行模擬器的資訊
    def LD_Call(self):
        File_Path = self.LD_Path + "ldconsole.exe"  # 此行ldconsole.exe 可能會因不同模擬器執行檔不同或取得方式不同
        #print(File_Path)
        output = subprocess.Popen([File_Path,'list2'], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(output.communicate())
        end = []
        for line in output.stdout.readlines():
            #output = line.decode("BIG5")
            output = line.decode("gbk")
            output = output.strip()
            if output != "":
                output = output.split(",")
                end.append(output)
        print(end)
        return end

    # 載取遊戲畫面1
    # 事前準備1 => 需安裝pywin32 => 使用win32gui
    # 事前準備2 => 需安裝PIL => 使用ImageGrab和Image => import => from PIL import ImageGrab , from PIL import Image
    def window_capture(self, hwnd, filename):
        game_rect = win32gui.GetWindowRect(int(hwnd))
        # print(game_rect)
        src_image = ImageGrab.grab(game_rect)
        src_image = src_image.resize(self.Screen_Size, Image.ANTIALIAS)
        src_image.save(filename)
        # 將截圖畫面存到adb物件本身的ScreenHot屬性
        self.ScreenHot = src_image
        # print(type(src_image))
    # 載取遊戲畫面2
    def windowCapture(self, hwnd, filename):
        # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根據視窗的DC獲取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC建立可相容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 建立bigmap準備儲存圖片
        saveBitMap = win32ui.CreateBitmap()
        # 獲取監控器資訊
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print(w, h)  #圖片大小
        # 為bitmap開闢空間
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，將截圖儲存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 擷取從左上角（0，0）長寬為（w，h）的圖片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)
        # 將截圖畫面存到adb物件本身的ScreenHot屬性
        self.ScreenHot = saveDC

    # 對模擬器下達指令
    def Touch(self, x, y, name, device_name=None):
        if device_name == None:
            device_name = self.Device_Name
        x = str(x)
        y = str(y)
        self.adb_call(device_name, ['shell', 'input', 'tap', x, y], name)
    # 執行ADB指令
    def adb_call(self, device_name, detail_list, name):
        print("-----adb commend start-----")
        command = [self.ADB_Path, '-s', device_name]
        for order in detail_list:
            command.append(order)
        #print(command)
        print("正在進行 %s 命令。" % name)
        p = subprocess.Popen(command)
        p.communicate()  # 等待外部程序執行結束
        print("-----adb commend end-----")

if __name__ == '__main__':
    Device_Name = "127.0.0.1:5555"
    #Device_Name = "emulator-5554"
    Screen_Size = [960, 540]
    ADB_Path = "vmTool/dnplayer_tw/adb.exe"
    #LD_Path = r"D:\Changzhi\dnplayer-tw\\"
    Emulator = "雷電模擬器"
    #Emulator = "BlueStacks"
    #obj = ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, Emulator=Emulator, LD_Path=LD_Path)
    obj = ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, Emulator=Emulator)

    # ======================TEST Function=====================
    # 取得模擬器資訊
    # emulator_data = obj.LD_Call()
    # print(emulator_data)

    # 取得模擬器資訊內的hawd
    #hawd = obj.Get_Self_Hawd(0)
    #print(hawd)

    # 取得模擬器資訊內的hawd => 載取整個遊戲畫面
    #hawd = obj.Get_Self_Hawd(0)
    #print(hawd)
    #obj.window_capture(hawd, 'chk_imgs/test_other.png')
    #obj.window_capture(hawd, 'chk_imgs/test.png')

    # 點擊遊戲畫面
    #obj.Touch(35, 25, "點擊人物等級")

