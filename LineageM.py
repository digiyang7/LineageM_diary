import os
import time
import win32gui

from threading import Thread
from PIL import Image, ImageGrab
import imagehash
import cv2
import numpy as np

import adb

class LM:
    def __init__(self, Device_Name, Screen_Size, Ck_Path, ADB_Path, Hwnd):
        # 初始化ADB物件
        #self.ADB = adb.ADB(Device_Name=Device_Name, Screen_Size=Screen_Size, ADB_Path=ADB_Path, Emulator=Emulator)
        self.ADB = adb.ADB(Device_Name=Device_Name, ADB_Path=ADB_Path)
        self.Ck_Path = Ck_Path
        self.Screen_Size = Screen_Size

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
        self.ScreenHot = None  # 預設截圖為None
        self.Hwnd = Hwnd

        # 起動執行載圖動作的執行緒
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
            # 祝武: 1856~      祝防:1890~2762 咒武,咒防,other:3000 武捲：1774 防捲: 1774 3,4,5,6樓:1804 1樓:1774 2樓:1794
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
            self.Btn_Map['DiaryFarLeft_Weapon'] = [335, 283, 338, 286]  # 轉日記 : 最左方格子 -> 祝福捲 -> 武捲 3x3

            #self.Btn_Map['DiaryFarLeft_NormalPaper'] = [207, 197, 257, 227]  # 交易所 - 一般捲 (50*30)*2 = 3000
            #self.Btn_Map['DiaryFarLeft_WishPaper'] = [207, 269, 257, 299]  # 交易所 - 祝福捲
            #self.Btn_Map['DiaryFarLeft_WishPaper_Weapon'] = [218, 282, 221, 283]  # 交易所 - 祝福捲 -> 武捲
            #self.Btn_Map['DiaryFarLeft_CursePaper'] = [207, 341, 257, 371]  # 交易所 - 咒咀捲

        elif str(sz) == "[1280, 720]":
            self.SaveImgSize = "1280x720"
            # 祝武:3366 ~ 4674 祝防:3422~4900 咒武,咒防,other:5280 武捲：3212 防捲:3212 1樓:3212 2樓:3240 3樓:3248 4樓:3250 5樓:3252 6樓:3254
            self.DiaryFarLeft_MaskVal = [5280, 3212, 3240, 3248, 3250, 3252, 3254]
            self.DiaryFarLeft_MaskValLow = 3366
            self.DiaryFarLeft_MaskValUp = 4900
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
            self.Btn_Map['DiaryFarLeft_Weapon'] = [464, 364, 467, 367]  # 轉日記 : 最左方格子 -> 祝福捲 -> 武捲

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
        return self.ScreenHot.crop(loc)  # 截取圖像範圍
    # 截取樣本圖(Size_BtnMapName.png) => 初始化時把需要的樣本圖透過UI介面截取
    def Intercept_Img(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '.png')
        print("完成檔名 %s 的截圖:" % (self.SaveImgSize + "_" + BtnMapName + '.png'))
    # 比對: 樣本圖(Size_BtnMapName.png) VS 目前圖像(Size_BtnMapName_Has.png
    def Chk_Imgs_Exist(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png')
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
        #print("hswing is :", hsvimg)  # 看一下轉成HSV的值落在那些範圍,以方便做MASK時提取依據
        # cv2.imshow("Source", hsvimg)
        # cv2.imwrite('Source.png', hsvimg)
        # mask是把HSV圖片中在顏色範圍內的區域變成白色(255,255,255)，其他區域變成黑色(0,0,0)
        # mask_lower = np.array([0, 0, 4])
        # mask_upper = np.array([255, 255, 255])
        mask = cv2.inRange(hsvimg, mask_lower, mask_upper)
        #cv2.imshow("Mask", mask)
        # cv2.imwrite('Mask.png', mask)
        # res = cv2.bitwise_and(cv2_Image, cv2_Image, mask=mask)
        # cv2.imshow("Res", res)
        # cv2.imwrite('Res.png', res)
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

    # 載圖
    def Keep_Game_ScreenDiary_fn(self, Hwnd, file_name):
        self.window_capture(hwnd=Hwnd, filename=file_name)

    # 建立一個執行緒(流水線)
    # 每經過一段時間 => 載取整個遊戲畫面 => 此動作指派給一個執行緒去做
    def Keep_Game_ScreenHot(self, Hwnd, file_name):
        # target = 執行載取畫面的函數
        th = Thread(target=self.Keep_Game_ScreenHot_fn, args=[Hwnd, file_name])
        th.start()

    # 載取整個遊戲畫面  => Emu_Index(模擬器索引) ,  file_name(載圖存檔的檔案名稱)
    def Keep_Game_ScreenHot_fn(self, Hwnd, file_name):
        # print("hwnd:", self.Hwnd)
        # 持續執行 => 需加個delay 才不會卡住
        while 1:
            self.window_capture(hwnd=Hwnd, filename=file_name)
            # self.windowCapture(hwnd=self.Hwnd, filename=file_name)
            time.sleep(2)

    # 載取遊戲畫面1
    #     # 事前準備1 => 需安裝pywin32 => 使用win32gui
    #     # 事前準備2 => 需安裝PIL => 使用ImageGrab和Image => import => from PIL import ImageGrab , from PIL import Image
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
    # def windowCapture(self, hwnd, filename):
    # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
    # hwndDC = win32gui.GetWindowDC(hwnd)
    # 根據視窗的DC獲取mfcDC
    # mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC建立可相容的DC
    # saveDC = mfcDC.CreateCompatibleDC()
    # 建立bigmap準備儲存圖片
    # saveBitMap = win32ui.CreateBitmap()
    # 獲取監控器資訊
    # MoniterDev = win32api.EnumDisplayMonitors(None, None)
    # w = MoniterDev[0][2][2]  # 截圖區域
    # h = MoniterDev[0][2][3]  # 截圖區域
    # print(w, h)  #圖片大小
    # 為bitmap開闢空間
    # saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，將截圖儲存到saveBitmap中
    # saveDC.SelectObject(saveBitMap)
    # 擷取從左上角（0，0）長寬為（w，h）的圖片
    # saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, filename)
    # 將截圖畫面存到adb物件本身的ScreenHot屬性
    # self.ScreenHot = saveDC

    # ============================================天堂M 圖像確認========================================================
    # weapon:武器, armor:防具, 紙:paper wish:祝
    # 確認日記本 - 最左方格子
    def Check_DiaryFarLeft(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png')
        time.sleep(0.5)
        # 日服-960*540-240dpi
        mask_lower = np.array([0, 0, 4])
        mask_upper = np.array([255, 255, 255])
        return self.Image_MaskLU(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png',
                                 mask_lower, mask_upper)
    # 祝福捲情況下 => 找出武捲與防捲的值
    # 祝武15-80,30-160,70-199 maskval 100次試驗 => 0:1次   2~18: 99次
    # 祝防0-40,0-100,200-255 maskval
    def Check_DiaryFarLeft_Weapon(self, BtnMapName):
        img = self.Intercept_ImgScop(BtnMapName)
        img.save(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png')
        time.sleep(0.5)
        # 日服-960*540-240dpi
        mask_lower = np.array([0, 0, 70])
        mask_upper = np.array([255, 255, 199])
        return self.Image_MaskLU(self.Ck_Path + '/' + self.SaveImgSize + "_" + BtnMapName + '_Has.png',
                                 mask_lower, mask_upper)

    # 自動轉日記本
    def autoDiary(self):
        conunt = 0
        while 1:
            conunt += 1
            print("轉第%d次" % conunt)
            self.Click_System_Btn('Diary_ChangeItem')
            time.sleep(1)  # 100變更點完等待1秒在截圖
            self.Keep_Game_ScreenDiary_fn(Hwnd=self.Hwnd, file_name=self.Ck_Path + '/test.png')
            v = self.Check_DiaryFarLeft('DiaryFarLeft')
            c = self.Check_DiaryFarLeft_Weapon('DiaryFarLeft_Weapon')  # 祝武 c != 0
            print("v值=%d , c值=%d:" % (v, c))
            #if v >= self.DiaryFarLeft_MaskValLow and v <= self.DiaryFarLeft_MaskValUp and v not in self.DiaryFarLeft_MaskVal and c > 0:
            if v >= self.DiaryFarLeft_MaskValLow and v <= self.DiaryFarLeft_MaskValUp and v not in self.DiaryFarLeft_MaskVal and c == 0:
                print("轉到..祝防(目前1280x720:10%機率, 960x540:1%機率 可能誤判為祝武)......")
                break
            elif v >= self.DiaryFarLeft_MaskValLow and v <= self.DiaryFarLeft_MaskValUp and v not in self.DiaryFarLeft_MaskVal and c != 0:
                print("轉到..祝武")
                break
            elif v >= self.DiaryFarLeft_MaskValLow and v <= self.DiaryFarLeft_MaskValUp and v not in self.DiaryFarLeft_MaskVal:
                print("轉到..祝福捲")
                break
            time.sleep(1)

    # 測試Diary MaskData
    def DiaryMaskData(self):
        conunt = 0
        while 1:
            conunt += 1
            print("轉第%d次" % conunt)
            time.sleep(1)
            self.Keep_Game_ScreenDiary_fn(Hwnd=self.Hwnd, file_name=self.Ck_Path + '/test.png')
            v = self.Check_DiaryFarLeft('DiaryFarLeft')
            c = self.Check_DiaryFarLeft_Weapon('DiaryFarLeft_Weapon')  # 祝武 c != 0
            print("v值=%d , c值=%d:" % (v, c))
            time.sleep(1)


if __name__ == '__main__':
    Device_Name = "127.0.0.1:5555"
    #Device_Name = "emulator-5554"
    Screen_Size = [960, 540]
    Screen_Size = [1280, 720]
    ADB_Path = "vmTool/dnplayer_tw/adb.exe"
    Ck_Path = "chk_imgs"
    Emulator = "雷電模擬器"
    Emulator_Hwnd = 5047226
    Emulator_Hwnd = 281544494
    obj = LM(Device_Name=Device_Name, Screen_Size=Screen_Size, Ck_Path=Ck_Path, ADB_Path=ADB_Path, Hwnd=Emulator_Hwnd)

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

    # 測試Diary MaskData
    #obj.DiaryMaskData()

    # 自動轉日記本
    obj.autoDiary()

    # 交易所 武防
    #obj.Keep_Game_ScreenDiary_fn(Emulator_Hwnd, Ck_Path + "/960x540_DiaryFarLeft_WishPaper_Has.png")
    #v = obj.Check_DiaryFarLeft_Weapon('DiaryFarLeft_WishPaper_Weapon')
    #print("v is ", v)

    # 日記本
    # obj.Keep_Game_ScreenDiary_fn(Emulator_Hwnd, Ck_Path + "/960x540_DiaryFarLeft_Weapon_Has.png")
    # obj.Check_DiaryFarLeft_Weapon('DiaryFarLeft_Weapon')





