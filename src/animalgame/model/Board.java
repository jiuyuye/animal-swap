package animalgame.model;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * 棋盘模型：负责格子布局、移动校验、撤销栈与胜负判定。
 *
 * <p>本类不涉及任何界面代码，可以在命令行下单独测试（见 {@code animalgame.test.GameModelTest}），
 * 这正是 MVC 分层的好处。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class Board {

    /** 棋盘格子总数。 */
    public static final int SLOT_COUNT = 7;

    /** 每侧动物数量。 */
    public static final int ANIMALS_PER_SIDE = 3;

    /** 完成游戏的理论最少步数：n 只 + n 只时为 n(n+2)，此处为 15。 */
    public static final int MIN_MOVES = ANIMALS_PER_SIDE * (ANIMALS_PER_SIDE + 2);

    /** 格子数组，{@code null} 表示空格。 */
    private final Animal[] slots = new Animal[SLOT_COUNT];

    /** 撤销栈，栈顶是最近一次移动。 */
    private final Deque<MoveRecord> history = new ArrayDeque<>();

    /** 跳跃规则，可替换以便扩展玩法。 */
    private final MoveRule moveRule;

    /** 已走步数。 */
    private int moveCount;

    /**
     * 使用标准规则构造棋盘，并自动摆好初始局面。
     */
    public Board() {
        this(new StandardMoveRule());
    }

    /**
     * 使用指定规则构造棋盘。
     *
     * @param moveRule 跳跃规则
     */
    public Board(MoveRule moveRule) {
        if (moveRule == null) {
            throw new IllegalArgumentException("跳跃规则不能为空");
        }
        this.moveRule = moveRule;
        reset();
    }

    /**
     * 恢复初始局面：左边 3 只兔、右边 3 只龟、正中间为空。
     */
    public final void reset() {
        for (int i = 0; i < SLOT_COUNT; i++) {
            slots[i] = null;
        }
        history.clear();
        moveCount = 0;
        for (int i = 0; i < ANIMALS_PER_SIDE; i++) {
            slots[i] = new LeftAnimal(i);
        }
        for (int i = 0; i < ANIMALS_PER_SIDE; i++) {
            int index = SLOT_COUNT - 1 - i;
            slots[index] = new RightAnimal(index);
        }
    }

    /**
     * 取得指定格子上的动物。
     *
     * @param index 格子下标
     * @return 动物；该格为空时返回 {@code null}
     */
    public Animal getAnimalAt(int index) {
        return slots[index];
    }

    /**
     * 取得格子数组的副本，供规则计算或界面绘制使用。
     *
     * @return 长度为 {@link #SLOT_COUNT} 的数组副本
     */
    public Animal[] getSlots() {
        return slots.clone();
    }

    /**
     * 判断某只动物当前是否可以移动。
     *
     * @param animal 待检查的动物
     * @return 可以移动返回 {@code true}
     */
    public boolean canMove(Animal animal) {
        return resolveTarget(animal) != MoveRule.NO_MOVE;
    }

    /**
     * 计算某只动物本次可以落到的格子下标。
     *
     * @param animal 待检查的动物
     * @return 目标下标；不能移动或参数为空时返回 {@link MoveRule#NO_MOVE}
     */
    public int resolveTarget(Animal animal) {
        if (animal == null) {
            return MoveRule.NO_MOVE;
        }
        return moveRule.resolveTarget(animal, slots);
    }

    /**
     * 尝试移动一只动物。
     *
     * @param animal 被点击的动物，不可能为 {@code null}
     * @return 成功时返回本次移动记录；不能移动时返回 {@code null}
     */
    public MoveRecord move(Animal animal) {
        if (animal == null) {
            return null;
        }
        int target = resolveTarget(animal);
        if (target == MoveRule.NO_MOVE) {
            return null;
        }
        int from = animal.getPosition();
        slots[from] = null;
        slots[target] = animal;
        animal.setPosition(target);
        MoveRecord record = new MoveRecord(animal, from, target);
        history.push(record);
        moveCount++;
        return record;
    }

    /**
     * 撤销最近一次移动。
     *
     * @return 被撤销的移动记录；没有可撤销的步骤时返回 {@code null}
     */
    public MoveRecord undo() {
        MoveRecord record = history.poll();
        if (record == null) {
            return null;
        }
        Animal animal = record.getAnimal();
        slots[record.getTo()] = null;
        slots[record.getFrom()] = animal;
        animal.setPosition(record.getFrom());
        moveCount--;
        return record;
    }

    /**
     * 取得已完成步数。
     *
     * @return 步数
     */
    public int getMoveCount() {
        return moveCount;
    }

    /**
     * 判断是否还有可撤销的步骤。
     *
     * @return 撤销栈非空返回 {@code true}
     */
    public boolean canUndo() {
        return !history.isEmpty();
    }

    /**
     * 判断是否已经完成换位：所有兔子都到了右侧，所有乌龟都到了左侧。
     *
     * @return 已完成返回 {@code true}
     */
    public boolean isSolved() {
        for (Animal animal : slots) {
            if (animal == null) {
                continue;
            }
            boolean isLeftAnimal = animal instanceof LeftAnimal;
            boolean onRightSide = animal.getPosition() >= SLOT_COUNT - ANIMALS_PER_SIDE;
            if (isLeftAnimal != onRightSide) {
                return false;
            }
        }
        return true;
    }

    /**
     * 统计当前还能行动的动物数量，供界面给出“无解”提示。
     *
     * @return 可以移动的动物个数
     */
    public int countMovableAnimals() {
        int count = 0;
        for (Animal animal : slots) {
            if (canMove(animal)) {
                count++;
            }
        }
        return count;
    }
}
