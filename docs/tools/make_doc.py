# -*- coding: utf-8 -*-
"""生成《Java 程序设计课程设计说明书》.docx（动物换位）。"""
import os

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = r"C:\Users\mjqqd\Documents\deepseek-harness\default-workspace\动物换位"
IMG = os.path.join(ROOT, "docs", "img")
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "Java程序设计课程设计说明书-动物换位.docx")

BLACK = RGBColor(0, 0, 0)
GRAY = RGBColor(0x44, 0x4A, 0x55)

doc = Document()

# ---------------------------------------------------------------- 页面与样式
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(2.54)
sec.different_first_page_header_footer = True


def set_font(run, ascii_font="Times New Roman", ea="宋体", size=12, bold=False, color=BLACK):
    run.font.name = ascii_font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), ea)


for name, size, before, after in [("Heading 1", 16, 20, 12),
                                  ("Heading 2", 14, 14, 8),
                                  ("Heading 3", 12, 10, 6)]:
    style = doc.styles[name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = BLACK
    style.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "黑体")
    pf = style.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.5
    pf.keep_with_next = True

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "宋体")


def h1(text):
    p = doc.add_heading(text, level=1)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        set_font(r, ea="黑体", size=16, bold=True)
    return p


def h2(text):
    p = doc.add_heading(text, level=2)
    for r in p.runs:
        set_font(r, ea="黑体", size=14, bold=True)
    return p


def h3(text):
    p = doc.add_heading(text, level=3)
    for r in p.runs:
        set_font(r, ea="黑体", size=12, bold=True)
    return p


def body(text, indent=True, size=12, after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, color=BLACK):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(after)
    pf.first_line_indent = Pt(size * 2) if indent else Pt(0)
    p.alignment = align
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=color)
    return p


def bullet(text, size=12):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(3)
    pf.left_indent = Cm(0.9)
    pf.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("· " + text)
    set_font(r, size=size)
    return p


def code(text, size=8.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.5)
    pf.right_indent = Cm(0.3)
    pf.space_before = Pt(4)
    pf.space_after = Pt(8)
    pf.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ppr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "F4F6F8")
    ppr.append(shd)
    pbdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:" + side)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "4")
        el.set(qn("w:color"), "D5DBE3")
        pbdr.append(el)
    ppr.append(pbdr)
    lines = text.replace("\t", "    ").split("\n")
    for i, line in enumerate(lines):
        r = p.add_run(line)
        set_font(r, "Consolas", "宋体", size)
        if i < len(lines) - 1:
            r.add_break(WD_BREAK.LINE)
    return p


def caption(text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(10)
    pf.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_font(r, size=10.5, color=GRAY)
    return p


def figure(name, width_cm, cap):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(IMG, name), width=Cm(width_cm))
    caption(cap)


def table(headers, rows, widths, cap=None, size=10.5, aligns=None):
    if cap:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(8)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(cap)
        set_font(r, size=10.5, color=GRAY)

    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    def fill(cell, text, bold=False, center=True, bg=None):
        cell.text = ""
        para = cell.paragraphs[0]
        para.paragraph_format.space_before = Pt(2)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.line_spacing = 1.15
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        run = para.add_run(text)
        set_font(run, size=size, bold=bold)
        if bg:
            tcpr = cell._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:fill"), bg)
            tcpr.append(shd)

    for i, text in enumerate(headers):
        fill(t.rows[0].cells[i], text, bold=True, bg="DCE6F3")
    for row in rows:
        cells = t.add_row().cells
        for i, text in enumerate(row):
            center = True if aligns is None else aligns[i]
            fill(cells[i], text, center=center)
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    # 让 tblGrid 与列宽一致，Word 才会按指定宽度渲染
    cols = t._tbl.tblGrid.findall(qn("w:gridCol"))
    for i, gc in enumerate(cols):
        gc.set(qn("w:w"), str(int(widths[i] / 2.54 * 1440)))
    tblw = t._tbl.tblPr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        t._tbl.tblPr.append(tblw)
    tblw.set(qn("w:type"), "dxa")
    tblw.set(qn("w:w"), str(int(sum(widths) / 2.54 * 1440)))
    # 表头跨页重复
    trpr = t.rows[0]._tr.get_or_add_trPr()
    tblheader = OxmlElement("w:tblHeader")
    tblheader.set(qn("w:val"), "true")
    trpr.append(tblheader)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def page_break():
    doc.add_page_break()


def add_field(paragraph, instr, placeholder=""):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text_el = OxmlElement("w:t")
    text_el.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr_el)
    run._r.append(sep)
    run._r.append(text_el)
    run._r.append(end)
    set_font(run, size=10.5)


def extract(path, sig):
    """从源文件中截取一个方法（含 javadoc 注释）。"""
    with open(path, encoding="utf-8") as fp:
        lines = fp.read().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(sig):
            start = i
            break
    if start is None:
        raise SystemExit("not found: %s in %s" % (sig, path))
    s = start
    while s - 1 >= 0:
        prev = lines[s - 1].strip()
        if (prev == "" or prev.startswith("@") or prev.startswith("*")
                or prev.startswith("/**") or prev.endswith("*/")):
            s -= 1
        else:
            break
    while s < start and lines[s].strip() == "":
        s += 1
    depth = 0
    started = False
    end = start
    for k in range(start, len(lines)):
        depth += lines[k].count("{") - lines[k].count("}")
        if "{" in lines[k]:
            started = True
        if started and depth == 0:
            end = k
            break
    return "\n".join(lines[s:end + 1])


# ---------------------------------------------------------------- 页脚页码
footer = doc.sections[0].footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_field(fp, " PAGE ", "1")

