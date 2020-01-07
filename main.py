
import subprocess
import LineageM

class Main():
    def __init__(self):
        # 系統預設
        print("正在初始化系統變數...........")
        self.Ck_Path = "chk_imgs"  # 系統預設值
        self.ADB_Path = "vmTool/dnplayer_tw/adb.exe"  # 系統預設值

        self.Device_Name = "127.0.0.1:5555"  # 使用者選擇 1:"127.0.0.1:5555" 2:"emulator-5554"
        self.Emulator = "雷電模擬器"  # 使用者選擇 1:雷電模擬器 2:BlueStacks 3:夜神
        self.Screen_Size = [960, 540]  # 使用者選擇 1:[960, 540] 2:[1280, 720]

        self.goAuto = 0
        self.userInputConf()

    # 使用者設定
    def userInputConf(self):
        while 1:
            # 使用者選擇模擬器
            f = 1
            while f:
                f = 0
                try:
                    Emulator = int(input("請選擇你的模擬器   (　1 : 雷電模擬器　2 : BlueStacks　3 : 夜神　0 : 跳出 )：\t"))
                    if Emulator < 0 or Emulator > 3:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Emulator >= 1 and Emulator <= 3:
                self.Emulator = "雷電模擬器" if Emulator == 1 else "BlueStacks" if Emulator == 2 else "夜神"
                # print("Emulator: ", Emulator)
            elif Emulator == 0:
                print("Bye~")
                break

            # 使用者選擇模擬器驅動名稱
            f = 1
            while f:
                f = 0
                try:
                    Device_Name = int(input("請選擇你的模擬器驅動名稱   (　1 : 127.0.0.1:5555　2 : emulator-5554　3:系統取得 0 : 跳出 )：\t"))
                    if Device_Name < 0 or Device_Name > 3:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Device_Name >= 1 and Device_Name <= 2:
                self.Device_Name = "127.0.0.1:5555" if Device_Name == 1 else "emulator-5554"
            elif Device_Name == 3:
                self.Device_Name = self.get_DeviceName()
                # print("Device_Name:%s testDeviceName" % self.Device_Name)
            elif Device_Name == 0:
                print("Bye~")
                break

            # 請選擇模擬器畫面尺寸
            f = 1
            while f:
                f = 0
                try:
                    Screen_Size = int(input("請選擇模擬器畫面尺寸　(　1 : [960, 540]　2 : [1280, 720]　0 : 跳出 )：\t"))
                    if Screen_Size < 0 or Screen_Size > 2:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if Screen_Size >= 1 and Screen_Size <= 2:
                self.Screen_Size = [960, 540] if Screen_Size == 1 else [1280, 720]
            elif Screen_Size == 0:
                print("Bye~")
                break;

            # 模擬器設定值 確認
            f = 1
            while f:
                f = 0
                try:
                    print("請確認你的模擬器資訊 : %s %s %s " % (self.Emulator, self.Device_Name, self.Screen_Size))
                    ck = int(input("1:確認 2:重新輸入 0:跳出 \t"))
                    if ck < 0 or ck > 2:
                        f = 1
                        print("不在選擇範圍內, 請重新輸入")
                except:
                    f = 1
                    print("輸入錯誤, 請重新輸入")
            if ck == 1:
                self.goAuto = 1
                break
            elif ck == 2:
                continue
            elif ck == 0:
                print("Bye~")
                break

    # 取得DeviceName
    def get_DeviceName(self):
        print("正在取得你的模擬器驅動名稱(Device Name) ...")
        proc = subprocess.Popen([self.ADB_Path, "devices"], stdout=subprocess.PIPE)
        #(out, err) = proc.communicate()
        out = proc.stdout.readlines()[1:2]
        end = []
        for b in out:
            s = bytes.decode(b).replace('device', '')
            end.append(s.split()[0])
        print("Your Device Name is:%s" % self.Device_Name)
        return end[0]

    # goAuto
    def AutoStart(self):
        if self.goAuto == 1:
            obj = LineageM.LM(Device_Name=self.Device_Name, Screen_Size=self.Screen_Size, Ck_Path=self.Ck_Path,
                              ADB_Path=self.ADB_Path, Emulator=self.Emulator)
            while 1:
                obj.autoDiary()

if __name__ == '__main__':
    m = Main()
    m.AutoStart()