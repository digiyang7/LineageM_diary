import subprocess
import LineageM
import Emulator

class Main():
    def __init__(self):
        # 系統預設
        print("正在初始化系統變數...........")
        # 預設變數
        self.Emu = Emulator.Emulator()
        self.Ck_Path = "chk_imgs"
        self.ADB_Path = "vmTool/dnplayer_tw/adb.exe"
        self.Emulator = ""
        self.Device_Name = ""
        self.Screen_Size = []

        self.Emulator_Hwnd = 0

        self.goAuto = 0
        self.userInputConf()

        #self.Device_Name = "127.0.0.1:5555"  # 使用者選擇 1:"127.0.0.1:5555" 2:"emulator-5554"
        #self.Emulator = "雷電模擬器"  # 使用者選擇 1:雷電模擬器 2:BlueStacks 3:夜神
        #self.Screen_Size = [960, 540]  # 使用者選擇 1:[960, 540] 2:[1280, 720]


    # 使用者設定
    def userInputConf(self):
        while 1:
            # 取得所有窗口名稱
            EmuNames = self.getWindewsName()
            s = "請選擇你的模擬器視窗名稱("
            i = 0
            for en in EmuNames:
                s += "" + str(i) + ":" + en + "  "
                i += 1
            s += " -1:跳出)  "
            # 使用者選擇的模擬器視窗名稱
            f = 1
            while f:
                f = 0
                try:
                    Emulator = int(input(s))
                    if Emulator < -1 or Emulator > len(EmuNames):
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Emulator >= 0 and Emulator <= len(EmuNames):
                #self.Emulator = "雷電模擬器" if Emulator == 1 else "BlueStacks" if Emulator == 2 else "夜神模擬器"
                self.Emulator = EmuNames[Emulator]
                self.Emulator_Hwnd = self.getEmulatorHwnd(self.Emulator)
                print("Emulator:%s , Emulator_Hwnd:%s" % (self.Emulator, self.Emulator_Hwnd))
            elif Emulator == -1:
                print("Bye~")
                break

            # 取得所有Device Name
            EmuDN = self.get_AllDeviceName()
            s = "請選擇你的模擬器驅動名稱("
            i = 0
            for emu in EmuDN:
                s += "" + str(i) + ":" + emu + "  "
                i += 1
            s += " -1:跳出)  "
            # 請使用者選擇模擬器驅動名稱
            f = 1
            while f:
                f = 0
                try:
                    # Device_Name = int(input("請選擇你的模擬器驅動名稱(1:127.0.0.1:5555 2:emulator-5554 3:系統取得 0:跳出)  "))
                    Device_Name = int(input(s))
                    if Device_Name < -1 or Device_Name > len(EmuDN):
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Device_Name >= 0 and Device_Name <= len(EmuDN):
                #self.Device_Name = "127.0.0.1:5555" if Device_Name == 1 else "emulator-5554"
                self.Device_Name = EmuDN[Device_Name]
            elif Device_Name == -1:
                print("Bye~")
                break

            # 請選擇模擬器畫面尺寸
            f = 1
            while f:
                f = 0
                try:
                    Screen_Size = int(input("請選擇模擬器畫面尺寸(0:[1280,720] 1:[960,540] -1:跳出)  "))
                    if Screen_Size < -1 or Screen_Size > 1:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Screen_Size >= 0 and Screen_Size <= 1:
                self.Screen_Size = [1280, 720] if Screen_Size == 0 else [960, 540]
            elif Screen_Size == -1:
                print("Bye~")
                break

            # 模擬器設定值 確認
            f = 1
            while f:
                f = 0
                try:
                    print("請確認你的模擬器資訊 : %s %s %s " % (self.Emulator, self.Device_Name, self.Screen_Size))
                    ck = int(input("(0:確認 1:重新輸入 -1:跳出)  "))
                    if ck < -1 or ck > 1:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if ck == 0:
                self.goAuto = 1
                break
            elif ck == 2:
                continue
            elif ck == -1:
                print("Bye~")
                break

    # 取得模擬器 Hwnd
    def getEmulatorHwnd(self, Emulator):
        print("正在取得模擬器 Hwnd....")
        return self.Emu.Get_Self_Hawd(Emulator, 0)

    # 取得所有視窗
    def getWindewsName(self):
        print("正在取得所有視窗 ...")
        self.Emu.getWindow()
        wn = [w for w in self.Emu.windowsNames if w]
        wn.sort()
        return wn

    # 取得所有模擬器Device Name
    def get_AllDeviceName(self):
        print("正在取得所有模擬器 Device Name ...")
        proc = subprocess.Popen([self.ADB_Path, "devices"], stdout=subprocess.PIPE)
        # (out, err) = proc.communicate()
        out = proc.stdout.readlines()[1:-1]
        EmulatorDN = []
        # print("out is:", out)
        for b in out:
            s = bytes.decode(b).replace('device', '')
            # print("s.split():", s)
            EmulatorDN.append(s.split()[0])
        return EmulatorDN
        # print("EmulatorDN size is ", len(EmulatorDN))
        # print("Your Device Name is:%s" % EmulatorDN[0])
        # return EmulatorDN[0]

    # goAuto
    def AutoStart(self):
        if self.goAuto == 1:
            #Device_Name, Screen_Size, Ck_Path, ADB_Path, Hwnd
            obj = LineageM.LM(Device_Name=self.Device_Name, Screen_Size=self.Screen_Size, Ck_Path=self.Ck_Path,
                              ADB_Path=self.ADB_Path, Hwnd=self.Emulator_Hwnd)

            obj.autoDiary()
            #obj.DiaryMaskData()

if __name__ == '__main__':
    m = Main()
    m.AutoStart()

    #m.get_AllDeviceName()