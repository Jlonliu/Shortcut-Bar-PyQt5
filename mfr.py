#初始化常量，识别操作系统，加载各类文件
#用于各类的初始化父类
#不建议主动调用

IMPORTED = True#模块导入状态
try:
    import os,sys,platform#系统相关
    import xlwt#Excel表格相关
except ImportError:
    IMPORTED = False#导入失败
    #print("Necessary module be imported failed : {os,sys,platfrom,safedog,xlwt}")#提醒模块导入失败

if IMPORTED:

    #常用函数记录
    class MFR():
        def __init__(self):
            super().__init__()#继承

            self.is_linux = None#是否是Linux环境下
            self.is_windows = None#是否是在Windows系统下
            self.dir_div = None#默认路径分割符
            self.thisstrfilepath = None#此文件所在的全路径

            self.msg = None#提示信息
            self.user = None#用户数据
            self.flag = None#标识参数

            self.__Init()#初始化
            

        def __Init(self):#初始化
            self.__ResetPathDivSign()#重新设置路径分隔符
            self.__InitThisstrFilePath()#获取此文件所在的全路径
            self.__LoadMsg()#重新加载信息文件
            self.__LoadUser()#重新加载用户数据
            self.__LoadFlag()#重新加载标识参数

        def __InitThisstrFilePath(self):#获取此文件所在的全路径
            if not self.thisstrfilepath:#如果尚未获取路径或者路径为空
                self.thisstrfilepath = os.path.split(os.path.abspath(sys.argv[0]))[0] + self.dir_div
        
        def __ResetPathDivSign(self):#根据操作系统环境重新设置路径分隔符
            os_platfrom = platform.platform()#获取操作系统信息
            if 'linux' in os_platfrom.lower():
                self.is_windows = False#否定Windows系统
                self.is_linux = True#确定linux系统
                self.dir_div = '/'#Linux环境下重新定义路径分割符号
            elif 'windows' in os_platfrom.lower():
                self.is_windows = True#否定Windows系统
                self.is_linux = False#确定linux系统
                self.dir_div = '\\'#Windows环境下重新定义路径分割符号                
            else:
                pass

        def __LoadDicFile(self,strPath,strcoding = 'utf-8-sig',intlinelimit = 65535,strdivsign = '=',blnnew = True):#加载字典文件
            
            #字典文件即数据全部为"键 = 值"的文件
            #参数1 文件路径 参数2 读取编码 参数3 读取行上限 参数4 键值分割符 参数5 是否允许创建新文件
            #返回一个字典

            dicVariable = {}#空字典
            blnExist = False#默认不存在文件
            if not os.path.exists(strPath):#没有找到目标文件
                if blnnew:#如果允许创建新文件
                    f = open(strPath,'w')#新建一个
                    f.close()#关闭它
                    blnExist = True#设为存在文件
            else:
                blnExist = True#设为存在文件
            if blnExist:#如果已经存在文件
                with open(strPath, 'r', encoding = strcoding) as fr: #打开文件
                    for i in range(0,intlinelimit):#获取读取上限
                        if i == intlinelimit - 1:#如果到达了读取上限
                            #print(self.msg['A00001'])#读取信息文件失败
                            break#退出循环
                        lines = fr.readline()#读取一行
                        if not lines:#到达行尾
                            break#退出循环
                        lines_valid = lines.replace('\n','')#清除换行符
                        lines_valid = lines_valid.replace('\r','')#清除回车符
                        if len(lines_valid):#获取到了数据
                            lis_lines_valid = lines_valid.split(strdivsign)#分割键值
                            if len(lis_lines_valid) == 2:#如果分割完成
                                dicVariable[lis_lines_valid[0].strip()] = lis_lines_valid[1].strip()#添加到字典
            else:
                pass#如果没有查找到文件的操作
            return dicVariable#返回字典

        def __LoadUser(self):#加载用户数据
            if self.user is None:#如果尚未加载用户数据
                strUserPath = self.thisstrfilepath + 'user.pdic'#用户数据全路径
                self.user = self.__LoadDicFile(strUserPath)#加载用户数据

        def __LoadFlag(self):#加载标识参数
            if self.flag is None:#如果尚未加载标识参数
                strFlag = self.thisstrfilepath + 'flag.pdic'#标识参数全路径
                self.flag = self.__LoadDicFile(strFlag)#加载标识参数

        def __LoadMsg(self):#加载用户数据
            if self.msg is None:#如果尚未加载用户数据
                strMsgPath = self.thisstrfilepath + 'msg.pdic'#用户数据全路径
                self.msg = self.__LoadDicFile(strMsgPath)#加载用户数据

        def IsUnEmptyString(self,stream):#检测字符串是否是非空字符串
            return isinstance(stream,str) and stream != ''#如果是字符串并且非空        

        def CutStringByEqualLen(self,stream,intcut): #以指定长度等长截取字符串，返回列表
            lishex = []#存储16进制字符串的列表
            if self.IsUnEmptyString(stream):#如果是可演算状态
                intlooptimes = int(len(stream) / intcut) + int(len(stream) % intcut > 0)#字符串能被分割多少个
                for i in range(0,intlooptimes):
                    lishex.append(stream[i*intcut:(i+1)*intcut])#每intcut位截取一次
            return lishex#返回列表

        def StatistNum(self,stream):#统计字符串中的总数字，返回整数
            intnumstatist = 0#字符串里含数字统计
            if isinstance(stream,str):#如果传入的是字符串
                for i in stream:#遍历字符串
                    intnumstatist += i.isnumeric()#如果寻找到数字，计数器加1
            return intnumstatist
    
        def StatistAlp(self,stream):#统计字符串中的总字母，返回整数
            intalpstatist = 0#字符串里含数字统计
            if isinstance(stream,str):#如果传入的是字符串
                for i in stream:#遍历字符串
                    intalpstatist += i.isalpha()#如果寻找到字母，计数器加1
            return intalpstatist

        def StatistChr(self,stream,chraim):#统计字符串中的指定字符数量
            intchrstatist = 0#字符串里含数字统计
            if isinstance(stream,str):#如果传入的是字符串
                for i in stream:#遍历字符串
                    intchrstatist += int(i == chraim)#如果寻找到字母，计数器加1
            return intchrstatist

        def UniqueSpace(self,stream):#去除头尾空格和重复空格
            strresult = ''#返回值字符串
            if isinstance(stream,str):#字符串检测
                lispuredata = [i for i in stream.split(' ') if i != '']#分割字符串:去除所有空格
                for i in lispuredata:
                    strresult += (i + ' ')
            return strresult.strip()#返回值

        def StrTailCheck(self,stream,chrtail):#检查字符串后面有没有指定字符，如果没有，就添加指定字符
            #参数 1.字符串 2.要追加的字符
            strresult = None#返回字符串
            if isinstance(stream,str) and isinstance(chrtail,str):#如果身体和尾巴是字符串
                int_len_chrtail = len(chrtail)#获取尾巴的长度
                if int_len_chrtail and stream[-int_len_chrtail:] != chrtail:#如果不是空气尾巴并且字符串没有尾巴
                    strresult = stream + chrtail#添加尾巴
                else:#如果追加的是空气尾巴或者已经有了尾巴
                    strresult = stream
            return strresult#返回字符串

        def StrNumCheck(self,strnum):#判断字符串是否是数字字符串，返回布尔值
            bln_result = False#是否是字符串,默认为否
            try:
                if complex(strnum):#检测输入的数字是否包含在复数之内
                    bln_result = True
            except ValueError:
                pass
            except TypeError:
                pass
            return bln_result#返回布尔值

        def Validation(self,stream,restrict = []):#判断输入的字符串是否是限定字符串
            lisres = []#缓存列表
            bln_result = False#默认输入的字符串不是限定字符串
            if isinstance(restrict,list):#如果输入的是限定字符串列表
                lisres = restrict#获取限定字符串列表
            elif isinstance(restrict,str):#如果输入的是限定字符串
                lisres.append(restrict)#获取限定字符串
            else:#如果输入了其他类型
                pass#类型错误的操作
                #print(self.msg['A00003'].format(restrict))
            if lisres != []:#如果缓存列表不为空，进行数据验证
                if stream in lisres:#如果输入了指定字符
                    bln_result = True#属于限定字符串
            else:#如果缓存列表为空,即不需要进行数据验证
                bln_result = True#不需要验证即为真
            return bln_result#返回布尔值

        def InputNum(self,stadata = 'num'):#获取字符串格式数字,返回数值格式数字
            numresult = None#要返回的数字
            try:
                strnum = input(stadata)#获取输入
                if complex(strnum):#检测输入的数字是否包含在负数之内
                    numresult = complex(strnum)
                    if float(strnum):#如果输入的是浮点型
                        numresult = float(strnum)
                        if int(strnum):#如果输入的是整数型
                            numresult = int(strnum)
                        else:
                            numresult = None#空
                    else:
                        numresult = None
                else:
                    numresult = None
            except ValueError:
                pass
            except EOFError:#末尾结束符
                print(self.msg['A00002'])#提示读取到了文件结尾符
            return numresult#返回值

        def InputValidation(self,stadata = "",restrict = []):#获取限定字符串,接收交互声明和限定字符串列表
            str_result = None#默认返回值为空
            try:
                res = input(stadata)#获取输入
                if self.Validation(res,restrict):#限定字符串验证
                    str_result = res#获取字符串
            except EOFError:#末尾结束符
                print(self.msg['A00002'])#提示读取到了结尾符
            return str_result#返回字符串

        def StrPathCheck(self,strpath):#判断字符串是否是路径字符串
            bln_result = False#默认不是路径字符串
            if not isinstance(strpath,str):#如果传入的数据不是字符串
                pass#参数错误的操作
                #print(self.msg['A00003'].format(strpath))#提醒参数错误
            #如果路径中没有路径分割符，视为路径字符串错误
            elif strpath.find('\\') < 0 and strpath.find('/') < 0:
                pass#没有路径分隔符
                #print(self.msg['A00004'].format(strpath))#提醒路径格式错误
            else:
                bln_result = True#是路径字符串
            return bln_result#返回布尔值

        def InputPath(self,stadata = "path: "):#获取路径
            pathresult = None#要返回的路径
            try:
                strpath = input(stadata)#获取输入
                if self.StrPathCheck(strpath):
                    pathresult = strpath#获取路径
            except EOFError:#末尾结束符
                pass#获取了EOF的处理
                #print(self.msg['A00002'])#提示读取到了文件结尾符
            return pathresult#返回值

        def SerchFiles(self,strabspath,filename,mode = 0):#在给定路径下查找文件，不会递归查找路径下的文件夹中的文件
            
            #参数 1.给定路径 2.要查找的文件名 3.查找方式
            #返回值 匹配到的文件名列表

            #如果 参数类型正确
            if isinstance(strabspath,str) and isinstance(filename,str) and isinstance(mode,int):
                files = os.listdir(self.StrTailCheck(strabspath,self.dir_div))#获取指定路径下文件名列表
                foundfiles = []
                if mode == 0:#模糊查找
                    for i in files:
                        if filename in i:
                            foundfiles.append(i)
                elif mode == 1:#精准查找
                    for i in files:
                        if filename == i:
                            foundfiles.append(i)
                else:#查找方式错误
                    pass#输入了错误的查找方式
                    #print(self.msg['A0005'].format(mode))
            else:#如果参数类型错误
                pass#参数类型错误的处理
                #print(self.msg['A00003'])

            return foundfiles#返回查找到的文件名的列表

        def OpenFloader(self,strpath):#接收一个路径字符串，打开相应的路径
            blnOpenedFile = False#
            if self.StrPathCheck(strpath):#检测是否是路径字符串
                #if os.path.exists(strpath)#检测路径是否存在[冗余验证]
                if self.is_linux:#如果是linux系统
                    strpath = strpath.replace('\\','/')#确保是Linux路径分隔符
                    os.system('xdg-open "%s" ' % strpath)
                    blnOpenedFile = True
                else:#如果是其他系统(默认Windows)
                    strpath = strpath.replace('/','\\')#确保是win路径分隔符
                    #print(strpath)
                    try:
                        #os.system("explorer.exe %s" % strpath)#使用cmd打开路径
                        os.startfile(strpath)#Hide CMD when open the path
                        blnOpenedFile = True
                    except FileNotFoundError:#如果没有发现相应的路径文件
                        blnOpenedFile = False
            else:
                blnOpenedFile = False
            return blnOpenedFile#返回是否打开了文件

        def ReadDicFile(self,strPath,strcoding = 'utf-8-sig',intlinelimit = 65535,strdivsign = '=',blnnew = True):#加载字典文件
            return self.__LoadDicFile(strPath,strcoding,intlinelimit,strdivsign,blnnew)#返回字典

        def WriteDicFile(self,dicdata,strfilepath,strencoding = 'utf-8-sig',strdivsign = '='):#将字典写入文件
            
            # 参数1 字典数据 参数2 文件路径 参数3 写入编码 参数4 分割符
            
            stream = ''#string to save all dictionary datas
            for i in dicdata.keys():#Iteration dictionary
                stream += ''.join([i,strdivsign,dicdata[i],'\n'])#Join Key and value with simple equal
            with open(strfilepath, 'w', encoding = strencoding) as fw: #Open dicfile
                fw.write(stream)#write in

        def ListToCsv(self,csvpath,listdata,strencoding = 'utf-8-sig'):#接收一个list数据，生成一个csv
            #参数1 输出路径 参数2 list数据 参数3 编码
            if self.StrPathCheck(csvpath):#路径检查
                stream = ''#写入CSV中的数据
                if isinstance(listdata,list):#如果接收到的是一个list
                    if len(listdata) > 0:#如果里面有数据
                        if isinstance(listdata[0],list):#如果是二维数据
                            for i in range(0,len(listdata)):#遍历行
                                for j in range(0,len(listdata[i])):#遍历列
                                    stream += str(listdata[i][j])
                                    stream += ','#加上逗号分隔符
                                stream +='\n'#读完一列加上回车
                        else:#如果是一维数据
                            for i in range(0,len(listdata)):#遍历行
                                stream += str(listdata[i])
                                stream +='\n'
                        
                #输出到CSV文件
                with open(csvpath,'w',encoding=strencoding) as fw:
                    fw.write(stream)#写入数据

        def ReadCsvToList(self,csvpath,strencoding = 'utf-8-sig',intlinelimit = 65535):#读取CSV文件生成List数据
            #参数1 读取路径 参数2 编码 参数3 读取上限
            if self.StrPathCheck(csvpath):#路径检查 

                #读取CSV文件
                lisRead = []#存储读取数据的列表
                with open(csvpath,'r',encoding=strencoding) as fr:
                    for i in range(0,intlinelimit):#获取读取上限
                        if i == intlinelimit - 1:#如果到达了读取上限
                            break#退出循环
                        lines = fr.readline()#读取一行
                        strLineValid = lines.replace('\n','')#清除换行符
                        strLineValid = strLineValid.replace('\r','')#清除回车符
                        lisRead.append(strLineValid.split(','))#将一行分割数据后存入list
                        if not lines:#到达行尾
                            break#退出循环
                return lisRead#返回读取到的数据

        def ListToXls(self,xlspath,sheetname,listdata):#接收一个list数据，生成一个csv
            #参数1 输出路径 参数2 sheet名 参数3 list数据 参4 编码
            if self.StrPathCheck(xlspath):#路径检查
                stream = ''#写入CSV中的数据
                if isinstance(listdata,list):#如果接收到的是一个list
                    if len(listdata) > 0:#如果里面有数据

                        #输出到Xls文件
                        book = xlwt.Workbook()#建立xls工作簿
                        sheet = book.add_sheet(sheetname)#添加sheet页

                        if isinstance(listdata[0],list):#如果是二维数据
                            for indexrow,i in enumerate(listdata):#遍历行
                                for indexcol, j in enumerate(i):#遍历列
                                    sheet.write(indexrow,indexcol,str(j))#写入数据
                            book.save(xlspath)#存储xls文件

                        else:#如果是一维数据
                            for index,i in enumerate(listdata):#遍历行
                                    sheet.write(index,0,str(i))#写入数据

                        #设置字体为宋体
                        font = xlwt.Font()
                        font.name = 'SimSun'

                        #存储xls文件
                        book.save(xlspath)




if __name__ == '__main__':#测试
    instest =MFR()
    print(instest.thisstrfilepath)