# ================================================================ 封面
for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Java 程序设计课程设计说明书")
set_font(r, ea="黑体", size=28, bold=True)

for _ in range(2):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("动物换位游戏的设计与实现")
set_font(r, ea="黑体", size=22, bold=True)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("（Animal Swap Game）")
set_font(r, size=14, color=GRAY)

for _ in range(4):
    doc.add_paragraph()

info = [("学    院", "计算机科学与技术学院"),
        ("专业班级", "计算机科学与技术　　　　班"),
        ("学    号", "　　　　　　　　　　"),
        ("姓    名", "　　　　　　　　　　"),
        ("指导教师", "　　　　　　　　　　")]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in info:
    cells = t.add_row().cells
    cells[0].width = Cm(3.6)
    cells[1].width = Cm(7.4)
    p0 = cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p0.paragraph_format.space_after = Pt(10)
    r0 = p0.add_run(k + "：")
    set_font(r0, ea="黑体", size=14)
    p1 = cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.space_after = Pt(10)
    r1 = p1.add_run(v)
    set_font(r1, size=14)
    # 下划线
    r1.font.underline = True

t.autofit = False
t.columns[0].width = Cm(3.4)
t.columns[1].width = Cm(7.6)

for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("2025 年 11 月")
set_font(r, size=14)

page_break()

# ================================================================ 摘要
h1("摘　要")
body("本课程设计使用 Java 语言和 Swing 图形界面库，实现了一个“动物换位”小游戏。"
     "程序采用 MVC 分层结构：模型层 Board 负责格子状态、移动合法性判定、撤销栈与胜负判定，"
     "不引用任何界面类，因此可以在命令行下直接测试；视图层使用 Java2D 矢量绘制兔子与乌龟，"
     "并用 16 ms 的定时器驱动移动动画；控制层 GameController 把鼠标点击和按钮事件翻译成模型操作，"
     "再把结果写回界面。设计过程中对移动规则做了形式化描述，推导出 3 对 3 局面最少需要 15 步才能完成换位，"
     "并用广度优先搜索枚举全部可达局面验证了该结论。程序提供撤销、重新开始、玩法说明与快捷键，"
     "配有 10 个模型层测试用例与完整的 javadoc API 文档。")
body("关键词：Java；Swing；MVC 分层；动物换位；广度优先搜索", indent=False, bold=True)

page_break()

# ================================================================ 目录
h1("目　录")
toc_p = doc.add_paragraph()
toc_p.paragraph_format.line_spacing = 1.5
add_field(toc_p, ' TOC \\o "1-3" \\h \\z \\u ',
          "（请在此处单击鼠标右键，选择“更新域”生成带页码的目录）")

body("说明：目录由 Word 域自动生成。打开文档后若未显示页码，请全选（Ctrl+A）后按 F9，"
     "或在目录上单击右键选择“更新域”。", indent=False, size=10.5, color=GRAY)
page_break()


# ================================================================ 第 1 章
h1("1　概述")

h2("1.1　设计任务")
body("本课程设计的题目是“动物换位”。任务书要求设计一个图形界面程序，把排成一行的两组动物按规则互换位置，"
     "具体要求如下：")
bullet("有一条水平线，上面共有 7 个位置；左端 3 个位置放同一种动物，右端 3 个位置放另一种动物，正中间留一个空位；")
bullet("左边的动物只能向右移动，右边的动物只能向左移动；")
bullet("用鼠标单击动物，如果它前方相邻的位置为空，就向前走一格；")
bullet("如果前方相邻的位置上有动物，而再前面一个位置为空，就越过这只动物跳到那个空位上；")
bullet("其他情况下（前方越界、或前方和隔位都被占）不能移动；")
bullet("提供“撤销”和“重新开始”两个功能，撤销可以退回上一步，重新开始恢复到初始局面；")
bullet("当左右两组动物完全交换位置时，游戏结束。")
body("在满足任务书要求的前提下，本设计还增加了移动动画、可落点提示、步数统计、玩法说明对话框与快捷键，"
     "并把“跳跃规则”抽象成接口，方便以后扩展出新的玩法。")

h2("1.2　开发环境")
table(["项目", "内容"],
      [["操作系统", "Windows 11（程序本身跨平台，在 Linux、macOS 上同样可以运行）"],
       ["开发语言", "Java，使用 JDK 25 编译（javac 26.0.2），源代码兼容 JDK 8 及以上版本"],
       ["图形界面", "Swing（JFrame、JPanel、JButton）与 Java2D（Graphics2D 矢量绘图）"],
       ["开发工具", "命令行 javac / java，源文件为 UTF-8 编码的纯文本，可直接用 IntelliJ IDEA 或 Eclipse 打开"],
       ["第三方库", "无。全部功能只依赖 JDK 标准库，不需要额外下载 jar 包"],
       ["文档工具", "javadoc 生成 API 文档；python-docx 排版本说明书"],
       ["测试方式", "模型层用带断言的 main 方法测试；界面用手工操作与离屏截图核对"]],
      [3.2, 13.4], cap="表 1-1　开发环境", aligns=[True, False])

h2("1.3　交付成果")
table(["序号", "成果", "说明"],
      [["1", "课程设计说明书", "即本文档，含需求分析、概要设计、详细设计、测试与总结"],
       ["2", "完整源程序", "src 目录下 17 个 Java 源文件，全部带中文注释，可直接编译运行"],
       ["3", "API 文档", "api 目录下的 javadoc 网页，打开 index.html 即可浏览"],
       ["4", "可执行工程", "动物换位.jar 双击即玩；run.bat 一键编译运行；run_tests.bat 跑模型层测试"]],
      [1.6, 4.2, 10.8], cap="表 1-2　交付成果", aligns=[True, False, False])

