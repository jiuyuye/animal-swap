# -*- coding: utf-8 -*-
"""把报告 docx 的第一页（封面）替换成学校实验报告封面。

用法：
    python replace_cover.py <报告.docx> <封面.docx> <输出.docx>

做法：
    1. 从封面文档里取出全部段落（封面没有表格和图片）与它的节属性 sectPr；
    2. 在报告文档里找到"第一页"的边界（第一个带 w:sectPr 的段落），把它之前的
       内容整段删除——也就是删掉原来自制的封面；
    3. 把封面的段落原样复制到开头，再补一个只带节属性的空段落，让封面单独成为一节；
    4. 封面用封面自己的页边距（因为封面上的字段是靠空格对齐的），正文那一节保持原样；
    5. 封面节的页眉页脚引用去掉（原封面的页眉是空的，留着会传给正文各页）。
"""

import copy
import sys

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

CT_HEADER = "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"

# 学校封面的顶端有一条横线，它其实来自"页眉"样式的下框线。
# 复制段落带不过样式，所以这里把横线直接写进页眉部件里。
COVER_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    "<w:p><w:pPr>"
    '<w:pBdr><w:bottom w:val="single" w:color="auto" w:sz="6" w:space="1"/></w:pBdr>'
    '<w:jc w:val="center"/>'
    "</w:pPr>"
    '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"'
    ' w:eastAsia="宋体" w:cs="Times New Roman"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    '<w:t xml:space="preserve"> </w:t></w:r></w:p>'
    "</w:hdr>"
).encode("utf-8")

# 正文各页不需要横线，所以正文那一节挂一个空页眉，切断从封面继承。
EMPTY_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    "<w:p/></w:hdr>"
).encode("utf-8")


def load(name):
    return Document(name)


def find_first_section_break(body):
    """返回第一个带 w:sectPr 的段落下标，找不到返回 -1。"""
    for index, child in enumerate(body):
        if child.tag != qn("w:p"):
            continue
        ppr = child.find(qn("w:pPr"))
        if ppr is not None and ppr.find(qn("w:sectPr")) is not None:
            return index
    return -1


def strip_refs(sect_pr):
    """去掉页眉页脚引用，避免把封面的页眉继承给后面每一页。"""
    for tag in ("w:headerReference", "w:footerReference"):
        for node in sect_pr.findall(qn(tag)):
            sect_pr.remove(node)


def fix_styles(element, id_map, known_ids):
    """按"样式名"重新映射样式 id，映射不到就删掉引用、回落到默认样式。

    两个文档的样式编号并不通用：封面里的 "7" 是"正文缩进"，而报告里的 "7"
    是"标题 5"，直接照抄会让封面段落变成标题。
    """
    for pstyle in element.iter(qn("w:pStyle")):
        val = pstyle.get(qn("w:val"))
        new_id = id_map.get(val)
        if new_id is None or new_id not in known_ids:
            pstyle.getparent().remove(pstyle)
        else:
            pstyle.set(qn("w:val"), new_id)
    for rstyle in element.iter(qn("w:rStyle")):
        val = rstyle.get(qn("w:val"))
        new_id = id_map.get(val)
        if new_id is None or new_id not in known_ids:
            rstyle.getparent().remove(rstyle)
        else:
            rstyle.set(qn("w:val"), new_id)


DEFAULT_FONTS = {
    "ascii": "Times New Roman",
    "hAnsi": "Times New Roman",
    "eastAsia": "宋体",
    "cs": "Times New Roman",
}


def apply_default_fonts(element):
    """封面里的文字原本靠"文档默认字体"（Times New Roman + 宋体）显示。

    报告文档的默认字体是主题字体（等线），搬过来会让封面的字变样，
    所以这里把封面自己的默认字体写成显式字体。
    """
    for rpr in list(element.iter(qn("w:rPr"))):
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.insert(0, rfonts)
        for key in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
            attr = qn("w:" + key)
            if attr in rfonts.attrib:
                del rfonts.attrib[attr]
        for key, value in DEFAULT_FONTS.items():
            if rfonts.get(qn("w:" + key)) is None:
                rfonts.set(qn("w:" + key), value)


def add_header_part(document, name, blob):
    """把一段页眉 XML 作为新部件加进文档，返回关系 id。"""
    part = Part(PackURI("/word/" + name), CT_HEADER, blob, document.part.package)
    return document.part.relate_to(part, RT.HEADER)


def set_header_reference(sect_pr, rid):
    """在 sectPr 里加上页眉引用（必须排在 footerReference 之前）。"""
    ref = OxmlElement("w:headerReference")
    ref.set(qn("w:type"), "default")
    ref.set(qn("r:id"), rid)
    sect_pr.insert(0, ref)


def main():
    report_path, cover_path, out_path = sys.argv[1:4]

    cover = load(cover_path)
    cover_body = cover.element.body
    cover_sect = copy.deepcopy(cover_body.find(qn("w:sectPr")))
    strip_refs(cover_sect)
    cover_parts = [copy.deepcopy(node) for node in cover_body if node.tag == qn("w:p")]

    report = load(report_path)
    body = report.element.body
    known_ids = {style.style_id for style in report.styles}
    by_name = {style.name: style.style_id for style in report.styles}
    id_map = {}
    for style in cover.styles:
        target_id = by_name.get(style.name)
        if target_id:
            id_map[style.style_id] = target_id

    cut = find_first_section_break(body)
    if cut < 0:
        raise SystemExit("没找到封面与正文之间的分节符，请检查文档结构")
    old = list(body)[: cut + 1]
    for node in old:
        body.remove(node)

    for offset, node in enumerate(cover_parts):
        fix_styles(node, id_map, known_ids)
        apply_default_fonts(node)
        body.insert(offset, node)

    # 让封面单独成一节：一个只带 sectPr 的空段落
    sect_para = copy.deepcopy(old[cut])
    for node in list(sect_para):
        if node.tag != qn("w:pPr"):
            sect_para.remove(node)
    ppr = sect_para.find(qn("w:pPr"))
    for node in list(ppr):
        if node.tag != qn("w:sectPr"):
            ppr.remove(node)
    for node in list(ppr.find(qn("w:sectPr"))):
        ppr.find(qn("w:sectPr")).remove(node)
    for node in cover_sect:
        ppr.find(qn("w:sectPr")).append(copy.deepcopy(node))
    body.insert(len(cover_parts), sect_para)

    # 封面那一节挂"带横线"的页眉；正文那一节挂空页眉，免得横线跑到每一页顶上。
    cover_rid = add_header_part(report, "header1.xml", COVER_HEADER)
    body_rid = add_header_part(report, "header2.xml", EMPTY_HEADER)
    set_header_reference(ppr.find(qn("w:sectPr")), cover_rid)
    set_header_reference(body.find(qn("w:sectPr")), body_rid)

    report.save(out_path)
    print("已写出：", out_path)


if __name__ == "__main__":
    main()
