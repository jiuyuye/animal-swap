package animalgame.view;

import animalgame.model.Board;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagLayout;
import java.awt.RenderingHints;
import java.awt.geom.RoundRectangle2D;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.AbstractAction;
import javax.swing.JComponent;
import javax.swing.JOptionPane;
import java.awt.event.ActionEvent;

/**
 * 主窗口：组装标题栏、棋盘与控制按钮。
 *
 * <p>窗口本身不处理游戏规则，只提供“拿得到控件、显示得了状态”的能力，
 * 由 {@code GameController} 把按钮和模型连接起来，符合 MVC 的职责划分。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class GameFrame extends JFrame {

    private static final long serialVersionUID = 1L;

    /** 棋盘面板。 */
    private final BoardPanel boardPanel;
    /** “撤销”按钮。 */
    private final RoundButton undoButton;
    /** “重新开始”按钮。 */
    private final RoundButton restartButton;
    /** “玩法说明”按钮。 */
    private final RoundButton helpButton;
    /** 步数标签。 */
    private final JLabel stepLabel;
    /** 状态提示标签。 */
    private final JLabel statusLabel;

    /**
     * 构造主窗口。
     *
     * @param board 棋盘模型
     */
    public GameFrame(Board board) {
        super("动物换位 —— Java 程序设计课程设计");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        getContentPane().setBackground(Theme.BACKGROUND_TOP);

        boardPanel = new BoardPanel(board);

        undoButton = new RoundButton("撤 销", new Color(0x8E, 0x9E, 0xB4));
        restartButton = new RoundButton("重新开始", Theme.ACCENT);
        helpButton = new RoundButton("玩法说明", new Color(0x4C, 0xB0, 0x8A));
        stepLabel = new JLabel();
        stepLabel.setFont(Theme.font(Font.PLAIN, 14));
        stepLabel.setForeground(Theme.TEXT);
        statusLabel = new JLabel("兔子只能向右走，乌龟只能向左走。");
        statusLabel.setFont(Theme.font(Font.PLAIN, 13));
        statusLabel.setForeground(Theme.TEXT_MUTED);

        add(buildHeader(), BorderLayout.NORTH);
        add(buildCenter(), BorderLayout.CENTER);
        add(buildFooter(), BorderLayout.SOUTH);

        installShortcuts();

        setMoveCount(0);
        pack();
        setLocationRelativeTo(null);
        setResizable(false);
    }

    /**
     * 构建顶部标题栏。
     *
     * @return 标题面板
     */
    private JPanel buildHeader() {
        JPanel header = new GradientPanel();
        header.setLayout(new BorderLayout());
        header.setBorder(BorderFactory.createEmptyBorder(16, 26, 16, 26));

        JPanel titles = new JPanel();
        titles.setOpaque(false);
        titles.setLayout(new BoxLayout(titles, BoxLayout.Y_AXIS));

        JLabel title = new JLabel("动物换位");
        title.setFont(Theme.font(Font.BOLD, 24));
        title.setForeground(Color.WHITE);
        JLabel subtitle = new JLabel("点击动物，让它向前走一格，或跳过面前的一只动物");
        subtitle.setFont(Theme.font(Font.PLAIN, 13));
        subtitle.setForeground(new Color(0xE3, 0xEE, 0xFF));

        titles.add(title);
        titles.add(Box.createVerticalStrut(4));
        titles.add(subtitle);

        JPanel steps = new StepsPill(stepLabel);
        header.add(titles, BorderLayout.WEST);
        header.add(steps, BorderLayout.EAST);
        return header;
    }

    /**
     * 构建中间的棋盘区域。
     *
     * @return 容器面板
     */
    private JPanel buildCenter() {
        JPanel center = new JPanel(new GridBagLayout());
        center.setBackground(Theme.BACKGROUND_TOP);
        center.setBorder(BorderFactory.createEmptyBorder(14, 10, 6, 10));
        center.add(boardPanel);
        return center;
    }

    /**
     * 构建底部状态栏与按钮区。
     *
     * @return 底部面板
     */
    private JPanel buildFooter() {
        JPanel footer = new JPanel(new BorderLayout());
        footer.setBackground(Theme.BACKGROUND_TOP);
        footer.setBorder(BorderFactory.createEmptyBorder(6, 26, 18, 26));
        footer.add(statusLabel, BorderLayout.WEST);

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        buttons.setOpaque(false);
        buttons.add(helpButton);
        buttons.add(undoButton);
        buttons.add(restartButton);
        footer.add(buttons, BorderLayout.EAST);
        return footer;
    }

    /**
     * 注册键盘快捷键：Ctrl+Z 撤销，Ctrl+R 重新开始，F1 查看玩法说明。
     */
    private void installShortcuts() {
        bindKey("control Z", "undo", e -> undoButton.doClick());
        bindKey("control R", "restart", e -> restartButton.doClick());
        bindKey("F1", "help", e -> helpButton.doClick());
    }

    /**
     * 把一个按键绑定到指定动作。
     *
     * @param key    按键描述，例如 {@code "control Z"}
     * @param name   动作名称
     * @param action 动作实现
     */
    private void bindKey(String key, String name, java.awt.event.ActionListener action) {
        getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                .put(KeyStroke.getKeyStroke(key), name);
        getRootPane().getActionMap().put(name, new AbstractAction() {
            private static final long serialVersionUID = 1L;

            @Override
            public void actionPerformed(ActionEvent e) {
                action.actionPerformed(e);
            }
        });
    }

    /**
     * 取得棋盘面板。
     *
     * @return 棋盘面板
     */
    public BoardPanel getBoardPanel() {
        return boardPanel;
    }

    /**
     * 取得撤销按钮。
     *
     * @return 按钮
     */
    public RoundButton getUndoButton() {
        return undoButton;
    }

    /**
     * 取得重新开始按钮。
     *
     * @return 按钮
     */
    public RoundButton getRestartButton() {
        return restartButton;
    }

    /**
     * 取得玩法说明按钮。
     *
     * @return 按钮
     */
    public RoundButton getHelpButton() {
        return helpButton;
    }

    /**
     * 刷新步数显示。
     *
     * @param moves 已走步数
     */
    public void setMoveCount(int moves) {
        stepLabel.setText("<html><div style='text-align:center'>步数 <b style='font-size:16px'>"
                + moves + "</b><br><span style='font-size:11px'>最少 "
                + Board.MIN_MOVES + " 步</span></div></html>");
    }

    /**
     * 在底部显示一条提示信息。
     *
     * @param message 提示文字
     * @param warning 是否使用警示颜色
     */
    public void setStatus(String message, boolean warning) {
        statusLabel.setText(message);
        statusLabel.setForeground(warning ? new Color(0xD9, 0x4A, 0x5A) : Theme.TEXT_MUTED);
    }

    /**
     * 弹出胜利对话框。
     *
     * @param moves 完成的步数
     */
    public void showWinDialog(int moves) {
        String comment;
        if (moves <= Board.MIN_MOVES) {
            comment = "完美！你走的是理论最少步数。";
        } else if (moves <= Board.MIN_MOVES + 4) {
            comment = "很棒，离最优解已经很近了。";
        } else {
            comment = "成功换位，再试试用更少的步数完成吧。";
        }
        JOptionPane.showMessageDialog(this,
                "恭喜，左右两组动物成功交换了位置！\n共用 " + moves + " 步。\n" + comment,
                "过关", JOptionPane.INFORMATION_MESSAGE);
    }

    /**
     * 弹出玩法说明。
     */
    public void showHelp() {
        String text = "【目标】\n"
                + "让左边三只兔子与右边三只乌龟交换位置。\n\n"
                + "【移动规则】\n"
                + "1. 兔子只能向右走，乌龟只能向左走；\n"
                + "2. 前方相邻格子为空时，走一格；\n"
                + "3. 前方相邻格子有动物、而再前面一格为空时，跳过这只动物；\n"
                + "4. 其余情况都不能移动。\n\n"
                + "【操作】\n"
                + "单击动物即可移动；点击“撤销”回退一步（Ctrl+Z）；"
                + "点击“重新开始”回到初始局面（Ctrl+R）；"
                + "按 F1 再次打开本说明。\n\n"
                + "【提示】\n理论最少 " + Board.MIN_MOVES + " 步即可完成。";
        JOptionPane.showMessageDialog(this, text, "玩法说明", JOptionPane.INFORMATION_MESSAGE);
    }

    /**
     * 渐变背景的标题面板。
     */
    private static class GradientPanel extends JPanel {

        private static final long serialVersionUID = 1L;

        @Override
        protected void paintComponent(Graphics g) {
            Graphics2D g2 = (Graphics2D) g.create();
            try {
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setPaint(new GradientPaint(0, 0, new Color(0x4F, 0x8C, 0xF7),
                        getWidth(), getHeight(), new Color(0x37, 0x5F, 0xD8)));
                g2.fillRect(0, 0, getWidth(), getHeight());
            } finally {
                g2.dispose();
            }
        }
    }

    /**
     * 步数“胶囊”容器。
     */
    private static class StepsPill extends JPanel {

        private static final long serialVersionUID = 1L;

        /**
         * 构造胶囊容器。
         *
         * @param content 内部标签
         */
        StepsPill(JLabel content) {
            setOpaque(false);
            setLayout(new GridBagLayout());
            setBorder(BorderFactory.createEmptyBorder(8, 18, 8, 18));
            content.setForeground(Color.WHITE);
            add(content);
        }

        @Override
        protected void paintComponent(Graphics g) {
            Graphics2D g2 = (Graphics2D) g.create();
            try {
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(new Color(255, 255, 255, 46));
                g2.fill(new RoundRectangle2D.Double(0, 0, getWidth(), getHeight(), 16, 16));
                g2.setColor(new Color(255, 255, 255, 90));
                g2.draw(new RoundRectangle2D.Double(0.5, 0.5, getWidth() - 1, getHeight() - 1, 16, 16));
            } finally {
                g2.dispose();
            }
        }

        @Override
        public Dimension getPreferredSize() {
            Dimension size = super.getPreferredSize();
            return new Dimension(Math.max(96, size.width), Math.max(48, size.height));
        }
    }
}