# ================================================================ 第 2 章
h1("2　需求分析")

h2("2.1　游戏规则的形式化描述")
body("为了让“能不能走”这件事可以被程序精确判断，先把规则写成数学形式。用 0～6 表示 7 个位置，"
     "用 slots[i] 记录第 i 个位置上的动物，空位记为 null。每只动物都有一个固定的方向 dir："
     "左侧的兔子 dir = +1（向右），右侧的乌龟 dir = -1（向左）。")
body("设某只动物当前位于位置 p，令 ahead = p + dir，beyond = p + 2×dir，则它的移动规则可以归纳为四条：")
bullet("R1（越界）：ahead 不在 0～6 之内，不能移动；")
bullet("R2（走一格）：ahead 在界内且 slots[ahead] 为空，移动到 ahead；")
bullet("R3（跳一格）：ahead 在界内且 slots[ahead] 有动物，同时 beyond 在界内且 slots[beyond] 为空，移动到 beyond；")
bullet("R4（被挡住）：其余情况不能移动。")
body("胜利条件：所有兔子所在位置 p ≥ 4，且所有乌龟所在位置 p ≤ 2。由于动物的数量固定、格子数固定，"
     "这个条件等价于“左右两组动物完全互换”。")
body("最少步数：这是一个经典的“青蛙过河”问题。因为动物之间不能互相穿越（同一方向的两只动物先后次序永远不变），"
     "所以每一对“左兽—右兽”最终都必须互相越过一次，n 对动物共需要 n² 次跳跃；此外每只动物至少还要走一步，"
     "共 2n 步。两者相加得到最少步数 f(n) = n² + 2n = n(n+2)。当 n = 3 时 f(3) = 15，"
     "即 3 对 3 的局面最少需要 15 步。")

h2("2.2　功能需求")
table(["编号", "功能", "需求说明"],
      [["FR1", "显示棋盘", "窗口中央显示 7 个格子，左右各 3 只动物，中间 1 个空位，动物要能分辨种类与朝向"],
       ["FR2", "点击移动", "单击动物时按 R1～R4 判定：能走则移动一格，能跳则跳一格"],
       ["FR3", "非法提示", "不能移动时给出可见反馈（动物闪红 + 状态栏文字），不能静默失败"],
       ["FR4", "撤销", "撤销最近一步，动物回到原位置，步数减一；没有可撤销步骤时按钮变灰"],
       ["FR5", "重新开始", "恢复初始局面，清空历史，步数归零"],
       ["FR6", "步数统计", "实时显示已走步数与理论最少步数 15"],
       ["FR7", "胜利判定", "换位完成后弹出对话框，显示本局用了多少步"],
       ["FR8", "玩法说明", "提供规则说明对话框，并支持 Ctrl+Z、Ctrl+R 快捷键"]],
      [1.5, 3.0, 12.1], cap="表 2-1　功能需求", aligns=[True, True, False])

h2("2.3　非功能需求")
table(["属性", "要求与实现思路"],
      [["可维护性", "按 MVC 分为 model、view、controller 三个包，界面改版不影响规则代码"],
       ["可测试性", "模型层不 import 任何 Swing 类，可以脱离界面在命令行中直接测试"],
       ["可扩展性", "移动规则抽象为 MoveRule 接口，换一个实现类即可支持新玩法（如一次跳两格）"],
       ["易用性", "鼠标悬停高亮可落点、移动有动画、非法操作有反馈、按钮有悬停效果、支持快捷键"],
       ["健壮性", "对空引用、越界下标、重复点击、动画期间点击都做了防护，不抛异常"],
       ["性能", "单次判定为常数时间 O(1)，动画由 16 ms 定时器驱动，占用资源很少"]],
      [3.0, 13.6], cap="表 2-2　非功能需求", aligns=[True, False])

# ================================================================ 第 3 章
h1("3　概要设计")

h2("3.1　总体结构与分层思想")
body("程序采用经典的 MVC（Model-View-Controller）三层结构，三个包之间是单向依赖：view 与 controller 依赖 model，"
     "model 不依赖任何界面代码；controller 同时持有 model 与 view 的引用，充当两者之间的桥梁。")
bullet("模型层 model：Animal、LeftAnimal、RightAnimal、Direction、MoveRule、StandardMoveRule、MoveRecord、Board。"
       "它只关心“状态是什么、这一步合不合法”，完全不知道界面长什么样。")
bullet("视图层 view：GameFrame、BoardPanel、AnimalRenderer、RoundButton、Theme。"
       "它负责把模型里的数组画成格子与动物，并把鼠标坐标换算成格子下标，不包含任何规则判断。")
bullet("控制层 controller：GameController。它监听棋盘点击与按钮动作，调用模型完成操作，再把结果写回视图。")
body("这样分层带来两个直接好处：一是规则可以在命令行下用断言测试，不必启动窗口；"
     "二是将来把 Swing 换成 JavaFX，只需要重写 view 包，model 与 controller 的逻辑几乎不用改。", indent=True)

