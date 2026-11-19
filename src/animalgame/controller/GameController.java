package animalgame.controller;

import animalgame.model.Animal;
import animalgame.model.Board;
import animalgame.model.MoveRecord;
import animalgame.view.BoardPanel;
import animalgame.view.GameFrame;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * 游戏控制器：把界面事件翻译成模型操作，再把结果写回界面。
 *
 * <p>它是 MVC 中的 C，负责“协调”而不是“计算”：
 * 能不能跳由 {@link Board} 判断，怎么画由 {@link BoardPanel} 决定。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class GameController implements BoardPanel.GameListener, ActionListener {

    private final Board board;
    private final GameFrame frame;

    /**
     * 构造控制器并完成事件绑定。
     *
     * @param board 棋盘模型
     * @param frame 主窗口
     */
    public GameController(Board board, GameFrame frame) {
        this.board = board;
        this.frame = frame;
        frame.getBoardPanel().setGameListener(this);
        frame.getUndoButton().addActionListener(this);
        frame.getRestartButton().addActionListener(this);
        frame.getHelpButton().addActionListener(this);
        refresh(null);
    }

    /**
     * 响应棋盘上的动物点击。
     *
     * <p>处理顺序：动画进行中则忽略本次点击；落点非法则闪烁提示；
     * 合法则执行移动、更新状态栏并播放动画。</p>
     *
     * @param animal 被点击的动物，不会为 {@code null}
     */
    @Override
    public void onAnimalClicked(Animal animal) {
        BoardPanel panel = frame.getBoardPanel();
        if (panel.isAnimating()) {
            return;
        }
        int from = animal.getPosition();
        int target = board.resolveTarget(animal);
        if (target < 0) {
            panel.flashInvalid(animal);
            frame.setStatus("这只" + animal.getName() + "前面被挡住了，换一只试试。", true);
            return;
        }
        MoveRecord record = board.move(animal);
        if (record == null) {
            return;
        }
        String action = record.isJump() ? "跳过一只动物" : "向前走了一格";
        frame.setStatus(animal.getName() + action + "，到了第 " + (target + 1) + " 个位置。", false);
        panel.animateMove(animal, from, target, this::afterMove);
        refresh(null);
    }

    /**
     * 动画结束后检查胜负并刷新界面。
     */
    private void afterMove() {
        refresh(null);
        if (board.isSolved()) {
            frame.setStatus("完成！共用了 " + board.getMoveCount() + " 步。", false);
            frame.showWinDialog(board.getMoveCount());
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object source = e.getSource();
        if (source == frame.getUndoButton()) {
            undo();
        } else if (source == frame.getRestartButton()) {
            restart();
        } else if (source == frame.getHelpButton()) {
            frame.showHelp();
        }
    }

    /**
     * 撤销上一步。
     */
    private void undo() {
        if (board.canUndo() == false) {
            frame.setStatus("已经没有可以撤销的步骤了。", true);
            return;
        }
        MoveRecord record = board.undo();
        frame.setStatus("已撤销：" + record.getAnimal().getName() + " 回到第 "
                + (record.getFrom() + 1) + " 个位置。", false);
        frame.getBoardPanel().repaint();
        refresh(null);
    }

    /**
     * 重新开始游戏。
     */
    private void restart() {
        board.reset();
        frame.setStatus("已重新开始，加油！", false);
        frame.getBoardPanel().repaint();
        refresh(null);
    }

    /**
     * 把模型状态同步到界面。
     *
     * @param message 需要显示的消息，可为 {@code null}
     */
    private void refresh(String message) {
        frame.setMoveCount(board.getMoveCount());
        frame.getUndoButton().setEnabled(board.canUndo());
        if (message != null) {
            frame.setStatus(message, false);
        }
    }
}
