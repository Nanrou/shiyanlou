#coding:utf-8
import math
import wx
from abc import ABCMeta,abstractmethod
from _pyio import __metaclass__


class Point(object):
    def __init__(self,x,y):  
        self.x = x
        self.y = y
    def __sub__(self,other):#定义点的减法
        return Point(self.x-other.x,self.y-other.y) 
    def __add__(self,other):#定义点的加法
        return Point(self.x+other.x,self.y+other.y)
    
    @property
    def xy(self):#将方法作为属性返回
        return (self.x,self.y)
    
    def __str__(self):#针对用户
        return 'x={0},y={1}'.format(self.x,self.y)#format就是格式化字符的函数，用{}代替%来映射，这里的{0},{1}就是指的后面值
    def __repr__(self):#针对python
        return str(self.xy)       
        
    @staticmethod
    def dist(a,b): 
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)#sqrt是平方，就是求出点的直线距离
        
class Polygon(object):
    __metaclass__ = ABCMeta#将polygon变为抽象类
    
    def __init__(self,points_list,**kwargs):#这里要求输入点的list
        for point in points_list:#先判断传进来的参数是不是Point
            assert isinstance(point, Point),"input must be Point type."
        self.points=points_list[:]#应该是跟points_list一个意思；这里的points是属性
        self.points.append(points_list[0])#现在pionts的尾部加上了list的第一个元素        
        self.color=kwargs.get('color','#000000')
    
    def drawPoints(self): 
        points_xy=[] 
        for point in self.points:
            points_xy.append(point.xy)#point.xy将返回其自身的x和y
        #print points_xy
        return tuple(points_xy)
    
    @abstractmethod#表明一个抽象对象，用装饰器的话就是只读。不用形状的算法不同，所以用抽象函数。
    def area(self):
        raise('not implement')
    
    def __lt__(self,other): #赋予一个属性，通过面积大小比较图形
        assert isinstance(other, Polygon)
        return self.area<other.area
    
class RectAngle(Polygon):#矩阵
    def __init__(self,startPoint,w,h,**kwargs):#获取起始点，宽，高
        self._w = w
        self._h = h
        Polygon.__init__(self,[startPoint,startPoint+Point(w,0),startPoint+Point(w,h),startPoint+Point(0,h)],**kwargs)
        #传入四个点坐标的list
    def area(self):
        return self._w*self._h
    
    
class TriAngleError(Exception):
    def __init__(self):
        Exception.__init__(self)
        
        
class TriAngle(Polygon):    
    def __init__(self,point1,point2,point3,**kw):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        
        if ((self.point2.y-self.point1.y)*(self.point3.x-self.point1.x)) == ((self.point3.y-self.point1.y)*(self.point2.x-self.point1.x)):
            raise TriAngleError()
          
        Polygon.__init__(self,[point1,point2,point3],**kw)      
    
    def area(self):
        a = Point.dist(self.point1,self.point2)
        b = Point.dist(self.point1,self.point3)
        c = Point.dist(self.point2,self.point2)
        p = (a+b+c)/2.0
        return math.sqrt(math.sqrt((p*(p-a)*(p-b)*(p-c))**2))
    
class Example(wx.Frame):        
        def __init__(self,title,shapes):
            super(Example,self).__init__(None,title=title,size=(600,400))
            self.shapes = shapes
            
            self.Bind(wx.EVT_PAINT,self.OnPaint)
            
            self.Center()
            self.Show()
        
        def OnPaint(self,e):
            dc = wx.PaintDC(self)
            
            for shape in self.shapes:
                dc.SetPen(wx.Pen(shape.color))
                dc.DrawLines(shape.drawPoints())
                

class Circle(Polygon):
    def __init__(self,CenterPoint,radius,edgeNum=360,**kwargs):
        self.r = radius
        
        center = CenterPoint.xy
        self.x = center[0]
        self.y = center[1]
        
        circlepoints = []
        
        deltaRad = (2*math.pi)/edgeNum#弧度,或者说是多少边型，角数越高，越趋近圆
        
        for n in range(edgeNum):
            circlepoints.append(Point(self.x + self.r*math.cos(deltaRad*n),self.y +self.r*math.sin(deltaRad*n)))
            
        Polygon.__init__(self, circlepoints)
        
    def area(self):
        return math.pi * self.r **2
        
        
if __name__ == '__main__':
    
    prepare_draws=[]
    
    start_p = Point(50,60)
    a = RectAngle(start_p,100,80,color='#ff0000')
    b = TriAngle(Point(111,30),Point(61,155),Point(99,255))
    c = Circle(Point(200,180),100)
    prepare_draws.append(a)
    prepare_draws.append(b)
    prepare_draws.append(c)
    
    for shape in prepare_draws:
        print shape.area()
        
    app = wx.App()
    Example('Shapes',prepare_draws)
    app.MainLoop()