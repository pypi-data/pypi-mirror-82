# BoneGame

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)![Upload Python Package](https://github.com/zrr1999/PyTex/workflows/Upload%20Python%20Package/badge.svg)

本代码库若干小游戏，并利用OpenCV实现渲染，方便完成大三课程的大作业。


## 安装[![Downloads](https://pepy.tech/badge/bone-games)](https://pepy.tech/project/bone-games)

这个项目使用 [Python](https://www.python.org/downloads/) 开发，请确保你本地安装了它。

使用PyPI安装（还没传）。

```sh
$ pip install bone-games
```

本地安装。
```sh
$ pip install .
```

## 使用说明

使用时，您可以直接引入GoBang类并实例化。

```python
from bonegame import GoBang
game = GoBang()
```

你可以调用game对象的所有方法，大部分方法支持函数式编程。

```python
game.down(0, (1, 1))  # 下子
game.render()  # 显示
```

## 代码示例

如下代码可以直接运行，点击屏幕轮流进行下棋。

```python
from bonegame import GoBang
import cv2

HEIGHT, WIDTH = 640, 640
SIZE = 7
WIN_NAME = "GoBang"

game = GoBang(SIZE, HEIGHT, WIDTH)
cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WIN_NAME, game.mouse_event)  # 创建默认鼠标事件（轮流下子）
while True:
    game.render(WIN_NAME)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
```

## 开发功能

- [x] 五子棋
- [x] 多人五子棋
- [ ] 更好的多人五子棋接口
- [ ] 中国象棋
- [ ] 围棋
- [ ] 决策树
- [ ] 添加详细注释（代码文档）
- [ ] 整合贪吃蛇
- [ ] 增加OpenGL等其他渲染方式
- [ ] 使用Taichi或Torch加速计算部分

## 更新日志

- (2020.10.11) v0.1.1 
    - 将鼠标事件移入GoBang类。
- (2020.10.10) v0.1.0 
    - 实现了五子棋并提供了接口允许开发者进行扩展。

## 维护者

[@詹荣瑞](https://github.com/tczrr1999)

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/tczrr1999/bonegame/issues/new) 或者提交一个 Pull Request。

### 贡献者

感谢以下参与项目的人：

## 使用许可

禁止将本辅助库及衍生品上传到百度网盘。
[GNU](LICENSE) © Rongrui Zhan