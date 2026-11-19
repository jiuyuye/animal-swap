package animalgame.model;

/**
 * 动物的抽象父类。
 *
 * <p>左侧动物与右侧动物共享“站在第几格、朝哪个方向、叫什么名字”这些属性，
 * 差异只在方向与外观，因此用抽象类 + 两个子类实现多态。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public abstract class Animal {

    /** 动物当前所在格子的下标。 */
    private int position;

    /** 动物出生时的下标，用于“重新开始”时复位。 */
    private final int homePosition;

    /**
     * 构造动物。
     *
     * @param position 初始所在格子下标
     */
    protected Animal(int position) {
        this.position = position;
        this.homePosition = position;
    }

    /**
     * 取得动物的前进方向。
     *
     * @return 前进方向
     */
    public abstract Direction getDirection();

    /**
     * 取得动物的显示名称。
     *
     * @return 例如“兔”“龟”
     */
    public abstract String getName();

    /**
     * 取得动物的初始下标。
     *
     * @return 出生位置
     */
    public int getHomePosition() {
        return homePosition;
    }

    /**
     * 取得动物当前所在格子下标。
     *
     * @return 当前下标
     */
    public int getPosition() {
        return position;
    }

    /**
     * 设置动物所在格子下标，仅供 {@link Board} 在移动或悔棋时调用。
     *
     * @param position 新的下标
     */
    void setPosition(int position) {
        this.position = position;
    }

    @Override
    public String toString() {
        return getName() + "@" + position;
    }
}
