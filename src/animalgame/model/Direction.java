package animalgame.model;

/**
 * 动物前进方向枚举。
 *
 * <p>棋盘是一维水平排列的格子，左侧动物以“向右”为前进方向，
 * 右侧动物以“向左”为前进方向，因此方向最终都换算成“下标 +1”或“下标 -1”。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public enum Direction {

    /** 向左：棋盘下标减小，供右侧动物使用。 */
    LEFT(-1, "向左"),

    /** 向右：棋盘下标增大，供左侧动物使用。 */
    RIGHT(1, "向右");

    private final int step;
    private final String label;

    Direction(int step, String label) {
        this.step = step;
        this.label = label;
    }

    /**
     * 取得该方向在数组下标上的步长。
     *
     * @return 前进一格时的下标增量，向右为 1，向左为 -1
     */
    public int getStep() {
        return step;
    }

    /**
     * 取得中文名称，用于界面提示与文档。
     *
     * @return “向左”或“向右”
     */
    public String getLabel() {
        return label;
    }
}
