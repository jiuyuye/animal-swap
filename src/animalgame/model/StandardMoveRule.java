package animalgame.model;

/**
 * 标准跳跃规则：走一步，或隔一个动物跳一步。
 *
 * <p>规则细节（与任务书一致）：</p>
 * <ol>
 *   <li>动物前方相邻位置为空，则直接走到该位置；</li>
 *   <li>前方相邻位置有动物，但再前面一格为空，则越过该动物跳到那一格；</li>
 *   <li>其余情况（前方有动物且隔位被占、或前方越界）一律不能移动。</li>
 * </ol>
 *
 * @author 课程设计
 * @version 1.0
 */
public class StandardMoveRule implements MoveRule {

    /**
     * 创建标准移动规则对象。
     *
     * <p>规则不含可变状态，因此可以安全地被多个棋盘共享。</p>
     */
    public StandardMoveRule() {
    }

    /**
     * 计算动物本次可以落到的格子。
     *
     * <p>先看前方一格：越界则失败；为空则走一格。前方有动物时再看隔位：
     * 隔位在界内且为空就跳过去，否则判定为不能移动。</p>
     *
     * @param animal 待移动的动物
     * @param slots  棋盘格子快照
     * @return 目标格下标；不能移动时返回 {@link MoveRule#NO_MOVE}
     */
    @Override
    public int resolveTarget(Animal animal, Animal[] slots) {
        int step = animal.getDirection().getStep();
        int position = animal.getPosition();

        // 第 1 步：尝试向前走一格
        int ahead = position + step;
        if (!inside(ahead, slots.length)) {
            return NO_MOVE;                       // 已经顶到边界，无法前进
        }
        if (slots[ahead] == null) {
            return ahead;                         // 前方为空，直接走过去
        }

        // 第 2 步：前方被占，尝试越过它跳到再前一格
        int beyond = position + step * 2;
        if (inside(beyond, slots.length) && slots[beyond] == null) {
            return beyond;                        // 隔位为空，可以跳过
        }

        // 第 3 步：前方有动物且隔位被占或越界
        return NO_MOVE;
    }

    /**
     * 判断下标是否落在棋盘范围内。
     *
     * @param index 待检查下标
     * @param size  棋盘格子数
     * @return 下标合法返回 {@code true}
     */
    private boolean inside(int index, int size) {
        return index >= 0 && index < size;
    }
}
