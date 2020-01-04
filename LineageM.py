# -*- coding: UTF-8 -*-
import os
import time
import win32gui

import adb

class LM:
    def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, LD_Path):
        # 初始化ADB物件
        self.ADB = adb.ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, LD_Path=LD_Path)

        # 初始化按鈕位置
        self.Btn_Map = {}
        self.Btn_init(Screen_Size)  # 依畫面大小設定座標點

        # Store all windows name
        self.windowsNames = set()

        # 初始化圖片位置
        self.Sample_Image = dict()
        self.Import_Sample_Image(Ck_Path)  # 導入所有樣本圖片檔(最後結果圖) => 並儲存到self.Sample_Image變數

        # 起動執行載圖動作的執行緒(呼叫ADB截圖函式)
        self.ADB.Keep_Game_ScreenHot(Emu_Index=0, file_name=Ck_Path+'/test.png')

        # 若截圖未處理完則進行等待
        while self.ADB.ScreenHot == None:
            print("等待ADB載入畫面...")
            time.sleep(0.5)

    # 設定  天堂M遊戲介面  座標點
    # 點擊用-只需設定單一坐標點
    # 圖片比對用-需設定左上角 與 右下角坐標, 也可設定一條線(X或Y單一座標不變)
    def Btn_init(self, sz):
        print("sz:", sz)
        if str(sz) == "[960, 540]":
            # 初始介面 -
            self.Btn_Map['PlayerState'] = [35, 25]  # 等級
            self.Btn_Map['Item_Box'] = [755, 30]  # 背包
            self.Btn_Map['F1'] = [410, 480]  # F1
            self.Btn_Map['F2'] = [470, 480]  # F2
            self.Btn_Map['F3'] = [530, 480]  # F3
            self.Btn_Map['F4'] = [590, 480]  # F4
            self.Btn_Map['F5'] = [720, 480]  # F5
            self.Btn_Map['F6'] = [780, 480]  # F6
            self.Btn_Map['F7'] = [840, 480]  # F7
            self.Btn_Map['F8'] = [900, 480]  # F8
            self.Btn_Map['Auto'] = [725, 385]  # AUTO
            self.Btn_Map['Self'] = [795, 305]  # SELF
            self.Btn_Map['Pick_up'] = [875, 320]  # 撿取
            self.Btn_Map['Attack'] = [825, 390]  # 攻擊

            # 背包介面
            # 日記本介面
            # 介面確認截取 - 設定左上角 與 右下角坐標

        elif str(sz) == "[1280, 720]":
            # 初始介面
            self.Btn_Map['PlayerState'] = [45, 30]  # 等級
            self.Btn_Map['Item_Box'] = [0, 0]  # 背包
            self.Btn_Map['F1'] = [540, 645]
            self.Btn_Map['F2'] = [625, 645]
            self.Btn_Map['F3'] = [705, 645]
            self.Btn_Map['F4'] = [785, 645]
            self.Btn_Map['F5'] = [965, 645]
            self.Btn_Map['F6'] = [1045, 645]
            self.Btn_Map['F7'] = [1125, 645]
            self.Btn_Map['F8'] = [1205, 645]
            self.Btn_Map['Auto'] = [0, 0]  # AUTO
            self.Btn_Map['Self'] = [0, 0]  # SELF
            self.Btn_Map['Pick_up'] = [0, 0]  # 撿取
            self.Btn_Map['Attack'] = [0, 0]  # 攻擊

            # 背包介面
            # 日記本介面
            # 介面確認截取

    # Path : 存放範例圖片的路徑
    # 將Path下所有樣本圖片(最後結果圖) 全部儲存在 Sample_Image[]內
    def Import_Sample_Image(self, Path):
        if os.path.isdir(Path) == False:
            print("範例圖片資料夾不存在")
            return 0
        File_List = os.listdir(Path)
        for File_Name in File_List:
            File_Index = File_Name.replace(".png", "")
            self.Sample_Image[File_Index] = Path + "/" + File_Name
        print("範例圖片導入成功")

    # 點擊畫面
    def Click_System_Btn(self, name):
        if name not in self.Btn_Map:
            print("無此按鍵名稱：{}".format(name))
            return 0
        click_loc = self.Btn_Map[name]
        self.ADB.Touch(click_loc[0], click_loc[1], name)

    # 自動轉日記本
    def autoDiary(self):
        self.Click_System_Btn('PlayerState')
        #while 1:
        #    self.Click_System_Btn('PlayerState')
        #    time.sleep(3)

    def checkWindow(self, hwnd, mouse):
        # 去掉下面這句就所有都輸出了，但是我不需要那麼多
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.windowsNames.add(win32gui.GetWindowText(hwnd))

if __name__ == '__main__':
    # obj = LM(Device_Name="emulator-5554", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img")
    # obj = LM(Device_Name="127.0.0.1:5555", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img", ADB_Path="xx", LD_Path="xx")

    Device_Name = "127.0.0.1:5555"
    # Device_Name = "emulator-5554"
    Screen_Size = [1280, 720]
    ADB_Path = "vmTool/dnplayer_tw/adb.exe"
    LD_Path = r"C:\Program Files\BlueStacks\\"
    Ck_Path = "chk_imgs"
    obj = LM(Device_Name=Device_Name, Screen_Size=Screen_Size, Ck_Path=Ck_Path, ADB_Path=ADB_Path, LD_Path=LD_Path)

    # List all windows name
    win32gui.EnumWindows(obj.checkWindow, 0)
    lt = [t for t in obj.windowsNames if t]
    lt.sort()
    #for t in lt:
        #print(t)

    obj.Click_System_Btn('PlayerState')

