#coding:utf-8

'''
    先设置一个框架，然后创建 初始化界面 ，首先先为界面画好各种框和按钮，然后对按钮进行赋值，从上而下的去设置
'''

import wx
from math import *

class CalcFrame(wx.Frame):
    def __init__(self,title):
        super(CalcFrame,self).__init__(None,title = title,size=(300,250))
        
        self.InitUI()
        
        self.Centre()
        self.Show()
    
    def InitUI(self):#设置界面
        vbox = wx.BoxSizer(wx.VERTICAL)#vertical垂直的意思。创建一个box
        self.textprint = wx.TextCtrl(self,style=wx.TE_RICH)
        self.equation = ''
        vbox.Add(self.textprint,flag=wx.EXPAND|wx.TOP|wx.BOTTOM,border=4)#添加文本输出框进去。border是指textprint框上下的间距
        
        gridBox = wx.GridSizer(5,4,5,5)#rows行数,cols列数,vgap格子之间的垂直间距,hgap格子之间的水平间距
        
        labels = ['AC','DEL','pi','CLOSE','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']
        
        for label in labels:#设置按钮内容
            buttonIterm = wx.Button(self,label=label)#为按钮赋值
            self.createHandler(buttonIterm, label)
            gridBox.Add(buttonIterm,1,wx.EXPAND)
            
        vbox.Add(gridBox,proportion=1,flag=wx.EXPAND)#添加这些按钮到框架内
        self.SetSizer(vbox)
        
        
    def OnAppend(self,event):
        eventbutton = event.GetEventObject()#获取事件对象（返回与事件相关的对象）
        label = eventbutton.GetLabel()#获取事件对象的标签
        self.equation += label#将当前的输入都放到一起
        self.textprint.SetValue(self.equation)#输出到文本输出框
    
    def OnDel(self,event):
        self.equation = self.equation[:-1]#利用切片来实现退格
        self.textprint.SetValue(self.equation)
    
    def OnAc(self,event):
        self.textprint.Clear()
        self.equation=''#重新赋值空
    
    def OnTarget(self,event):
        string = self.equation#获取现文本输出框的内容
        try:
            target = eval(string)#等于直接执行string
            self.equation = str(target)
            self.textprint.SetValue(self.equation)#输出处理后的内容
        except SyntaxError:#防止错误
            dlg = wx.MessageDialog(self,u'格式错误，请输入正确的等式。',u'请注意',wx.OK|wx.ICON_INFORMATION)
            #赋予错误信息（父类，错误内容，错误标题，事件类型）
            dlg.ShowModal()#出现弹窗
            dlg.Destroy()#关闭弹窗
            
    def OnExit(self,event):
        self.Close()#直接退出app
    
    
    def createHandler(self,button,labels):#分别赋予按钮处理方法
        item = 'DEL AC = CLOSE'
        if labels not in item:
            self.Bind(wx.EVT_BUTTON,self.OnAppend,button)#bind是将事件绑定到按钮上。bind（事件，事件处理方法，对象）
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON,self.OnDel,button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON,self.OnAc,button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON,self.OnTarget,button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON,self.OnExit,button)
    
    
        
        
if __name__ == '__main__':
    
    app = wx.App()
    CalcFrame(title = 'Calculator')
    app.MainLoop()