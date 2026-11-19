package animalgame.model;

/**
 * 跳跃规则接口。
 *
 * <p>把“能不能跳、跳到哪里”从动物与棋盘中独立出来，
 * 便于替换规则（例如将来增加“只能跳不能走”的变种），体现面向接口编程。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public interface MoveRule {

    /** 无法移动时 {@link #resolveTarget} 的返回值。 */
    int NO_MOVE = -1;

    /**
     * 计算动物本次可以落到的目标下标。
     *
     * @param animal 待移动的动物，其 {@link Animal#getPosition()} 为当前下标
     * @param slots  棋盘快照，{@code null} 表示该位置为空
     * @return 目标下标；如果本次不能移动则返回 {@link #NO_MOVE}
     */
    int resolveTarget(Animal animal, Animal[] slots);
}