h2("3.2　模块划分")
table(["包", "主要类", "职责"],
      [["animalgame", "Main", "程序入口：设置系统外观，创建模型、窗口与控制器"],
       ["animalgame.model", "Board", "棋盘状态、落点判定、撤销栈、胜负判定"],
       ["animalgame.model", "Animal 及其子类", "动物的位置、方向、名称；LeftAnimal 向右，RightAnimal 向左"],
       ["animalgame.model", "MoveRule / StandardMoveRule", "移动规则的接口与默认实现（走一格或隔位跳）"],
       ["animalgame.model", "MoveRecord / Direction", "一次移动的起点终点快照；方向枚举"],
       ["animalgame.view", "GameFrame", "主窗口：标题栏、棋盘、状态栏与三个按钮，快捷键绑定"],
       ["animalgame.view", "BoardPanel", "棋盘面板：绘制格子与动物、处理鼠标点击、播放移动动画"],
       ["animalgame.view", "AnimalRenderer / Theme", "用 Java2D 矢量绘制兔子与乌龟；统一配色与字体"],
       ["animalgame.view", "RoundButton", "自绘圆角按钮，带悬停、按下、禁用三种状态"],
       ["animalgame.controller", "GameController", "把点击与按钮事件翻译成模型操作，并把结果写回界面"],
       ["animalgame.test", "GameModelTest", "模型层的 10 个测试用例（main 方法 + 断言）"],
       ["animalgame.tools", "PreviewTool", "离屏渲染界面截图，供说明书使用"]],
      [3.4, 3.8, 9.4], cap="表 3-1　模块划分", aligns=[False, False, False])

h2("3.3　模块调用关系")
body("程序的调用关系可以概括为一条主线和三条支线：")
body("主线：Main.main → 创建 Board（摆好初始局面）→ 创建 GameFrame（搭界面）→ 创建 GameController"
     "（把按钮与棋盘的监听器注册到自己身上）→ frame.setVisible(true) 进入事件循环。", indent=True)
body("支线一（玩家点击）：BoardPanel 捕获 MouseEvent → 换算成格子下标 → 调用 listener.onAnimalClicked(animal)"
     " → GameController 调用 board.resolveTarget / board.move → 成功后调用 panel.animateMove 播放动画"
     " → 动画结束回调 afterMove → 判断 board.isSolved 并刷新界面。", indent=True)
body("支线二（按钮）：JButton 触发 ActionEvent → GameController.actionPerformed 分辨事件源"
     " → 分别执行 undo()、restart()、showHelp()。", indent=True)
body("支线三（绘制）：Swing 重绘时调用 BoardPanel.paintComponent → 依次绘制背景、格子、提示、动物与标签，"
     "其中动物的形状交给 AnimalRenderer 用矢量方式绘制。", indent=True)

h2("3.4　类图")
body("图 3-1 是模型层的类图，包含继承（Animal → LeftAnimal / RightAnimal）、接口实现"
     "（StandardMoveRule → MoveRule）与组合（Board 持有 MoveRecord 的历史栈）三种关系。")
figure("uml_model.png", 15.0, "图 3-1　模型层类图")
body("图 3-2 是视图层与控制层的类图。GameFrame 组合了 BoardPanel 与三个 RoundButton；"
     "BoardPanel 通过 AnimalRenderer 绘制动物；GameController 持有 Board 与 GameFrame，"
     "既向棋盘注册点击监听，也向按钮注册动作监听。")
figure("uml_view.png", 15.6, "图 3-2　视图层与控制层类图")

h2("3.5　关键算法设计")
body("（1）落点判定算法。这是整个程序的核心。给定一只动物，先看它前方一格：越界则失败；为空则走一格；"
     "有动物再看隔位：隔位为空则跳过去，否则失败。整个过程只访问常数个数组元素，时间复杂度 O(1)，"
     "空间复杂度 O(1)，不需要任何搜索。")
body("（2）最少步数的验证。为了确认 15 步这个结论，作者另外写了一个小型的广度优先搜索程序："
     "把 7 个格子的状态编码成一个字符串，从初始局面开始逐层扩展所有合法走法，第一次遇到目标局面时的层数就是最少步数，"
     "搜索结果为 15 步，与公式 n(n+2) 完全一致，同时得到一条最优解：")
code("(2→3) (4→2) (5→4) (3→5) (1→3) (0→1) (2→0) (4→2)\n"
     "(6→4) (5→6) (3→5) (1→3) (2→1) (4→2) (3→4)")
body("这条 15 步的走法被直接写进了单元测试的第 10 个用例，用来验证“走满 15 步之后程序确实判定为胜利”。", indent=True)
body("（3）撤销算法。Board 内部维护一个双端队列 history 作为栈：每走一步就压入一条 MoveRecord"
     "（记录动物、起点、终点）；撤销时弹出栈顶，把动物从终点搬回起点、步数减一。入栈与出栈都是 O(1)。")
body("（4）胜利判定。遍历 7 个格子，跳过空位，检查“是兔子”与“在右半边”这两个条件是否同时成立，"
     "只要有一只动物不满足就立即返回 false。格子数固定为 7，因此也是 O(1)。")

h2("3.6　关键算法流程图")
body("图 3-3 给出了一次点击的完整判定流程，它是 2.1 节 R1～R4 四条规则的程序化表达；"
     "图 3-4 给出了程序从启动到响应玩家操作的总体流程。")
figure("flow_move.png", 13.6, "图 3-3　移动判定流程图")
figure("flow_game.png", 14.6, "图 3-4　程序总体流程图")

# ================================================================ 第 4 章
h1("4　详细设计")

h2("4.1　模型层的实现")
h3("4.1.1　动物与方向")
body("Animal 是一个抽象类，只保存两个状态：动物当前所在的位置 position 和它的“老家” homePosition"
     "（用来在重新开始时复位）。它把自己“往哪个方向走”和“叫什么名字”留给子类回答，"
     "这样 Board 里就不需要写任何 if (是兔子) 这样的分支，新增一种动物只要再写一个子类。")
