# 动物换位（Java 课程设计）

一个用 Java Swing 实现的"动物换位"小游戏：左边 3 只兔子、右边 3 只乌龟，中间一格空位；
兔子只能向右走，乌龟只能向左走；前方为空走一格，前方有动物且隔位为空就跳过去。
把两侧动物完全换成位置即为胜利，最少需要 15 步。

## 运行环境

- JDK 8 及以上（开发时使用 JDK 26 / javac 26.0.2）
- 无任何第三方依赖，只用 JDK 自带的 Swing 与 Java2D

## 快速开始

三种方式，任选其一：

1. **双击 `动物换位.jar`** —— 免编译，最省事（前提：`.jar` 已关联到 JDK/JRE）。
2. **双击 `run.bat`** —— 自动编译 `src` 下全部源文件并启动游戏。
3. 命令行手工执行（在工程根目录）：

```bat
javac -encoding UTF-8 -d build\classes -sourcepath src src\animalgame\*.java src\animalgame\model\*.java src\animalgame\view\*.java src\animalgame\controller\*.java src\animalgame\test\*.java src\animalgame\tools\*.java
java -cp build\classes animalgame.Main
```

> 注意：批处理文件必须保存为 **GBK（ANSI）** 编码。命令解释器按系统代码页逐字节读取 `.bat`，
> 若存成 UTF-8，中文提示会被拆成非法命令，表现为"黑窗口一闪而过"或提示某段中文"不是内部或外部命令"。

运行模型层单元测试（10 个用例）：

```bat
run_tests.bat
```

## 操作说明

| 操作 | 说明 |
| --- | --- |
| 单击动物 | 若可移动则播放动画；若被挡住则该动物闪红光并给出提示 |
| 玩法说明（F1） | 弹出规则说明对话框 |
| 撤销（Ctrl+Z） | 撤销上一步，步数减一 |
| 重新开始（Ctrl+R） | 恢复初始局面并清零步数 |

## 目录结构

```
动物换位/                                   ← 全部交付物都在这一个文件夹里
├─ Java课程设计报告-动物换位.docx           课程设计报告（正文 + 附录：完整源程序）
├─ 动物换位.jar                            已编译好的可执行 jar（双击即玩）
├─ run.bat                                 一键编译并运行游戏
├─ run_tests.bat                           一键运行模型层单元测试（10 个用例）
├─ README.md                               本文件
├─ src/animalgame/                         源程序（17 个 .java，含详细中文注释）
│  ├─ Main.java                            程序入口
│  ├─ model/                               模型层：棋盘、动物、规则、移动记录（不依赖 Swing）
│  ├─ view/                                视图层：主窗口、棋盘面板、矢量绘制、按钮、配色
│  ├─ controller/                          控制层：把界面事件翻译成模型操作
│  ├─ test/GameModelTest.java              模型层单元测试（main 方法 + 断言）
│  └─ tools/PreviewTool.java               离屏渲染界面截图的小工具
├─ api/                                    javadoc 生成的 API 文档（双击 api\index.html）
├─ build/classes/                          编译输出（可由 run.bat 重新生成）
└─ docs/
   ├─ img/                                 报告里的插图（PNG 原图）
   └─ tools/                               生成插图与文档的 Python 辅助脚本（与运行无关）
```

## 三个文件夹怎么用

| 文件夹 | 用途 | 内容 |
| --- | --- | --- |
| `动物换位-只玩` | 只想玩 | 只有 `动物换位.jar`，双击即玩 |
| `动物换位-提交` | 交作业 | 报告 + jar + 源码 + API 文档 + 两个 bat（无 build、无图片素材） |
| `动物换位` | 开发用 | 上面全部，外加 `docs\img` 插图和 `docs\tools` 辅助脚本 |

## 设计要点

- **MVC 分层**：`model` 不引用任何 Swing 类，因此可以在命令行里直接测试；`view` 只负责画；
  `controller` 负责把两者粘起来。
- **规则可替换**：`MoveRule` 是接口，`StandardMoveRule` 是默认实现，换一个实现类就能扩展新玩法。
- **撤销**：`Board` 内部用 `Deque<MoveRecord>` 保存历史，撤销时把动物放回原格。
- **动画**：`BoardPanel` 用 16 ms 的 `javax.swing.Timer` 驱动，按缓动曲线插值，跳跃时叠加抛物线。
