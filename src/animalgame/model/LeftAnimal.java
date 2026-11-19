package animalgame.model;

/**
 * 左侧动物（兔子）。
 *
 * <p>以“向右”为前进方向，目标是走到棋盘的右半部。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class LeftAnimal extends Animal {

    /**
     * 构造一只位于指定格子的兔子。
     *
     * @param position 初始下标，一般取 0、1、2
     */
    public LeftAnimal(int position) {
        super(position);
    }

    @Override
    public Direction getDirection() {
        return Direction.RIGHT;
    }

    @Override
    public String getName() {
        return "兔";
    }
}