code(extract(os.path.join(SRC, "animalgame", "model", "Animal.java"), "public abstract class Animal"))
body("方向用枚举 Direction 表示，枚举项自带一个整数步长（向左为 -1，向右为 +1）和一个中文标签，"
     "判定算法里直接使用 step，可以避免正负号写反的低级错误。", indent=False)
code(extract(os.path.join(SRC, "animalgame", "model", "Direction.java"), "public enum Direction"))

h3("4.1.2　移动规则")
body("MoveRule 是一个只有一个方法的接口，方法 resolveTarget 的语义是“给我一只动物，告诉我它能落到哪个格子”，"
     "不能移动时返回常量 NO_MOVE（-1）。把规则抽成接口的好处是：Board 只依赖接口，"
     "将来要实现“一次能跳两格”或者“某种动物不能跳”的新玩法，只要再写一个实现类，Board 一行都不用改。")
code(extract(os.path.join(SRC, "animalgame", "model", "StandardMoveRule.java"), "public int resolveTarget"))
body("这段代码就是 2.1 节 R1～R4 的直接翻译：先算前方一格，越界或已被占则尝试隔位，隔位也不行就返回 NO_MOVE。"
     "注意 inside 方法把“下标是否在 0～6 之间”这一判断收敛到一处，避免了在多个分支里重复写边界条件。", indent=False)

h3("4.1.3　移动记录")
body("MoveRecord 是一次移动的不可变快照，保存三个信息：哪只动物、从哪个格子来、到哪个格子去。"
     "它额外提供 isJump()，通过“起点与终点的距离是否为 2”判断这一步是走还是跳，界面可以据此决定动画的抛物线高度。")

h3("4.1.4　棋盘 Board")
body("Board 是模型层的核心。它持有 7 个格子的数组、一个存历史的双端队列、一个规则对象和当前步数。"
     "下面四个方法分别对应“复位”“走一步”“撤销”“判胜”。")
code(extract(os.path.join(SRC, "animalgame", "model", "Board.java"), "public final void reset"))
code(extract(os.path.join(SRC, "animalgame", "model", "Board.java"), "public MoveRecord move(Animal animal)"))
body("move 方法先向规则对象询问落点，落点非法就返回 null（调用者据此给出提示）；落点合法则先记下 from，"
     "把动物从原格搬到目标格，再生成一条 MoveRecord 压入历史栈，最后步数加一。"
     "“先判定、后修改”的顺序保证了失败时棋盘状态不被污染。", indent=False)
code(extract(os.path.join(SRC, "animalgame", "model", "Board.java"), "public MoveRecord undo()"))
code(extract(os.path.join(SRC, "animalgame", "model", "Board.java"), "public boolean isSolved()"))
body("undo 与 move 互为逆操作：move 把 from 写进记录，undo 就按记录把动物搬回 from，并把步数减一。"
     "isSolved 用 instanceof 区分种类，再比较位置是否已经越过分界线；由于“是兔子”与“在右半边”这两个条件"
     "对同一只动物不会同时为假，所以用 |= 累积即可，遇到第一个不满足的动物就直接返回 false。", indent=False)

h2("4.2　视图层的实现")
h3("4.2.1　主窗口 GameFrame")
body("窗口采用 BorderLayout：北部是渐变色的标题栏（左侧标题与副标题，右侧是显示步数的胶囊面板），"
     "中部是棋盘面板，南部是状态栏与三个圆角按钮。窗口 setResizable(false) 并 pack()，"
     "因此布局在 772×393 像素下正好放得下，不会因为拉伸而错位。"
     "另外用 InputMap/ActionMap 把 Ctrl+Z、Ctrl+R 绑定到撤销与重新开始，"
     "这样即使焦点在按钮上，快捷键依然有效。")

h3("4.2.2　棋盘面板与移动动画")
body("BoardPanel 负责三件事：把格子与动物画出来、把鼠标坐标换算成格子下标、在动物移动时播放动画。"
     "动画不使用额外的线程，而是用一个 16 ms 周期的 javax.swing.Timer 不断重绘，"
     "每次重绘时根据“已经过去的时间 / 总时长”算出进度，再插值出坐标。")
code(extract(os.path.join(SRC, "animalgame", "view", "BoardPanel.java"),
             "public void animateMove(Animal animal, int from, int to, Runnable onFinished)"))
body("animateMove 只是把动画参数记下来并启动定时器，真正的绘制发生在 paintFlyingAnimal 中。", indent=False)
code(extract(os.path.join(SRC, "animalgame", "view", "BoardPanel.java"), "private void paintFlyingAnimal"))
body("这里有两个细节：一是水平方向用缓入缓出（easeInOut）曲线，起步和收尾都慢，中间快，看起来更自然；"
     "二是竖直方向叠加了一个 sin 曲线，跳跃时抬高 46 像素、走路时只抬高 16 像素，"
     "并且用原始的 progress 而不是 eased，保证起跳和落地时高度都正好为 0。"
     "动画结束后调用 onFinished.run()，把控制权交回控制器去判断胜负。", indent=False)

h3("4.2.3　动物的矢量绘制")
body("动物不是用图片，而是用 Java2D 现场画出来的，这样任意缩放都不会模糊，也不需要额外的资源文件。"
     "AnimalRenderer.draw 先把坐标系平移到动物中心，再按 size/100 缩放，"
     "于是所有绘制代码都可以在一套 100×100 的“设计坐标”里书写：耳朵、眼睛、胡须、龟壳花纹都是固定数值。"
     "兔子和乌龟的区别只在颜色与形状，朝向则由 getDirection().getStep() 决定（乌龟的头画在 -34 或 +34 处）。")

