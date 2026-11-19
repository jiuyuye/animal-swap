package animalgame.view;

import animalgame.model.Animal;
import animalgame.model.Board;
import animalgame.model.Direction;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GradientPaint;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.Ellipse2D;
import java.awt.geom.RoundRectangle2D;
import javax.swing.JPanel;
import javax.swing.Timer;

/**
 * 棋盘面板：负责绘制 7 个格子、动物以及移动动画，并把点击事件交给控制器。
 *
 * <p>本类只“画”和“收事件”，所有规则判断都在模型层完成，
 * 因此界面代码里看不到任何关于“能不能跳”的逻辑。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public class BoardPanel extends JPanel {

    private static final long serialVersionUID = 1L;

    /** 面板内边距。 */
    private static final int PADDING = 24;
    /** 单个格子的宽度。 */
    private static final int SLOT_WIDTH = 92;
    /** 格子之间的间距。 */
    private static final int SLOT_GAP = 10;
    /** 单个格子的高度。 */
    private static final int SLOT_HEIGHT = 168;
    /** 动物图形的边长。 */
    private static final int ANIMAL_SIZE = 86;
    /** 动画总时长（毫秒）。 */
    private static final int ANIMATION_MILLIS = 260;
    /** 无效点击提示的持续时间（毫秒）。 */
    private static final int FLASH_MILLIS = 480;

    private final Board board;

    /** 点击回调。 */
    private GameListener listener;

    /** 鼠标悬停的格子下标，-1 表示没有悬停。 */
    private int hoverIndex = -1;

    /** 正在做动画的动物。 */
    private Animal flyingAnimal;
    /** 动画起点格子下标。 */
    private int flyFrom = -1;
    /** 动画终点格子下标。 */
    private int flyTo = -1;
    /** 动画开始时刻（纳秒）。 */
    private long flyStart;
    /** 动画结束后的回调。 */
    private Runnable flyCallback;

    /** 需要闪烁提示“不能移动”的动物。 */
    private Animal flashAnimal;
    /** 闪烁开始时刻（毫秒）。 */
    private long flashStart;

    /** 统一驱动动画与闪烁重绘的定时器。 */
    private final Timer ticker;

    /**
     * 构造棋盘面板。
     *
     * @param board 棋盘模型
     */
    public BoardPanel(Board board) {
        this.board = board;
        setOpaque(true);
        setPreferredSize(new Dimension(
                PADDING * 2 + Board.SLOT_COUNT * SLOT_WIDTH + (Board.SLOT_COUNT - 1) * SLOT_GAP,
                PADDING * 2 + SLOT_HEIGHT));
        setFocusable(true);

        ticker = new Timer(16, e -> {
            boolean animating = flyingAnimal != null;
            if (animating && System.nanoTime() - flyStart >= ANIMATION_MILLIS * 1_000_000L) {
                finishAnimation();
            }
            if (flashAnimal != null && System.currentTimeMillis() - flashStart > FLASH_MILLIS) {
                flashAnimal = null;
            }
            if (flyingAnimal == null && flashAnimal == null) {
                ((Timer) e.getSource()).stop();
            }
            repaint();
        });

        MouseAdapter mouse = new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                handleClick(e);
            }

            @Override
            public void mouseMoved(MouseEvent e) {
                int index = slotAt(e.getX(), e.getY());
                if (index != hoverIndex) {
                    hoverIndex = index;
                    repaint();
                }
            }

            @Override
            public void mouseExited(MouseEvent e) {
                hoverIndex = -1;
                repaint();
            }
        };
        addMouseListener(mouse);
        addMouseMotionListener(mouse);
    }

    /**
     * 设置点击监听器。
     *
     * @param listener 监听器
     */
    public void setGameListener(GameListener listener) {
        this.listener = listener;
    }

    /**
     * 判断当前是否正在播放移动动画。
     *
     * @return 动画进行中返回 {@code true}
     */
    public boolean isAnimating() {
        return flyingAnimal != null;
    }

    /**
     * 播放一次移动动画。
     *
     * @param animal     被移动的动物
     * @param from       起点下标
     * @param to         终点下标
     * @param onFinished 动画结束后的回调，可为 {@code null}
     */
    public void animateMove(Animal animal, int from, int to, Runnable onFinished) {
        this.flyingAnimal = animal;
        this.flyFrom = from;
        this.flyTo = to;
        this.flyStart = System.nanoTime();
        this.flyCallback = onFinished;
        if (!ticker.isRunning()) {
            ticker.start();
        }
        repaint();
    }

    /**
     * 让某只动物短暂闪红，提示“这一步不能走”。
     *
     * @param animal 被点击但无法移动的动物
     */
    public void flashInvalid(Animal animal) {
        this.flashAnimal = animal;
        this.flashStart = System.currentTimeMillis();
        if (!ticker.isRunning()) {
            ticker.start();
        }
        repaint();
    }

    /**
     * 结束动画并执行回调。
     */
    private void finishAnimation() {
        flyingAnimal = null;
        flyFrom = -1;
        flyTo = -1;
        Runnable callback = flyCallback;
        flyCallback = null;
        if (callback != null) {
            callback.run();
        }
    }

    /**
     * 处理鼠标点击：命中动物就通知监听器。
     *
     * @param e 鼠标事件
     */
    private void handleClick(MouseEvent e) {
        if (isAnimating() || listener == null) {
            return;
        }
        int index = slotAt(e.getX(), e.getY());
        if (index < 0) {
            return;
        }
        Animal animal = board.getAnimalAt(index);
        if (animal != null) {
            listener.onAnimalClicked(animal);
        }
    }

    /**
     * 把像素坐标换算成格子下标。
     *
     * @param x 横坐标
     * @param y 纵坐标
     * @return 格子下标；落空时返回 -1
     */
    private int slotAt(int x, int y) {
        for (int i = 0; i < Board.SLOT_COUNT; i++) {
            if (slotBounds(i).contains(x, y)) {
                return i;
            }
        }
        return -1;
    }

    /**
     * 计算第 {@code index} 个格子的矩形区域。
     *
     * @param index 格子下标
     * @return 矩形
     */
    private RoundRectangle2D slotBounds(int index) {
        int x = PADDING + index * (SLOT_WIDTH + SLOT_GAP);
        int y = PADDING;
        return new RoundRectangle2D.Double(x, y, SLOT_WIDTH, SLOT_HEIGHT, 22, 22);
    }

    /**
     * 计算第 {@code index} 个格子的中心横坐标。
     *
     * @param index 格子下标
     * @return 中心横坐标
     */
    private double slotCenterX(int index) {
        return PADDING + index * (SLOT_WIDTH + SLOT_GAP) + SLOT_WIDTH / 2.0;
    }

    /**
     * 计算动物图形中心的纵坐标。
     *
     * @return 中心纵坐标
     */
    private double animalCenterY() {
        return PADDING + SLOT_HEIGHT / 2.0 - 8;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g.create();
        try {
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
            g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                    RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

            paintBackground(g2);
            paintSlots(g2);
            paintHint(g2);
            paintAnimals(g2);
        } finally {
            g2.dispose();
        }
    }

    /**
     * 绘制整体背景渐变，以及承载格子的白色卡片。
     *
     * @param g2 画笔
     */
    private void paintBackground(Graphics2D g2) {
        g2.setPaint(new GradientPaint(0, 0, Theme.BACKGROUND_TOP, 0, getHeight(), Theme.BACKGROUND_BOTTOM));
        g2.fillRect(0, 0, getWidth(), getHeight());

        double cardX = PADDING - 14;
        double cardY = PADDING - 16;
        double cardW = getWidth() - cardX * 2;
        double cardH = getHeight() - cardY - 10;
        g2.setColor(new Color(0, 0, 0, 14));
        g2.fill(new RoundRectangle2D.Double(cardX, cardY + 4, cardW, cardH, 26, 26));
        g2.setColor(new Color(255, 255, 255, 190));
        g2.fill(new RoundRectangle2D.Double(cardX, cardY, cardW, cardH, 26, 26));
    }

    /**
     * 绘制 7 个格子。
     *
     * @param g2 画笔
     */
    private void paintSlots(Graphics2D g2) {
        int emptySlot = findEmptySlot();
        for (int i = 0; i < Board.SLOT_COUNT; i++) {
            RoundRectangle2D rect = slotBounds(i);
            boolean isEmpty = board.getAnimalAt(i) == null;
            g2.setColor(isEmpty ? Theme.EMPTY_SLOT_FILL : Theme.SLOT_FILL);
            g2.fill(rect);

            if (isEmpty) {
                g2.setColor(new Color(0xB8, 0xC8, 0xDA));
                g2.setStroke(new BasicStroke(1.6f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
                        1.0f, new float[] {6f, 5f}, 0f));
            } else {
                g2.setColor(Theme.SLOT_BORDER);
                g2.setStroke(new BasicStroke(1.6f));
            }
            g2.draw(rect);

            if (i == emptySlot) {
                g2.setColor(new Color(0x9E, 0xAF, 0xC2));
                g2.setFont(Theme.font(java.awt.Font.PLAIN, 13));
                String text = "空位";
                int w = g2.getFontMetrics().stringWidth(text);
                g2.drawString(text, (int) (rect.getCenterX() - w / 2.0), (int) (rect.getY() + 26));
            }
        }
    }

    /**
     * 绘制可落点提示：鼠标悬停在可移动动物上时，用绿色虚线圈出目标格子。
     *
     * @param g2 画笔
     */
    private void paintHint(Graphics2D g2) {
        if (hoverIndex < 0 || isAnimating()) {
            return;
        }
        Animal hovered = board.getAnimalAt(hoverIndex);
        if (hovered == null || !board.canMove(hovered)) {
            return;
        }
        int target = findTargetOf(hovered);
        if (target < 0) {
            return;
        }
        RoundRectangle2D rect = slotBounds(target);
        g2.setColor(new Color(Theme.HINT.getRed(), Theme.HINT.getGreen(), Theme.HINT.getBlue(), 60));
        g2.fill(rect);
        g2.setColor(Theme.HINT);
        g2.setStroke(new BasicStroke(2.4f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
                1.0f, new float[] {7f, 5f}, 0f));
        g2.draw(rect);
    }

    /**
     * 绘制所有动物以及标题文字。
     *
     * @param g2 画笔
     */
    private void paintAnimals(Graphics2D g2) {
        double cy = animalCenterY();
        for (int i = 0; i < Board.SLOT_COUNT; i++) {
            Animal animal = board.getAnimalAt(i);
            if (animal == null || animal == flyingAnimal) {
                continue;
            }
            double cx = slotCenterX(i);
            AnimalRenderer.draw(g2, animal, cx, cy, ANIMAL_SIZE);
            paintLabel(g2, animal, cx);
            paintHoverRing(g2, animal, cx, cy);
        }
        paintFlyingAnimal(g2, cy);
    }

    /**
     * 绘制动物下方的名字与前进方向。
     *
     * @param g2     画笔
     * @param animal 动物
     * @param cx     中心横坐标
     */
    private void paintLabel(Graphics2D g2, Animal animal, double cx) {
        String arrow = animal.getDirection() == Direction.RIGHT ? "→" : "←";
        String text = animal.getName() + " " + arrow;
        g2.setFont(Theme.font(java.awt.Font.PLAIN, 13));
        int w = g2.getFontMetrics().stringWidth(text);
        int y = PADDING + SLOT_HEIGHT - 12;
        g2.setColor(Theme.TEXT_MUTED);
        g2.drawString(text, (int) (cx - w / 2.0), y);
    }

    /**
     * 鼠标悬停在可移动的动物上时，给它加一圈蓝色高亮。
     *
     * @param g2     画笔
     * @param animal 动物
     * @param cx     中心横坐标
     * @param cy     中心纵坐标
     */
    private void paintHoverRing(Graphics2D g2, Animal animal, double cx, double cy) {
        boolean hovered = animal.getPosition() == hoverIndex;
        boolean invalid = animal == flashAnimal;
        if (!hovered && !invalid) {
            return;
        }
        boolean movable = board.canMove(animal);
        Color color = invalid || !movable ? new Color(0xE0, 0x4F, 0x5F) : Theme.ACCENT;
        double pad = 4;
        g2.setColor(new Color(color.getRed(), color.getGreen(), color.getBlue(), 45));
        g2.fill(new Ellipse2D.Double(cx - ANIMAL_SIZE / 2.0 - pad, cy - ANIMAL_SIZE / 2.0 - pad,
                ANIMAL_SIZE + pad * 2, ANIMAL_SIZE + pad * 2));
        g2.setColor(color);
        g2.setStroke(new BasicStroke(2.2f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
                1.0f, new float[] {8f, 5f}, 0f));
        g2.draw(new Ellipse2D.Double(cx - ANIMAL_SIZE / 2.0 - pad, cy - ANIMAL_SIZE / 2.0 - pad,
                ANIMAL_SIZE + pad * 2, ANIMAL_SIZE + pad * 2));
    }

    /**
     * 绘制正在播放动画的动物：水平线性插值，跳跃时叠加抛物线高度。
     *
     * @param g2 画笔
     * @param cy 目标中心纵坐标
     */
    private void paintFlyingAnimal(Graphics2D g2, double cy) {
        if (flyingAnimal == null) {
            return;
        }
        double progress = (System.nanoTime() - flyStart) / (double) (ANIMATION_MILLIS * 1_000_000L);
        progress = Math.max(0, Math.min(1, progress));
        double eased = progress < 0.5
                ? 2 * progress * progress
                : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        double x = slotCenterX(flyFrom) + (slotCenterX(flyTo) - slotCenterX(flyFrom)) * eased;
        boolean jump = Math.abs(flyTo - flyFrom) == 2;
        double arc = jump ? 46 : 16;
        double y = cy - Math.sin(Math.PI * progress) * arc;
        AnimalRenderer.draw(g2, flyingAnimal, x, y, ANIMAL_SIZE);
    }

    /**
     * 找到当前唯一空格的下标。
     *
     * @return 空格下标；异常时返回 -1
     */
    private int findEmptySlot() {
        for (int i = 0; i < Board.SLOT_COUNT; i++) {
            if (board.getAnimalAt(i) == null) {
                return i;
            }
        }
        return -1;
    }

    /**
     * 计算某只动物本次可以落到的格子下标。
     *
     * @param animal 动物
     * @return 目标下标；不能移动时返回 -1
     */
    private int findTargetOf(Animal animal) {
        return board.resolveTarget(animal);
    }

    /**
     * 棋盘点击事件的监听接口。
     */
    public interface GameListener {

        /**
         * 用户点击了某只动物。
         *
         * @param animal 被点击的动物
         */
        void onAnimalClicked(Animal animal);
    }
}
