#coding:utf-8

import wx
import os
import random
import copy

class Frame(wx.Frame):
    
    def __init__(self,title):
        super(Frame,self).__init__(None,-1,title,size=(500,600),
                                   style = wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER)
        self.colors = {0:(204,192,179),2:(238,228,218),4:(237,224,200),
                       8:(242,177,121),16:(245,149,99),32:(246,124,95),
                       64:(246,94,59),128:(237,207,114),256:(237,207,114),
                       512:(237,207,114),1024:(237,207,114),2048:(237,207,114)}
        
        self.initGame()#初始化游戏内容
        self.set_Icon()#设置图标ico
        self.set_Log()#设置那个图并将其设置为按钮
        '''
        panel = wx.Panel(self)#panel：仪表
        panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        panel.SetFocus()#?   
        '''
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)#现在是绑定这个事件到Frame 
        self.SetFocus()#激活Frame
        self.initBuffer()#初始化窗口大小
        self.Bind(wx.EVT_SIZE,self.onSize)#为改变尺寸这个事件，绑定方法
        self.Bind(wx.EVT_PAINT,self.onPaint)#这个事件是绘图重绘
        self.Bind(wx.EVT_CLOSE,self.onClose)#赋予关闭事件方法
        self.SetClientSize((505,680))#设置整个frame的大小
        self.Centre()#居中
        self.Show()
        
    def onPaint(self,event):
        dc = wx.BufferedPaintDC(self,self.buffer)#BufferedDC的子类，缓存指令来用于画图
        
    def onClose(self,event):
        self.saveScore()
        self.Destroy()#关闭了
        
    def set_Log(self):
        panel_log = wx.Panel(self)
        log = wx.Image('cat.ico',wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button = wx.BitmapButton(panel_log,-1,log,pos=(10,10))
        self.Bind(wx.EVT_BUTTON,self.doMe,self.button)
        self.button.SetDefault()
        #__w = log.GetWidth()
        #__h = log.Height()
        panel_log.SetSize((150,150))
        self.Fit()
        #self.Center()
        self.Show()
    def doMe(self,event):
        if self.flag_fb:
            self.drawChange(-self.score_fb,Flashback=True)
            self.data = copy.deepcopy(self.oldData)
            self.SetFocus()
            self.flag_fb=False
        else:
            wx.MessageBox(u'只能悔一步喔~~',u'咔咔~',wx.ICON_INFORMATION) 
            self.SetFocus()
        
    def set_Icon(self):
        icon = wx.Icon('cat.ico',wx.BITMAP_TYPE_ICO)#加载图标
        self.SetIcon(icon)#设置图标
     
    def loadScore(self):
        if os.path.exists('bestscore.ini'):
            with open('bestscore.ini','r') as ff:
                self.bestScore = ff.read()
    
    def saveScore(self):
        with open('bestscore.ini','w') as ff:
            ff.write(str(self.bestScore))
            
        
    def initGame(self):#初始化游戏
        self.bgFont = wx.Font(50,wx.SWISS,wx.NORMAL,wx.BOLD,face = u'Roboto')#设置字体
        self.scFont = wx.Font(36,wx.SWISS,wx.NORMAL,wx.BOLD,face = u'Roboto')
        self.smFont = wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,face = u'Roboto')
        self.curScore = 0
        self.bestScore = 0
        self.score_fb = 0
        self.loadScore()#读取数据
        self.data = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]#设置初始值
        self.oldData = self.data
        self.flag_fb = False
        count = 0
        while count<2:#设置最开始的那两个数
            row = random.randint(0,len(self.data)-1)
            col = random.randint(0,len(self.data[0])-1)
            if self.data[row][col]!=0:continue#重新跳到循环的开头，就是万一第二个数位置跟第一个一样，就重新选择第二个数的位置
            self.data[row][col] =2 if random.randint(0,3) else 4
            count +=1
    
    def initBuffer(self):
        w,h = self.GetClientSize()#获取可能需要的客户端大小
        self.buffer = wx.EmptyBitmap(w,h)#应该是创建一个空的位图
        
    def onSize(self,event):
        self.initBuffer()#重新找到大小
        self.drawAll()#重新画全部
        
    def putTile(self,Flashback=False):#在空的位置产生新的数，并返回一个bool
        available = []
        if Flashback:self.data = self.oldData
        for row in range(len(self.data)):#遍历行数
            for col in range(len(self.data[0])):#遍历列数
                if self.data[row][col] == 0:available.append((row,col))#找到仍未赋值的坐标放到available里面
        if available:#若存在空的位置
            row,col = available[random.randint(0,len(available)-1)]#在其中随机找到一个坐标
            self.data[row][col] = 2 if random.randint(0,2) else 4#赋值2或4
            return True#返回一个真值
        return False
    
    def update(self,vlist,direct):#接收传入的非空值的坐标列表，和bool值(为什么要判断这个bool）
        
        score = 0
        if direct:#向上或者向左，都是前一个
            i = 1
            while i<len(vlist):
                if vlist[i-1] == vlist[i]:#若相邻两个元素相等
                    del vlist[i] #则消去一个(后者)；这里会令len(vlist)-1
                    vlist[i-1] *=2#前者*2作为得分
                    score += vlist[i-1]#加分数
                    i += 1#因为这次操作是比较了两个，所以要跳一位
                i += 1#循环加位
        else:#为什么要用else，算法应该是一样的，需要尝试取消这部分，尝试direct=True
            i = len(vlist)-1
            while i>0:
                if vlist[i-1] == vlist[i]:
                    del vlist[i]
                    vlist[i-1] *=2
                    score += vlist[i-1]                        
                    i -= 1
                i -= 1
        return score

    def slideUpDown(self,up):#通过bool来判断上下移动
        score = 0
        numCols = len(self.data[0])
        numRows = len(self.data)
        oldData = copy.deepcopy(self.data)#deepcopy是直接复制，产生一个新的。只是等号的话，是引用。
        
        for col in range(numCols):#遍历列数，一个循环只搞一列
            cvl = [self.data[row][col] for row in range(numRows) if self.data[row][col]!=0]
            #遍历行数，在这列的4个数中找到非0值放到cvl这个list里面
            #因为有个靠边的操作，比如1列位置[0,1,2,3]对应的值为[0,2,0,2],则cvl中的值为[2,2],则len(cvl)=2
            if len(cvl)>=2:#这个值应该大于2.（因为一列只有4个数，有两个就可以判断是否相邻且相等）
                score += self.update(cvl,up)#将cvl这个list和bool传给update
                #cvl经过update已经被改变了，现在cvl的值是[4,]
            for i in range(numRows - len(cvl)):#若4个格都有数，则不执行这补0循环
                if up : cvl.append(0)#然后如果向上操作,则在cvl后面补入0
                else: cvl.insert(0,0)
            for row in range(numRows):self.data[row][col] = cvl[row]#重新赋值,将[4,]变成[4,0,0,0]
        return oldData !=self.data,score#换回一个bool值,当oldData不等于data时为真，则当该列4个都有数时为假(4个数都没变);和返回得分
        #经过update会将重复项消掉(或将0移位)
        
    def slideLeftRight(self,left):
        score = 0
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)
        
        for row in range(numRows):
            rvl = [self.data[row][col] for col in range(numCols) if self.data[row][col]!=0]
            
            if len(rvl)>=2:
                score += self.update(rvl,left)
            for i in range(numCols - len(rvl)):
                if left : rvl.append(0)
                else: rvl.insert(0,0)
            for col in range(numCols):self.data[row][col] = rvl[col]
        return oldData !=self.data,score
    
    def isGameOver(self):#判断是否结束游戏。
        #！！！！这个判断是有问题的，当满格数字的时候就直接判断为gameover了！！！！
        copyData = copy.deepcopy(self.data)#先备份data，因为下面判断执行会把data打乱
        
        flag = False
        if not self.slideLeftRight(True)[0] and not self.slideLeftRight(False)[0] and \
                not self.slideUpDown(True)[0] and not self.slideUpDown(False)[0]:
            #对四个方向进行操作，若
            #这个[0]是指函数返回的第一个值。retrun返回的是一个tuple
            flag = True
        if not flag: self.data = copyData#若能移动则会打乱data，所以需要重新赋值。
        return flag
    
    def doMove(self,move,score):#接收一个bool和score
        if move:
            self.flag_fb = True
            self.score_fb = score
            self.putTile()
            self.drawChange(score)
            #if not self.putTile():#先进行是否存在空位置的判断
            if self.isGameOver():#再判断是否能移动
                if wx.MessageBox(u'游戏结束，是否重新开始？',u'哈哈~',wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                    bestScore = self.bestScore
                    self.initGame()
                    self.bestScore = bestScore
                    self.drawAll()
                    self.SetFocus() 
                else:
                    self.saveScore()
                    self.Destroy()
                
                    
    def onKeyDown(self,event):#响应EVT_KEY_DOWN事件的方法
        
        keyCode = event.GetKeyCode()#获取按键的编码
        self.oldData = copy.deepcopy(self.data)
        
        if keyCode == wx.WXK_UP:#87:
            self.doMove(*self.slideUpDown(True))#需要用*来表示接收的tuple
        elif keyCode == wx.WXK_DOWN:#83:
            self.doMove(*self.slideUpDown(False))
        elif keyCode == wx.WXK_LEFT:#65:
            self.doMove(*self.slideLeftRight(True))
        elif keyCode == wx.WXK_RIGHT:#68:
            self.doMove(*self.slideLeftRight(False))
        elif keyCode == 82:
            if wx.MessageBox(u'确认重来？',u'哈哈~',wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                self.initGame()
                self.drawAll()
                self.SetFocus()
        elif keyCode == wx.WXK_ESCAPE:
            if wx.MessageBox(u'确认退出？',u'嘻嘻~',wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                self.onClose(event)
         
    def drawBg(self,dc):#画背景
        dc.SetBackground(wx.Brush((250,248,239)))
        dc.Clear()
        dc.SetBackground(wx.Brush((187,173,160)))
        dc.SetPen(wx.Pen((187,173,160)))
        dc.DrawRoundedRectangle(15,150,475,475,5)
        
    def drawTips(self,dc):#画出那些字
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119,110,101))
        dc.DrawText(u'合并相同数字，得到2048吧！',165,114)
        dc.DrawText(u'怎么玩：\n用方向箭头来移动方块。\
                    \n当两个相同数字的方块碰到一起时，会合成一个！',15,630)
        
    def drawScore(self,dc):
        dc.SetFont(self.smFont)
        scoreLabelSize = dc.GetTextExtent(u'SCORE')
        bestLabelSize = dc.GetTextExtent(u'BEST')
        curScoreBoardMinW = 15*2+scoreLabelSize[0]
        bestScoreBoardMinW = 15*2+bestLabelSize[0]
        curScoreSize = dc.GetTextExtent(str(self.curScore))
        bestScoreSize = dc.GetTextExtent(str(self.bestScore))
        curScoreBoardNedW = 10+curScoreSize[0]
        bestScoreBoardNedw = 10+bestLabelSize[0]
        curScoreBoardW = max(curScoreBoardMinW,curScoreBoardNedW)
        bestScoreBoardW = max(bestScoreBoardMinW,bestScoreBoardNedw)
        dc.SetBrush(wx.Brush((187,173,160)))
        dc.SetPen(wx.Pen((187,173,160)))
        dc.DrawRoundedRectangle(505-15-bestScoreBoardW,40,bestScoreBoardW,50,3)
        dc.DrawRoundedRectangle(505-15-bestScoreBoardW-5-curScoreBoardW,40,curScoreBoardW,50,3)
        dc.SetTextForeground((238,228,218))
        dc.DrawText(u'BEST',505-15-bestScoreBoardW+(bestScoreBoardW-bestLabelSize[0])/2,48)
        dc.DrawText(u'SCORE',505-15-bestScoreBoardW-5-curScoreBoardW+(curScoreBoardW-scoreLabelSize[0])/2,48)
        dc.SetTextForeground((255,255,255))
        dc.DrawText(str(self.bestScore),505-15-bestScoreBoardW+(bestScoreBoardW-bestScoreSize[0])/2,68)
        dc.DrawText(str(self.curScore),505-15-bestScoreBoardW-5-curScoreBoardW+(curScoreBoardW-curScoreSize[0])/2,68)
        
    def drawTiles(self,dc,Flashback=False):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col] if not Flashback else self.oldData[row][col]
                color = self.colors[value]
                if value == 2 or value == 4:
                    dc.SetTextForeground((119,110,101))
                else:
                    dc.SetTextForeground((255,255,255))
                dc.SetBrush(wx.Brush(color))
                dc.SetPen(wx.Pen(color))
                dc.DrawRoundedRectangle(30+col*115,165+row*115,100,100,2)
                size = dc.GetTextExtent(str(value))
                while size[0]>100-15*2:
                    self.scFont = wx.Font(self.scFont.GetPointSize()*4/5,wx.SWISS,wx.NORMAL,wx.BOLD,face=u'Roboto')
                    dc.SetFont(self.scFont)
                    size = dc.GetTextExtent(str(value))
                if value != 0 :dc.DrawText(str(value),30+col*115+(100-size[0])/2,165+row*115+(100-size[1])/2)

    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
        self.drawBg(dc)
        self.drawTips(dc)
        self.drawScore(dc)
        self.drawTiles(dc)
        
    def drawChange(self,score,Flashback=False):
        dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
        
        if abs(score):
            self.curScore += score
            if int(self.curScore)>int(self.bestScore):#定义int
                self.bestScore = self.curScore
            self.drawScore(dc)
        self.drawTiles(dc,Flashback)
        
        
        
if __name__ == '__main__':
    app = wx.App()
    Frame(u'2048 v1.0.1 by Nanrou')
    app.MainLoop()