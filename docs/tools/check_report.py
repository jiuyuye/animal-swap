# -*- coding: utf-8 -*-
"""检查生成的课程设计报告 .docx 是否有格式/编号/引用方面的问题（不依赖 Word）。"""
import os
import re
import sys
import unicodedata
import zipfile

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Twips

ROOT = r"C:\Users\mjqqd\Documents\deepseek-harness\default-workspace\动物换位"
DOCX = os.path.join(ROOT, "Java课程设计报告-动物换位.docx")
TEXT_W = 21 - 2.2 * 2          # 版心宽 16.6cm
errors, warns, notes = [], [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


def note(msg):
    notes.append(msg)


def em_width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


# ---------------------------------------------------------------- 1. 包完整性
if not os.path.exists(DOCX):
    sys.exit("找不到 %s" % DOCX)
size = os.path.getsize(DOCX)
with zipfile.ZipFile(DOCX) as z:
    bad = z.testzip()
    if bad:
        err("压缩包内文件损坏：%s" % bad)
    names = z.namelist()
    media = [n for n in names if n.startswith("word/media/")]
    note("文件 %.1f KB，压缩包内 %d 个部件，图片 %d 张" % (size / 1024.0, len(names), len(media)))
    xml = z.read("word/document.xml").decode("utf-8")
    footers = [z.read(n).decode("utf-8") for n in names if re.match(r"word/footer\d*\.xml$", n)]

doc = Document(DOCX)

# ---------------------------------------------------------------- 2. 段落/表格
paras = doc.paragraphs
texts = [p.text.strip() for p in paras]
cell_text = []
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            cell_text.append(c.text)
all_text = "\n".join(texts + cell_text)

FIG_CAP = re.compile(r"^图\s*\d+\u3000")
TAB_CAP = re.compile(r"^表\s*\d+\u3000")
fig_caps = [(i, t) for i, t in enumerate(texts) if FIG_CAP.match(t)]
tab_caps = [(i, t) for i, t in enumerate(texts) if TAB_CAP.match(t)]
note("段落 %d，表格 %d，插图 %d，图题 %d，表题 %d"
     % (len(paras), len(doc.tables), len(doc.inline_shapes), len(fig_caps), len(tab_caps)))

# 图题与插图数量必须一致
if len(fig_caps) != len(doc.inline_shapes):
    err("图题数量（%d）与插图数量（%d）不一致" % (len(fig_caps), len(doc.inline_shapes)))

# 编号连续
for label, caps in (("图", fig_caps), ("表", tab_caps)):
    nums = [int(re.match(r"^%s\s*(\d+)" % label, t).group(1)) for _, t in caps]
    if nums != list(range(1, len(nums) + 1)):
        err("%s编号不连续：%s" % (label, nums))
    else:
        note("%s编号连续：1～%d" % (label, len(nums)))

# 每个图/表都要在正文里被引用
cap_idx = {i for i, _ in fig_caps} | {i for i, _ in tab_caps}
body_text = "\n".join(t for i, t in enumerate(texts) if i not in cap_idx)
for label, caps in (("图", fig_caps), ("表", tab_caps)):
    for n in range(1, len(caps) + 1):
        pat = r"%s\s*%d(?!\d)" % (label, n)
        if not re.search(pat, body_text):
            err("正文里没有引用 %s%d" % (label, n))

# 图题必须在图下方、表题在表格上方（按文档顺序检查：图题紧跟在插图所在段落之后）
body = doc.element.body
order = []
for child in body.iterchildren():
    if child.tag == qn("w:p"):
        has_pic = child.findall(".//" + qn("w:drawing"))
        txt = "".join(t.text or "" for t in child.iter(qn("w:t"))).strip()
        if has_pic:
            order.append(("pic", txt))
        elif re.match(r"^图\s*\d+", txt):
            order.append(("figcap", txt))
        elif re.match(r"^表\s*\d+", txt):
            order.append(("tabcap", txt))
        elif txt:
            order.append(("text", txt))
    elif child.tag == qn("w:tbl"):
        order.append(("tbl", ""))

for k, (kind, txt) in enumerate(order):
    if kind == "pic":
        nxt = order[k + 1][0] if k + 1 < len(order) else None
        if nxt != "figcap":
            err("插图后面没有紧跟图题：%s" % (order[k + 1][1][:20] if k + 1 < len(order) else "文末"))

# 封面两张表不参与"表题在表格上方"的检查：重新按顺序核对，跳过前两个 tbl
tbl_seen = 0
for k, (kind, txt) in enumerate(order):
    if kind != "tbl":
        continue
    tbl_seen += 1
    if tbl_seen <= 2:
        continue
    if k == 0 or order[k - 1][0] != "tabcap":
        err("第 %d 张表格上方没有紧跟表题" % tbl_seen)

# ---------------------------------------------------------------- 3. 字体与字号
for p in paras:
    if p.style.name.startswith("Heading"):
        continue
    if not p.text.strip():
        continue
    for r in p.runs:
        sz = r.font.size.pt if r.font.size else None
        if sz is None:
            err("有文字没有显式字号：%r" % p.text[:30])
        elif sz not in (12, 10.5, 9, 7.5, 32, 26, 15, 14):
            warn("字号 %.1fpt 不在预期范围：%r" % (sz, p.text[:30]))
        color = r.font.color.rgb if r.font.color and r.font.color.rgb else None
        if color is not None and str(color) != "000000":
            err("文字颜色不是黑色：%r -> %s" % (p.text[:30], color))

# 标题字号
for p in paras:
    if p.style.name == "Heading 1":
        for r in p.runs:
            if r.font.size and r.font.size.pt != 15:
                err("一级标题不是小3号(15pt)：%s" % p.text)
    if p.style.name == "Heading 2":
        for r in p.runs:
            if r.font.size and r.font.size.pt != 14:
                err("二级标题不是4号(14pt)：%s" % p.text)

# ---------------------------------------------------------------- 4. 表格宽度
for i, t in enumerate(doc.tables, 1):
    grid = t._tbl.tblGrid.findall(qn("w:gridCol"))
    total = sum(int(gc.get(qn("w:w"))) for gc in grid) / 1440.0 * 2.54
    if i <= 2:
        note("封面第 %d 张表宽度 %.2f cm" % (i, total))
    elif abs(total - TEXT_W) > 0.3:
        err("第 %d 张表总宽 %.2f cm，应为 %.2f cm" % (i, total, TEXT_W))

# ---------------------------------------------------------------- 5. 代码块是否超宽
code_bad = 0
for p in paras:
    if not p.runs or p.runs[0].font.name != "Consolas":
        continue
    li = p.paragraph_format.left_indent.cm if p.paragraph_format.left_indent else 0
    ri = p.paragraph_format.right_indent.cm if p.paragraph_format.right_indent else 0
    avail = TEXT_W - li - ri
    size_pt = p.runs[0].font.size.pt
    for line in p.text.split("\n"):
        w = em_width(line) * size_pt / 72.0 * 2.54
        if w > avail + 0.05:
            code_bad += 1
            if code_bad <= 5:
                err("代码行超宽（%.2fcm > %.2fcm，%.1fpt）：%s" % (w, avail, size_pt, line[:50]))
if code_bad > 5:
    err("……另有 %d 行代码超宽" % (code_bad - 5))
if code_bad == 0:
    note("所有代码行都在版心宽度以内")

# ---------------------------------------------------------------- 6. 域与页码
if "TOC \\o" not in xml and 'TOC \\o' not in xml:
    if "TOC" not in xml:
        err("没有目录域（TOC）")
if not any("PAGE" in f for f in footers):
    err("页脚里没有页码域（PAGE）")
else:
    note("页脚里共 %d 个页码域" % sum(f.count("PAGE") for f in footers))
if doc.sections[0].footer.is_linked_to_previous is False:
    note("封面页脚与正文分离")
if len(doc.sections) < 2:
    err("没有分节（封面应当单独一节）")
else:
    note("共 %d 节；正文第一节带页码起始设置" % len(doc.sections))

# ---------------------------------------------------------------- 7. 内容自查
for bad in ["×××", "这些要删", "TODO", "待补", "占位", "lorem"]:
    if bad in all_text:
        err("正文里残留占位文字：%s" % bad)

for must in ["中南林业科技大学", "设计名称", "指导教师评定情况", "综合评语及成绩",
             "设计概述", "总体设计", "详细设计", "软件实现", "测试", "结　论",
             "心得体会", "参 考 文 献"]:
    if must not in all_text:
        err("缺少必需内容：%s" % must)

# 章标题顺序
heads = [p.text.strip() for p in paras if p.style.name == "Heading 1"]
expect_order = ["1　设计概述", "2　总体设计", "3　详细设计", "4　软件实现", "5　测试",
                "6　结　论", "7　心得体会", "8　参 考 文 献", "附录 A　完整源程序"]
if heads != expect_order:
    err("章标题不符合预期：%s" % heads)
else:
    note("章标题顺序正确（共 %d 章 + 附录）" % (len(heads) - 1))

# 附录文件数
appendix_heads = [p.text for p in paras if p.style.name == "Heading 2" and p.text.startswith("A.")]
if len(appendix_heads) != 17:
    err("附录里只列了 %d 个源文件，应为 17 个" % len(appendix_heads))
else:
    note("附录包含 17 个源文件（A.1～A.17）")

# 正文里应当提到"如图N所示""如表N所示"这类引用
ref_pat = re.compile(r"(如)?[图表]\s*\d+")
note("正文中的图表引用共 %d 处" % len(ref_pat.findall(body_text)))

# 字数统计（正文中文字符）
cn = len(re.findall(r"[\u4e00-\u9fa5]", body_text))
note("正文汉字约 %d 字（不含代码与表格）" % cn)

# ---------------------------------------------------------------- 输出
print("=" * 60)
for n in notes:
    print("[信息]", n)
for w in warns:
    print("[提醒]", w)
for e in errors:
    print("[错误]", e)
print("=" * 60)
print("检查完成：错误 %d 个，提醒 %d 个。" % (len(errors), len(warns)))
sys.exit(1 if errors else 0)
