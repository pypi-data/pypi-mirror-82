
# ConsoleCanvas用法：

### 0.安装
```shell
pip install ConsoleCanvas -i https://pypi.python.org/simple
```
### 0.1.终端显示cv2的img：
```python
import consoleCanvas,cv2
img=cv2.imread("C:\\Users\\Administrator\\Desktop\\1.png")
consoleCanvas.cvShow(img)
```

### 1.先初始化对象：

```python
import consoleCanvas
A=consoleCanvas.consoleCanvas()
```
### 2.生成画布：
```python
A.ProduceCanvas(80,80)#创建画布
```
### 3.绘制像素点：
```python
A.reviseCanvas([x,y],1)
#[x,y]是坐标，1是代表绘制黑色点，0是绘制白色点
```
### 4.显示画布：
```python
A.show() #显示画布
```
### 5.清空画布：
```python
A.ProduceCanvas(80,80)#也就是重新创建画布
```
### 6.例子
```python

#绘制圆形
import consoleCanvas
a=10
b=10
r=10
A=consoleCanvas.consoleCanvas()#初始化
A.ProduceCanvas(21,21)#创建画布
A.reviseCanvas([0,0],1)
for x in range(a-r,a+r):
    y=int((((r**2)-(x-a)**2)**(1/2))+b)
    A.reviseCanvas([x,y],1)#绘制画布像素
for x in range(a+r,a-r,-1):
    y=int(-1*(((r**2)-(x-a)**2)**(1/2))+b)
    A.reviseCanvas([x,y],1)#绘制画布像素
A.show() #显示画布

```
输出:
```shell
⠁⠀⠔⠀⠀⠁⠀⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠠⠃⠀⠀⠀⠀⠀⠀⠈⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠇⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠇⠀⠀⠀⠀⠀⠀⠀⠀⠨⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠇⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠆⠀⠀⠀⠀⠀⠀⠠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠑⠀⠀⠄⠀⠂⠁⠀
```