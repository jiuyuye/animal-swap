# -*- coding: utf-8 -*-
"""把类图拆成“模型层”和“视图+控制层”两张，保证插入 Word 后字号可读。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_diagrams import (Cv, class_box, MODEL_HDR, MODEL_BRD, VIEW_HDR, VIEW_BRD,
                           CTRL_HDR, CTRL_BRD, LINE, OUT)  # noqa: E402


def uml_model():
    cv = Cv(1100, 1160)
    for i, (t, hdr, brd) in enumerate([("model 模型层", MODEL_HDR, MODEL_BRD)]):
        cv.rr(40, 26, 24, 20, 5, hdr, brd, 2)
        cv.ltxt(72, 36, t, 16)

    animal = class_box(cv, 40, 80, 310, "Animal", "«abstract 抽象类»",
                       ["# position : int", "# homePosition : int"],
                       ["+ getDirection() : Direction", "+ getName() : String",
                        "+ getPosition() : int", "+ getHomePosition() : int",
                        "~ setPosition(int) : void"], MODEL_HDR, MODEL_BRD)
    direction = class_box(cv, 410, 80, 250, "Direction", "«enumeration 枚举»",
                          ["+ LEFT(-1, \"向左\")", "+ RIGHT(+1, \"向右\")"],
                          ["+ getStep() : int", "+ getLabel() : String"],
                          MODEL_HDR, MODEL_BRD)
    moverule = class_box(cv, 700, 80, 340, "MoveRule", "«interface 接口»",
                         ["+ NO_MOVE : int = -1"],
                         ["+ resolveTarget(Animal, Animal[]) : int"], MODEL_HDR, MODEL_BRD)
    left = class_box(cv, 40, 430, 250, "LeftAnimal", None, [],
                     ["+ getDirection() : Direction", "+ getName() : String"],
                     MODEL_HDR, MODEL_BRD)
    right = class_box(cv, 320, 430, 250, "RightAnimal", None, [],
                      ["+ getDirection() : Direction", "+ getName() : String"],
                      MODEL_HDR, MODEL_BRD)
    std = class_box(cv, 700, 430, 340, "StandardMoveRule", None, [],
                    ["+ resolveTarget(Animal, Animal[]) : int", "- inside(int, int) : boolean"],
                    MODEL_HDR, MODEL_BRD)
    record = class_box(cv, 700, 620, 340, "MoveRecord", None,
                       ["- animal : Animal", "- from : int", "- to : int"],
                       ["+ getAnimal() : Animal", "+ getFrom() : int",
                        "+ getTo() : int", "+ isJump() : boolean"], MODEL_HDR, MODEL_BRD)
    board = class_box(cv, 40, 640, 430, "Board", None,
                      ["- slots : Animal[7]", "- history : Deque<MoveRecord>",
                       "- moveRule : MoveRule", "- moveCount : int"],
                      ["+ reset() : void", "+ getAnimalAt(int) : Animal",
                       "+ getSlots() : Animal[]", "+ canMove(Animal) : boolean",
                       "+ resolveTarget(Animal) : int", "+ move(Animal) : MoveRecord",
                       "+ undo() : MoveRecord", "+ isSolved() : boolean",
                       "+ canUndo() : boolean", "+ getMoveCount() : int",
                       "+ countMovableAnimals() : int"], MODEL_HDR, MODEL_BRD)

    # 泛化关系
    cv.ln([(animal["cx"], animal["bottom"]), (animal["cx"], 390)], LINE, 2)
    cv.ln([(left["cx"], 390), (right["cx"], 390)], LINE, 2)
    cv.ln([(left["cx"], 390), (left["cx"], left["top"])], LINE, 2)
    cv.arrow((left["cx"], left["top"]), "down", "hollow")
    cv.ln([(right["cx"], 390), (right["cx"], right["top"])], LINE, 2)
    cv.arrow((right["cx"], right["top"]), "down", "hollow")

    # 实现关系
    cv.ln([(std["cx"], std["top"]), (std["cx"], moverule["bottom"])], LINE, 2)
    cv.arrow((moverule["cx"], moverule["bottom"]), "up", "hollow")
    cv.label(moverule["cx"] + 76, (moverule["bottom"] + std["top"]) / 2 - 18, "«implements»")

    # Animal -> Direction
    cv.ln([(animal["right"], 190), (direction["left"], 190)], LINE, 2)
    cv.arrow((direction["left"], 190), "right", "open")
    cv.label((animal["right"] + direction["left"]) / 2, 170, "方向 1")

    # Board -> Animal
    cv.ln([(board["left"], 760), (24, 760), (24, 190), (animal["left"], 190)], LINE, 2)
    cv.arrow((animal["left"], 190), "right", "open")
    cv.label(36, 620, "持有")

    # Board -> MoveRule
    cv.ln([(board["right"], 700), (620, 700), (620, 300), (moverule["cx"], 300),
           (moverule["cx"], moverule["bottom"])], LINE, 2)
    cv.arrow((moverule["cx"], moverule["bottom"]), "up", "open")
    cv.label(620, 480, "«use»")

    # Board - MoveRecord
    cv.ln([(board["right"], 1000), (record["cx"], 1000), (record["cx"], record["bottom"])], LINE, 2)
    cv.arrow((record["cx"], record["bottom"]), "up", "open")
    cv.diamond(board["right"] + 13, 1000, 26, 16, "#FFFFFF", LINE, 2)
    cv.label(record["cx"] - 80, 978, "历史记录 0..*")

    cv.txt(550, 1118, "说明：Board 通过 MoveRule 接口完成落点判定，替换实现类即可扩展出新玩法。",
           15, False, (107, 114, 128))
    cv.save(os.path.join(OUT, "uml_model.png"))


def uml_view():
    cv = Cv(1100, 900)
    for i, (t, hdr, brd) in enumerate([("view 视图层", VIEW_HDR, VIEW_BRD),
                                       ("controller 控制层", CTRL_HDR, CTRL_BRD)]):
        cv.rr(40 + i * 220, 26, 24, 20, 5, hdr, brd, 2)
        cv.ltxt(72 + i * 220, 36, t, 16)

    frame = class_box(cv, 40, 80, 340, "GameFrame", "«JFrame»",
                      ["- boardPanel : BoardPanel", "- stepsPill : JLabel",
                       "- statusLabel : JLabel", "- undoButton : RoundButton",
                       "- restartButton : RoundButton"],
                      ["+ setMoveCount(int) : void", "+ setStatus(String, boolean) : void",
                       "+ showWinDialog(int) : void", "+ showHelp() : void"],
                      VIEW_HDR, VIEW_BRD)
    panel = class_box(cv, 410, 80, 340, "BoardPanel", "«JPanel»",
                      ["- board : Board", "- hoverIndex : int", "- animation : MoveAnimation"],
                      ["+ paintComponent(Graphics) : void",
                       "+ animateMove(Animal, int, int, Runnable) : void",
                       "+ flashInvalid(Animal) : void", "+ isAnimating() : boolean"],
                      VIEW_HDR, VIEW_BRD)
    renderer = class_box(cv, 780, 80, 290, "AnimalRenderer", None, [],
                         ["+ draw(Graphics2D, Animal, double, double, double) : void",
                          "- drawRabbit(Graphics2D) : void",
                          "- drawTurtle(Graphics2D) : void"], VIEW_HDR, VIEW_BRD)
    btn = class_box(cv, 40, 470, 280, "RoundButton", "«JButton»",
                    ["- hover : boolean"], ["+ paintComponent(Graphics) : void"],
                    VIEW_HDR, VIEW_BRD)
    theme = class_box(cv, 720, 470, 240, "Theme", "«工具类»",
                      ["+ ACCENT : Color", "+ HINT : Color", "+ RABBIT_BODY : Color",
                       "+ TURTLE_SHELL : Color"], ["+ font(int, int) : Font"],
                      VIEW_HDR, VIEW_BRD)
    ctrl = class_box(cv, 350, 470, 340, "GameController", None,
                     ["- board : Board", "- frame : GameFrame"],
                     ["+ onAnimalClicked(Animal) : void",
                      "+ actionPerformed(ActionEvent) : void",
                      "- undo() : void", "- restart() : void",
                      "- afterMove() : void", "- refresh(String) : void"],
                     CTRL_HDR, CTRL_BRD)
    main = class_box(cv, 780, 720, 280, "Main", "«启动类»", [],
                     ["+ main(String[]) : void"], CTRL_HDR, CTRL_BRD)

    # 组合
    cv.ln([(frame["right"], 200), (panel["left"], 200)], LINE, 2)
    cv.diamond(frame["right"] + 13, 200, 26, 16, "#FFFFFF", LINE, 2)
    cv.arrow((panel["left"], 200), "right", "open")
    cv.label((frame["right"] + panel["left"]) / 2, 180, "1")

    # GameFrame - RoundButton
    cv.ln([(120, frame["bottom"]), (120, btn["top"])], LINE, 2)
    cv.diamond(120, frame["bottom"] + 13, 16, 26, "#FFFFFF", LINE, 2)
    cv.arrow((120, btn["top"]), "down", "open")

    # BoardPanel -> AnimalRenderer
    cv.ln([(panel["right"], 180), (renderer["left"], 180)], LINE, 2)
    cv.arrow((renderer["left"], 180), "right", "open")

    # AnimalRenderer ..> Theme
    cv.ln([(renderer["cx"], renderer["bottom"]), (renderer["cx"], theme["top"])], LINE, 2, dash=7)
    cv.arrow((renderer["cx"], theme["top"]), "down", "open")
    cv.label(renderer["cx"] + 44, 400, "«use»")

    # GameController -> BoardPanel
    cv.ln([(560, ctrl["top"]), (560, panel["bottom"])], LINE, 2)
    cv.arrow((560, panel["bottom"]), "up", "open")

    # GameController ..> GameFrame
    cv.ln([(470, ctrl["top"]), (470, 430), (215, 430), (215, frame["bottom"])], LINE, 2, dash=7)
    cv.arrow((215, frame["bottom"]), "up", "open")
    cv.label(330, 412, "回调 / 刷新")

    # Main -> GameController
    cv.ln([(main["left"], 800), (520, 800), (520, ctrl["bottom"])], LINE, 2, dash=7)
    cv.arrow((520, ctrl["bottom"]), "up", "open")
    cv.label(660, 782, "创建")

    # 模型层引用
    cv.rr(40, 760, 250, 86, 8, (248, 250, 252), (148, 163, 184), 2)
    cv.txt(165, 790, "Board（模型层）", 17, True, (31, 41, 55))
    cv.txt(165, 818, "移动校验 / 撤销栈 / 胜负判定", 14, False, (107, 114, 128))
    cv.ln([(290, 803), (340, 803), (340, ctrl["bottom"])], LINE, 2, dash=7)
    cv.arrow((340, ctrl["bottom"]), "up", "open")

    cv.save(os.path.join(OUT, "uml_view.png"))


if __name__ == "__main__":
    uml_model()
    uml_view()
