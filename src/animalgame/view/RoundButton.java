package animalgame.view;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JButton;

/**
 * 圆角按钮：把 Java 默认的方角按钮换成更柔和的样式。
 *
 * <p>通过重写 {@link #paintComponent(Graphics)} 自行绘制背景，
 * 并根据鼠标是否悬停、是否按下改变颜色，得到轻量的交互反馈。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class RoundButton extends JButton {

    private static final long serialVersionUID = 1L;

    /** 底色。 */
    private final Color baseColor;
    /** 鼠标是否悬停。 */
    private boolean hover;

    /**
     * 构造按钮。
     *
     * @param text      按钮文字
     * @param baseColor 底色
     */
    public RoundButton(String text, Color baseColor) {
        super(text);
        this.baseColor = baseColor;
        setFont(Theme.font(Font.PLAIN, 14));
        setForeground(Color.WHITE);
        setFocusPainted(false);
        setContentAreaFilled(false);
        setBorderPainted(false);
        setOpaque(false);
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        setPreferredSize(new Dimension(112, 38));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                hover = true;
                repaint();
            }

            @Override
            public void mouseExited(MouseEvent e) {
                hover = false;
                repaint();
            }
        });
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        try {
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                    RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

            Color fill;
            if (!isEnabled()) {
                fill = new Color(0xCB, 0xD5, 0xE1);
            } else if (getModel().isPressed()) {
                fill = baseColor.darker();
            } else if (hover) {
                fill = lighten(baseColor, 0.12);
            } else {
                fill = baseColor;
            }
            g2.setColor(new Color(0, 0, 0, 18));
            g2.fill(new RoundRectangle2D.Double(0, 2, getWidth(), getHeight() - 1, 14, 14));
            g2.setColor(fill);
            g2.fill(new RoundRectangle2D.Double(0, 0, getWidth(), getHeight() - 2, 14, 14));

            g2.setColor(isEnabled() ? Color.WHITE : new Color(0xF2, 0xF5, 0xF9));
            g2.setFont(getFont());
            FontMetrics fm = g2.getFontMetrics();
            String text = getText();
            int x = (getWidth() - fm.stringWidth(text)) / 2;
            int y = (getHeight() - 2 - fm.getHeight()) / 2 + fm.getAscent();
            g2.drawString(text, x, y);
        } finally {
            g2.dispose();
        }
    }

    /**
     * 把颜色按比例调亮。
     *
     * @param color 原色
     * @param ratio 调亮比例，0 表示不变，1 表示全白
     * @return 调亮后的颜色
     */
    private Color lighten(Color color, double ratio) {
        int r = (int) (color.getRed() + (255 - color.getRed()) * ratio);
        int g = (int) (color.getGreen() + (255 - color.getGreen()) * ratio);
        int b = (int) (color.getBlue() + (255 - color.getBlue()) * ratio);
        return new Color(Math.min(255, r), Math.min(255, g), Math.min(255, b));
    }
}
