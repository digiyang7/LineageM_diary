import subprocess

class ADB:
    #def __init__(self, Device_Name, Screen_Size, ADB_Path, Emulator, LD_Path):
    #def __init__(self, Device_Name, Screen_Size, ADB_Path, Emulator, Hwnd):
    def __init__(self, Device_Name, ADB_Path):
        self.Device_Name = Device_Name
        self.ADB_Path = ADB_Path

    # 對模擬器下達指令
    def Touch(self, x, y, name, device_name=None):
        if device_name == None:
            device_name = self.Device_Name
        x = str(x)
        y = str(y)
        self.adb_call(device_name, ['shell', 'input', 'tap', x, y], name)
    # 執行ADB指令
    def adb_call(self, device_name, detail_list, name):
        #print("-----adb commend start-----")
        command = [self.ADB_Path, '-s', device_name]
        for order in detail_list:
            command.append(order)
        #print(command)
        #print("正在進行 %s 命令。" % name)
        p = subprocess.Popen(command)
        p.communicate()  # 等待外部程序執行結束
        #print("-----adb commend end-----")

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
    #obj.window_capture(hawd, 'chk_imgs/test.png')
    #obj.windowCapture(hawd, 'chk_imgs/test_other.png')


    # 點擊遊戲畫面
    #obj.Touch(35, 25, "點擊人物等級")

