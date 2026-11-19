package animalgame.model;

/**
 * 右侧动物（乌龟）。
 *
 * <p>以“向左”为前进方向，目标是走到棋盘的左半部。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class RightAnimal extends Animal {

    /**
     * 构造一只位于指定格子的乌龟。
     *
     * @param position 初始下标，一般取 4、5、6
     */
    public RightAnimal(int position) {
        super(position);
    }

    @Override
    public Direction getDirection() {
        return Direction.LEFT;
    }

    @Override
    public String getName() {
        return "龟";
    }
}
