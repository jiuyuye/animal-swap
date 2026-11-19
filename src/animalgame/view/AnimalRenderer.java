package animalgame.view;

import animalgame.model.Animal;
import animalgame.model.LeftAnimal;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Shape;
import java.awt.geom.AffineTransform;
import java.awt.geom.Arc2D;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Path2D;
import java.awt.geom.RoundRectangle2D;

/**
 * 动物绘制器：用 Java2D 矢量图形画出兔子与乌龟。
 *
 * <p>不使用图片资源，因此程序可以单文件发布，也不会因缺少素材而显示异常；
 * 绘制统一在一个边长为 {@code size} 的正方形区域中完成，内部以 100 为坐标单位缩放。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public final class AnimalRenderer {

    /** 兔子耳朵内侧的粉色。 */
    private static final Color RABBIT_EAR_INNER = new Color(0xF7, 0xC2, 0xD3);
    /** 眼睛颜色。 */
    private static final Color EYE = new Color(0x2B, 0x2B, 0x2B);
    /** 鼻子颜色。 */
    private static final Color NOSE = new Color(0xE8, 0x79, 0x8F);
    /** 龟壳花纹颜色。 */
    private static final Color SHELL_PATTERN = new Color(0x3E, 0x8F, 0x4F);
    /** 龟的皮肤颜色。 */
    private static final Color TURTLE_SKIN = new Color(0xA8, 0xDC, 0xA8);
    /** 阴影颜色。 */
    private static final Color SHADOW = new Color(0, 0, 0, 28);

    private AnimalRenderer() {
    }

    /**
     * 在指定中心位置绘制一只动物。
     *
     * @param g2     画笔
     * @param animal 动物对象
     * @param cx     中心横坐标（像素）
     * @param cy     中心纵坐标（像素）
     * @param size   包围盒边长（像素）
     */
    public static void draw(Graphics2D g2, Animal animal, double cx, double cy, double size) {
        Graphics2D g = (Graphics2D) g2.create();
        try {
            g.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING,
                    java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
            g.translate(cx, cy);
            double unit = size / 100.0;
            g.scale(unit, unit);

            drawShadow(g);
            if (animal instanceof LeftAnimal) {
                drawRabbit(g);
            } else {
                drawTurtle(g, animal.getDirection().getStep());
            }
        } finally {
            g.dispose();
        }
    }

    /**
     * 绘制动物脚下的柔和阴影。
     *
     * @param g 画笔（已缩放到 100 单位坐标系）
     */
    private static void drawShadow(Graphics2D g) {
        g.setColor(SHADOW);
        g.fill(new Ellipse2D.Double(-30, 34, 60, 12));
    }

    /**
     * 绘制兔子（正面视角）。
     *
     * @param g 画笔（已缩放到 100 单位坐标系）
     */
    private static void drawRabbit(Graphics2D g) {
        // 耳朵（先左后右，带一点外张角度）
        Shape leftEar = new RoundRectangle2D.Double(-21, -62, 15, 46, 15, 15);
        Shape rightEar = new RoundRectangle2D.Double(6, -62, 15, 46, 15, 15);
        paintShape(g, leftEar, Theme.RABBIT_BODY, Theme.RABBIT_LINE, 2.6f);
        paintShape(g, rightEar, Theme.RABBIT_BODY, Theme.RABBIT_LINE, 2.6f);

        g.setColor(RABBIT_EAR_INNER);
        g.fill(new RoundRectangle2D.Double(-17.5, -57, 8, 34, 8, 8));
        g.fill(new RoundRectangle2D.Double(9.5, -57, 8, 34, 8, 8));

        // 身体
        paintShape(g, new Ellipse2D.Double(-26, 0, 52, 30), Theme.RABBIT_BODY, Theme.RABBIT_LINE, 2.6f);

        // 头
        paintShape(g, new Ellipse2D.Double(-31, -34, 62, 58), Theme.RABBIT_BODY, Theme.RABBIT_LINE, 2.6f);

        // 眼睛
        g.setColor(EYE);
        g.fill(new Ellipse2D.Double(-15, -16, 9, 9));
        g.fill(new Ellipse2D.Double(6, -16, 9, 9));
        g.setColor(Color.WHITE);
        g.fill(new Ellipse2D.Double(-13.2, -14.2, 3.4, 3.4));
        g.fill(new Ellipse2D.Double(7.8, -14.2, 3.4, 3.4));

        // 鼻子与嘴
        g.setColor(NOSE);
        Path2D nose = new Path2D.Double();
        nose.moveTo(-4.5, 4);
        nose.lineTo(4.5, 4);
        nose.lineTo(0, 9.5);
        nose.closePath();
        g.fill(nose);
        g.setColor(Theme.RABBIT_LINE);
        g.setStroke(new BasicStroke(1.8f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g.draw(new Arc2D.Double(-8, 6, 8, 9, 200, 120, Arc2D.OPEN));
        g.draw(new Arc2D.Double(0, 6, 8, 9, 220, 120, Arc2D.OPEN));

        // 胡须
        g.setStroke(new BasicStroke(1.4f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g.setColor(new Color(0xC9, 0xA6, 0xB4));
        g.draw(new java.awt.geom.Line2D.Double(-10, 4, -30, -1));
        g.draw(new java.awt.geom.Line2D.Double(-10, 9, -30, 12));
        g.draw(new java.awt.geom.Line2D.Double(10, 4, 30, -1));
        g.draw(new java.awt.geom.Line2D.Double(10, 9, 30, 12));

        // 腮红
        g.setColor(new Color(0xF9, 0xC5, 0xD2, 150));
        g.fill(new Ellipse2D.Double(-24, -4, 10, 7));
        g.fill(new Ellipse2D.Double(14, -4, 10, 7));
    }

    /**
     * 绘制乌龟（俯视视角）。
     *
     * @param g    画笔（已缩放到 100 单位坐标系）
     * @param step 前进方向：1 表示向右，-1 表示向左
     */
    private static void drawTurtle(Graphics2D g, int step) {
        // 四条腿
        g.setColor(TURTLE_SKIN);
        g.fill(new Ellipse2D.Double(-38, -14, 16, 11));
        g.fill(new Ellipse2D.Double(22, -14, 16, 11));
        g.fill(new Ellipse2D.Double(-38, 8, 16, 11));
        g.fill(new Ellipse2D.Double(22, 8, 16, 11));

        // 尾巴
        g.setColor(TURTLE_SKIN);
        Path2D tail = new Path2D.Double();
        tail.moveTo(-step * 26, 0);
        tail.lineTo(-step * 40, 4);
        tail.lineTo(-step * 26, 9);
        tail.closePath();
        g.fill(tail);

        // 头
        double headX = step * 34;
        paintShape(g, new Ellipse2D.Double(headX - 11, -6, 22, 20), TURTLE_SKIN, Theme.TURTLE_LINE, 2.2f);
        g.setColor(EYE);
        g.fill(new Ellipse2D.Double(headX - 6.2, -1.4, 4.8, 4.8));
        g.fill(new Ellipse2D.Double(headX + 1.4, -1.4, 4.8, 4.8));
        g.setColor(Color.WHITE);
        g.fill(new Ellipse2D.Double(headX - 4.9, -0.2, 1.8, 1.8));
        g.fill(new Ellipse2D.Double(headX + 2.7, -0.2, 1.8, 1.8));

        // 龟壳外圈
        paintShape(g, new Ellipse2D.Double(-30, -28, 60, 60), Theme.TURTLE_SHELL, Theme.TURTLE_LINE, 3.2f);

        // 龟壳花纹
        g.setColor(SHELL_PATTERN);
        g.setStroke(new BasicStroke(1.8f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        Ellipse2D inner = new Ellipse2D.Double(-19, -17, 38, 38);
        g.draw(inner);
        for (int i = 0; i < 6; i++) {
            double angle = Math.PI / 6 + i * Math.PI / 3;
            double x1 = Math.cos(angle) * 8;
            double y1 = Math.sin(angle) * 8 + 2;
            double x2 = Math.cos(angle) * 26;
            double y2 = Math.sin(angle) * 26 + 2;
            g.draw(new java.awt.geom.Line2D.Double(x1, y1, x2, y2));
        }
        g.fill(new Ellipse2D.Double(-7, -5, 14, 14));

        // 高光
        g.setColor(new Color(255, 255, 255, 70));
        g.fill(new Arc2D.Double(-24, -22, 30, 30, 100, 70, Arc2D.PIE));
    }

    /**
     * 以“填充 + 描边”的方式绘制一个图形。
     *
     * @param g      画笔
     * @param shape  图形
     * @param fill   填充色
     * @param stroke 描边色
     * @param width  描边宽度
     */
    private static void paintShape(Graphics2D g, Shape shape, Color fill, Color stroke, float width) {
        g.setColor(fill);
        g.fill(shape);
        g.setColor(stroke);
        g.setStroke(new BasicStroke(width, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g.draw(shape);
    }
}