h3("4.2.4　配色与圆角按钮")
body("Theme 类集中存放所有颜色与字体：背景用浅蓝渐变，兔子用粉色系，乌龟用绿色系，"
     "可落点提示用绿色虚线描边。字体按“微软雅黑 → 黑体 → 对话框默认字体”的顺序自动挑选，"
     "保证在不同版本的 Windows 上都能显示中文。RoundButton 继承 JButton 并重写 paintComponent，"
     "用圆角矩形自绘背景，根据悬停、按下、禁用三种状态切换深浅，从而摆脱系统默认按钮的灰白色调。")

h2("4.3　控制层的实现")
body("GameController 同时实现了 BoardPanel.GameListener 和 ActionListener，是整个程序的中枢。"
     "它把“用户点了哪里”翻译成“模型该怎么变”，再把“模型变成了什么样”写回界面。")
code(extract(os.path.join(SRC, "animalgame", "controller", "GameController.java"), "public void onAnimalClicked"))
body("这段代码里有三处防护：第一，动画还没结束时再次点击会被直接忽略，避免一只动物同时出现在两个位置；"
     "第二，点击空格子时 animal 为 null，直接返回；第三，落点非法时不是简单忽略，而是让动物闪红光并给出文字提示，"
     "让用户知道“为什么不能走”。只有移动成功后才更新状态栏、播放动画，并在动画结束后判断胜负。", indent=False)

h2("4.4　界面运行效果")
body("图 4-1 是程序启动后的主界面。标题栏显示游戏名称与操作提示，右上角的胶囊面板实时显示步数与理论最少步数，"
     "中间 7 个格子中左边 3 只兔子朝右、右边 3 只乌龟朝左，空位用虚线框标出，底部是状态栏与三个功能按钮。")
figure("shot_window.png", 14.4, "图 4-1　程序主界面")
body("图 4-2 是游戏进行到中盘时的棋盘：动物已经交错排列，此时每一步都必须依靠“隔位跳”才能继续，"
     "这正是本游戏的可玩性所在。")
figure("shot_board_mid.png", 12.6, "图 4-2　中盘局面")

# ================================================================ 第 5 章
h1("5　程序测试")

h2("5.1　测试方法")
body("测试分两部分进行。模型层用“main 方法 + 断言”的方式测试：GameModelTest 里写了 10 个静态方法，"
     "每个方法构造一个局面、执行若干步操作，然后用布尔表达式核对结果，最后统计通过与失败的数量，"
     "有失败时以非零状态码退出。这样做的原因是本工程坚持“零第三方依赖”，不引入 JUnit，"
     "任何一台装了 JDK 的机器都能直接运行测试，不需要配置 classpath。")
body("界面部分采用手工测试：按照功能需求逐条操作，观察动画、提示、按钮状态是否与预期一致，"
     "并用离屏渲染把界面保存成图片，逐张检查字体、对齐、颜色与遮挡问题。")

h2("5.2　测试用例设计")
table(["编号", "用例", "输入 / 操作", "预期结果", "实测"],
      [["T1", "初始局面", "启动程序", "0～2 号为兔子，3 号为空，4～6 号为乌龟", "通过"],
       ["T2", "单步移动", "点击 2 号位兔子", "走到 3 号位，步数变 1，记录 isJump 为假", "通过"],
       ["T3", "隔位跳跃", "先走 2→3，再点 4 号位乌龟", "乌龟跳过兔子落到 2 号位，isJump 为真", "通过"],
       ["T4", "阻挡判定", "局面 兔兔_兔龟龟龟，点 3 号位兔子", "前方 4、5 都被占，不能移动，返回 -1", "通过"],
       ["T5", "边界判定", "点 6 号位乌龟；再把兔子送到 6 号位后点击", "两端动物都不会越界移动", "通过"],
       ["T6", "方向规则", "查询 0 号与 6 号动物的方向", "兔子为 RIGHT，乌龟为 LEFT", "通过"],
       ["T7", "移动记录", "构造 (1→2) 与 (1→3) 两条记录", "前者 isJump 为假，后者为真", "通过"],
       ["T8", "撤销", "走两步后撤销，再全部撤销", "位置与步数逐一回退，最终回到初始局面", "通过"],
       ["T9", "重新开始", "走两步后点重新开始", "步数归零、历史清空、局面复位且未判胜", "通过"],
       ["T10", "最优解", "按 15 步最优解依次移动", "第 15 步后判胜，步数等于 MIN_MOVES", "通过"]],
      [1.3, 2.6, 6.4, 4.6, 1.7], cap="表 5-1　模型层测试用例",
      aligns=[True, False, False, False, True])

h2("5.3　测试结果")
body("在命令行执行 java animalgame.test.GameModelTest，输出如下：")
code("[通过] 初始局面：左三兔、中间空、右三龟\n"
     "[通过] 单步移动：2 号位兔子走到 3 号空位\n"
     "[通过] 隔位跳跃：4 号位乌龟跳过 3 号位兔子落到 2 号位\n"
     "[通过] 阻挡判定：前方与隔位都被占时不能移动\n"
     "[通过] 边界判定：位于两端的动物不会越界移动\n"
     "[通过] 方向规则：兔子向右、乌龟向左\n"
     "[通过] 移动记录：能区分单步与跨格跳\n"
     "[通过] 撤销：逐级回退并最终恢复初始局面\n"
     "[通过] 重新开始：步数归零、历史清空、局面复位\n"
     "[通过] 最优解：15 步完成换位并被判为胜利\n"
     "\n"
     "测试完成：共 10 项，通过 10 项，失败 0 项。")
