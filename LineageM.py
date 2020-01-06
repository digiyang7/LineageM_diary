import os
import time

from PIL import Image
import imagehash
import cv2
import numpy as np

import adb

class LM:
    #def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, Emulator, LD_Path):
    def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, Emulator):
        # 初始化ADB物件
        self.ADB = adb.ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, Emulator=Emulator)
        self.Ck_Path = Ck_Path

        # 初始化按鈕位置 & 各項初始值
        self.SaveImgSize = ""
        self.DiaryFarLeft_MaskVal = []
        self.DiaryFarLeft_MaskValLow = 0
        self.DiaryFarLeft_MaskValUp = 0
        self.Btn_Map = {}
        self.Btn_init(Screen_Size)  # 依畫面大小設定座標點

        # 初始化圖片位置
        self.Sample_Image = dict()
        self.Import_Sample_Image(Ck_Path)  # 導入所有樣本圖片檔(最後結果圖) => 並儲存到self.Sample_Image變數

        # 起動執行載圖動作的執行緒(呼叫ADB截圖函式)
        #self.ADB.Keep_Game_ScreenHot(Emu_Index=0, file_name=Ck_Path+'/test.png')

        # 若截圖未處理完則進行等待
        #while self.ADB.ScreenHot == None:
            #print("等待ADB載入畫面...")
            #time.sleep(0.5)

    # 設定  天堂M遊戲介面  座標點
    # 點擊用-只需設定單一坐標點
    # 圖片比對用-需設定左上角 與 右下角坐標, 也可設定一條線(X或Y單一座標不變)
    def Btn_init(self, sz):
        print("sz:", sz)
        if str(sz) == "[960, 540]":  # 240dpi
            self.SaveImgSize = "960x540"
            # 祝武:       祝防:1890 ~ 2762 咒武,咒防,other:3000 武捲：1774 防捲: 1774 3,4,5,6樓:1804 1樓:1774 2樓:1794
            self.DiaryFarLeft_MaskVal = [3000, 1774, 1794, 1804]
            self.DiaryFarLeft_MaskValLow = 1890
            self.DiaryFarLeft_MaskValUp = 2762
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
            self.Btn_Map['Diary_ChangeItem'] = [610, 365]  # 日記本100元變更按鈕

            # 介面截取 - 設定左上角 與 右下角坐標
            self.Btn_Map['Potion_Red'] = [230, 40, 268, 57]  # 左上紅水位置(截取圖形範圍38x17)
            self.Btn_Map['DiaryFarLeft'] = [327, 269, 377, 299]  # 轉日記-最左方格子 (50*30)*2 = 3000
            #self.Btn_Map['DiaryFarLeft_NormalPaper'] = [207, 197, 257, 227]  # 交易所 - 一般捲 (50*30)*2 = 3000
            #self.Btn_Map['DiaryFarLeft_WishPaper'] = [207, 269, 257, 299]  # 交易所 - 祝福捲
            #self.Btn_Map['DiaryFarLeft_CursePaper'] = [207, 341, 257, 371]  # 交易所 - 咒咀捲

        elif str(sz) == "[1280, 720]":
            self.SaveImgSize = "1280x720"
            # 祝武:3366 ~ 4674 祝防: 咒武,咒防,other:5280 武捲：3212 防捲:3212 1樓:3212 2樓:3240 3樓:3248 4樓:3250 5樓:3252 6樓:3254
            self.DiaryFarLeft_MaskVal = [5280, 3212, 3240, 3248, 3250, 3252, 3254]
            self.DiaryFarLeft_MaskValLow = 3366
            self.DiaryFarLeft_MaskValUp = 4674
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
            self.Btn_Map['Diary_ChangeItem'] = [815, 490]  # 日記本100元變更按鈕

            # 介面截取坐標 - 設定左上角 與 右下角坐標
            self.Btn_Map['Potion_Red'] = [0, 0, 0, 0]  # 左上紅水位置
            self.Btn_Map['DiaryFarLeft'] = [436, 358, 502, 398]  # 轉日記-最左方格子 (66*40)*2 = 5280

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

    # ============================================圖象比對 Function=====================================================
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
        #print("圖像比對 樣本: %s VS %s" % (SampleImgName, HasImgName))
        Sample_img = Image.open(self.Sample_Image[SampleImgName])

        Sample_hash = imagehash.phash(Sample_img)
        Has_hash = imagehash.phash(HasImgName)
        Point = Sample_hash - Has_hash
        # print("Sample_hash:", Sample_hash)
        # print("Has_hash:", Has_hash)
        # print(Point)
        return Point
    # 靜態圖像 => 取得圖像MASK中的白色區域點數
    def Image_MaskLU(self, source_img, mask_lower, mask_upper):
        cv2_Image = cv2.imread(source_img)
        hsvimg = cv2.cvtColor(cv2_Image, cv2.COLOR_BGR2HSV)
        #print(hsvimg)  # 看一下轉成HSV的值落在那些範圍,以方便做MASK時提取依據
        # cv2.imshow("Source", hsvimg)
        #cv2.imwrite('Source.png', hsvimg)
        # mask是把HSV圖片中在顏色範圍內的區域變成白色(255,255,255)，其他區域變成黑色(0,0,0)
        # mask_lower = np.array([0, 0, 4])
        # mask_upper = np.array([255, 255, 255])
        mask = cv2.inRange(hsvimg, mask_lower, mask_upper)
        # cv2.imshow("Mask", mask)
        #cv2.imwrite('Mask.png', mask)
        res = cv2.bitwise_and(cv2_Image, cv2_Image, mask=mask)
        # cv2.imshow("Res", res)
        #cv2.imwrite('Res.png', res)
        # 找出某一點的數量
        pointCount = self.Get_Array_Num_Count(mask, 255)  # 找出白色區域(255)有多少個點
        #print("共找到%d個你所需要的點" % pointCount)
        return pointCount
    # 計算NP列表中,符合某一數值的總數(ex:mask中符合255的總數)
    def Get_Array_Num_Count(self, NP_Arr, Num):
        rs = np.where(NP_Arr == Num)
        #print(rs)
        k = 0
        for row in rs:
            for n in row:
                k += 1
        return k

    # ============================================天堂M 圖像確認========================================================
    # weapon:武器, Armor:防具, 紙:paper wish:祝
    # 確認日記本 - 最左方格子
    def Check_DiaryFarLeft(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png')
        time.sleep(0.5)
        # 日服-960*540-240dpi
        mask_lower = np.array([0, 0, 4])
        mask_upper = np.array([255, 255, 255])
        return self.Image_MaskLU(Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png',
                                 mask_lower, mask_upper)

    # 自動轉日記本
    def autoDiary(self):
        conunt = 0
        while 1:
            conunt += 1
            print("轉第%d次" % conunt)
            obj.Click_System_Btn('Diary_ChangeItem')
            time.sleep(1)  # 100變更點完等待1秒在截圖
            self.ADB.Keep_Game_ScreenDiary_fn(Emu_Index=0, file_name=self.Ck_Path + '/test.png')
            v = obj.Check_DiaryFarLeft('DiaryFarLeft')
            print("v值=%d:" % v)
            if v >= self.DiaryFarLeft_MaskValLow and v <= self.DiaryFarLeft_MaskValUp and v not in self.DiaryFarLeft_MaskVal:
                print("轉到祝武 祝防....")
                break
            time.sleep(1)

    # 測試Diary MaskData
    def DiaryMaskData(self):
        conunt = 0
        while 1:
            conunt += 1
            print("轉第%d次" % conunt)
            time.sleep(1)
            self.ADB.Keep_Game_ScreenDiary_fn(Emu_Index=0, file_name=self.Ck_Path + '/test.png')
            v = obj.Check_DiaryFarLeft('DiaryFarLeft')
            print("v值=%d:" % v)
            time.sleep(1)

if __name__ == '__main__':
    # obj = LM(Device_Name="emulator-5554", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img")
    # obj = LM(Device_Name="127.0.0.1:5555", Screen_Size=[960, 540], Sample_Path="../Data/Sample_img", ADB_Path="xx", LD_Path="xx")

    Device_Name = "127.0.0.1:5555"
    #Device_Name = "emulator-5554"
    Screen_Size = [960, 540]
    #Screen_Size = [1280, 720]
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

    #obj.Intercept_Img('DiaryFarLeft_WishPaper')

    ####obj.Check_WishPaper('DiaryFarLeft_NormalPaper')  # 防捲:1774 武捲：1774 (3,4,5,6樓:1804),(1樓:1774),(2樓:1794)
    ####obj.Check_WishPaper('DiaryFarLeft_WishPaper')  # 祝防:1834 ~ 2516 祝武:1862 ~ 2646
    ####obj.Check_WishPaper('DiaryFarLeft_CursePaper')  # 咒武,咒防:3000

    #obj.Check_DiaryFarLeft('DiaryFarLeft')

    # 自動轉日記本
    #obj.autoDiary()

    # 測試Diary MaskData
    obj.DiaryMaskData()





