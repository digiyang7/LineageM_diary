import os
import time

from PIL import Image
import imagehash

import adb

class LM:
    #def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, Emulator, LD_Path):
    def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, Emulator):
        # 初始化ADB物件
        self.ADB = adb.ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, Emulator=Emulator)

        # 初始化按鈕位置
        self.SaveImgSize = ""
        self.Btn_Map = {}
        self.Btn_init(Screen_Size)  # 依畫面大小設定座標點


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
            self.SaveImgSize = "960x540"
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
            # 介面截取 - 設定左上角 與 右下角坐標
            self.Btn_Map['Potion_Red'] = [230, 40, 268, 57]  # 左上紅水位置(截取圖形範圍38x17)

        elif str(sz) == "[1280, 720]":
            self.SaveImgSize = "1280x720"
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
            self.Btn_Map['Potion_Red'] = [0, 0, 0, 0]  # 左上紅水位置

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

    # 圖像範圍
    def Intercept_ImgScop(self, BtnMapName):
        loc = self.Btn_Map[BtnMapName]
        return self.ADB.ScreenHot.crop(loc)  # 截取圖像範圍
    # 截取樣本圖(Size_BtnMapName.png) => 初始化時把需要的樣本圖透過UI介面截取
    def Intercept_Img(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '.png')
        print("完成檔名 %s 的截圖:" % (self.SaveImgSize + "_" + BtnMapName + '.png'))
    # 比對: 樣本圖(Size_BtnMapName.png) VS 目前圖像(Size_BtnMapName_Has.png
    def Chk_Imgs_Exist(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png')
        result = self.Image_CMP(BtnMapName, img)
        if result == 0:
            return 0
        else:
            return 1
    # 靜態圖像比對 =>  return 0:圖像無差異 1:圖像有差異
    def Image_CMP(self, BtnMapName, HasImgName):
        # 載入範例圖像
        SampleImgName = self.SaveImgSize + "_" + BtnMapName
        print("圖像比對 樣本: %s VS %s" % (SampleImgName, HasImgName))
        Sample_img = Image.open(self.Sample_Image[SampleImgName])

        Sample_hash = imagehash.phash(Sample_img)
        Has_hash = imagehash.phash(HasImgName)
        Point = Sample_hash - Has_hash
        # print("Sample_hash:", Sample_hash)
        # print("Has_hash:", Has_hash)
        # print(Point)
        return Point

    # 自動轉日記本
    def autoDiary(self):

        while 1:
            self.Click_System_Btn('PlayerState')
            time.sleep(5)

if __name__ == '__main__':
    # obj = LM(Device_Name="emulator-5554", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img")
    # obj = LM(Device_Name="127.0.0.1:5555", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img", ADB_Path="xx", LD_Path="xx")

    # Device_Name = "127.0.0.1:5555"
    Device_Name = "emulator-5554"
    Screen_Size = [960, 540]
    # Screen_Size = [1280, 720]
    ADB_Path = "vmTool/dnplayer_tw/adb.exe"
    #LD_Path = r"D:\Changzhi\dnplayer-tw\\"
    Ck_Path = "chk_imgs"
    Emulator = "雷電模擬器"
    #Emulator = "BlueStacks"
    #obj = LM(Device_Name=Device_Name, Screen_Size=Screen_Size, Ck_Path=Ck_Path, ADB_Path=ADB_Path, Emulator=Emulator, LD_Path=LD_Path)
    obj = LM(Device_Name=Device_Name, Screen_Size=Screen_Size, Ck_Path=Ck_Path, ADB_Path=ADB_Path, Emulator=Emulator)

    # ======================TEST Function=====================
    #obj.Click_System_Btn('PlayerState')
    #obj.autoDiary()

    # 靜態圖像比對流程 => 1.先載取樣本圖 2.比對 樣本圖 和 目前圖像
    # 1.載取樣本圖
    # obj.Intercept_Img('Potion_Red')
    # 2.樣本圖 VS 目前圖像 做比對
    # res = obj.Chk_Imgs_Exist('Potion_Red')
    # print(res)


