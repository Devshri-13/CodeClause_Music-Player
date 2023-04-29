from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
import os
import random,time
from pygame import mixer
from mutagen.mp3 import MP3
import style

mixer.init()
musiclist=[]
mute = False
play = False
current_song = None
count = 0
songLength = 0
index = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setGeometry(450,50,480,700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainlayout.setObjectName("mainlayout")
        self.topgroupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.topgroupBox.setFont(font)
        self.topgroupBox.setStyleSheet("background-color:lavender")
        self.topgroupBox.setObjectName("topgroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.topgroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topLayout = QtWidgets.QHBoxLayout()
        self.topLayout.setObjectName("topLayout")
        self.progressBar = QtWidgets.QProgressBar(self.topgroupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(style.progressbarStyle())
        self.progressBar.setObjectName("progressBar")
        self.topLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.topLayout)
        self.middleLayout = QtWidgets.QHBoxLayout()
        self.middleLayout.setContentsMargins(0, -1, -1, -1)
        self.middleLayout.setObjectName("middleLayout")
        self.middleLayout.addStretch()
        self.addButton = QtWidgets.QToolButton(self.topgroupBox)
        self.addButton.setStyleSheet("border:0\n""\n""")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assests/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QtCore.QSize(48, 48))
        self.addButton.setObjectName("addButton")
        self.middleLayout.addWidget(self.addButton)
        self.shuffleButton = QtWidgets.QToolButton(self.topgroupBox)
        self.shuffleButton.setStyleSheet("border:0")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assests/shuffle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shuffleButton.setIcon(icon1)
        self.shuffleButton.setIconSize(QtCore.QSize(48, 48))
        self.shuffleButton.setObjectName("shuffleButton")
        self.middleLayout.addWidget(self.shuffleButton)
        self.playButton = QtWidgets.QToolButton(self.topgroupBox)
        self.playButton.setStyleSheet("border:0")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assests/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon2)
        self.playButton.setIconSize(QtCore.QSize(64, 64))
        self.playButton.setObjectName("playButton")
        self.middleLayout.addWidget(self.playButton)
        self.previousButton = QtWidgets.QToolButton(self.topgroupBox)
        self.previousButton.setStyleSheet("border:0\n""")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assests/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previousButton.setIcon(icon3)
        self.previousButton.setIconSize(QtCore.QSize(48, 48))
        self.previousButton.setObjectName("previousButton")
        self.middleLayout.addWidget(self.previousButton)
        self.nextButton = QtWidgets.QToolButton(self.topgroupBox)
        self.nextButton.setStyleSheet("border:0")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assests/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(icon4)
        self.nextButton.setIconSize(QtCore.QSize(48, 48))
        self.nextButton.setObjectName("nextButton")
        self.middleLayout.addWidget(self.nextButton)
        self.volumeSlider = QtWidgets.QSlider(self.topgroupBox)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.middleLayout.addWidget(self.volumeSlider)
        self.muteButton = QtWidgets.QToolButton(self.topgroupBox)
        self.muteButton.setStyleSheet("border:0")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("assests/mute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteButton.setIcon(icon5)
        self.muteButton.setIconSize(QtCore.QSize(24, 24))
        self.muteButton.setObjectName("muteButton")
        self.middleLayout.addStretch()

        self.middleLayout.addWidget(self.muteButton)
        self.verticalLayout.addLayout(self.middleLayout)
        self.mainlayout.addWidget(self.topgroupBox,25) 
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.bottomLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.bottomLayout.setObjectName("bottomLayout")
        self.playlist = QtWidgets.QListWidget(self.centralwidget)
        self.playlist.setObjectName("playlist")
        self.playlist.doubleClicked.connect(self.playsong_1)
        self.bottomLayout.addWidget(self.playlist)
        self.mainlayout.addLayout(self.bottomLayout,75)
        MainWindow.setCentralWidget(self.centralwidget)
        self.songTimerLabel = QtWidgets.QLabel("0:00")
        self.songLengthLabel=QtWidgets.QLabel("/ 0:00")
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLengthLabel)

        self.addButton.clicked.connect(self.addSound)
        self.shuffleButton.clicked.connect(self.shuffleplaylist)
        self.playButton.clicked.connect(self.playsong) 
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(70)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setvolume)
        self.muteButton.clicked.connect(self.mutesong)
        self.previousButton.clicked.connect(self.previoussong)
        self.nextButton.clicked.connect(self.nextsong)
        self.topgroupBox.setStyleSheet(style.groupboxStyle())
        self.playlist.setStyleSheet(style.playliststyle())


        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateprogressbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Player"))
        self.topgroupBox.setTitle(_translate("MainWindow", "Music Player"))
        self.addButton.setToolTip(_translate("MainWindow", "Add a song"))
        self.addButton.setText(_translate("MainWindow", "..."))
        self.shuffleButton.setToolTip(_translate("MainWindow", "Shuffle the list"))
        self.shuffleButton.setText(_translate("MainWindow", "..."))
        self.playButton.setToolTip(_translate("MainWindow", "Play"))
        self.playButton.setText(_translate("MainWindow", "..."))
        self.previousButton.setToolTip(_translate("MainWindow", "Play previous"))
        self.previousButton.setText(_translate("MainWindow", "..."))
        self.nextButton.setToolTip(_translate("MainWindow", "Play next"))
        self.nextButton.setText(_translate("MainWindow", "..."))
        self.volumeSlider.setToolTip(_translate("MainWindow", "Volume"))
        self.muteButton.setToolTip(_translate("MainWindow", "Mute"))
        self.muteButton.setText(_translate("MainWindow", "..."))

    def addSound(self):
        directory=QFileDialog.getOpenFileName(MainWindow,"Add Sound","","Sound Filed(*.mp3 *.ogg *.wav)")        
        filename = os.path.basename(directory[0])
        # print(filename)
        musiclist.append(directory[0])
        self.playlist.addItem(filename)

    def shuffleplaylist(self):
        random.shuffle(musiclist)
        # print(musiclist)
        self.playlist.clear()
        for song in musiclist:
            filename = os.path.basename(song)
            self.playlist.addItem(filename)
    def playsong_1(self):
        global play,current_song,songLength,count,index
        count = 0
        index = self.playlist.currentRow()      
        try:
            mixer.music.load(str(musiclist[index]))
            mixer.music.play()
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap("assests/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon7)
            play =True
            current_song = index
            self.timer.start()
            sound = MP3(str(musiclist[index]))
            songLength = sound.info.length
            songLength =round(songLength)
            # print(songLength)
            min,sec=divmod(songLength,60)
            self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setMaximum(songLength)
            
        except:
            pass 
    def playsong(self):
        global play,current_song,songLength,count,index
        index = self.playlist.currentRow()
        if play == False:
            if current_song == index:
                play = True
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap("assests/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.playButton.setIcon(icon2)
                self.timer.start()
                mixer.music.unpause()

            else:   
                try:
                    count = 0
                    mixer.music.load(musiclist[index])
                    mixer.music.play()
                    icon7 = QtGui.QIcon()
                    icon7.addPixmap(QtGui.QPixmap("assests/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.playButton.setIcon(icon7)
                    current_song = index
                    self.timer.start()
                    sound = MP3(str(musiclist[index]))
                    songLength = sound.info.length
                    songLength =round(songLength)
                    # print(songLength)
                    min,sec=divmod(songLength,60)
                    self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
                    self.progressBar.setMaximum(songLength)
            
                except:
                    pass 
            play = True        
        elif play ==True:
            play = False
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("assests/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon2)
            self.timer.stop()
            mixer.music.pause()        
    def setvolume(self):
        global mute
        self.volume=self.volumeSlider.value()
        if self.volume > 0 and mute == True:
            self.mutesong()  
        mixer.music.set_volume(self.volume/100)    
    def mutesong(self):
        global mute 
        _translate = QtCore.QCoreApplication.translate
        if mute == False:
            mixer.music.set_volume(0.0)
            icon6 = QtGui.QIcon()
            icon6.addPixmap(QtGui.QPixmap("assests/unmuted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.muteButton.setIcon(icon6)
            self.muteButton.setToolTip(_translate("MainWindow", "Unmute"))
            self.volumeSlider.setValue(0)
            mute = True
        else:
            icon6 = QtGui.QIcon()
            icon6.addPixmap(QtGui.QPixmap("assests/mute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.muteButton.setIcon(icon6)   
            self.muteButton.setToolTip(_translate("MainWindow", "Mute"))
            self.volumeSlider.setValue(70)
            mute = False
    def previoussong(self):
        global play,current_song,songLength,count,index
        if index ==0:
            index = len(musiclist)-1
        else:
            index-=1    
        try:
            count = 0
            mixer.music.load(musiclist[index])
            mixer.music.play()
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap("assests/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon7)
            current_song = index
            self.timer.start()
            sound = MP3(str(musiclist[index]))
            songLength = sound.info.length
            songLength =round(songLength)
            # print(songLength)
            min,sec=divmod(songLength,60)
            self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setMaximum(songLength)
    
        except:
            pass 
    def nextsong(self):  
        global play,current_song,songLength,count,index
        if index ==len(musiclist)-1:
            index = 0
        else:
            index+=1    
        try:
            count = 0
            mixer.music.load(musiclist[index])
            mixer.music.play()
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap("assests/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playButton.setIcon(icon7)
            current_song = index
            self.timer.start()
            sound = MP3(str(musiclist[index]))
            songLength = sound.info.length
            songLength =round(songLength)
            # print(songLength)
            min,sec=divmod(songLength,60)
            self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
            self.progressBar.setMaximum(songLength)
    
        except:
            pass       
    def updateprogressbar(self):
        global count,songLength
        count +=1
        self.progressBar.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S",time.gmtime(count)))
        if count == songLength:
            self.timer.stop()
            self.nextsong()
                
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

