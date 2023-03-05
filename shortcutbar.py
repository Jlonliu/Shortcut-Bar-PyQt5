#窗口构建程序不进行参数检测
#为保证参数正确，请在调用此文件内类之前进行参数的预处理

IMPORTED = True
try:
    import sys
    import re#正则表达式模块
    import xlrd#Excel表读取模块
    from PyQt5.QtWidgets import QApplication, QFileDialog,QInputDialog,QWidget,QFrame,QHBoxLayout,QGridLayout,QSplitter,QMainWindow,QAction
    from PyQt5.QtWidgets import QMenu, qApp,QListWidget,QListWidgetItem,QAbstractItemView,QPushButton,QComboBox,QMessageBox,QLineEdit
    from PyQt5.QtCore import Qt,QPoint,QSize
    from PyQt5.QtGui import QPalette,QColor,QIcon,QMouseEvent,QFont,QCursor
    from mfr import *
    from qmfr import *
except ImportError:
    IMPORTED = False
if IMPORTED:
    class MainWindow(QWidget):#搜索框类
        def __init__(self):
            super().__init__()#继承
            self.mfr = MFR()

            #Data Path
            self.datapathfile = self.mfr.thisstrfilepath + 'datapath.txt'
            self.datapath = self.mfr.ReadDicFile(self.datapathfile)
            self.msg = self.mfr.ReadDicFile(self.mfr.thisstrfilepath + 'msg.pdic')
            #self.partpath = self.mfr.ReadDicFile(self.mfr.thisstrfilepath + 'partpath.txt')

            self.width = 620#初始宽度
            self.height = 40#初始高度
            self.shrink = False#是否缩小了
            self.leavetriger = False#是否触发离开窗口事件
            self.casesensitive = False#是否区分大小写
            self.wholecase = True#是否全字符匹配
            self.regular = False#是否使用正则表达式
            self.listwindowshowed = False#是否显示了list窗口
            self.listitemremane = False#更改了列表中的项目名称，用于引导新项目名查找路径
            self.headlesspath = None#更改列表项目名后，失去名称的路径
            self.listitemchanged = True#切换了当前选中的列表项目,初始即为真
            self.shrinkw = 36#折叠后宽度
            self.__InitWindow()#初始化

        def __InitWindow(self):
            self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool) # 去掉标题栏&置顶
            # self.setWindowFlags(Qt.FramelessWindowHint)#去掉标题栏
            # self.setWindowFlags(Qt.WindowStaysOnTopHint)#置顶
            # self.setAttribute(Qt.WA_TranslucentBackground)#透明背景色
            # self.setWindowOpacity(1)#透明度
            # self.setFixedSize(self.width(), self.height())#禁止拉伸窗口
            # self.setWindowFlags(Qt.WindowMinimizeButtonHint)#禁止窗口最大化
            # self.setCursor(Qt.SizeAllCursor)
            # self.setStyleSheet("background:rgb(51,51,51)")
            self.resize(self.width,self.height)
            self.move(400,0)
            self.show()

        def EvtShrink(self):#隐藏事件
            if self.shrink:#如果缩小了
                self.resize(self.width,self.height)
                self.shrink = False
            else:
                self.resize(self.shrinkw,self.height)
                self.shrink = True

        def NewPath(self):#获取用户输入
            return QInputDialog.getText(self, self.msg['M001'], self.msg['M002'], text="")[0]
            # QInputDialog.getText()   # 返回字符串
            # QInputDialog.getInt()   # 返回整数
            # QInputDialog.getDouble()   # 返回小数
            # QInputDialog.getItem()   # 下拉式，返回选择的内容

        #鼠标离开窗口自动折叠
        def leaveEvent(self, a0):
            if self.leavetriger:#如果选择触发窗口事件选项
                self.resize(self.shrinkw,self.height)#
                self.shrink = True#标记为缩小了
            return super().leaveEvent(a0)

        #禁用标题栏后的鼠标移动事件
        def mousePressEvent(self, e):
            if e.button() == Qt.LeftButton:
                self.ismoving = True
                self.start_point = e.globalPos()
                self.window_point = self.frameGeometry().topLeft()
        def mouseMoveEvent(self, e):
            try:
                if self.ismoving:
                    relpos = e.globalPos() - self.start_point#QPoint类型可以直接相减
                    self.move(self.window_point + relpos)
            except AttributeError:#目标类型错误
                pass#什么都不做
        def mouseReleaseEvent(self, e):
            self.ismoving = False

