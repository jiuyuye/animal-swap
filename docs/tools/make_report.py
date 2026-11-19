# -*- coding: utf-8 -*-
"""按学校《java课程设计报告封面.doc》《java课程设计报告编写要求.doc》的格式，
生成《Java 课程设计报告——动物换位游戏》.docx。

格式要点（来自编写要求）：
  章标题 小3号(15pt)黑体加粗，段前0.5行、段后0.5行；
  正文   小4号(12pt)宋体，1.5 倍行距；
  2级标题 4号(14pt)黑体加粗；
  图题在图下方、表题在表格上方，编号为 图1/表1 连续序号；
  表格与插图的文字用 5号(10.5pt)宋体；
  页脚居中阿拉伯数字页码；全文文字统一黑色。
"""
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
OUT = os.path.join(ROOT, "Java课程设计报告-动物换位.docx")

BLACK = RGBColor(0, 0, 0)
doc = Document()
doc.core_properties.title = "动物换位游戏的设计与实现"
doc.core_properties.author = ""
doc.core_properties.last_modified_by = ""

# ------------------------------------------------------------------ 页面
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(2.54)


def set_font(run, ascii_font="Times New Roman", ea="宋体", size=12, bold=False,
             color=BLACK, underline=False):
    run.font.name = ascii_font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.underline = underline
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), ea)


# ------------------------------------------------------------------ 样式
for name, size in (("Heading 1", 15), ("Heading 2", 14), ("Heading 3", 12)):
    style = doc.styles[name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.italic = False
    style.font.color.rgb = BLACK
    style.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "黑体")
    pf = style.paragraph_format
    pf.space_before = Pt(9)
    pf.space_after = Pt(9)
    pf.line_spacing = 1.5
    pf.keep_with_next = True
    pf.page_break_before = False

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.font.color.rgb = BLACK
normal.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "宋体")
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(0)


