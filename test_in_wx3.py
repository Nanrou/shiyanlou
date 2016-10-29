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
        
        #self.set_Icon()#?
        self.initGame()#未定义
        
        panel = wx.Panel(self,-1)#panel：仪表
        panel.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)#
        panel.SetFocus()#?     
                        
        self.initBuffer()#未定义
        self.Bind(wx.EVT_SIZE,self.onSize)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_CLOSE,self.onClose)
        self.SetClientSize((505,680))
        self.Centre()
        self.Show(True)
        
    def onPaint(self,event):
        dc = wx.BufferedPaintDC(self,self.buffer)
        
    def onClose(self,event):
        self.saveScore()
        self.Destroy()
    '''    
    def set_Icon(self):
        icon = wx.Icon('icon.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
    '''    
    def loadScore(self):
        if os.path.exists('bestscore.ini'):
            ff = open('bestscore.ini')#可以搭配with
            self.bstScore = ff.read()
            ff.close()
        
    def saveScore(self):
        ff = open('bestscore.ini','w')
        ff.write(str(self.bestScore))
        ff.close()
        
    def initGame(self):
        self.bgFont = wx.Font(50,wx.SWISS,wx.NORMAL,wx.BOLD,face = u'Roboto')
        self.scFont = wx.Font(36,wx.SWISS,wx.NORMAL,wx.BOLD,face = u'Roboto')
        self.smFont = wx.Font(12,wx.SWISS,wx.NORMAL,wx.NORMAL,face = u'Roboto')
        self.curScore = 0
        self.bestScore = 0
        self.loadScore()
        self.data = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        count = 0
        while count<2:
            row = random.randint(0,len(self.data)-1)
            col = random.randint(0,len(self.data[0])-1)
            if self.data[row][col]!=0:continue#?
            self.data[row][col] =2 if random.randint(0,1) else 4#设置最开始的那两个数
            count +=1
    
    def initBuffer(self):
        w,h = self.GetClientSize()#?
        self.buffer = wx.EmptyBitmap(w,h)
        
    def onSize(self,event):
        self.initBuffer()
        self.drawAll()
        
    def putTile(self):
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:available.append((row,col))
        if available:
            row,col = available[random.randint(0,len(available)-1)]
            self.data[row][col] = 2 if random.randint(0,1) else 4
            return True
        return False
    
    def update(self,vlist,direct):
        score = 0
        if direct:
            i = 1
            while i<len(vlist):
                if vlist[i-1] == vlist[i]:
                    del vlist[i]
                    vlist[i-1] *=2
                    score += vlist[i-1]
                    i += 1
                i += 1
        else:
            i = len(vlist)-1
            while i>0:
                if vlist[i-1] == vlist[i]:
                    del vlist[i]
                    vlist[i-1] *=2
                    score += vlist[i-1]                        
                    i -= 1
                i -= 1
        return score

    def slideUpDown(self,up):
        score = 0
        numCols = len(self.data[0])
        numRows = len(self.data)
        oldData = copy.deepcopy(self.data)
        
        for col in range(numCols):
            cvl = [self.data[row][col] for row in range(numRows) if self.data[row][col]!=0]
            
            if len(cvl)>=2:
                score += self.update(cvl,up)
            for i in range(numRows - len(cvl)):
                if up : cvl.append(0)
                else: cvl.insert(0,0)
            for row in range(numRows):self.data[row][col] = cvl[row]
        return oldData !=self.data,score
            
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
    
    def isGameOver(self):
        copyData = copy.deepcopy(self.data)
        
        flag = False
        if not self.slideLeftRight(True)[0] and not self.slideLeftRight(False)[0] and \
            not self.slideLeftRight(True)[0] and not self.slideLeftRight(False)[0]:
            flag = True
        if not flag: self.data = copyData
        return flag
    
    def doMove(self,move,score):
        if move:
            self.putTile()
            self.drawChange(score)
            if self.isGameOver():
                if wx.MessageBox(u'游戏结束，是否重新开始？',u'哈哈~',wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                    bestScore = self.bestScore
                    self.initGame()
                    self.bestScore = bestScore
                    self.drawAll()
                    
    def onKeyDown(self,event):
        
        keyCode = event.GetKeyCode()
        
        if keyCode == 87:#wx.WXK_UP:
            self.doMove(*self.slideUpDown(True))
        elif keyCode == 83:#wx.WXK_DOWN:
            self.doMove(*self.slideUpDown(False))
        elif keyCode == 65:#wx.WXK_LEFT:
            self.doMove(*self.slideLeftRight(True))
        elif keyCode == 68:#wx.WXK_RIGHT:
            self.doMove(*self.slideLeftRight(False))
        elif keyCode == wx.WXK_ESCAPE:
            self.onClose(event)
            
    def drawBg(self,dc):
        dc.SetBackground(wx.Brush((250,248,239)))
        dc.Clear()
        dc.SetBackground(wx.Brush((187,173,160)))
        dc.SetPen(wx.Pen((187,173,160)))
        dc.DrawRoundedRectangle(15,150,475,475,5)
        
    def drawLogo(self,dc):
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119,110,101))
        dc.DrawText(u'合并相同数字，得到2048吧！',15,114)
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
        
    def drawTiles(self,dc):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
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
        self.drawLogo(dc)
        self.drawLogo(dc)
        self.drawScore(dc)
        self.drawTiles(dc)
        
    def drawChange(self,score):
        dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
        if score:
            self.curScore += score
            if self.curScore > self.bestScore:
                self.bestScore = self.curScore
            self.drawScore(dc)
        self.drawTiles(dc)
        
        
        
if __name__ == '__main__':
    app = wx.App()
    Frame(u'2048 v1.0.1 by Nanrou')
    app.MainLoop()