if __name__ == '__main__':#测试用
    if IMPORTED:
        app = QApplication(sys.argv)#Create application
        app.setQuitOnLastWindowClosed(False)#Application quit while all windows be quited
        main_window = MainWindow()#获取主窗口
        oper = Oper()#通用操作类

        #搜索条
        serchbar = SerchBar()
        serchbar.Create(main_window)
        serchbar.move(0,0)
        serchbar.setCursor(Qt.SizeAllCursor)#设置移动光标

        def EvtAlterLeaveTriger():#反转离开事件触发标记位
            if main_window.leavetriger:
                main_window.leavetriger = False
                serchbar.button[8].setFlat(False)
            else:
                main_window.leavetriger = True
                serchbar.button[8].setFlat(True)

        def EvtCaseSensitive():#区分大小写触发事件
            if main_window.casesensitive:#如果区分大小写
                main_window.casesensitive = False
                serchbar.button[1].setFlat(True)
            else:
                main_window.casesensitive = True
                serchbar.button[1].setFlat(False)

        def EvtWholeCase():#区分大小写触发事件
            if main_window.wholecase:#如果区分大小写
                main_window.wholecase = False
                serchbar.button[2].setFlat(True)
            else:
                main_window.wholecase = True
                serchbar.button[2].setFlat(False)

        def EvtRegular():#切换使用正则表达式事件
            if main_window.regular:#如果当前正在使用正则表达式
                main_window.regular = False
                serchbar.button[3].setFlat(True)
            else:
                main_window.regular = True
                serchbar.button[3].setFlat(False)


        def EvtListWindow():#显示列表窗口
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                if main_window.listwindowshowed:#如果已经显示了窗口
                    list_window.hide()#将其隐藏
                    main_window.listwindowshowed = False#
                else:#否则
                    x = main_window.geometry().x()
                    y= main_window.geometry().y() + main_window.geometry().height()
                    list_window.move(x,y)
                    list_window.show()#显示出来
                    main_window.listwindowshowed = True#

        def EvtOpenFile():#打开文件
            blnOpened = False#File be opened
            strkey = ""#文件索引key
            strtext = ""#要查找的文件
            intDataPathLimit = len(main_window.datapath)#Get datapath's value quantity
            for i in main_window.datapath.keys():#Loop short key of path
                intDataPathLimit -= 1#
                strtext = serchbar.serchbox.text()#获取要查询的字符串
                strkey = i#获取key

                #区分大小写
                if main_window.casesensitive:#如果区分大小写
                    pass
                else:
                    strtext = strtext.lower()#转化为小写
                    strkey = strkey.lower()#转化为小写

                #全字符匹配
                if main_window.wholecase:#如果全字符匹配
                    pass
                else:
                    if strtext in strkey:#如果部分字符匹配
                        strtext = strkey#将其设置为全字符匹配

                #使用正则表达式匹配
                if main_window.regular:#如果使用正则表达式
                    if re.match(strtext,strkey):#如果匹配成功
                        strtext = strkey
                else:
                    pass#

                if strkey == strtext:#
                    blnOpened=main_window.mfr.OpenFloader(main_window.datapath[i])
                    break
                else: 
                    if intDataPathLimit < 1:
                        #self.shortpathlineedit.setText(self.comfun.msg['A00006'].format(self.shortpathlineedit.text()))
                        blnOpened = False

            if not blnOpened:#如果未能打开文件
                QMessageBox.information(None,main_window.msg['M019'], main_window.msg['M020'],QMessageBox.Ok)

        def EvtSerchPart():#查询部品事件
            blnSerched = False#部品查询到标记位
            strCurrentPath = ""#当前使用的路径
            intPartPathLimit = len(main_window.partpath)#获取partpath的长度
            for i in main_window.partpath.keys():#Loop short key of path
                intPartPathLimit -= 1#
                strCurrentPath = main_window.partpath[i]#依次获取路径
                wb= xlrd.open_workbook(strCurrentPath)#获取当前路径下的excel表
                sheetName = wb.sheet_names()#获取sheet名称
                sheetNums = wb.sheets()#获取sheet数量
                print(sheetName,sheetNums)
                #****尚未完成******



        def EvtSerching():#搜索事件
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                EvtOpenFile()#调用打开文件事件
            elif serchbar.selectitem.currentText() == main_window.msg['M004']:
                pass#EvtSerchPart()#调用部品查询事件
            elif serchbar.selectitem.currentText() == main_window.msg['M026']:
                pass#调用图纸查询事件

        def EvtLinkFolder():#链接文件夹
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                strLinkName = main_window.NewPath()#获取超链接名
                if isinstance(strLinkName,str) and len(strLinkName) > 0:
                    selectfilepath = QFileDialog(main_window)#打开文件夹
                    FilePath = selectfilepath.getExistingDirectory()#创建新文件夹链接
                    if len(FilePath):#如果成功获取了路径
                        main_window.datapath[strLinkName] = FilePath#获取文件夹路径
                        main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将文件夹路径写入txt文件
                        list_window.listbox.addItem(strLinkName)#将新添加的超链接添加到列表

        def EvtLinkFile():#链接文件按钮
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                strLinkName = main_window.NewPath()#获取超链接名
                if isinstance(strLinkName,str) and len(strLinkName) > 0:
                    selectfilepath = QFileDialog(main_window)#打开文件
                    FilePath,filter = selectfilepath.getOpenFileName()#获取文件链接
                    if len(FilePath):#如果成功获取了路径
                        main_window.datapath[strLinkName] = FilePath#获取文件路径
                        main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将文件路径写入txt文件
                        list_window.listbox.addItem(strLinkName)#将新添加的超链接添加到列表

        def ListItemDoubleClickEvent(item):
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                blnOpened = False
                intDataPathLimit = len(main_window.datapath)#Get datapath's value quantity
                strPathKey = item.text()#获取文件夹名

                if main_window.listitemremane:#如果有过重命名事件
                    if not main_window.listitemchanged:#如果此后未切换选中的Item
                        main_window.listitemremane = False#将更改标记失效
                        blnOpened = main_window.mfr.OpenFloader(main_window.headlesspath)#打开野路径
                    else:#如果切换过Item
                        #删除更名Item对应的超链接
                        strOldName = None#
                        for i in main_window.datapath.keys():
                            if main_window.datapath[i] == main_window.headlesspath:#查找野路径的曾经名
                                strOldName = i
                        if strOldName is not None:#如果找到了曾经名
                            main_window.datapath.pop(strOldName)#找到之后删除此名
                        main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将字典更新到文件
                        main_window.headlesspath = None#将野路径清除
                        #正常操作打开文件事件
                        for i in main_window.datapath.keys():#遍历超链接名称
                            intDataPathLimit -= 1#
                            if i == strPathKey:#如果获取到了匹配的名称
                                blnOpened = main_window.mfr.OpenFloader(main_window.datapath[strPathKey])
                                break
                            else:
                                if intDataPathLimit < 1:
                                    blnOpened = False
                else:#没有重命名事件
                    for i in main_window.datapath.keys():#遍历超链接名称
                        intDataPathLimit -= 1#
                        if i == strPathKey:#如果获取到了匹配的名称
                            blnOpened = main_window.mfr.OpenFloader(main_window.datapath[strPathKey])
                            break
                        else:
                            if intDataPathLimit < 1:
                                blnOpened = False

                if not blnOpened:#如果未能打开文件
                    QMessageBox.information(None, main_window.msg['M019'],main_window.msg['M020'],QMessageBox.Ok)
                else:#如果打开了文件
                    if main_window.headlesspath is not None and not main_window.listitemchanged:#如果存在野路径,未切换过Item
                        strOldName = None#
                        for i in main_window.datapath.keys():
                            if main_window.datapath[i] == main_window.headlesspath:#查找野路径的曾经名
                                strOldName = i
                        if strOldName is not None:#如果找到了曾经名
                            main_window.datapath.pop(strOldName)#找到之后删除此名
                        main_window.datapath[list_window.listbox.currentItem().text()] = main_window.headlesspath#将新名链接野路径
                        main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将字典更新到文件
                        main_window.headlesspath = None#将野路径清除

        #设置装饰条颜色
        #serchbar.prink.setStyleSheet("background:rgb(0,255,255)")
        serchbar.prink.setProperty("name","prink")
        serchbar.prink.setCursor(Qt.SizeAllCursor)#设置移动光标

        #搜索框
        serchbar.serchbox.returnPressed.connect(EvtOpenFile)

        #列表框
        list_window = ListBox()
        list_window.Create()
        list_window.hide()
        list_window.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool)#置顶显示
        #list_window.listbox.currentItemChanged.connect()#切换选中的item触发
        for i in main_window.datapath.keys():#遍历超链接
            list_window.listbox.addItem(i)#添加项目
        for index in range(list_window.listbox.count()):#设为不可编辑
            item = list_window.listbox.item(index)
            item.setFlags(item.flags())

        def CreateNewItem():#创建新项
            # 创建一个没有名字的item
            item = QListWidgetItem("")#无名Item
            item.setTextAlignment(Qt.AlignLeft)#Item靠左显示
            # 使得item是可以编辑的
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            list_window.listbox.addItem(item)
            # 创建后就可以编辑item,用户自己起名字.
            list_window.listbox.editItem(item)#进入可编辑状态
            #编辑完成后返回不可编辑状态
            list_window.listbox.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置不可触发编辑状态

        def DeleteItem():#删除现有项
            strItemName = list_window.listbox.currentItem().text()#获取被删除Item的名称
            list_window.listbox.takeItem(list_window.listbox.currentRow())#删除选中的Item
            #将超链接文件中的此项目也删除
            for i in main_window.datapath.keys():
                if i == strItemName:#如果删除了存在于文件内的项目
                    main_window.datapath.pop(strItemName)#将字典中的此项目也删除
                    main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将字典重新写入文件
                    break#退出循环

        def RenameItem():#重命名项
            # curRow = list_window.listbox.currentRow()#获取当前选中的行
            # item = list_window.listbox.item(curRow)#获取
            strItemName = list_window.listbox.currentItem().text()#获取被删除Item的名称
            main_window.headlesspath = main_window.datapath[strItemName]#获取当前Item链接的路径
            main_window.listitemremane = True#设定刚刚更改了项目名
            item = list_window.listbox.currentItem()#获取当前选中的Item
            item.setFlags(item.flags() | Qt.ItemIsEditable)#Item设置位可编辑
            list_window.listbox.editItem(item)#设置为编辑状态
            #编辑完成后返回不可编辑状态
            list_window.listbox.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置不可触发编辑状态
            main_window.listitemchanged = False#将选中Item项目切换改为假
            #list_window.listbox.itemChanged.connect(lambda: ChangeItem(item))

        def EvtItemLinkFile():#列表项目超链接文件
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                strLinkName = list_window.listbox.currentItem().text()#获取当前Item名称
                #strLinkName = main_window.NewPath()#获取超链接名
                if isinstance(strLinkName,str) and len(strLinkName) > 0:
                    selectfilepath = QFileDialog(main_window)#打开文件
                    FilePath,filter = selectfilepath.getOpenFileName()#获取文件链接
                    main_window.datapath[strLinkName] = FilePath#获取文件路径
                    main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将文件路径写入txt文件
        
        def EvtItemLinkFolder():#列表项目超链接文件夹
            if serchbar.selectitem.currentText() == main_window.msg['M003']:
                strLinkName = list_window.listbox.currentItem().text()#获取当前Item名称
                #strLinkName = main_window.NewPath()#获取超链接名
                if isinstance(strLinkName,str) and len(strLinkName) > 0:
                    selectfilepath = QFileDialog(main_window)#打开文件
                    FilePath = selectfilepath.getExistingDirectory()#获取文件链接
                    main_window.datapath[strLinkName] = FilePath#获取文件路径
                    main_window.mfr.WriteDicFile(main_window.datapath,main_window.datapathfile)#将文件路径写入txt文件
       
        def EvtRightMouseMenu():#列表右键菜单
            menu = QMenu(list_window.listbox)
            lisAction = []
            lisAction.append(menu.addAction(main_window.msg['M021']))
            lisAction.append(menu.addAction(main_window.msg['M022']))
            lisAction.append(menu.addAction(main_window.msg['M023']))
            lisAction.append(menu.addAction(main_window.msg['M024']))
            lisAction.append(menu.addAction(main_window.msg['M025']))
            lisAction[0].triggered.connect(RenameItem)
            lisAction[1].triggered.connect(CreateNewItem)
            lisAction[2].triggered.connect(DeleteItem)
            lisAction[3].triggered.connect(EvtItemLinkFile)
            lisAction[4].triggered.connect(EvtItemLinkFolder)

            menu.exec_(QCursor.pos())

        def EvtCurItemChg():#选中Item改变事件
            main_window.listitemchanged = True#将改变了当前项目设置为真

        list_window.listbox.currentItemChanged.connect(EvtCurItemChg)
        list_window.listbox.itemDoubleClicked.connect(ListItemDoubleClickEvent)#双击事件
        list_window.listbox.setContextMenuPolicy(Qt.CustomContextMenu)#设置为支持右键
        list_window.listbox.customContextMenuRequested.connect(EvtRightMouseMenu)#链接右键事件

        #设置选择框
        #serchbar.selectitem.addItems([main_window.msg['M003'],main_window.msg['M004'],main_window.msg['M026']])
        serchbar.selectitem.addItems([main_window.msg['M003']])

        #缩小按钮
        serchbar.button[0].clicked.connect(main_window.EvtShrink)#按钮链接窗口缩小
        serchbar.button[0].setToolTip(main_window.msg['M005'])

        #区分大小写
        serchbar.button[1].clicked.connect(EvtCaseSensitive)#区分大小写
        serchbar.button[1].setToolTip(main_window.msg['M006'])
        serchbar.button[1].setFlat(True)

        #全字匹配
        serchbar.button[2].clicked.connect(EvtWholeCase)#全字匹配
        serchbar.button[2].setToolTip(main_window.msg['M027'])
        serchbar.button[2].setFlat(False)

        #正则表达式
        serchbar.button[3].clicked.connect(EvtRegular)#正则表达式
        serchbar.button[3].setToolTip(main_window.msg['M028'])
        serchbar.button[3].setFlat(True)

        #退出按钮
        serchbar.button[9].clicked.connect(oper.closeEvent)#链接退出函数
        serchbar.button[9].setToolTip(main_window.msg['M007'])
        serchbar.button[9].setText(main_window.msg['M013'])

        #离开事件按钮
        serchbar.button[8].clicked.connect(EvtAlterLeaveTriger)#反转离开事件触发标记位
        serchbar.button[8].setToolTip(main_window.msg['M008'])
        serchbar.button[8].setText(main_window.msg['M014'])
        serchbar.button[8].setFlat(False)
        #serchbar.button[8].setStyleSheet("font-size:14px")

        #打开列表按钮
        serchbar.button[7].clicked.connect(EvtListWindow)#反转离开事件触发标记位
        serchbar.button[7].setToolTip(main_window.msg['M009'])
        serchbar.button[7].setText(main_window.msg['M015'])

        #搜索按钮
        serchbar.button[6].clicked.connect(EvtSerching)#反转离开事件触发标记位
        serchbar.button[6].setToolTip(main_window.msg['M010'])
        serchbar.button[6].setText(main_window.msg['M016'])
        #serchbar.button[6].setStyleSheet("font-size:24px")

        #添加文件夹超链接按钮
        serchbar.button[5].clicked.connect(EvtLinkFolder)#反转离开事件触发标记位
        serchbar.button[5].setToolTip(main_window.msg['M011'])
        serchbar.button[5].setText(main_window.msg['M017'])
        #serchbar.button[5].setStyleSheet("font-size:24px")

        #添加文件超链接按钮
        serchbar.button[4].clicked.connect(EvtLinkFile)#反转离开事件触发标记位
        serchbar.button[4].setToolTip(main_window.msg['M012'])
        serchbar.button[4].setText(main_window.msg['M018'])
        #serchbar.button[4].setStyleSheet("font-size:24px")


        with open(main_window.mfr.thisstrfilepath + "mytest.qss", "r",encoding='utf-8-sig') as f:#Read qss
            qApp.setStyleSheet(f.read())
            
        try:
            sys.exit(app.exec_())#进入消息循环
        except SystemExit:#退出主程序不退出调用命令行
            pass