def half_line(p, before=50, after=50):
    """把段前/段后设成“0.5 行”（Word 的 beforeLines/afterLines 单位是 1/100 行）。"""
    pf = p.paragraph_format
    pf.space_before = Pt(9)
    pf.space_after = Pt(9)
    ppr = p._p.get_or_add_pPr()
    sp = ppr.find(qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing")
        ppr.append(sp)
    sp.set(qn("w:beforeLines"), str(before))
    sp.set(qn("w:afterLines"), str(after))


def h1(text, center=False):
    p = doc.add_heading(text, level=1)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    for r in p.runs:
        set_font(r, ea="黑体", size=15, bold=True)
    half_line(p)
    return p


def h2(text):
    p = doc.add_heading(text, level=2)
    for r in p.runs:
        set_font(r, ea="黑体", size=14, bold=True)
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(6)
    return p


def h3(text):
    p = doc.add_heading(text, level=3)
    for r in p.runs:
        set_font(r, ea="黑体", size=12, bold=True)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    return p


def body(text, indent=True, size=12, after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(after)
    pf.first_line_indent = Pt(size * 2) if indent else Pt(0)
    p.alignment = align
    r = p.add_run(text)
    set_font(r, size=size)
    return p


def num_item(no, text, size=12):
    """带“（1）”序号的段落，悬挂缩进。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = 1.5
    pf.left_indent = Cm(1.0)
    pf.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("（%s）%s" % (no, text))
    set_font(r, size=size)
    return p


PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
    "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
    "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
    "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
    "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
    "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange",
]


def fix_ppr_order(p):
    """按 OOXML 规定的顺序重排 pPr 的子元素，避免 Word 报“内容有问题”。"""
    ppr = p._p.pPr
    if ppr is None:
        return
    children = list(ppr)
    children.sort(key=lambda el: PPR_ORDER.index(el.tag.split("}")[1])
                  if el.tag.split("}")[1] in PPR_ORDER else 99)
    for el in children:
        ppr.remove(el)
    for el in children:
        ppr.append(el)


def code(text, size=7.5, boxed=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.6)
    pf.right_indent = Cm(0.2)
    pf.space_before = Pt(4)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.0
    pf.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if boxed:
        ppr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "F5F5F5")
        ppr.append(shd)
        pbdr = OxmlElement("w:pBdr")
        for side in ("top", "left", "bottom", "right"):
            el = OxmlElement("w:" + side)
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "4")
            el.set(qn("w:space"), "4")
            el.set(qn("w:color"), "D0D0D0")
            pbdr.append(el)
        ppr.append(pbdr)
        fix_ppr_order(p)
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
    pf.space_after = Pt(6)
    pf.line_spacing = 1.0
    pf.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_font(r, size=10.5)
    return p


def figure(name, width_cm, cap):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.0
    pf.first_line_indent = Cm(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(IMG, name), width=Cm(width_cm))
    caption(cap)


def table(headers, rows, widths, cap=None, size=10.5, aligns=None, first_col_left=False):
    if cap:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(8)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.0
        pf.first_line_indent = Cm(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(cap)
        set_font(r, size=10.5)

    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    def fill(cell, text, bold=False, center=True, bg=None):
        cell.text = ""
        para = cell.paragraphs[0]
        para.paragraph_format.space_before = Pt(2)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.line_spacing = 1.0
        para.paragraph_format.first_line_indent = Cm(0)
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
        fill(t.rows[0].cells[i], text, bold=True, bg="E7E6E6")
    for row in rows:
        cells = t.add_row().cells
        for i, text in enumerate(row):
            if aligns is not None:
                center = aligns[i]
            elif first_col_left:
                center = i != 0
            else:
                center = True
            fill(cells[i], text, center=center)
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    cols = t._tbl.tblGrid.findall(qn("w:gridCol"))
    for i, gc in enumerate(cols):
        gc.set(qn("w:w"), str(int(widths[i] / 2.54 * 1440)))
    tblw = t._tbl.tblPr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        t._tbl.tblPr.append(tblw)
    tblw.set(qn("w:type"), "dxa")
    tblw.set(qn("w:w"), str(int(sum(widths) / 2.54 * 1440)))
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
    """从源文件中截取一个方法（连同它上面的注释）。"""
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


def src(cls_path):
    return os.path.join(SRC, cls_path.replace("/", os.sep))


def code_of(cls_path, sig):
    return extract(src(cls_path), sig)


def line_count(cls_path):
    with open(src(cls_path), encoding="utf-8") as fp:
        return len(fp.read().splitlines())


# ================================================================== 封面
def cover():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(26)
    p.paragraph_format.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("中南林业科技大学")
    set_font(r, ea="黑体", size=26, bold=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("课 程 设 计 报 告")
    set_font(r, ea="黑体", size=32, bold=True)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(28)
    p.paragraph_format.line_spacing = 1.0

    # 基本信息（下划线表格）
    t = doc.add_table(rows=0, cols=4)
    t.autofit = False
    widths = [3.0, 5.2, 2.6, 5.4]

    def cell_text(cell, text, align=WD_ALIGN_PARAGRAPH.LEFT, size=14, bold=False):
        cell.text = ""
        para = cell.paragraphs[0]
        para.alignment = align
        para.paragraph_format.space_before = Pt(2)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.line_spacing = 1.0
        para.paragraph_format.first_line_indent = Cm(0)
        run = para.add_run(text)
        set_font(run, ea="黑体", size=size, bold=bold)

    def bottom_border(cell):
        tcpr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        el = OxmlElement("w:bottom")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "8")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
        tcpr.append(borders)

    def field_row(label, value="", second_label=None, second_value=""):
        row = t.add_row()
        row.height = Cm(1.05)
        cell_text(row.cells[0], label, WD_ALIGN_PARAGRAPH.RIGHT, 14, True)
        cell_text(row.cells[1], value, WD_ALIGN_PARAGRAPH.CENTER, 14)
        bottom_border(row.cells[1])
        if second_label is None:
            merged = row.cells[2].merge(row.cells[3])
            cell_text(merged, "", WD_ALIGN_PARAGRAPH.CENTER, 14)
            bottom_border(merged)
        else:
            cell_text(row.cells[2], second_label, WD_ALIGN_PARAGRAPH.RIGHT, 14, True)
            cell_text(row.cells[3], second_value, WD_ALIGN_PARAGRAPH.CENTER, 14)
            bottom_border(row.cells[3])

    field_row("设计名称：", "动物换位游戏的设计与实现")
    field_row("姓　　名：", "", "学　　号：", "")
    field_row("专业班级：")
    field_row("院（系）：")
    field_row("设计时间：")
    field_row("设计地点：")
    field_row("指导老师：")
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    cols = t._tbl.tblGrid.findall(qn("w:gridCol"))
    for i, gc in enumerate(cols):
        gc.set(qn("w:w"), str(int(widths[i] / 2.54 * 1440)))

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(26)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("指导教师评定情况：")
    set_font(r, ea="黑体", size=14, bold=True)

    # 评定表：考核内容 / 等级（优良中合格不合格） / 综合评语及成绩
    t2 = doc.add_table(rows=7, cols=7)
    t2.style = "Table Grid"
    t2.autofit = False
    w2 = [3.6, 1.5, 1.5, 1.5, 1.5, 1.5, 5.0]

    def put(cell, text, size=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
        cell.text = ""
        para = cell.paragraphs[0]
        para.alignment = align
        para.paragraph_format.space_before = Pt(1)
        para.paragraph_format.space_after = Pt(1)
        para.paragraph_format.line_spacing = 1.0
        para.paragraph_format.first_line_indent = Cm(0)
        run = para.add_run(text)
        set_font(run, size=size, bold=bold)

    put(t2.cell(0, 0), "考核内容", bold=True)
    grade = t2.cell(0, 1).merge(t2.cell(0, 5))
    put(grade, "等级", bold=True)
    comment = t2.cell(0, 6).merge(t2.cell(5, 6))
    put(comment, "综合评语及成绩", bold=True)
    for _ in range(4):
        pp = comment.add_paragraph()
        pp.paragraph_format.space_before = Pt(1)
        pp.paragraph_format.space_after = Pt(1)
        pp.paragraph_format.line_spacing = 1.0
    for i, name in enumerate(["优", "良", "中", "合格", "不合格"]):
        put(t2.cell(1, i + 1), name, bold=True)
    put(t2.cell(1, 0), "", bold=True)
    items = ["功能实现　30", "类和界面设计　20", "设计报告　30", "答辩　20"]
    for i, name in enumerate(items):
        put(t2.cell(2 + i, 0), name, align=WD_ALIGN_PARAGRAPH.LEFT)
        for j in range(1, 6):
            put(t2.cell(2 + i, j), "")
    sign = t2.cell(6, 0).merge(t2.cell(6, 6))
    put(sign, "签名：　　　　　　　　　　　　　　　　　　　年　　月　　日", align=WD_ALIGN_PARAGRAPH.RIGHT)
    for i, row in enumerate(t2.rows):
        row.height = Cm(1.1) if i == 6 else Cm(0.95)
    for row in t2.rows:
        for i, w in enumerate(w2):
            row.cells[i].width = Cm(w)
    cols = t2._tbl.tblGrid.findall(qn("w:gridCol"))
    for i, gc in enumerate(cols):
        gc.set(qn("w:w"), str(int(w2[i] / 2.54 * 1440)))


# ================================================================== 页码
def start_numbered_section():
    s2 = doc.add_section(WD_SECTION.NEW_PAGE)
    s2.page_width, s2.page_height = Cm(21), Cm(29.7)
    s2.left_margin = s2.right_margin = Cm(2.2)
    s2.top_margin = s2.bottom_margin = Cm(2.54)
    s2.footer.is_linked_to_previous = False
    fp = s2.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(fp, " PAGE ", "1")
    sectPr = s2._sectPr
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:start"), "1")
    cols = sectPr.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(pg)
    else:
        sectPr.append(pg)
    return s2


# ================================================================== 目录
def toc_page():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("目　　录")
    set_font(r, ea="黑体", size=15, bold=True)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    add_field(p, ' TOC \\o "1-2" \\h \\z \\u ',
              "（目录尚未生成：在此处单击右键，选择“更新域 → 更新整个目录”）")


# ================================================================== 第 1 章
def chapter1():
    h1("1　设计概述")

    h2("1.1　设计题目")
    body("本次课程设计的题目是“动物换位游戏”。程序运行后会在屏幕上出现一排 7 个格子：左边的 3 个格子各站一只兔子，"
         "右边的 3 个格子各站一只乌龟，正中间空出一格。兔子只会朝右走，乌龟只会朝左走，两边都不能后退。"
         "玩家用鼠标单击某只动物，程序判断它这一步能不能走，能走就播一小段移动动画；走不了就给出提示。"
         "当 3 只兔子和 3 只乌龟的位置整体对调过来，游戏就结束了。")
    body("具体的游戏规则如下：")
    num_item(1, "单击一只动物，如果它前面的格子是空的，就向前走一格；")
    num_item(2, "如果它前面站着一只动物、而再前面的一格是空的，就跳过这只动物，落到再前面那一格；")
    num_item(3, "其它情况都不能走：前面是界外，或者前面被挡住、再前面也被挡住时，点了不动，只给一句提示；")
    num_item(4, "兔子只能向右、乌龟只能向左，程序不允许反方向移动。")
    body("除移动之外，界面上还要有“撤销”和“重新开始”两个按钮：“撤销”取消上一步，“重新开始”把棋盘恢复成开局的样子。"
         "另外，界面上要能随时看到已经走了多少步。")

    h2("1.2　设计目的")
    body("这次课设的目的不是写一个多复杂的游戏，而是把一学期学过的零散知识串起来用一遍。具体有下面几点：")
    num_item(1, "复习 Java 的基本写法：类、对象、继承、接口、枚举、集合（这里把双端队列当栈来用）和异常处理；")
    num_item(2, "练习用 Swing 写图形界面：窗口、面板、按钮、布局、鼠标事件、定时器，以及用 Java2D 画图；")
    num_item(3, "体会“把数据和界面分开写”的好处，学会按职责把代码分到不同的包里，而不是全堆在一个类里；")
    num_item(4, "学会写一小段测试程序来验证规则对不对，而不是每次都靠手点、靠眼睛看；")
    num_item(5, "练习写设计文档，把“怎么想、怎么写、怎么测”讲清楚，这对以后做项目同样有用。")

    h2("1.3　设计要求")
    body("根据任务书的要求，程序需要实现表1中列出的功能。")
    table(["编号", "要求", "具体说明"],
          [["F1", "棋盘布局", "一排 7 个格子，左边 3 格放兔子，右边 3 格放乌龟，中间 1 格为空"],
           ["F2", "走一格", "单击动物，若前方相邻格子为空，则向前移动一格"],
           ["F3", "跳一格", "若前方相邻格子有动物、再前方一格为空，则跳过它落到再前方那一格"],
           ["F4", "限制方向", "兔子只能向右、乌龟只能向左；越界或被挡住时不能移动"],
           ["F5", "撤销", "单击“撤销”退回上一步，可以连续撤销，直到回到开局"],
           ["F6", "重新开始", "单击“重新开始”，棋盘和步数都恢复成开局状态"],
           ["F7", "判断胜负", "3 只兔子全部到右侧、3 只乌龟全部到左侧时，提示游戏成功"],
           ["F8", "步数显示", "界面上显示已经走了多少步，并给出最少步数供参考"]],
          [1.6, 2.6, 12.4], cap="表1　程序的功能要求", first_col_left=False)
    body("除了表1中的功能，还希望界面干净、有中文提示，每次操作后能马上看到反馈。这些偏“使用感受”的要求，"
         "在后面的界面设计和测试两章里具体说明。")

    h2("1.4　工作计划")
    body("课设安排在两周内完成，按“先想清楚、再动手写、最后测试和写报告”的顺序推进，具体安排如表2所示。")
    table(["阶段", "时间", "主要工作", "阶段成果"],
          [["1", "第 1 天", "读任务书，确定题目和规则，画界面草图", "需求清单、界面草图"],
           ["2", "第 2 天", "划分类和接口，画类图和流程图", "类图、流程草图"],
           ["3", "第 3～5 天", "写模型层：棋盘、动物、规则、撤销", "可以运行的模型代码"],
           ["4", "第 6～8 天", "写界面层：窗口、棋盘绘制、按钮、动画", "可以用鼠标点的界面"],
           ["5", "第 9 天", "写控制层，把界面和模型接起来", "完整可玩的程序"],
           ["6", "第 10 天", "写测试程序，逐条验证规则", "10 项测试全部通过"],
           ["7", "第 11～12 天", "补注释、生成 API 文档", "API 文档（HTML）"],
           ["8", "第 13～14 天", "写课程设计报告、准备答辩", "课程设计报告"]],
          [1.4, 2.6, 8.0, 4.6], cap="表2　课程设计工作计划")

    h2("1.5　开发环境")
    body("程序只用到 JDK 自带的类库，没有引入任何第三方包，开发与运行环境如表3所示。")
    table(["项目", "内容"],
          [["操作系统", "Windows 11（64 位）"],
           ["开发语言", "Java（源文件编码 UTF-8）"],
           ["JDK 版本", "JDK 26（javac 26.0.2），代码按 JDK 8 以上的语法书写，低版本也能编译"],
           ["图形界面", "Swing 与 Java2D（JDK 自带）"],
           ["第三方库", "无"],
           ["开发工具", "文本编辑器 + 命令行（javac 编译、java 运行）"],
           ["运行方式", "双击 动物换位.jar；或双击 run.bat 自动编译后运行"]],
          [3.4, 13.2], cap="表3　开发与运行环境", first_col_left=True)


# ================================================================== 第 2 章
def chapter2():
    h1("2　总体设计")

    h2("2.1　设计方法与思路")
    body("这个程序要做的事情其实只有三件：记住棋盘上每个格子站着谁，把棋盘和动物画出来，响应鼠标和按钮的动作。"
         "如果把这三种代码混在一个类里，改界面时容易碰到规则，改规则时又怕弄坏界面。所以采用了“分开写”的办法，"
         "把程序分成三部分：")
    num_item(1, "数据部分（model 包）：管棋盘、动物、移动规则和撤销记录，完全不碰窗口和按钮，可以单独用命令行跑起来；")
    num_item(2, "显示部分（view 包）：只管把棋盘画出来、把按钮摆好、播放动画，自己不做“能不能走”的判断；")
    num_item(3, "连接部分（controller 包）：接收鼠标和按钮的动作，向模型要结果，再让视图刷新。")
    body("这种“数据、界面、事件处理”分开的写法就是常说的 MVC。好处很直接：界面还没写的时候，模型里的规则就可以用"
         "测试程序验证；以后想把 Swing 换成别的界面，规则一行都不用改。")
    body("棋盘用最简单的方式表示：一个长度为 7 的数组，数组的每个位置对应屏幕上的一个格子，格子里放一只动物对象，"
         "空格子就放 null。每只动物自己记住两件事——它最开始站在哪个格子（“家”），以及它是往右走还是往左走。"
         "这样判断方向时不必再区分兔子还是乌龟，直接问动物“你往哪边走”就行。")
    body("“能不能走、走到哪一格”这件事没有写死在棋盘里，而是单独抽成一个规则接口（MoveRule），"
         "由 StandardMoveRule 这个类按 1.1 节的规则去实现。棋盘只负责“问规则要一个目标格号，再照着搬”。"
         "这样以后如果再加一种“可以连跳两格”的新玩法，只要再写一个实现类，棋盘和界面都不用动。")
    body("撤销的做法很朴素：每走一步，就把“谁、从哪格、到哪格”记成一条记录，压进一个栈里；点“撤销”时弹出最后一条，"
         "把动物搬回原来的格子。“重新开始”则直接把棋盘恢复成开局，并把记录清空。")
    body("动画没有用现成的动画库，而是用一个每 16 毫秒触发一次的定时器：移动开始时记下起点、终点和开始时间，"
         "定时器每次触发就按“已经过去的时间占总时长的比例”算出动物当前应该在的位置，画在两只格子之间。"
         "跳的时候让轨迹高一些，走的时候低一些，看上去就有“跳过去”和“走过去”的区别。")

    h2("2.2　类和接口的设计")
    body("按上面的分工，程序一共写了 17 个 Java 文件。其中跟规则有关的 8 个类放在 model 包里，它们的继承和依赖关系"
         "如图1所示；跟界面和控制有关的类放在 view、controller 包里，关系如图2所示。")
    figure("uml_model.png", 15.4, "图1　模型层的类图")
    body("图1 中，Animal 是抽象类，代表“一只动物”，它只规定两件事：自己往哪个方向走、自己叫什么名字；"
         "具体是兔子还是乌龟，由 LeftAnimal（兔子，向右）和 RightAnimal（乌龟，向左）两个子类回答。"
         "Direction 是一个枚举，把“向左”“向右”和对应的步长（−1、+1）绑在一起，避免在代码里到处写 ±1。"
         "MoveRule 是规则接口，StandardMoveRule 是它的默认实现。MoveRecord 表示一条移动记录，用来支持撤销。"
         "Board 是棋盘，它持有 7 个格子和一个撤销用的栈，并通过 MoveRule 接口判断落点。")
    figure("uml_view.png", 15.4, "图2　视图层与控制层的类图")
    body("图2 中，GameFrame 是主窗口，里面装着标题栏、棋盘面板和三个按钮；BoardPanel 负责画格子、画动物、"
         "跟踪鼠标位置和播放动画；AnimalRenderer 专门用 Java2D 画兔子和乌龟的图形；RoundButton 是自绘的圆角按钮；"
         "Theme 集中存放颜色和字体。GameController 是“中间人”，它监听按钮和棋盘的点击，调用 Board 的方法，"
         "再让 GameFrame 更新步数和提示。Main 只做一件事：把上面这些对象按顺序创建出来并显示窗口。")

    h2("2.3　模块划分与调用关系")
    body("整个程序按职责分成四个部分，如表4所示。")
    table(["包", "主要类", "职责"],
          [["model", "Board、Animal、MoveRule 等 8 个", "棋盘数据、移动规则、撤销记录、胜负判断"],
           ["view", "GameFrame、BoardPanel、AnimalRenderer 等 5 个", "窗口与棋盘绘制、按钮、动画、配色"],
           ["controller", "GameController", "接收点击和按钮动作，调用模型，刷新界面"],
           ["（默认包）、test、tools", "Main、GameModelTest、PreviewTool", "程序入口、命令行测试、离屏截图"]],
          [3.6, 6.4, 6.6], cap="表4　程序的模块划分", first_col_left=True)
    body("一次点击在程序里的完整过程如下，从中可以看出各模块是怎么配合的：")
    num_item(1, "玩家在棋盘上按下鼠标，BoardPanel 根据坐标算出点的是第几个格子，把这只动物交给 GameController；")
    num_item(2, "GameController 先看动画有没有播完，没播完就直接忽略这次点击，防止连续点击把状态弄乱；")
    num_item(3, "然后问 Board：这只动物现在能落到哪一格？")
    num_item(4, "Board 把问题转给 MoveRule，由规则算出目标格号；算不出来就返回 −1；")
    num_item(5, "如果得到 −1，GameController 让棋盘闪一下红框，并在状态栏写一句提示，这次点击就结束了；")
    num_item(6, "如果得到了格号，Board 搬动动物、把这一步记进撤销栈、步数加一；")
    num_item(7, "GameController 让棋盘播放动画，动画结束时刷新步数；如果已经换位成功，就弹出提示框。")


# ================================================================== 第 3 章
def chapter3():
    h1("3　详细设计")

    h2("3.1　界面设计")
    body("界面分成上、中、下三层，如图3所示。上面是一条深蓝色的标题栏：左边写着游戏名称和一句玩法提示，"
         "右边一块小面板显示“步数”和“最少 15 步”。中间是棋盘，7 个格子横向排开，每个格子是一张白色的圆角卡片，"
         "动物画在卡片中间，格子底部写着“兔 →”“龟 ←”提醒方向。下面一行左边是状态栏，用来写提示语；"
         "右边是三个按钮：玩法说明、撤销、重新开始。")
    figure("shot_window.png", 13.4, "图3　程序的主界面")
    body("界面上的各个元素及其作用如表5所示。")
    table(["界面元素", "类型", "作用"],
          [["标题栏", "自绘面板（渐变蓝）", "显示游戏名称、玩法提示和步数"],
           ["步数面板", "自绘标签", "显示已走步数和最少步数，换位后自动更新"],
           ["棋盘", "自绘面板 BoardPanel", "画出 7 个格子与动物，接收鼠标点击"],
           ["动物图形", "Java2D 矢量绘制", "兔子（粉色）、乌龟（绿色），画在格子中间"],
           ["玩法说明", "圆角按钮", "弹窗说明规则和最少步数"],
           ["撤销", "圆角按钮", "退回上一步；没有可撤销的步骤时按钮变灰"],
           ["重新开始", "圆角按钮", "把棋盘和步数恢复到开局"],
           ["状态栏", "标签 JLabel", "显示操作提示；不能移动时用红字提醒"]],
          [3.0, 5.2, 8.4], cap="表5　界面元素及其作用", first_col_left=True)
    body("界面上的处理逻辑主要有下面几条：")
    num_item(1, "鼠标移到某只可以走的动物上时，它将要落到的格子会显示一个绿色虚线框，告诉玩家“能走到这里”，"
                "鼠标移开就消失。")
    num_item(2, "点击动物后先判断再动画：能走就播一段约 0.26 秒的移动动画，动画期间界面不接受新的点击，"
                "以免一步没走完又走一步。")
    num_item(3, "点击不能走的动物，那个格子会闪一下浅红色，状态栏用红字提示“前面被挡住了，这只动物现在不能动”，"
                "步数不变。")
    num_item(4, "点了“撤销”或“重新开始”，状态栏会分别写一句“已撤销上一步”“已重新开始”，同时刷新步数和按钮状态。")
    num_item(5, "三个按钮都有键盘快捷键：Ctrl+Z 撤销、Ctrl+R 重新开始、F1 打开玩法说明，不习惯用鼠标时更顺手。")
    num_item(6, "换位成功时弹出一个对话框，告诉玩家一共走了多少步，并与最少步数比较，玩家可以选择再来一局。")

    h2("3.2　算法设计")
    body("程序里有两处关键算法：一是“一只动物这一步能不能走、走到哪一格”，二是程序从头到尾的运行流程。"
         "前者如图4所示，后者如图5所示。")
    figure("flow_move.png", 14.4, "图4　一次点击的移动判定流程")
    body("图4 的判断过程可以用几句话讲清楚：先算出这只动物的方向步长 step（兔子 +1、乌龟 −1），那么它正前方就是 i+step。"
         "如果 i+step 已经越界，或者那个格子不是空的，就再看隔一格的位置 i+2×step：只要它在界内而且是空的，"
         "就跳过去；否则这一步不能走。如果正前方本来就是空的，那就直接走一格。"
         "要注意“能走”和“不能走”最后都会回到等待下一次点击的状态，程序不会因为一次无效点击卡住。")
    figure("flow_game.png", 14.4, "图5　程序总体运行流程")
    body("图5 是程序从启动到退出的主干流程：设置界面风格 → 创建棋盘（摆好 3 兔 3 龟）→ 创建窗口 → "
         "创建控制器并注册监听 → 显示窗口 → 等待用户操作。Swing 程序里这个“等待”并不是写一个循环，"
         "而是由 Swing 自己的“事件分发线程”负责——可以把它理解成一个专门排队接收鼠标和键盘动作的循环，"
         "我们只要在监听方法里写好“收到之后做什么”就行；每次处理完都会回到等待状态。")

    h2("3.3　最少步数的计算")
    body("任务书要求界面上给出最少步数。这个问题可以换一种说法来看：把“棋盘上现在是什么样子”算作一种局面，"
         "每走一步就换到下一种局面，那么“最少步数”就是“从开局走到目标，最少要换几次”。"
         "求这个数用的是一个很朴素的笨办法：从开局出发，先把走 1 步能到达的所有局面都列出来，"
         "再把走 2 步能到达的列出来……一层一层往外找，第一次碰到目标局面时用的步数就是最少的。"
         "这种“一层层往外找”的办法在书里叫广度优先搜索，好处是只要局面数量不太大，就一定能找到最优解。"
         "本人用一个小程序按这个思路算过，3 对动物最少需要 15 步。")
    body("这个结果和理论值一致：n 对动物最少需要 n×(n+2) 步，n=3 时正好是 15。程序里把它写成常量 MIN_MOVES，"
         "界面右上角显示“最少 15 步”，测试程序里也用这 15 步的走法验证了胜负判断。"
         "一种 15 步的走法（数字是格子编号，从左到右为 0～6）是：2→3、4→2、5→4、3→5、1→3、0→1、2→0、4→2、"
         "6→4、5→6、3→5、1→3、2→1、4→2、3→4。")


# ================================================================== 第 4 章
def chapter4():
    h1("4　软件实现")

    h2("4.1　代码的组织")
    body("全部代码共 17 个文件、约 2300 行，按第 2 章的分工放在四个位置，清单如表6所示。"
         "每个类、每个方法上面都写了中文注释，说明它“做什么、怎么用”，这些注释同时也是 API 文档的来源。")
    files = [
        ("Main.java", "（默认包）", "animalgame/Main.java", "程序入口：设置界面风格，创建模型、窗口和控制器"),
        ("Animal.java", "model", "animalgame/model/Animal.java", "抽象类：动物的位置、方向、名字"),
        ("Direction.java", "model", "animalgame/model/Direction.java", "枚举：向左 / 向右，以及对应的步长"),
        ("MoveRule.java", "model", "animalgame/model/MoveRule.java", "规则接口：算出动物这一步能落到哪一格"),
        ("StandardMoveRule.java", "model", "animalgame/model/StandardMoveRule.java", "默认规则：走一格、跳一格，否则不能走"),
        ("LeftAnimal.java", "model", "animalgame/model/LeftAnimal.java", "兔子：方向向右，名字为“兔”"),
        ("RightAnimal.java", "model", "animalgame/model/RightAnimal.java", "乌龟：方向向左，名字为“龟”"),
        ("MoveRecord.java", "model", "animalgame/model/MoveRecord.java", "一条移动记录：谁、从哪格、到哪格、是否跳跃"),
        ("Board.java", "model", "animalgame/model/Board.java", "棋盘：布局、移动、撤销、胜负判断"),
        ("Theme.java", "view", "animalgame/view/Theme.java", "颜色与字体常量，统一界面风格"),
        ("AnimalRenderer.java", "view", "animalgame/view/AnimalRenderer.java", "用 Java2D 画兔子和乌龟"),
        ("BoardPanel.java", "view", "animalgame/view/BoardPanel.java", "棋盘面板：绘制、鼠标、动画"),
        ("RoundButton.java", "view", "animalgame/view/RoundButton.java", "圆角自绘按钮"),
        ("GameFrame.java", "view", "animalgame/view/GameFrame.java", "主窗口：标题栏、棋盘、按钮、提示"),
        ("GameController.java", "controller", "animalgame/controller/GameController.java", "控制器：响应点击与按钮，刷新界面"),
        ("GameModelTest.java", "test", "animalgame/test/GameModelTest.java", "命令行测试程序，共 10 条用例"),
        ("PreviewTool.java", "tools", "animalgame/tools/PreviewTool.java", "离屏渲染界面截图的小工具"),
    ]
    rows = []
    total = 0
    for i, (name, pkg, path, desc) in enumerate(files, 1):
        n = line_count(path)
        total += n
        rows.append([str(i), name, pkg, str(n), desc])
    rows.append(["合计", "17 个文件", "—", str(total), "—"])
    table(["序号", "文件名", "所属包", "行数", "主要功能"], rows,
          [1.2, 4.0, 2.2, 1.3, 7.9], cap="表6　源程序文件清单")

    h2("4.2　模型层的实现")
    body("模型层是程序的“大脑”，最核心的是 Board 里的三个方法：走一步、撤销、判断是否完成。"
         "走一步的代码如下，它先请规则算出目标格号，算不出来就返回 null，表示这次点击无效；能走的话搬动动物、"
         "记录这一步、步数加一。")
    code(code_of("animalgame/model/Board.java", "public MoveRecord move(Animal animal)"))
    body("撤销就是走一步的逆操作：从栈里弹出最后一条记录，把动物搬回出发的格子，步数减一。"
         "判断是否完成则分别检查兔子和乌龟：兔子要全部走到右半边，乌龟要全部走到左半边，两边都满足才算成功。")
    code(code_of("animalgame/model/Board.java", "public MoveRecord undo()"))
    code(code_of("animalgame/model/Board.java", "public boolean isSolved()"))
    body("移动规则单独放在 StandardMoveRule 里。它只做三件事：先看正前方能不能走，再看能不能跳过一只动物，"
         "都不行就返回 −1（接口里定义的“不能走”）。这样写的好处是规则可以整块替换，棋盘完全不用改。")
    code(code_of("animalgame/model/StandardMoveRule.java", "public int resolveTarget(Animal animal, Animal[] slots)"))
    body("MoveRecord 很小，只记录“谁、从哪、到哪”，另外提供一个 isJump() 用来区分“走一格”和“跳一格”，"
         "界面和测试都用得上。")
    code(code_of("animalgame/model/MoveRecord.java", "public boolean isJump()"))

    h2("4.3　视图层的实现")
    body("视图层最麻烦的是动画。BoardPanel 里用三个字段记住“谁在飞、从哪飞到哪、什么时候开始”，"
         "然后启动一个 16 毫秒触发一次的定时器；每次触发都把进度换算成 0～1 之间的数，再交给绘制方法去画。")
    code(code_of("animalgame/view/BoardPanel.java", "public void animateMove(Animal animal, int from, int to, Runnable onFinished)"))
    body("绘制时用了一个小技巧：位置的推进用“先慢后快再慢”的缓动函数，竖直方向再叠加一条正弦曲线，"
         "于是走一格时是贴着格子平移，跳一格时会明显抬起来，看起来像真的跳过去。")
    code(code_of("animalgame/view/BoardPanel.java", "private void paintFlyingAnimal(Graphics2D g2, double cy)"))
    body("兔子和乌龟没有用图片，全部是用圆形、椭圆、弧线拼出来的矢量图形，所以窗口放大也不会模糊，"
         "而且不用额外带资源文件。AnimalRenderer 里的 draw 方法负责把坐标系缩放到 100×100 的“设计尺寸”，"
         "再分别调用 drawRabbit 或 drawTurtle。")

    h2("4.4　控制层的实现")
    body("控制层的任务是把“用户动作”翻译成“模型操作 + 界面刷新”。最关键的 onAnimalClicked 方法如下："
         "先挡掉动画期间的点击，再问模型能不能走，能走就播动画并在动画结束后检查和刷新。")
    code(code_of("animalgame/controller/GameController.java", "public void onAnimalClicked(Animal animal)"))
    body("动画结束后的收尾集中在 afterMove 里：刷新步数、判断是否换位完成、给出提示。"
         "撤销和重新开始也都在这个类里，它们做的事情一样——调用模型、刷新界面、写一句提示。")
    code(code_of("animalgame/controller/GameController.java", "private void afterMove()"))

    h2("4.5　完整源程序")
    body("上面几节挑的是每个层次里最有代表性的代码。完整的源程序（含逐行中文注释）共 17 个文件、"
         "约 2300 行，按包和文件的顺序全部列在附录A中，文件名与表6一一对应。"
         "另外，用 JDK 自带的 javadoc 工具可以把这些注释直接生成一套网页版的 API 文档，"
         "点开就能查到每个类、每个方法是做什么的，这套文档已随源程序一起提交（放在 api 文件夹里）。")


# ================================================================== 第 5 章
def chapter5():
    h1("5　测试")

    h2("5.1　测试方法")
    body("测试分成两部分。第一部分是写一个命令行的测试程序，直接调用模型里的方法，逐条检查结果对不对。"
         "这类测试不依赖界面，跑起来只要一两秒，改一次代码就能重新验证一遍。第二部分是在真实的窗口里用手点，"
         "检查动画、提示、按钮这些“看得见”的东西是否正常。")
    body("自动测试的写法很朴素：每测完一条就打印一行“[通过] 说明”，全部跑完再打印一行合计；"
         "只要有一条不符合预期，就打印“[失败]”并以非 0 的退出码结束，这样不管是在命令行里还是脚本里，"
         "都能一眼看出有没有问题。")

    h2("5.2　测试用例设计")
    body("针对规则、撤销和胜负判断，一共设计了 10 条测试用例，覆盖初始局面、两种走法、走不了的情况、边界、方向、"
         "记录、撤销、重开和完整解法，如表7所示。")
    table(["编号", "测试内容", "操作或输入", "预期结果"],
          [["TC01", "初始局面", "新建一个棋盘", "0～2 号位是兔子，3 号位为空，4～6 号位是乌龟"],
           ["TC02", "单步移动", "点击 2 号位的兔子", "3 号位变成兔子，2 号位变空，步数为 1"],
           ["TC03", "隔位跳跃", "点击 4 号位的乌龟（3 号有兔、2 号为空）", "乌龟落到 2 号位，记录被标记为“跳”"],
           ["TC04", "阻挡判定", "0 号兔子前面有动物、隔位也有动物时点击它", "返回 −1，棋盘没有任何变化"],
           ["TC05", "边界判定", "点击最左边的兔子向左、最右边的乌龟向右", "返回 −1，不会越界"],
           ["TC06", "方向规则", "分别读取兔子和乌龟的方向", "兔子是 +1（向右），乌龟是 −1（向左）"],
           ["TC07", "移动记录", "先走一格，再跳一格", "两条记录的 isJump 分别为 false 和 true"],
           ["TC08", "撤销", "连走 3 步后连续撤销 3 次", "局面和步数都回到开局，撤销栈为空"],
           ["TC09", "重新开始", "走若干步后点“重新开始”", "步数归零、栈清空、局面复位"],
           ["TC10", "最优解", "按 15 步的走法走完", "第 14 步时未完成，第 15 步后判定为完成"]],
          [1.4, 2.8, 6.6, 5.8], cap="表7　模型层的测试用例", first_col_left=False)

    h2("5.3　测试结果")
    body("在命令行里运行 animalgame.test.GameModelTest，输出如下：")
    code("""[通过] 初始局面：左三兔、中间空、右三龟
[通过] 单步移动：2 号位兔子走到 3 号空位
[通过] 隔位跳跃：4 号位乌龟跳过 3 号位兔子落到 2 号位
[通过] 阻挡判定：前方与隔位都被占时不能移动
[通过] 边界判定：位于两端的动物不会越界移动
[通过] 方向规则：兔子向右、乌龟向左
[通过] 移动记录：能区分单步与跨格跳
[通过] 撤销：逐级回退并最终恢复初始局面
[通过] 重新开始：步数归零、历史清空、局面复位
[通过] 最优解：15 步完成换位并被判为胜利

测试完成：共 10 项，通过 10 项，失败 0 项。""", size=9)
    body("从输出看，10 条用例全部通过，说明模型的移动规则、撤销和胜负判断都是对的，表1里与规则有关的要求都已实现。")

    h2("5.4　界面与操作测试")
    body("自动测试只能证明“算得对”，界面还得亲手点。图6 是走了一部分之后的中盘局面，表8 记录了界面部分的测试情况。")
    figure("shot_board_mid.png", 12.2, "图6　游戏进行中的中盘局面")
    table(["测试项", "操作", "预期结果", "实际结果"],
          [["点击动物", "点击 2 号位的兔子", "兔子平滑地走到 3 号位，步数加 1", "与预期一致"],
           ["跳越动画", "点击 4 号位的乌龟", "乌龟从 3 号兔子上方跳过，落在 2 号位", "与预期一致"],
           ["无效点击", "点击被挡住的动物", "该格闪红，状态栏出现红字提示，步数不变", "与预期一致"],
           ["悬停提示", "鼠标移到可走的动物上", "落点格子显示绿色虚线框", "与预期一致"],
           ["撤销", "点击“撤销”按钮", "退回上一步，步数减 1；无可撤销时按钮变灰", "与预期一致"],
           ["重新开始", "点击“重新开始”按钮", "恢复开局，步数归零，按钮状态正确", "与预期一致"],
           ["胜利提示", "按 15 步走完", "弹出对话框提示成功，并显示所用步数", "与预期一致"],
           ["快捷键", "按 Ctrl+Z、Ctrl+R、F1", "分别执行撤销、重开、显示玩法说明", "与预期一致"]],
          [2.6, 4.6, 6.2, 3.2], cap="表8　界面与操作的测试情况", first_col_left=True)

    h2("5.5　测试结论")
    body("测试结果表明：程序实现了表1中列出的全部功能；移动规则与理论分析一致（最少 15 步）；撤销和重新开始可以"
         "反复使用，多次操作后状态依然正确；界面上的提示、动画、按钮状态都符合预期；连续快速点击不会让程序错乱。"
         "程序达到了任务书的要求。")


# ================================================================== 第 6 章
def chapter6():
    h1("6　结　论", center=True)

    h2("6.1　课程设计中遇到的主要问题和解决方法")
    body("整个课设过程中遇到的问题不少，下面挑几个印象深的记下来，也算给以后的自己留个备忘。")
    num_item(1, "动画还没播完就点下一只动物，画面和数据会打架。一开始为了让动画顺畅，没管点击，结果前一步还在飞、"
                "后一步已经把数据改了，画面停在半路。后来在控制器里加了一个“正在动画”的判断，动画没播完就忽略点击，"
                "问题就消失了。")
    num_item(2, "撤销之后界面没跟着变。撤销改的是模型，界面上的步数和按钮状态得自己刷新，一开始只在部分地方刷新，"
                "于是出现了“数据已经回退、步数还停在原来”的情况。后来把刷新集中写成一个方法，每次操作结束都调用一次，"
                "就不会漏了。")
    num_item(3, "点空格子会报错。最初写点击处理时，不管点到的格子里有没有动物都往下算，点到中间的空位就出现"
                "空指针异常，程序直接退出。后来在取到动物之后先判断是不是 null，是就直接返回，不再往下走。")
    num_item(4, "命令行里中文变成乱码、编译报“编码 GBK 的不可映射字符”。原因是源文件是 UTF-8，而编译器和运行时的"
                "默认编码跟它不一致。解决办法是编译时加 -encoding UTF-8，运行时指定输出的编码。")
    num_item(5, "双击 run.bat 时中文提示变成乱码、还提示命令找不到。批处理文件如果存成 UTF-8，而命令行按系统本地编码"
                "逐字节去读，其中的中文就会被切坏。改成用 GBK 保存，并在开头执行 chcp 936，问题就解决了。")
    num_item(6, "用 javadoc 生成 API 文档时报“目标目录不可写”。查了半天发现是目标目录里已经有上一次的文件，"
                "换成一个新目录生成、再把新目录改回原来的名字就好了。")

    h2("6.2　创新和得意之处")
    body("这次课设里，自己比较满意的有下面几点：")
    num_item(1, "把“能不能走”单独抽成一个规则接口，棋盘只负责搬动物。以后想加“连跳两格”或者“只能走奇数格”之类的玩法，"
                "只要再写一个规则类，棋盘和界面一行都不用改。")
    num_item(2, "兔子和乌龟没有用图片，而是用 Java2D 拼出来的矢量图形，放大窗口也不会模糊，还省掉了图片资源。")
    num_item(3, "移动动画做了缓动和抛物线：走一格是贴着格子平移，跳一格会明显抬起来，看画面就能分清是走还是跳。")
    num_item(4, "模型完全不依赖界面，所以在没有打开窗口的情况下也能跑测试，10 条用例一秒钟跑完，改完代码立刻能验证。")
    num_item(5, "界面上的一些小细节——鼠标悬停时用绿色虚线框预告落点、无效点击时闪红并给红字提示、"
                "Ctrl+Z 撤销、步数与最少步数对照显示——让程序比“能玩”更好用一点。")
    num_item(6, "每个类、每个方法都写了中文注释，用 javadoc 可以直接生成网页版的 API 文档，别人接手时不用从头读代码。")

    h2("6.3　存在的不足和进一步改进的设想")
    body("程序虽然能用，但离“一个完整的游戏”还差得远，主要不足有：")
    num_item(1, "目前固定是 3 对动物、7 个格子，想换成 4 对或 5 对，得改常量、还得把窗口宽度一起调，"
                "没有做成开始界面里可选。")
    num_item(2, "没有“提示下一步”和“自动求解”。卡住的时候只能自己试，如果能给出下一步该怎么走，会更容易上手。")
    num_item(3, "动画时长、配色、字体都写死在代码里，用户不能调；做一套“设置”窗口会更友好。")
    num_item(4, "没有保存进度和成绩记录，关掉窗口就什么都没了，可以加上“保存当前局面”和“最少步数排行”。")
    num_item(5, "界面是按 100% 缩放设计的，在高分屏上字会显得偏小，需要按屏幕缩放比例调整。")
    num_item(6, "测试只覆盖了模型，界面部分还是靠手工点，有条件可以补一些自动化的界面测试。")


# ================================================================== 第 7 章
def chapter7():
    h1("7　心得体会", center=True)
    body("这次课设从读任务书到交报告，前后两个星期。刚开始觉得题目不难——不就是点一下走一步吗，真正动手才发现，"
         "“规则想清楚”和“代码写正确”之间隔着不少坑。最典型的是动画：为了让移动看起来自然，我给每一步加了 0.26 秒的"
         "过渡，结果忘了处理“动画期间又点了一下”的情况，画面和数据就对不上了。后来加了判断才明白，"
         "凡是“有时间的过程”，都要考虑过程中的状态。")
    body("第二个感受是“分开写”真的省事。一开始我把判断和绘制混在一个类里，改一个提示颜色都要小心翼翼，"
         "生怕碰坏规则。后来按模型、界面、控制三层拆开，规则可以单独用测试程序跑，界面改颜色、改圆角都碰不到规则，"
         "心里踏实很多。特别是那 10 条测试用例，写完以后每次改代码跑一遍，几秒钟就知道有没有改坏，比用手点可靠得多。")
    body("第三个感受是关于“细节”。老师看的是最终效果，而最终效果往往由细节决定：鼠标移上去有没有提示、"
         "点错了有没有反馈、按钮在没有可撤销步骤时会不会变灰、跳的时候能不能看出是在跳。这些都不难，但要一条条想到、"
         "一条条做出来。做完这些，程序才从“能跑”变成“好用”。")
    body("最后是文档。以前写代码很少写注释，这次要求每个类、每个方法都写清楚，还要生成 API 文档，一开始觉得麻烦，"
         "写到后面反而觉得轻松——过两天再回来看代码，注释直接告诉我这个方法在干什么，省了重新读一遍的时间。"
         "总的来说，这次课设让我把一学期学的东西真正串起来用了一遍，也知道了自己在大程序组织、异常处理这些方面"
         "还需要多练。")


# ================================================================== 第 8 章
def chapter8():
    h1("8　参 考 文 献", center=True)
    refs = [
        "[1] 耿祥义, 张跃平. Java 2 实用教程[M]. 6 版. 北京: 清华大学出版社, 2019.",
        "[2] 李兴华. Java 开发实战经典[M]. 北京: 清华大学出版社, 2018.",
        "[3] 明日科技. Java 从入门到精通[M]. 5 版. 北京: 清华大学出版社, 2019.",
        "[4] Cay S. Horstmann. Java 核心技术 卷Ⅰ 基础知识[M]. 11 版. 林琪, 苏钰涵, 译. 北京: 机械工业出版社, 2019.",
        "[5] 张海藩, 牟永敏. 软件工程导论[M]. 6 版. 北京: 清华大学出版社, 2013.",
        "[6] Oracle. The Java Tutorials: Creating a GUI With Swing[EB/OL]. "
        "https://docs.oracle.com/javase/tutorial/uiswing/, 2024.",
        "[7] Oracle. Java Platform, Standard Edition 17 API Specification[EB/OL]. "
        "https://docs.oracle.com/en/java/javase/17/docs/api/, 2024.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = Pt(18)
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-1.0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(ref)
        set_font(r, size=12)


# ================================================================== 附录
def appendix():
    h1("附录 A　完整源程序")
    body("下面按包和文件的顺序列出全部源程序，文件名与表6一致。代码中的注释就是代码的说明，"
         "生成 API 文档时也直接使用这些注释。")
    files = [
        ("Main.java", "程序入口", "animalgame/Main.java"),
        ("Animal.java", "动物的抽象父类", "animalgame/model/Animal.java"),
        ("Direction.java", "方向枚举", "animalgame/model/Direction.java"),
        ("LeftAnimal.java", "兔子", "animalgame/model/LeftAnimal.java"),
        ("RightAnimal.java", "乌龟", "animalgame/model/RightAnimal.java"),
        ("MoveRule.java", "移动规则接口", "animalgame/model/MoveRule.java"),
        ("StandardMoveRule.java", "标准的移动规则", "animalgame/model/StandardMoveRule.java"),
        ("MoveRecord.java", "移动记录", "animalgame/model/MoveRecord.java"),
        ("Board.java", "棋盘", "animalgame/model/Board.java"),
        ("Theme.java", "配色与字体", "animalgame/view/Theme.java"),
        ("AnimalRenderer.java", "动物的矢量绘制", "animalgame/view/AnimalRenderer.java"),
        ("RoundButton.java", "圆角按钮", "animalgame/view/RoundButton.java"),
        ("BoardPanel.java", "棋盘面板", "animalgame/view/BoardPanel.java"),
        ("GameFrame.java", "主窗口", "animalgame/view/GameFrame.java"),
        ("GameController.java", "控制器", "animalgame/controller/GameController.java"),
        ("GameModelTest.java", "模型测试程序", "animalgame/test/GameModelTest.java"),
        ("PreviewTool.java", "界面截图工具", "animalgame/tools/PreviewTool.java"),
    ]
    for i, (name, desc, path) in enumerate(files, 1):
        h2("A.%d　%s（%s）" % (i, name, desc))
        with open(src(path), encoding="utf-8") as fp:
            text = fp.read().replace("\r\n", "\n").rstrip("\n")
        code(text, size=7.5, boxed=False)


# ================================================================== 主流程
def main():
    cover()
    start_numbered_section()
    toc_page()
    page_break()
    chapter1()
    chapter2()
    chapter3()
    chapter4()
    chapter5()
    chapter6()
    chapter7()
    chapter8()
    appendix()
    doc.save(OUT)

    heads = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    print("saved", OUT)
    print("段落 %d，表格 %d，插图 %d" % (len(doc.paragraphs), len(doc.tables), len(doc.inline_shapes)))
    print("标题 %d 个：" % len(heads))
    for h in heads:
        print("   ", h)


if __name__ == "__main__":
    main()



