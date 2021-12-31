from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMovie
import sys
import os
import socket
import psutil

barcount = 0

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/raspberypi.ui', self)

        self.movie = QMovie(os.path.dirname(__file__) + '/digitalruh3.gif')

       
        self.btnKapat.clicked.connect(shutdownmsg)

       
        self.btnBaslat.clicked.connect(self.btn_reboot)

        
        self.btnCikis.clicked.connect(showDialog)

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.lcdupdate)
        self.timer.start(1000)

        # self.lblpix.setMovie(self.movie)
        self.movie.start()

        self.show()


    def lcdupdate(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.lblSaat.setText(label_time)
        self.lblTemp.setText("%4.2f°C" % get_cpu_temp())
        self.lblEth.setText(get_ip_address_2("eth0"))
        self.lblWlan.setText(get_ip_address_2("wlan0"))
        self.progBarCpu.setValue(int(psutil.cpu_percent()))
        self.progBarMemory.setValue(int(psutil.virtual_memory().percent))
        ramtoplam = str(round(float((psutil.virtual_memory().total/1024)/1024), 2))
        ramkul = str(round(float((psutil.virtual_memory().used/1024)/1024), 2))
        self.lblDisk.setText(ramtoplam + ' / ' + ramkul + ' MB')
        self.lblFreq.setText(str(psutil.cpu_freq().current) + ' MHz')

        hdd = psutil.disk_usage('/')
        strdisktotal = "%d" % (hdd.total / (2**30))
        strdiskusage = "%d" % (hdd.used / (2**30))
        self.lblDisk_2.setText(strdisktotal + " GiB / " + strdiskusage + " GiB")




    def btn_reboot(self):
        os.system("sudo reboot now")

    def btn_shutdown(self):
        os.system("sudo shutdown now")

    def btn_temp_goster(self):
        self.lblTemp.setText("%4.2f°C" % get_cpu_temp())

def shutdownmsg():
    sdmsgbox = QMessageBox()
    sdmsgbox.setIcon(QMessageBox.Information)
    sdmsgbox.setText("Kapatmak istediğinizden eminmisiniz?")
    sdmsgbox.setWindowTitle("Sistem Uyarı !")
    sdmsgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    retsd = sdmsgbox.exec()
    if retsd == sdmsgbox.Ok:
        os.system("sudo shutdown now")


def showDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Çıkıs Yapmak İstediginize Emin misiniz?")
    msgBox.setWindowTitle("QMessageBox Example")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.buttonClicked.connect(msgButtonClick)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')
        exit()


def msgButtonClick(i):
    print("Button clicked is:", i.text())


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_ip_address_2(conval):
    try:
        interfaces = psutil.net_if_addrs()
        ip = interfaces[conval][0][1]
        return ip
    except:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def get_cpu_temp():
    try:
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return round(float(cpu_temp) / 1000, 2)
    except:
        return 0

def cpu():
    return str(psutil.cpu_percent()) + '%'

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()