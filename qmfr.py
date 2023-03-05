#窗口构建程序不进行参数检测
#为保证参数正确，请在调用此文件内类之前进行参数的预处理

#使用方式

#作成者 刘加龙
#修改履历************************************************************
#2022-01-08 #追加了区分大小写按钮事件
#*******************************************************************
from PyQt5.QtWidgets import QLabel


IMPORTED = True
try:
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget,QFrame,QHBoxLayout,QGridLayout,QSplitter,QMainWindow,QAction
    from PyQt5.QtWidgets import QMenu, qApp,QListWidget,QListWidgetItem,QAbstractItemView,QPushButton,QComboBox,QMessageBox,QLineEdit
    from PyQt5.QtCore import Qt,QPoint,QSize
    from PyQt5.QtGui import QPalette,QColor,QIcon,QMouseEvent,QFont,QCursor
except ImportError:
    IMPORTED = False
if IMPORTED:

    class SerchBar(QWidget):#搜索框类
        def __init__(self):
            super().__init__()#继承

            self.x = None#x坐标 
            self.y = None#y坐标 
            self.width = None#宽 
            self.height = None#高
            self.exist = False#窗口绘制成功
            self.prink = None#左侧装饰条
            self.serchbox = None#搜索编辑框
            self.selectitem = None#选择框
            self.csen = False#区分大小写
            self.button = []#按钮列表
            self.buttonnum = 10#默认10个按钮
            self.__InitWindow()#初始化

        def __InitWindow(self):
            # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool) # 去掉标题栏&置顶
            self.setWindowFlags(Qt.FramelessWindowHint)#去掉标题栏
            # self.setWindowFlags(Qt.WindowStaysOnTopHint)#置顶
            # self.setAttribute(Qt.WA_TranslucentBackground)#透明背景色
            # self.setWindowOpacity(1)#透明度
            # self.setFixedSize(self.width(), self.height())#禁止拉伸窗口
            # self.setWindowFlags(Qt.WindowMinimizeButtonHint)#禁止窗口最大化
            # self.setCursor(Qt.SizeAllCursor)#设置移动光标
            self.exist = True#窗口绘制成功

        def __SetGeo(self,x,y,w,h):#设置几何参数
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.move(x,y)
            self.resize(w,h)

        def Create(self,p=None,x=100,y = 100,w=620,h=40):#搜索框：有下拉框，复数按钮
            #宽度是100的倍数，高度是40的倍数
            if self.exist:#如果窗口绘制成功

                #左侧装饰条
                self.prink = QWidget(self)
                self.prink.move(0,0)
                self.prink.resize(int(0.01*w),h)
                #self.prink.setStyleSheet('background:pink')

                #搜索条窗口设置
                if p is not None:
                    self.setParent(p)#设置父对象
                #self.setProperty("serchbar")#设置属性名称，用于qss设计
                self.__SetGeo(x,y,w,h)#设置几何参数

                #搜索框设置
                self.serchbox = QLineEdit()#绘制单行编辑框
                self.serchbox.setParent(self)
                self.serchbox.move(int(0.06*w),int(0.125*h))
                self.serchbox.resize(int(0.5*w),int(0.75*h))

                #选择框设置
                self.selectitem = QComboBox(self)#设置文本条
                self.selectitem.move(int(0.06*w+0.5*w+1),int(0.175*h))#
                self.selectitem.resize(int(0.14*w),int(0.65*h))
                self.selectitem.setCursor(Qt.PointingHandCursor)#设置鼠标光标
                # self.selectitem.addItem('文件夹')
                # self.selectitem.addItem('部品查询')

                #按钮设置
                for i in range(0,self.buttonnum):#创建功能按钮
                    self.button.append(QPushButton(self))#绘制按钮
                    self.button[i].resize(int(0.65*h),int(0.65*h))#设置按钮大小
                    self.button[i].setCursor(Qt.PointingHandCursor)#设置鼠标光标
                    self.button[i].setFlat(True)#扁平化
                    #self.button[i].setIconSize(QSize(0.04*w,0.5*h))

                #按钮独立属性设置
                self.button[0].resize(int(0.05*w),h)#重新设置大小
                self.button[0].move(int(0.01*w),0)#将按钮设置在最左侧
                self.button[0].setText(">")#设置按钮文字
                self.button[0].setToolTip("预备按钮")
                #self.button[0].setDown(True)#将按钮设置为被按下的状态

                self.button[1].move(int(0.06*w+0.5*w-1-3*0.65*h),int(0.175*h))
                self.button[1].setText("Aa")
                self.button[1].setToolTip("区分大小写")

                self.button[2].move(int(0.06*w+0.5*w-1-2*0.65*h),int(0.175*h))
                self.button[2].setText("ab")
                self.button[2].setToolTip("全字匹配")

                self.button[3].move(int(0.06*w+0.5*w-1-1*0.65*h),int(0.175*h))
                self.button[3].setText(".*")
                self.button[3].setToolTip("使用正则表达式")

                self.button[4].move(int(w-1-6*0.65*h),int(0.175*h))
                self.button[4].setText("Sp")
                self.button[4].setToolTip("预备按钮")

                self.button[5].move(int(w-1-5*0.65*h),int(0.175*h))
                self.button[5].setText("Sp")
                self.button[5].setToolTip("预备按钮")

                self.button[6].move(int(w-1-4*0.65*h),int(0.175*h))
                self.button[6].setText("Sp")
                self.button[6].setToolTip("预备按钮")

                self.button[7].move(int(w-1-3*0.65*h),int(0.175*h))
                self.button[7].setText("Sp")
                self.button[7].setToolTip("预备按钮")

                self.button[8].move(int(w-1-2*0.65*h),int(0.175*h))
                self.button[8].setText("Sp")
                self.button[8].setToolTip("预备按钮")

                self.button[9].move(int(w-1-1*0.65*h),int(0.175*h))
                self.button[9].setText("Sp")
                self.button[9].setToolTip("预备按钮")
                
                self.show()#显示窗口
                
        def EvtSetCSen(self):#设置是否区分大小写
            if self.csen:#如果已经是区分大小写状态
                self.csen = False
            else:#如果不是区分大小写状态
                self.csen = True

        # #禁用标题栏后的鼠标移动事件
        # def mousePressEvent(self, e):
        #     if e.button() == Qt.LeftButton:
        #         self.ismoving = True
        #         self.start_point = e.globalPos()
        #         self.window_point = self.frameGeometry().topLeft()
        # def mouseMoveEvent(self, e):
        #     try:
        #         if self.ismoving:
        #             relpos = e.globalPos() - self.start_point#QPoint类型可以直接相减
        #             self.move(self.window_point + relpos)
        #     except AttributeError:#目标类型错误
        #         pass#什么都不做
        # def mouseReleaseEvent(self, e):
        #     self.ismoving = False

    class ListBox(QWidget):
        def __init__(self):
            super().__init__()#继承
            self.x = None#x坐标 
            self.y = None#y坐标 
            self.width = None#宽 
            self.height = None#高
            self.listbox = None#列表窗口
            self.exist = False#窗口绘制成功
            self.__InitWindow()#初始化

        def __InitWindow(self):
            # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool) # 去掉标题栏&置顶
            self.setWindowFlags(Qt.FramelessWindowHint)#去掉标题栏
            # self.setWindowFlags(Qt.WindowStaysOnTopHint)#置顶
            # self.setAttribute(Qt.WA_TranslucentBackground)#透明背景色
            # self.setWindowOpacity(1)#透明度
            # self.setFixedSize(self.width(), self.height())#禁止拉伸窗口
            # self.setWindowFlags(Qt.WindowMinimizeButtonHint)#禁止窗口最大化
            # self.setCursor(Qt.SizeAllCursor)#设置移动光标
            self.exist = True#窗口绘制成功

        def __SetGeo(self,x,y,w,h):#设置几何参数
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.move(x,y)
            self.resize(w,h)

        def Create(self,p = None, withmenu = False,x = 100,y = 100,w = 620,h = 300,listitem=[]):#
            if self.exist:#如果窗口绘制成功

                #搜索条窗口设置
                if p is not None:
                    self.setParent(p)#设置父对象
                #self.setProperty("serchbar")#设置属性名称，用于qss设计
                self.__SetGeo(x,y,w,h)#设置几何参数

                self.listbox = QListWidget(self)#获取listwidget
                self.listbox.move(0,0)
                self.listbox.resize(w,h)
                self.listbox.setCursor(Qt.PointingHandCursor)
                self.listbox.setAcceptDrops(True)#拖拽设置
                self.listbox.setDragEnabled(True)#拖拽设置
                self.listbox.setSelectionMode(QAbstractItemView.SingleSelection)#设置选定模式，单选
                #listbox.setStyleSheet(self.ins_const.listboxstylesheet)#设置QlistWidget背景为淡黑色，字体颜色白色
                self.listbox.setFrameShape(QListWidget.NoFrame)#无边框
                self.listbox.addItems(listitem)#添加项目
                #font = QFont()#获取字体设置
                #font.setFamily("SimSun")#字体
                #font.setPointSize(11)#字号
                #listbox.itemDoubleClicked.connect(self.ListItemDoubleClickEvent)#连接双击事件
                if withmenu:#如果需要默认的右键菜单
                    self.listbox.setContextMenuPolicy(Qt.CustomContextMenu)#设置为支持右键
                    self.listbox.customContextMenuRequested.connect(self.EvtRightMouseMenu)#链接右键事件
                self.show()

        def CreateNewItem(self):#创建新Item
            item = QListWidgetItem("")#无名Item
            item.setTextAlignment(Qt.AlignLeft)#Item靠左显示
            item.setFlags(item.flags() | Qt.ItemIsEditable)# 使得item是可以编辑的
            self.listbox.addItem(item)
            self.listbox.editItem(item)#进入可编辑状态
            #编辑完成后返回不可编辑状态
            self.listbox.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置不可触发编辑状态

        def DeleteItem(self):
            self.listbox.takeItem(self.listbox.currentRow())#删除选中的Item

        def RenameItem(self):
            item = self.listbox.currentItem()#获取当前选中的Item
            item.setFlags(item.flags() | Qt.ItemIsEditable)#Item设置位可编辑
            self.listbox.editItem(item)#设置为编辑状态
            #编辑完成后返回不可编辑状态
            self.listbox.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置不可触发编辑状态
            
        def EvtRightMouseMenu(self):
            menu = QMenu(self.listbox)
            lisAction = []
            lisAction.append(menu.addAction("更改"))
            lisAction.append(menu.addAction("添加"))
            lisAction.append(menu.addAction("删除"))
            lisAction[0].triggered.connect(self.RenameItem)
            lisAction[1].triggered.connect(self.CreateNewItem)
            lisAction[2].triggered.connect(self.DeleteItem)

            menu.exec_(QCursor.pos())


    #常用操作函数
    class Oper(QWidget):
        def __init__(self):
            #Inherit
            super().__init__()

        def closeEvent(self):#退出程序
            app = QApplication.instance()
            app.quit()

if __name__ == '__main__':#测试用
    if IMPORTED:
        app = QApplication(sys.argv)#Create application
        app.setQuitOnLastWindowClosed(False)#Application quit while all windows be quited
        main_window = SerchBar()#获取主窗口
        main_window.Create()
        listbox = ListBox()
        listbox.Create()
        listbox.move(200,200)
        oper = Oper()
        main_window.button[9].clicked.connect(oper.closeEvent)
        try:
            sys.exit(app.exec_())#进入消息循环
        except SystemExit:#退出主程序不退出调用命令行
            pass
