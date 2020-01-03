
# mymain.py -> LineageM.py -> adb
#           -> LineageM_diary.py
# ui 轉 py 指令 (在檔案目錄下執行) :  pyuic5 -o LineageM_diary.py LineageM_diary.ui

# import ui
from PyQt5 import QtWidgets
from UI.LineageM_diary import Ui_MainWindow
import sys

# cmd proc , file read/write
import subprocess
import configparser

# control
import LineageM
import time
from PyQt5.QtCore import QThread

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        #self.LM = LineageM.LM(Device_Name="127.0.0.1:5555", Screen_Size=[960, 540], Chkimg_Path="chk_imgs")
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.LM = ""
        self.VM_Type = 0  # 選擇使的模擬器, 0:雷電 1:夜神 2:BS
        self.VM_Size = 0  # 透過下拉選單取得目前的畫面大小, 0:960x540 1:1280x720
        self.ADB_Path = ""  # 專案放置abd.exe的位置, 依選擇不同模擬器使用不同的adb.exe
        self.ScreenSize = []  # 依選擇不同的畫面尺寸,使用不同的畫面大小
        self.LD_Path = ""  # 執行本地端LD程式的位置, 選擇各自模擬器的位置
        self.Device_Name = ""  # 透過指令取得目前的Device_Name
        self.Ck_Path = ""  # 存放 樣本圖片, 用來做圖片比對使用

        # 0:雷電 1:BS 2:夜神 adb.exe執行檔位置
        self.myplayer = ["vmTool/dnplayer_tw/adb.exe", "vmTool/bsplayer_tw/x_adb.exe", "vmTool/xplayer_tw/x_adb.exe"]
        self.size960x540 = [960, 540]  # 模擬器畫面大小
        self.size1280x720 = [1280, 720]

        # 下拉選單item設定
        yourvmtype = ['雷電', 'BS', '夜神']
        yourvmsize = ["960x540", "1280x720"]
        self.ui.cb_vmtype.addItems(yourvmtype)
        self.ui.cb_vmsize.addItems(yourvmsize)

        # Button => 綁定按鈕的事件處理
        self.ui.getdevice_btn.clicked.connect(self.getDeviceId)
        self.ui.setdevice_btn.clicked.connect(self.setDeviceId)
        self.ui.clearmsg_btn.clicked.connect(self.clearmsg)
        self.ui.left_btn1.clicked.connect(self.leftpic1)
        self.ui.left_btn2.clicked.connect(self.leftpic2)
        self.ui.right_btn1.clicked.connect(self.rightpic1)
        self.ui.right_btn2.clicked.connect(self.rightpic2)
        self.ui.start_btn.clicked.connect(self.autostart)
        self.ui.end_btn.clicked.connect(self.exit)
        # ComboBox => 綁定下拉選單的事件處理
        self.ui.cb_vmtype.currentIndexChanged.connect(self.vmtype)
        self.ui.cb_vmsize.currentIndexChanged.connect(self.vmsize)
        # HorizontalSlider
        self.ui.hs_diarycount.valueChanged.connect(self.diarycount)

        # 變數初始化
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # 區分大小寫, 不加此行檔案內容會全部變小寫
        self.config.read('config.ini')
        #ADB_Path = "vmTool/dnplayer_tw/adb.exe"
        #LD_Path = r"D:\Changzhi\dnplayer-tw\\"
        #screenSize = [960, 540]
        #Device_Name = "127.0.0.1:5555"

        # UI初始化
        self.get_Config()  # 取得config.ini設定檔資料
        self.init_UI()  # 介面初始化

    # UI初始化
    def init_UI(self):
        self.ui.txt_sysmsg.append("正在進行介面初始化...")
        self.ui.cb_vmtype.setCurrentIndex(self.VM_Type)
        self.ui.cb_vmsize.setCurrentIndex(self.VM_Size)
        self.ui.le_device.setText(self.Device_Name)

    # 要修改Section, Key 的 Value => self.set_Config("IMG_Config", "Test", "CCS")
    def set_Config(self, section, key, key_value, sysmsg):
        self.ui.txt_sysmsg.append("正在設定config.ini檔...")
        self.config.set(section, key, key_value)
        self.config.write(open('config.ini', 'w'))
        self.ui.txt_sysmsg.append(sysmsg)

    # 讀取config.ini設定檔內的資料,並顯示在UI上面 =>  self.get_Config()
    def get_Config(self):
        self.ui.txt_sysmsg.append("正在讀取config.ini檔...")
        self.VM_Type = int(self.config.get('SYS_Config', 'VM_Type'))  # GET "VM_Type"
        self.VM_Size = int(self.config.get('SYS_Config', 'VM_Size'))  # GET "ScreenSize"
        self.Device_Name = self.config.get('SYS_Config', 'Device_Name')  # GET "Device_Name"
        self.LD_Path = self.config.get('SYS_Config', 'LD_Path')  # GET "LD_Path"
        self.Ck_Path = self.config.get('SYS_Config', 'Ck_Path')  # GET "Ck_Path"
        if self.VM_Type >= 0 and self.VM_Type <= 2:
            self.ADB_Path = self.myplayer[self.VM_Type]
        else:
            pass
        if self.VM_Size >= 0 and self.VM_Size <= 1:
            if self.VM_Size == 0:
                self.ScreenSize = self.size960x540
            elif self.VM_Size == 1:
                self.ScreenSize = self.size1280x720
        else:
            pass
        print("VM_Type = ", self.VM_Type)
        print("VM_Size = ", self.VM_Size)
        print("Device_Name = ", self.Device_Name)
        print("LD_Path = ", self.LD_Path)
        print("Ck_Path = ", self.Ck_Path)
        print("ADB_Path = ", self.ADB_Path)
        print("ScreenSize = ", self.ScreenSize)

    # 呼叫get_DeviceName函數, 取得device資訊, 並顯示在UI
    def getDeviceId(self):
        self.get_DeviceMsg()
    # 設定config.ini檔內的device_name
    def setDeviceId(self):
        deviceId = self.ui.le_device.text()
        if deviceId.strip() != "":
            deviceId = deviceId.strip()
            self.set_Config("SYS_Config", "Device_Name", deviceId, "device:" + deviceId + "已設定")
        else:
            self.ui.txt_sysmsg.append("device不能為空")

    # 取得DeviceName 資訊並顯示在UI => 使用者複自行複製資訊中的某些資料到指定的textbox(txt_DeviceName) => 按下變更按鈕後儲存到ini檔
    def get_DeviceMsg(self):
        self.ui.txt_sysmsg.append("正在取得你的模擬器 Device Name ...")
        # print(self.ADB_Path)
        proc = subprocess.Popen([self.ADB_Path, "devices"], stdout=subprocess.PIPE)
        #out = p.stdout.readlines()[1:2]
        (out, err) = proc.communicate()
        #print("program output:", str(out.split()))
        self.ui.txt_sysmsg.append("get device:%s" % str(out.split()))
        #for line in out:
        #    line = line.split()  # 預設去掉'\n', '\r', '\t', ' '
        #    self.ui.txt_sysmsg.append("device 訊息:" + str(line))
            # print("line:%s" % line)

    def clearmsg(self):
        self.ui.txt_sysmsg.clear()
    def diarycount(self):
        d_dirarycount = self.ui.hs_diarycount.value()
        self.ui.lab_displaydiraycount.setText(d_dirarycount.__str__())
        print('lab_displaydiraycount is %s ' % self.ui.lab_displaydiraycount.text())
        #print('dirarycount:%d' % d_dirarycount)
    def vmtype(self):
        s_vmtype = self.ui.cb_vmtype.currentText()
    def vmsize(self):
        s_vmsize = self.ui.cb_vmsize.currentText()
    def exit(self):
        self.destroy()
        sys.exit()
    def leftpic1(self):
        print('leftpic1')
    def leftpic2(self):
        print('leftpic2')
    def rightpic1(self):
        print('rightpic1')
    def rightpic2(self):
        print('rightpic2')
    def autostart(self):
        # 起動LineageM
        self.ui.txt_sysmsg.append("LineageM模組正在起動...")
        self.LM = LineageM.LM(Device_Name=self.Device_Name, Screen_Size=self.ScreenSize, Ck_Path=self.Ck_Path,
                              ADB_Path=self.ADB_Path, LD_Path=self.LD_Path)
        #self.LM.autoDiary()


if __name__ == '__main__':
    # 選擇使用的模擬器 => Device_Name(模擬器ID), *必須依不同模擬器取得不同的模擬器ID , # ADB_Path(ADB程式位置+檔名), 依模擬器設定不同的ADB程式位置+檔名
    # 選擇模擬器畫面尺寸 => Screen_Size(畫面大小)
    # Sample_Path(儲存比對圖片的位置),=>做二個按鈕分別用來儲存 => 1."日記本最左邊想要的圖(diary_left)", 2."日記本最右邊想要的圖(diary_left)", 可設定左右都符合 或 只符合其中一種

    #app = QtWidgets.QApplication([])
    #app = QtWidgets.QApplication(sys.argv)
    #w = MainWindow()
    #w.show()
    #print("Hello! 歡迎使用天堂M-自動轉日記輔助程式!!")
    #sys.exit(app.exec_())
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    print("Hello! 歡迎使用天堂M-自動轉日記輔助程式!!")
    sys.exit(app.exec_())
