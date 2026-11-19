# -*- coding: utf-8 -*-
"""生成课程设计说明书需要的插图：UML 类图、算法流程图、程序流程图。"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2
FONT_R = r"C:\Windows\Fonts\msyh.ttc"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"

TXT = (31, 41, 55)
MUTED = (107, 114, 128)
LINE = (71, 85, 105)

MODEL_HDR = (219, 234, 254)
MODEL_BRD = (59, 111, 212)
VIEW_HDR = (220, 243, 228)
VIEW_BRD = (46, 158, 91)
CTRL_HDR = (253, 232, 214)
CTRL_BRD = (217, 119, 6)

_fcache = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(FONT_B if bold else FONT_R, int(size * S))
    return _fcache[key]


def wrap(text, size, bold, maxw):
    """按单词优先折行；单个单词过长时再按字符切分。"""
    f = font(size, bold)
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            cand = (line + " " + word).strip()
            if f.getlength(cand) / S <= maxw:
                line = cand
                continue
            if line:
                out.append(line)
            while f.getlength(word) / S > maxw:
                cut = len(word)
                while cut > 1 and f.getlength(word[:cut]) / S > maxw:
                    cut -= 1
                out.append(word[:cut])
                word = word[cut:]
            line = word
        out.append(line)
    return out


class Cv:
    def __init__(self, w, h, bg="#FFFFFF"):
        self.W, self.H = w, h
        self.img = Image.new("RGB", (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.img)

    # ---------- primitives ----------
    def rr(self, x, y, w, h, r, fill, outline=None, width=2):
        self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S],
                                 radius=r * S, fill=fill, outline=outline,
                                 width=max(1, int(width * S)))

    def ell(self, x, y, w, h, fill, outline=None, width=2):
        self.d.ellipse([x * S, y * S, (x + w) * S, (y + h) * S],
                       fill=fill, outline=outline, width=max(1, int(width * S)))

    def ln(self, pts, color=LINE, width=2, dash=None):
        for i in range(len(pts) - 1):
            self._seg(pts[i], pts[i + 1], color, width, dash)

    def _seg(self, p, q, color, width, dash):
        (x1, y1), (x2, y2) = p, q
        w = max(1, int(width * S))
        if not dash:
            self.d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=color, width=w)
            return
        dx, dy = x2 - x1, y2 - y1
        dist = (dx * dx + dy * dy) ** 0.5
        if dist == 0:
            return
        ux, uy = dx / dist, dy / dist
        t = 0.0
        on = True
        while t < dist:
            step = min(dash if on else dash * 0.75, dist - t)
            if on:
                self.d.line([(x1 + ux * t) * S, (y1 + uy * t) * S,
                             (x1 + ux * (t + step)) * S, (y1 + uy * (t + step)) * S],
                            fill=color, width=w)
            t += step
            on = not on

    def poly(self, pts, fill, outline=None, width=2):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill,
                       outline=outline, width=max(1, int(width * S)))

    def txt(self, x, y, s, size=19, bold=False, fill=TXT, maxw=None, lh=1.5):
        lines = wrap(s, size, bold, maxw) if maxw else s.split("\n")
        f = font(size, bold)
        step = size * lh
        y0 = y - (len(lines) - 1) * step / 2
        for i, line in enumerate(lines):
            self.d.text((x * S, (y0 + i * step) * S), line, font=f, fill=fill, anchor="mm")

    def ltxt(self, x, y, s, size=16, bold=False, fill=MUTED):
        self.d.text((x * S, y * S), s, font=font(size, bold), fill=fill, anchor="lm")

    # ---------- arrows ----------
    def arrow(self, tip, d, kind="open", color=LINE, size=13):
        x, y = tip
        if kind == "open":
            if d == "up":
                pts = [(x - size * 0.6, y + size), (x, y), (x + size * 0.6, y + size)]
            elif d == "down":
                pts = [(x - size * 0.6, y - size), (x, y), (x + size * 0.6, y - size)]
            elif d == "left":
                pts = [(x + size, y - size * 0.6), (x, y), (x + size, y + size * 0.6)]
            else:
                pts = [(x - size, y - size * 0.6), (x, y), (x - size, y + size * 0.6)]
            self.ln(pts, color, 2)
        elif kind == "filled":
            if d == "up":
                pts = [(x, y), (x - size * 0.62, y + size), (x + size * 0.62, y + size)]
            elif d == "down":
                pts = [(x, y), (x - size * 0.62, y - size), (x + size * 0.62, y - size)]
            elif d == "left":
                pts = [(x, y), (x + size, y - size * 0.62), (x + size, y + size * 0.62)]
            else:
                pts = [(x, y), (x - size, y - size * 0.62), (x - size, y + size * 0.62)]
            self.poly(pts, color, color, 1)
        elif kind == "hollow":
            if d == "up":
                pts = [(x, y), (x - size * 0.7, y + size * 1.15), (x + size * 0.7, y + size * 1.15)]
            elif d == "down":
                pts = [(x, y), (x - size * 0.7, y - size * 1.15), (x + size * 0.7, y - size * 1.15)]
            elif d == "left":
                pts = [(x, y), (x + size * 1.15, y - size * 0.7), (x + size * 1.15, y + size * 0.7)]
            else:
                pts = [(x, y), (x - size * 1.15, y - size * 0.7), (x - size * 1.15, y + size * 0.7)]
            self.poly(pts, "#FFFFFF", color, 2)

    def diamond(self, cx, cy, w, h, fill, outline, width=2):
        self.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
                  fill, outline, width)

    def label(self, x, y, s, size=16, fill=MUTED):
        f = font(size)
        tw = f.getlength(s) / S
        self.rr(x - tw / 2 - 4, y - 12, tw + 8, 24, 5, "#FFFFFF")
        self.d.text((x * S, y * S), s, font=f, fill=fill, anchor="mm")

    def save(self, path):
        self.img = self.img.resize((self.W, self.H), Image.LANCZOS)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.img.save(path, "PNG")
        print("saved", path, self.img.size)


# ---------------- UML ----------------
def class_box(cv, x, y, w, name, stereo, fields, methods, hdr, brd):
    lh, pad = 25, 10
    if stereo:
        head = 66
    else:
        head = 48
    # 超长成员自动折行，保证文字不越出类框
    flines = []
    for f in fields:
        flines.extend(wrap(f, 16, False, w - 24))
    mlines = []
    for m in methods:
        mlines.extend(wrap(m, 16, False, w - 24))
    fields, methods = flines, mlines
    h = head + (len(fields) * lh + pad if fields else 0) + (len(methods) * lh + pad if methods else 0)

    cv.rr(x + 3, y + 4, w, h, 10, (243, 244, 246))
    cv.rr(x, y, w, h, 10, "#FFFFFF", brd, 2)
    cv.rr(x, y, w, head, 10, hdr, None)
    cv.d.rectangle([x * S, (y + head - 12) * S, (x + w) * S, (y + head) * S], fill=hdr)
    cv.ln([(x, y + head), (x + w, y + head)], brd, 2)
    if stereo:
        cv.txt(x + w / 2, y + 21, stereo, 15, False, (90, 100, 115))
        cv.txt(x + w / 2, y + 45, name, 21, True, (17, 24, 39))
    else:
        cv.txt(x + w / 2, y + 24, name, 21, True, (17, 24, 39))

    cy = y + head
    if fields:
        cv.ln([(x, cy + len(fields) * lh + pad / 2), (x + w, cy + len(fields) * lh + pad / 2)],
              (203, 213, 225), 1.5)
        for i, f in enumerate(fields):
            cv.ltxt(x + 12, cy + pad / 2 + i * lh + lh / 2 - 2, f, 16)
        cy += len(fields) * lh + pad
    elif methods:
        cy += pad
    for i, m in enumerate(methods):
        cv.ltxt(x + 12, cy + i * lh + lh / 2 - 2, m, 16)
    return dict(x=x, y=y, w=w, h=h, top=y, bottom=y + h, left=x, right=x + w,
                cx=x + w / 2, cy=y + h / 2)


def uml():
    cv = Cv(1700, 1730)
    # 图例
    for i, (t, hdr, brd) in enumerate([("model 模型层", MODEL_HDR, MODEL_BRD),
                                       ("view 视图层", VIEW_HDR, VIEW_BRD),
                                       ("controller 控制层", CTRL_HDR, CTRL_BRD)]):
        x = 60 + i * 210
        cv.rr(x, 26, 24, 20, 5, hdr, brd, 2)
        cv.ltxt(x + 32, 36, t, 16)

    animal = class_box(cv, 60, 90, 340, "Animal", "«abstract 抽象类»",
                       ["# position : int", "# homePosition : int"],
                       ["+ getDirection() : Direction", "+ getName() : String",
                        "+ getPosition() : int", "+ getHomePosition() : int",
                        "~ setPosition(int) : void"],
                       MODEL_HDR, MODEL_BRD)
    direction = class_box(cv, 470, 90, 250, "Direction", "«enumeration 枚举»",
                          ["+ LEFT(-1, \"向左\")", "+ RIGHT(+1, \"向右\")"],
                          ["+ getStep() : int", "+ getLabel() : String"],
                          MODEL_HDR, MODEL_BRD)
    moverule = class_box(cv, 740, 90, 340, "MoveRule", "«interface 接口»",
                         ["+ NO_MOVE : int = -1"],
                         ["+ resolveTarget(Animal, Animal[]) : int"],
                         MODEL_HDR, MODEL_BRD)
    record = class_box(cv, 1120, 90, 270, "MoveRecord", None,
                       ["- animal : Animal", "- from : int", "- to : int"],
                       ["+ getAnimal() : Animal", "+ getFrom() : int",
                        "+ getTo() : int", "+ isJump() : boolean"],
                       MODEL_HDR, MODEL_BRD)

    left = class_box(cv, 60, 430, 280, "LeftAnimal", None, [],
                     ["+ getDirection() : Direction", "+ getName() : String"],
                     MODEL_HDR, MODEL_BRD)
    right = class_box(cv, 380, 430, 280, "RightAnimal", None, [],
                      ["+ getDirection() : Direction", "+ getName() : String"],
                      MODEL_HDR, MODEL_BRD)
    std = class_box(cv, 740, 430, 340, "StandardMoveRule", None, [],
                    ["+ resolveTarget(Animal, Animal[]) : int", "- inside(int, int) : boolean"],
                    MODEL_HDR, MODEL_BRD)

    board = class_box(cv, 60, 720, 420, "Board", None,
                      ["- slots : Animal[7]", "- history : Deque<MoveRecord>",
                       "- moveRule : MoveRule", "- moveCount : int"],
                      ["+ reset() : void", "+ getAnimalAt(int) : Animal",
                       "+ getSlots() : Animal[]", "+ canMove(Animal) : boolean",
                       "+ resolveTarget(Animal) : int", "+ move(Animal) : MoveRecord",
                       "+ undo() : MoveRecord", "+ isSolved() : boolean",
                       "+ canUndo() : boolean", "+ getMoveCount() : int",
                       "+ countMovableAnimals() : int"],
                      MODEL_HDR, MODEL_BRD)

    frame = class_box(cv, 60, 1290, 320, "GameFrame", "«JFrame»",
                      ["- boardPanel : BoardPanel", "- stepsPill : JLabel",
                       "- statusLabel : JLabel", "- undoButton : RoundButton"],
                      ["+ setMoveCount(int) : void", "+ setStatus(String, boolean) : void",
                       "+ showWinDialog(int) : void", "+ showHelp() : void"],
                      VIEW_HDR, VIEW_BRD)
    panel = class_box(cv, 420, 1290, 320, "BoardPanel", "«JPanel»",
                      ["- board : Board", "- hoverIndex : int", "- animation : MoveAnimation"],
                      ["+ paintComponent(Graphics) : void",
                       "+ animateMove(Animal, int, int, Runnable) : void",
                       "+ flashInvalid(Animal) : void", "+ isAnimating() : boolean"],
                      VIEW_HDR, VIEW_BRD)
    btn = class_box(cv, 760, 1290, 280, "RoundButton", "«JButton»",
                    ["- hover : boolean"], ["+ paintComponent(Graphics) : void"],
                    VIEW_HDR, VIEW_BRD)
    renderer = class_box(cv, 1070, 1290, 290, "AnimalRenderer", None, [],
                         ["+ draw(Graphics2D, Animal, double, double, double) : void",
                          "- drawRabbit(Graphics2D) : void",
                          "- drawTurtle(Graphics2D) : void"],
                         VIEW_HDR, VIEW_BRD)
    theme = class_box(cv, 1395, 1290, 260, "Theme", "«工具类»",
                      ["+ ACCENT : Color", "+ HINT : Color",
                       "+ RABBIT_BODY : Color", "+ TURTLE_SHELL : Color"],
                      ["+ font(int, int) : Font"], VIEW_HDR, VIEW_BRD)

    ctrl = class_box(cv, 700, 720, 330, "GameController", None,
                     ["- board : Board", "- frame : GameFrame"],
                     ["+ onAnimalClicked(Animal) : void",
                      "+ actionPerformed(ActionEvent) : void",
                      "- undo() : void", "- restart() : void",
                      "- afterMove() : void", "- refresh(String) : void"],
                     CTRL_HDR, CTRL_BRD)
    main = class_box(cv, 1080, 720, 250, "Main", "«启动类»", [],
                     ["+ main(String[]) : void"], CTRL_HDR, CTRL_BRD)

    # 1 泛化：Animal -> LeftAnimal / RightAnimal
    cv.ln([(animal["cx"], animal["bottom"]), (animal["cx"], 390)], LINE, 2)
    cv.ln([(left["cx"], 390), (right["cx"], 390)], LINE, 2)
    cv.ln([(left["cx"], 390), (left["cx"], left["top"])], LINE, 2)
    cv.arrow((left["cx"], left["top"]), "down", "hollow")
    cv.ln([(right["cx"], 390), (right["cx"], right["top"])], LINE, 2)
    cv.arrow((right["cx"], right["top"]), "down", "hollow")

    # 2 实现：StandardMoveRule -.-|> MoveRule
    cv.ln([(std["cx"], std["top"]), (std["cx"], moverule["bottom"])], LINE, 2)
    cv.arrow((moverule["cx"], moverule["bottom"]), "up", "hollow")
    cv.label(moverule["cx"] + 70, (moverule["bottom"] + std["top"]) / 2 - 16, "«implements»")

    # 3 Animal -> Direction
    cv.ln([(animal["right"], 200), (direction["left"], 200)], LINE, 2)
    cv.arrow((direction["left"], 200), "right", "open")
    cv.label((animal["right"] + direction["left"]) / 2, 172, "方向 1")

    # 4 Board -> Animal（使用）
    cv.ln([(board["left"], 930), (44, 930), (44, 250), (animal["left"], 250)], LINE, 2)
    cv.arrow((animal["left"], 250), "right", "open")
    cv.label(44, 620, "持有")

    # 5 Board -> MoveRule（依赖）
    cv.ln([(board["right"], 770), (640, 770), (640, 180), (moverule["left"], 180)], LINE, 2)
    cv.arrow((moverule["left"], 180), "right", "open")
    cv.label(640, 300, "«use»")

    # 6 Board - MoveRecord（组合）
    cv.ln([(470, board["top"]), (470, 600), (680, 600), (680, 355), (record["cx"], 355),
           (record["cx"], record["bottom"])], LINE, 2)
    cv.arrow((record["cx"], record["bottom"]), "up", "open")
    cv.diamond(470, board["top"] - 13, 16, 26, "#FFFFFF", LINE, 2)
    cv.label(560, 578, "历史记录 0..*")

    # 7 控制器 -> Board
    cv.ln([(ctrl["left"], 860), (board["right"], 860)], LINE, 2)
    cv.arrow((board["right"], 860), "left", "open")
    cv.label(590, 845, "调用")

    # 8 控制器 -> BoardPanel
    cv.ln([(ctrl["cx"] - 20, ctrl["bottom"]), (ctrl["cx"] - 20, 1230),
           (panel["cx"], 1230), (panel["cx"], panel["top"])], LINE, 2)
    cv.arrow((panel["cx"], panel["top"]), "down", "open")

    # 9 控制器 -> GameFrame（虚线依赖）
    cv.ln([(ctrl["cx"] + 20, ctrl["bottom"]), (ctrl["cx"] + 20, 1252),
           (frame["cx"], 1252), (frame["cx"], frame["top"])], LINE, 2, dash=7)
    cv.arrow((frame["cx"], frame["top"]), "down", "open")

    # 10 Main -> GameController
    cv.ln([(main["left"], 780), (ctrl["right"], 780)], LINE, 2, dash=7)
    cv.arrow((ctrl["right"], 780), "left", "open")
    cv.label((main["left"] + ctrl["right"]) / 2, 762, "创建")

    # 11 GameFrame - BoardPanel（组合）
    cv.ln([(frame["right"], 1380), (panel["left"], 1380)], LINE, 2)
    cv.arrow((panel["left"], 1380), "right", "open")
    cv.diamond(frame["right"], 1380, 26, 16, "#FFFFFF", LINE, 2)
    cv.label((frame["right"] + panel["left"]) / 2, 1360, "1")

    # 12 GameFrame - RoundButton（组合）
    cv.ln([(frame["cx"] - 60, frame["bottom"]), (frame["cx"] - 60, 1655),
           (btn["cx"], 1655), (btn["cx"], btn["bottom"])], LINE, 2)
    cv.diamond(btn["cx"], btn["bottom"], 26, 16, "#FFFFFF", LINE, 2)
    cv.label(btn["cx"] + 130, 1637, "3 个按钮")

    # 13 BoardPanel -> AnimalRenderer（调用）
    cv.ln([(panel["cx"], panel["top"]), (panel["cx"], 1266), (renderer["cx"], 1266),
           (renderer["cx"], renderer["top"])], LINE, 2)
    cv.arrow((renderer["cx"], renderer["top"]), "down", "open")
    cv.label(renderer["cx"] - 90, 1250, "绘制动物")

    # 14 AnimalRenderer ..> Theme
    cv.ln([(renderer["right"], 1360), (theme["left"], 1360)], LINE, 2, dash=7)
    cv.arrow((theme["left"], 1360), "right", "open")

    # 注释
    cv.rr(1080, 880, 300, 118, 6, (255, 251, 224), (202, 138, 4), 2)
    cv.poly([(1080, 900), (1090, 900), (1090, 930), (1080, 930), (1072, 915)],
            (255, 251, 224), (202, 138, 4), 2)
    cv.ln([(main["cx"], main["bottom"]), (main["cx"], 880)], LINE, 1.5, dash=5)
    cv.txt(1232, 940, "启动类：创建 Board、GameFrame、\nGameController，注册监听后显示窗口",
           15, False, (120, 90, 20), maxw=276)

    cv.save(os.path.join(OUT, "uml_class.png"))


# ---------------- 流程图 ----------------
def box_node(cv, cx, y, w, text, h=64, fill="#F5F7FA", brd=(148, 163, 184), size=19):
    cv.rr(cx - w / 2, y, w, h, 10, fill, brd, 2)
    cv.txt(cx, y + h / 2, text, size, False, TXT, maxw=w - 30)
    return dict(cx=cx, top=y, bottom=y + h, cy=y + h / 2)


def dec_node(cv, cx, y, w, h, text, size=18):
    cv.diamond(cx, y + h / 2, w, h, (255, 247, 230), (217, 119, 6), 2)
    cv.txt(cx, y + h / 2, text, size, False, TXT, maxw=w - 90)
    return dict(cx=cx, top=y, bottom=y + h, cy=y + h / 2)


def pill_node(cv, cx, y, w, text, h=56, fill=(232, 240, 254), brd=(59, 111, 212)):
    cv.rr(cx - w / 2, y, w, h, h / 2, fill, brd, 2)
    cv.txt(cx, y + h / 2, text, 19, False, TXT, maxw=w - 40)
    return dict(cx=cx, top=y, bottom=y + h, cy=y + h / 2)


def flow_move():
    cv = Cv(1180, 1240)
    A = 380      # 主列中心
    B = 880      # 分支列中心
    p1 = pill_node(cv, A, 40, 460, "开始：玩家单击棋盘第 i 格")
    b1 = box_node(cv, A, 122, 460, "animal = slots[i]；\nstep = animal.getDirection().getStep()", 86)
    d1 = dec_node(cv, A, 242, 300, 104, "animal 为 null？", 18)
    p2 = pill_node(cv, 880, 266, 340, "结束：忽略本次点击",
                   fill=(243, 244, 246), brd=(148, 163, 184))
    b2 = box_node(cv, A, 386, 460, "next = i + step", 62)
    d2 = dec_node(cv, A, 482, 400, 124, "next 越界，或 slots[next] 非空？", 17)
    d3 = dec_node(cv, B, 482, 360, 124, "next2 = i + 2*step\n越界或非空？", 17)
    bc = box_node(cv, A, 646, 460, "target = next（前进一步）", 64, (236, 253, 245), (16, 185, 129))
    bd = box_node(cv, B, 646, 340, "target = next2（隔位跳跃）", 64, (236, 253, 245), (16, 185, 129))
    be = box_node(cv, B, 756, 340, "提示：前方被挡住，不能移动", 64, (254, 236, 236), (220, 90, 90))
    bf = box_node(cv, A, 756, 460, "board.move(animal)：\n压入 MoveRecord、步数 +1", 86)
    bg = box_node(cv, A, 890, 460, "播放移动动画（260ms），刷新步数与按钮状态", 76)
    d4 = dec_node(cv, A, 1006, 320, 104, "board.isSolved()？", 18)
    bh = box_node(cv, B, 1026, 340, "弹出胜利对话框：换位完成！", 64, (254, 249, 195), (202, 138, 4))
    p3 = pill_node(cv, A, 1140, 460, "结束：等待下一次单击")

    # 连线
    cv.ln([(A, p1["bottom"]), (A, b1["top"])], LINE, 2)
    cv.arrow((A, b1["top"]), "down", "open")
    cv.ln([(A, b1["bottom"]), (A, d1["top"])], LINE, 2)
    cv.arrow((A, d1["top"]), "down", "open")
    cv.ln([(d1["cx"] + 150, d1["cy"]), (p2["cx"] - 170, d1["cy"])], LINE, 2)
    cv.arrow((p2["cx"] - 170, d1["cy"]), "right", "open")
    cv.label(d1["cx"] + 190, d1["cy"] - 18, "是")
    cv.ln([(A, d1["bottom"]), (A, b2["top"])], LINE, 2)
    cv.arrow((A, b2["top"]), "down", "open")
    cv.label(A + 22, (d1["bottom"] + b2["top"]) / 2, "否")
    cv.ln([(A, b2["bottom"]), (A, d2["top"])], LINE, 2)
    cv.arrow((A, d2["top"]), "down", "open")
    cv.ln([(d2["cx"] + 200, d2["cy"]), (d3["cx"] - 180, d2["cy"])], LINE, 2)
    cv.arrow((d3["cx"] - 180, d2["cy"]), "right", "open")
    cv.label(d2["cx"] + 226, d2["cy"] - 18, "是")
    cv.ln([(A, d2["bottom"]), (A, bc["top"])], LINE, 2)
    cv.arrow((A, bc["top"]), "down", "open")
    cv.label(A - 22, (d2["bottom"] + bc["top"]) / 2, "否")
    cv.ln([(B, d3["bottom"]), (B, bd["top"])], LINE, 2)
    cv.arrow((B, bd["top"]), "down", "open")
    cv.label(B - 22, (d3["bottom"] + bd["top"]) / 2, "否")
    cv.ln([(d3["cx"] + 180, d3["cy"]), (1102, d3["cy"]), (1102, be["cy"]), (be["cx"] + 170, be["cy"])],
          LINE, 2)
    cv.arrow((be["cx"] + 170, be["cy"]), "left", "open")
    cv.label(d3["cx"] + 196, d3["cy"] - 18, "是")

    # target 两路汇入 board.move
    cv.ln([(A, bc["bottom"]), (A, bf["top"])], LINE, 2)
    cv.arrow((A, bf["top"]), "down", "open")
    cv.ln([(B, bd["bottom"]), (B, 724), (A, 724), (A, bf["top"])], LINE, 2)

    # 提示 -> 结束
    cv.ln([(be["cx"] - 170, be["cy"]), (664, be["cy"]), (664, p3["cy"] - 18), (p3["cx"] + 230, p3["cy"] - 18)],
          LINE, 2)
    cv.arrow((p3["cx"] + 230, p3["cy"] - 18), "left", "open")
    cv.label(664, 900, "提示后", size=15)

    cv.ln([(A, bf["bottom"]), (A, bg["top"])], LINE, 2)
    cv.arrow((A, bg["top"]), "down", "open")
    cv.ln([(A, bg["bottom"]), (A, d4["top"])], LINE, 2)
    cv.arrow((A, d4["top"]), "down", "open")
    cv.ln([(A, d4["bottom"]), (A, p3["top"])], LINE, 2)
    cv.arrow((A, p3["top"]), "down", "open")
    cv.label(A - 22, (d4["bottom"] + p3["top"]) / 2, "否")
    cv.ln([(d4["cx"] + 160, d4["cy"]), (bh["cx"] - 170, d4["cy"])], LINE, 2)
    cv.arrow((bh["cx"] - 170, d4["cy"]), "right", "open")
    cv.label(d4["cx"] + 190, d4["cy"] - 18, "是")

    cv.save(os.path.join(OUT, "flow_move.png"))


def flow_game():
    cv = Cv(1180, 900)
    A, B = 340, 880
    p0 = pill_node(cv, A, 40, 420, "启动程序 main(String[])")
    s1 = box_node(cv, A, 120, 460, "UIManager 设置系统外观（LookAndFeel）", 64)
    s2 = box_node(cv, A, 208, 460, "new Board()：初始化 7 个格子\n（兔 兔 兔 空 龟 龟 龟）", 82)
    s3 = box_node(cv, A, 314, 460, "new GameFrame() / new BoardPanel()\n搭建标题栏、棋盘与按钮", 86)
    s4 = box_node(cv, A, 424, 460, "new GameController()：注册按钮动作\n与棋盘单击监听", 86)
    s5 = box_node(cv, A, 534, 460, "frame.setVisible(true) 显示窗口", 64)
    d0 = dec_node(cv, A, 622, 400, 120, "等待用户操作\n（Swing 事件分发线程）", 17)
    e1 = box_node(cv, B, 476, 320, "单击动物：\n判定并执行移动", 76, (254, 236, 236), (220, 90, 90))
    e2 = box_node(cv, B, 578, 320, "单击“撤销”：\n回退上一步", 76, (255, 247, 230), (217, 119, 6))
    e3 = box_node(cv, B, 680, 320, "单击“重新开始”：\n复位棋盘与步数", 76, (236, 253, 245), (16, 185, 129))
    back = pill_node(cv, B, 800, 320, "处理完成后回到等待状态",
                     fill=(232, 240, 254), brd=(59, 111, 212))

    cv.ln([(A, p0["bottom"]), (A, s1["top"])], LINE, 2)
    cv.arrow((A, s1["top"]), "down", "open")
    for a, b in [(s1, s2), (s2, s3), (s3, s4), (s4, s5), (s5, d0)]:
        cv.ln([(A, a["bottom"]), (A, b["top"])], LINE, 2)
        cv.arrow((A, b["top"]), "down", "open")

    # 三条分支
    cv.ln([(d0["cx"] + 200, d0["cy"]), (660, d0["cy"])], LINE, 2)
    cv.ln([(660, e1["cy"]), (660, e3["cy"])], LINE, 2)
    for e in (e1, e2, e3):
        cv.ln([(660, e["cy"]), (e["cx"] - 160, e["cy"])], LINE, 2)
        cv.arrow((e["cx"] - 160, e["cy"]), "right", "open")

    # 汇合
    cv.ln([(B, e3["bottom"]), (B, back["top"])], LINE, 2)
    cv.arrow((B, back["top"]), "down", "open")
    cv.ln([(back["cx"] - 160, back["cy"]), (A, back["cy"]), (A, d0["bottom"])], LINE, 2)
    cv.arrow((A, d0["bottom"]), "up", "open")

    cv.save(os.path.join(OUT, "flow_game.png"))


OUT = r"C:\Users\mjqqd\Documents\deepseek-harness\default-workspace\动物换位\docs\img"
if __name__ == "__main__":
    uml()
    flow_move()
    flow_game()
