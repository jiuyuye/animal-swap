package animalgame.test;

import animalgame.model.Animal;
import animalgame.model.Board;
import animalgame.model.Direction;
import animalgame.model.LeftAnimal;
import animalgame.model.MoveRecord;
import animalgame.model.RightAnimal;

/**
 * 模型层测试用例（不依赖 JUnit，可直接用 java 运行）。
 *
 * <p>覆盖：初始布局、单步移动、隔位跳跃、越界与阻挡、撤销、重新开始、
 * 以及一条 15 步的最优解能否被判为胜利。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public final class GameModelTest {

    /** 通过数量。 */
    private static int passed;
    /** 失败数量。 */
    private static int failed;

    private GameModelTest() {
    }

    /**
     * 运行全部用例。
     *
     * @param args 命令行参数（不使用）
     */
    public static void main(String[] args) {
        testInitialLayout();
        testStepForward();
        testJumpOverOne();
        testCannotPassTwoAnimals();
        testBoundary();
        testDirectionOfEachSide();
        testMoveRecordJumpFlag();
        testUndo();
        testRestart();
        testOptimalSolution();

        System.out.println();
        System.out.println("测试完成：共 " + (passed + failed) + " 项，通过 " + passed
                + " 项，失败 " + failed + " 项。");
        if (failed > 0) {
            System.exit(1);
        }
    }

    /**
     * 用例 1：初始局面应当是“左边三只兔、中间空、右边三只龟”。
     */
    private static void testInitialLayout() {
        Board board = new Board();
        boolean ok = true;
        for (int i = 0; i < 3; i++) {
            ok &= board.getAnimalAt(i) instanceof LeftAnimal;
        }
        ok &= board.getAnimalAt(3) == null;
        for (int i = 4; i < 7; i++) {
            ok &= board.getAnimalAt(i) instanceof RightAnimal;
        }
        check("初始局面：左三兔、中间空、右三龟", ok);
    }

    /**
     * 用例 2：前方为空时，兔子应该走到相邻格子。
     */
    private static void testStepForward() {
        Board board = new Board();
        Animal rabbit = board.getAnimalAt(2);
        MoveRecord record = board.move(rabbit);
        boolean ok = record != null
                && record.getFrom() == 2
                && record.getTo() == 3
                && !record.isJump()
                && board.getAnimalAt(3) == rabbit
                && board.getAnimalAt(2) == null
                && rabbit.getPosition() == 3;
        check("单步移动：2 号位兔子走到 3 号空位", ok);
    }

    /**
     * 用例 3：前方有动物而隔位为空时，应该跳过一只动物。
     */
    private static void testJumpOverOne() {
        Board board = new Board();
        // 先让 2 号位兔子走到 3 号位，局面变成 兔兔_龟兔龟龟
        board.move(board.getAnimalAt(2));
        Animal turtle = board.getAnimalAt(4);   // 4 号位乌龟，左边 3 号位是兔子，2 号位为空
        MoveRecord record = board.move(turtle);
        boolean ok = record != null
                && record.getFrom() == 4
                && record.getTo() == 2
                && record.isJump()
                && board.getAnimalAt(2) == turtle
                && board.getAnimalAt(4) == null;
        check("隔位跳跃：4 号位乌龟跳过 3 号位兔子落到 2 号位", ok);
    }

    /**
     * 用例 4：前方和隔位都被占时，不能移动。
     */
    private static void testCannotPassTwoAnimals() {
        Board board = new Board();
        board.move(board.getAnimalAt(2));       // 兔兔_兔龟龟龟
        Animal rabbit = board.getAnimalAt(3);   // 前方 4、5 都有乌龟
        boolean ok = !board.canMove(rabbit) && board.resolveTarget(rabbit) == -1;
        check("阻挡判定：前方与隔位都被占时不能移动", ok);
    }

    /**
     * 用例 5：越界时不能向前移动。
     */
    private static void testBoundary() {
        // 最右侧的乌龟前进方向是“向左”，但左边被兔子挡住且隔位也被占，因此动不了
        Board board = new Board();
        boolean turtleBlocked = !board.canMove(board.getAnimalAt(6));

        // 按最优解的前 10 步走，把一只兔子送到最右端 6 号位
        int[][] head = {
            {2, 3}, {4, 2}, {5, 4}, {3, 5}, {1, 3},
            {0, 1}, {2, 0}, {4, 2}, {6, 4}, {5, 6}
        };
        Board far = new Board();
        for (int[] mv : head) {
            far.move(far.getAnimalAt(mv[0]));
        }
        Animal edgeRabbit = far.getAnimalAt(6);
        boolean atEdge = edgeRabbit instanceof LeftAnimal;
        boolean outOfBoard = !far.canMove(edgeRabbit);

        check("边界判定：位于两端的动物不会越界移动", turtleBlocked && atEdge && outOfBoard);
    }

    /**
     * 用例 6：左侧动物只能向右、右侧动物只能向左。
     */
    private static void testDirectionOfEachSide() {
        Board board = new Board();
        boolean ok = board.getAnimalAt(0).getDirection() == Direction.RIGHT
                && board.getAnimalAt(6).getDirection() == Direction.LEFT;
        check("方向规则：兔子向右、乌龟向左", ok);
    }

    /**
     * 用例 7：移动记录应能区分“走”和“跳”。
     */
    private static void testMoveRecordJumpFlag() {
        MoveRecord step = new MoveRecord(new LeftAnimal(1), 1, 2);
        MoveRecord jump = new MoveRecord(new LeftAnimal(1), 1, 3);
        check("移动记录：能区分单步与跨格跳", !step.isJump() && jump.isJump());
    }

    /**
     * 用例 8：撤销应当恢复位置与步数。
     */
    private static void testUndo() {
        Board board = new Board();
        Animal rabbit = board.getAnimalAt(2);
        board.move(rabbit);
        board.move(board.getAnimalAt(4));
        int before = board.getMoveCount();
        MoveRecord undone = board.undo();
        boolean ok = undone != null
                && board.getMoveCount() == before - 1
                && undone.getAnimal().getPosition() == undone.getFrom()
                && board.getAnimalAt(undone.getFrom()) == undone.getAnimal()
                && board.getAnimalAt(undone.getTo()) == null;
        // 全部撤销后应回到初始局面
        while (board.canUndo()) {
            board.undo();
        }
        ok &= board.getMoveCount() == 0 && board.getAnimalAt(3) == null
                && board.getAnimalAt(2) instanceof LeftAnimal;
        check("撤销：逐级回退并最终恢复初始局面", ok);
    }

    /**
     * 用例 9：重新开始应清空历史并复位所有动物。
     */
    private static void testRestart() {
        Board board = new Board();
        board.move(board.getAnimalAt(2));
        board.move(board.getAnimalAt(4));
        board.reset();
        boolean ok = board.getMoveCount() == 0
                && !board.canUndo()
                && board.getAnimalAt(0) instanceof LeftAnimal
                && board.getAnimalAt(3) == null
                && board.getAnimalAt(6) instanceof RightAnimal
                && !board.isSolved();
        check("重新开始：步数归零、历史清空、局面复位", ok);
    }

    /**
     * 用例 10：按 15 步最优解走完，应当判定胜利。
     */
    private static void testOptimalSolution() {
        int[][] moves = {
            {2, 3}, {4, 2}, {5, 4}, {3, 5}, {1, 3},
            {0, 1}, {2, 0}, {4, 2}, {6, 4}, {5, 6},
            {3, 5}, {1, 3}, {2, 1}, {4, 2}, {3, 4}
        };
        Board board = new Board();
        boolean ok = true;
        for (int i = 0; i < moves.length; i++) {
            Animal animal = board.getAnimalAt(moves[i][0]);
            MoveRecord record = board.move(animal);
            boolean stepOk = record != null && record.getTo() == moves[i][1];
            if (!stepOk) {
                ok = false;
                System.out.println("  第 " + (i + 1) + " 步失败：期望从 " + moves[i][0]
                        + " 到 " + moves[i][1]);
                break;
            }
        }
        ok &= board.isSolved();
        ok &= board.getMoveCount() == Board.MIN_MOVES;
        check("最优解：15 步完成换位并被判为胜利", ok);
    }

    /**
     * 记录一条断言结果。
     *
     * @param name 用例名称
     * @param ok   是否通过
     */
    private static void check(String name, boolean ok) {
        if (ok) {
            passed++;
            System.out.println("[通过] " + name);
        } else {
            failed++;
            System.out.println("[失败] " + name);
        }
    }
}
