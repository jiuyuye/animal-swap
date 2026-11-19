package animalgame.view;

import java.awt.Color;
import java.awt.Font;
import java.awt.GraphicsEnvironment;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * 界面配色与字体工具类。
 *
 * <p>把颜色、字号集中在一处，方便统一调整风格；
 * 字体则按优先级挑选系统中真实存在的字族，避免中文显示成方块。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public final class Theme {

    /** 窗口与面板的主背景色。 */
    public static final Color BACKGROUND_TOP = new Color(0xF7, 0xFB, 0xFF);
    /** 背景渐变的下半部分颜色。 */
    public static final Color BACKGROUND_BOTTOM = new Color(0xE4, 0xEE, 0xF9);
    /** 格子底色。 */
    public static final Color SLOT_FILL = new Color(0xFF, 0xFF, 0xFF);
    /** 格子边框色。 */
    public static final Color SLOT_BORDER = new Color(0xC7, 0xD8, 0xEA);
    /** 空格子（中间那个位置）的底色。 */
    public static final Color EMPTY_SLOT_FILL = new Color(0xEF, 0xF4, 0xFA);
    /** 主文字颜色。 */
    public static final Color TEXT = new Color(0x2F, 0x3D, 0x4F);
    /** 次要文字颜色。 */
    public static final Color TEXT_MUTED = new Color(0x7B, 0x8B, 0x9E);
    /** 强调色（按钮、高亮）。 */
    public static final Color ACCENT = new Color(0x3B, 0x82, 0xF6);
    /** 可落点提示色。 */
    public static final Color HINT = new Color(0x22, 0xC5, 0x5E);
    /** 兔子主色。 */
    public static final Color RABBIT_BODY = new Color(0xFF, 0xF6, 0xF9);
    /** 兔子描边色。 */
    public static final Color RABBIT_LINE = new Color(0xE0, 0x9C, 0xB6);
    /** 乌龟主色。 */
    public static final Color TURTLE_SHELL = new Color(0x6F, 0xC2, 0x7C);
    /** 乌龟描边色。 */
    public static final Color TURTLE_LINE = new Color(0x3F, 0x8C, 0x52);

    /** 候选字体，按优先级排列。 */
    private static final String[] FONT_CANDIDATES = {
        "Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", "Dialog"
    };

    private static final String UI_FONT = pickFont();

    private Theme() {
    }

    /**
     * 在系统中挑选第一个可用的中文字族。
     *
     * @return 可用的字族名称
     */
    private static String pickFont() {
        Set<String> available = new HashSet<>(Arrays.asList(
                GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames()));
        for (String name : FONT_CANDIDATES) {
            if (available.contains(name)) {
                return name;
            }
        }
        return Font.DIALOG;
    }

    /**
     * 取得界面通用字体。
     *
     * @param style 字形，如 {@link Font#PLAIN}
     * @param size  字号
     * @return 字体对象
     */
    public static Font font(int style, int size) {
        return new Font(UI_FONT, style, size);
    }

    /**
     * 取得当前使用的字族名称。
     *
     * @return 字族名称
     */
    public static String fontFamily() {
        return UI_FONT;
    }
}
