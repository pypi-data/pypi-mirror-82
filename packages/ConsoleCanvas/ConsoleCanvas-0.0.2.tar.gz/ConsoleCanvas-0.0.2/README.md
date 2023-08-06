
# ConsoleCanvas用法：
1.先初始化对象：

```python
A=consoleCanvas()
```
2.生成画布：
```python
A.ProduceCanvas(80,80)#创建画布
```
3.绘制像素点：
```python
A.reviseCanvas([x,y],1)
#[x,y]是坐标，1是代表绘制黑色点，0是绘制白色点
```
4.显示画布：
```python
A.show() #显示画布
```
5.清空画布：
```python
A.ProduceCanvas(80,80)#也就是重新创建画布
```