body("10 个用例全部通过，说明移动判定、方向约束、边界处理、撤销与重开、胜负判定这五个核心逻辑都是正确的。"
     "其中第 10 个用例最有说服力：它按广度优先搜索得到的最优解连续走 15 步，只要有一步判定错误，"
     "后面的步骤就会全部失败，因此它同时验证了判定算法与胜负条件。")

h2("5.4　界面测试")
body("界面测试按功能需求逐条核对，结果见表 5-2。")
table(["检查项", "检查内容", "结果"],
      [["布局", "窗口尺寸固定、7 个格子等宽等高、左右对称、无控件重叠", "正常"],
       ["中文显示", "标题、按钮、标签、状态栏均无乱码，字体统一为微软雅黑", "正常"],
       ["交互反馈", "悬停时格子高亮、可落点显示绿色虚线、非法点击闪红光", "正常"],
       ["动画", "走一格为小弧度、跳一格为大弧度，动画期间重复点击被忽略", "正常"],
       ["按钮状态", "无历史时撤销按钮变灰且点击无效", "正常"],
       ["胜利提示", "走满 15 步后弹出对话框并显示步数", "正常"],
       ["快捷键", "Ctrl+Z 撤销、Ctrl+R 重新开始", "正常"]],
      [2.6, 11.6, 2.4], cap="表 5-2　界面测试", aligns=[True, False, True])
body("图 5-1 是初始局面的截图（中盘局面见图 4-2），可以看到虚线的空位、动物的朝向箭头与底部的步数标签都显示正确。")
figure("shot_board_start.png", 12.6, "图 5-1　初始局面")

# ================================================================ 第 6 章
h1("6　使用说明")

h2("6.1　编译与运行")
body("方式一（最省事）：双击工程根目录下的 动物换位.jar，直接启动游戏，不需要编译。")
body("方式二：双击 run.bat，脚本会检查 JDK、自动编译全部源文件并启动游戏；"
     "如果只想跑测试，双击 run_tests.bat。", indent=False)
body("方式三：在工程根目录下打开命令提示符，手工执行两条命令。", indent=False)
code("javac -encoding UTF-8 -d build\\classes -sourcepath src "
     "src\\animalgame\\*.java src\\animalgame\\model\\*.java src\\animalgame\\view\\*.java "
     "src\\animalgame\\controller\\*.java src\\animalgame\\test\\*.java src\\animalgame\\tools\\*.java\n"
     "java -cp build\\classes animalgame.Main")
body("注意 -encoding UTF-8 不能省略：源文件里有大量中文注释与中文字符串，"
     "如果按系统默认编码（GBK）读取就会编译报错或显示乱码。", indent=False)
body("另外，run.bat 必须以 GBK（ANSI）编码保存：命令解释器按系统代码页逐个字节读取批处理文件，"
     "若存成 UTF-8，中文注释与提示语会被拆成非法命令而报错。本工程的两个批处理文件即按 GBK 保存。",
     indent=False)

h2("6.2　操作说明")
table(["操作", "说明"],
      [["单击动物", "可移动则播放动画；被挡住则动物闪红光，状态栏给出原因"],
       ["玩法说明", "弹出对话框，列出三条规则与最少步数"],
       ["撤销 / Ctrl+Z", "撤销上一步，步数减一；没有可撤销的步骤时按钮为灰色"],
       ["重新开始 / Ctrl+R", "恢复初始局面并清零步数"],
       ["通关", "弹出对话框提示用了多少步，可关掉后继续研究更短的走法"]],
      [4.2, 12.4], cap="表 6-1　操作说明", aligns=[True, False])

h2("6.3　工程目录结构")
body("全部交付物都放在同一个文件夹 动物换位 中，目录结构如下：")
code("动物换位/\n"
     "├─ Java程序设计课程设计说明书-动物换位.docx   本说明书\n"
     "├─ 动物换位.jar                             可执行 jar，双击即可运行\n"
     "├─ run.bat                                  一键编译并运行\n"
     "├─ run_tests.bat                            一键编译并测试\n"
     "├─ README.md                                简要说明\n"
     "├─ src/animalgame/\n"
     "│   ├─ Main.java                 程序入口\n"
     "│   ├─ model/                    模型层（不依赖 Swing）\n"
     "│   ├─ view/                     视图层（窗口、棋盘、绘制、按钮）\n"
     "│   ├─ controller/               控制层（事件 -> 模型 -> 界面）\n"
     "│   ├─ test/GameModelTest.java   10 个模型层测试用例\n"
     "│   └─ tools/PreviewTool.java    离屏截图工具\n"
     "├─ api/                         javadoc 生成的 API 文档\n"
     "├─ build/classes/               javac 输出目录\n"
     "└─ docs/\n"
     "    ├─ img/                     说明书插图（PNG 原图）\n"
     "    └─ tools/                   生成插图与文档的 Python 辅助脚本")

h2("6.4　API 文档")
body("API 文档用 JDK 自带的 javadoc 生成，覆盖全部 17 个类与接口，包含类说明、方法说明、参数与返回值说明。"
     "生成命令如下（在工程根目录执行）：")
code("javadoc -encoding UTF-8 -charset UTF-8 -docencoding UTF-8 -private \\\n"
     "        -d api -sourcepath src -subpackages animalgame \\\n"
     "        -windowtitle \"动物换位游戏 API 文档\"")
body("生成后用浏览器打开 api/index.html 即可浏览，左侧是包与类的树形导航，右侧是详细说明。", indent=False)

