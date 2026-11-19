package animalgame.model;

/**
 * 一次移动的记录，供“撤销”功能使用。
 *
 * <p>撤销只需要两件事：谁动了，以及它从哪一格到了哪一格。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class MoveRecord {

    private final Animal animal;
    private final int from;
    private final int to;

    /**
     * 构造一条移动记录。
     *
     * @param animal 被移动的动物
     * @param from   移动前的下标
     * @param to     移动后的下标
     */
    public MoveRecord(Animal animal, int from, int to) {
        this.animal = animal;
        this.from = from;
        this.to = to;
    }

    /**
     * 取得被移动的动物。
     *
     * @return 动物对象
     */
    public Animal getAnimal() {
        return animal;
    }

    /**
     * 取得移动前的下标。
     *
     * @return 原位置
     */
    public int getFrom() {
        return from;
    }

    /**
     * 取得移动后的下标。
     *
     * @return 目标位置
     */
    public int getTo() {
        return to;
    }

    /**
     * 判断本次移动是否是“跳过一只动物”的跨格跳。
     *
     * @return 跨过一格返回 {@code true}
     */
    public boolean isJump() {
        return Math.abs(to - from) == 2;
    }
}
