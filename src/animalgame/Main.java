package animalgame;

import animalgame.controller.GameController;
import animalgame.model.Board;
import animalgame.view.GameFrame;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;

/**
 * 程序入口。
 *
 * <p>只做三件事：设置界面外观、创建模型与窗口、把控制器接上去。
 * 所有 Swing 组件都在事件分发线程（EDT）中创建，避免线程安全问题。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public final class Main {

    private Main() {
    }

    /**
     * 程序主方法。
     *
     * @param args 命令行参数（本程序不使用）
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {
                // 主题设置失败不影响程序运行，继续使用默认外观
            }
            Board board = new Board();
            GameFrame frame = new GameFrame(board);
            new GameController(board, frame);
            frame.setVisible(true);
        });
    }
}
