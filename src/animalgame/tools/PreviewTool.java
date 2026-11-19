package animalgame.tools;

import animalgame.model.Board;
import animalgame.view.BoardPanel;
import animalgame.view.GameFrame;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.JComponent;

/**
 * 截图工具：把界面离屏渲染成 PNG，供课程设计说明书使用。
 *
 * <p>它不参与游戏运行，只在生成文档时调用，因此单独放在 tools 包中。</p>
 *
 * @author 课程设计
 * @version 1.0
 */
public final class PreviewTool {

    private PreviewTool() {
    }

    /**
     * 生成初始局面、中局与整窗三张截图。
     *
     * @param args 第一个参数为输出目录，缺省为当前目录
     * @throws Exception 写文件失败时抛出
     */
    public static void main(String[] args) throws Exception {
        String dir = args.length > 0 ? args[0] : ".";
        int[][] head = {
            {2, 3}, {4, 2}, {5, 4}, {3, 5}, {1, 3}, {0, 1}
        };

        Board initial = new Board();
        save(new BoardPanel(initial), dir + File.separator + "shot_board_start.png");

        Board mid = new Board();
        for (int[] mv : head) {
            mid.move(mid.getAnimalAt(mv[0]));
        }
        save(new BoardPanel(mid), dir + File.separator + "shot_board_mid.png");

        try {
            GameFrame frame = new GameFrame(new Board());
            frame.pack();
            save(frame.getContentPane(), dir + File.separator + "shot_window.png");
        } catch (Throwable t) {
            System.out.println("整窗截图跳过：" + t);
        }
        System.out.println("截图已生成到 " + new File(dir).getAbsolutePath());
        System.exit(0);
    }

    /**
     * 把一个组件离屏绘制成 PNG。
     *
     * @param component 目标组件
     * @param path      输出路径
     * @throws Exception 写文件失败时抛出
     */
    private static void save(Component component, String path) throws Exception {
        Dimension size = component.getPreferredSize();
        component.setSize(size);
        if (component instanceof Container) {
            doLayoutRecursively((Container) component);
        }
        BufferedImage image = new BufferedImage(size.width, size.height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = image.createGraphics();
        try {
            g.setColor(Color.WHITE);
            g.fillRect(0, 0, size.width, size.height);
            component.paint(g);
        } finally {
            g.dispose();
        }
        ImageIO.write(image, "png", new File(path));
    }

    /**
     * 递归执行布局，保证离屏绘制时子组件位置正确。
     *
     * @param container 容器
     */
    private static void doLayoutRecursively(Container container) {
        container.doLayout();
        for (Component child : container.getComponents()) {
            if (child instanceof Container) {
                doLayoutRecursively((Container) child);
            }
        }
    }
}