# ================================================================ 第 7 章
h1("7　总结与体会")

body("这次课程设计从读任务书开始，到最后交出一份可运行的工程、一份说明书和一套 API 文档，"
     "整个过程比预想的更完整，也更有收获。")
body("在技术层面，最大的体会是“分层不是形式，而是为了能测试”。一开始我把判定逻辑直接写在面板的鼠标事件里，"
     "结果每改一次规则都要启动窗口、点几下鼠标才能验证，非常低效。后来把 Board、MoveRule 抽到 model 包，"
     "让它们不 import 任何 Swing 类，测试就变成了在命令行里跑十几行断言，几秒钟就能知道对错。"
     "第 10 个用例能一口气走完 15 步，正是这种结构带来的便利。")
body("第二个体会是关于“规则的形式化”。任务书里的规则是用自然语言写的，“前方有动物但隔位为空就跳过去”，"
     "看似清楚，但真正写成代码时会遇到一堆边界问题：隔位越界算不算空？两端动物怎么办？"
     "把规则写成 R1～R4 四条之后，这些情况都被迫想清楚了，代码里也就不再需要零散的 if 补丁。"
     "为了确认最少步数，我还写了一个二十行的广度优先搜索程序，用穷举的结果反过来验证公式 n(n+2)，"
     "这种“用程序验证推理”的做法让我对结论更有信心。")
body("第三个体会来自界面部分。Swing 的布局管理器、双缓冲与定时器都有不少细节，"
     "比如动画必须用 javax.swing.Timer 而不能用 Thread.sleep，否则会阻塞事件分发线程导致界面卡死；"
     "又比如自定义绘制的按钮要自己处理悬停与按下状态，否则鼠标移上去毫无反馈。"
     "为了让程序“看起来像个成品”，我在配色、圆角、阴影、缓动曲线上花了不少时间，"
     "这些工作虽然没有出现在需求里，却直接决定了使用体验。")
body("当然，程序还有可以改进的地方。一是动画期间点击会被忽略，"
     "如果做成“点击立即结束当前动画并执行新的一步”会更跟手；二是目前只有 3 对 3 一种难度，"
     "可以增加 4 对 4、5 对 5，并让最少步数按 n(n+2) 自动计算；"
     "三是没有记录最佳成绩，可以增加一个本地存档，把历史最少步数保存下来。"
     "这些都可以在现有结构上小步扩展，不需要重写。")
body("总的来说，这次设计让我把课堂上分散学习的继承、接口、枚举、集合、异常、事件监听、图形绘制串成了一个完整的东西，"
     "也让我第一次认真对待“注释、文档、测试”这些平时容易忽略的部分。")

# ================================================================ 参考文献
h1("参考文献")
refs = [
    "[1] 耿祥义, 张跃平. Java 2 实用教程（第 5 版）[M]. 北京: 清华大学出版社, 2017.",
    "[2] Bruce Eckel. Java 编程思想（第 4 版）[M]. 陈昊鹏, 译. 北京: 机械工业出版社, 2007.",
    "[3] Cay S. Horstmann. Java 核心技术 卷 I 基础知识（第 11 版）[M]. 林琪, 苏钰涵, 译. 北京: 机械工业出版社, 2019.",
    "[4] Oracle. Java Platform, Standard Edition 17 API Specification [EB/OL]. https://docs.oracle.com/en/java/javase/17/docs/api/, 2021.",
    "[5] Oracle. Lesson: Performing Custom Painting — The Java Tutorials [EB/OL]. https://docs.oracle.com/javase/tutorial/uiswing/painting/, 2020.",
]
for ref in refs:
    body(ref, indent=False, size=10.5, after=4)

h1("附录 A　源程序文件清单")
files = [
    ("animalgame/Main.java", "程序入口，设置外观并装配 MVC"),
    ("animalgame/model/Animal.java", "动物抽象类：位置、方向、名称"),
    ("animalgame/model/LeftAnimal.java", "左侧动物（兔子），向右"),
    ("animalgame/model/RightAnimal.java", "右侧动物（乌龟），向左"),
    ("animalgame/model/Direction.java", "方向枚举：步长与中文标签"),
    ("animalgame/model/MoveRule.java", "移动规则接口"),
    ("animalgame/model/StandardMoveRule.java", "标准规则：走一格或隔位跳"),
    ("animalgame/model/MoveRecord.java", "一次移动的记录"),
    ("animalgame/model/Board.java", "棋盘：状态、判定、撤销、胜负"),
    ("animalgame/view/Theme.java", "配色与字体"),
    ("animalgame/view/AnimalRenderer.java", "兔子和乌龟的矢量绘制"),
    ("animalgame/view/BoardPanel.java", "棋盘面板与动画"),
    ("animalgame/view/RoundButton.java", "圆角按钮"),
    ("animalgame/view/GameFrame.java", "主窗口"),
    ("animalgame/controller/GameController.java", "控制器"),
    ("animalgame/test/GameModelTest.java", "模型层测试用例"),
    ("animalgame/tools/PreviewTool.java", "离屏截图工具"),
]
rows = []
total = 0
for path, desc in files:
    full = os.path.join(SRC, *path.split("/"))
    with open(full, encoding="utf-8") as fp:
        n = len(fp.read().splitlines())
    total += n
    rows.append([path, str(n), desc])
rows.append(["合计", str(total), "17 个源文件，全部带中文注释"])
table(["源文件", "行数", "说明"], rows, [7.4, 1.4, 7.8],
      cap="表 A-1　源程序文件清单", aligns=[False, True, False])

doc.save(OUT)
print("saved", OUT)
