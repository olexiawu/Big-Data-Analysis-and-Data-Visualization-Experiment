import math
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from matplotlib import font_manager


# 字体设置
def get_chinese_font():
    candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans CN",
        "WenQuanYi Zen Hei",
    ]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return "DejaVu Sans"


FONT = get_chinese_font()
plt.rcParams["font.family"] = FONT
plt.rcParams["axes.unicode_minus"] = False


# 绘制南丁格尔圆环图
def draw_chart():
    values = [37.5, 29.2, 20.8, 12.5]
    labels = ["[20,30)", "[30,40)", "[40,50)", ">=50"]

    # 与参考图对应的颜色
    colors = [
        "#512DCB",
        "#6073F3",
        "#66CBDD",
        "#F5C353",
    ]

    bg = "#1A1E43"

    fig = plt.figure(figsize=(8.69, 6.50), dpi=100, facecolor=bg)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=bg)
    ax.set_xlim(0, 869)
    ax.set_ylim(650, 0)
    ax.axis("off")

    # 标题
    ax.text(
        54, 31,
        "2022年上半年各年龄段人数分布",
        color="#F2F2F2",
        fontsize=30,
        fontweight="bold",
        va="top",
        ha="left",
    )

    # 副标题
    ax.text(
        54, 88,
        "公司平均年龄32.5，20-30员工比例最高占比37.5%",
        color="#F2F2F2",
        fontsize=22,
        va="top",
        ha="left",
    )

    # 圆环中心
    cx, cy = 434, 389
    inner_r = 111

    # 四个扇区角度严格按照人数占比换算
    start_angle = -90
    angles = []
    for v in values:
        sweep = v / 100.0 * 360.0
        angles.append((start_angle, start_angle + sweep))
        start_angle += sweep

    # 五层同心圆环，对应“人数占比 + 占位1~4”
    # 每一层很薄，并用细线分隔，形成参考图中的层次感
    outer_radii = [187, 174, 158, 141]
    layer_count = 5

    for idx, ((theta1, theta2), outer_r) in enumerate(zip(angles, outer_radii)):
        total_thickness = outer_r - inner_r
        layer_thickness = total_thickness / layer_count

        for layer in range(layer_count):
            r1 = inner_r + layer * layer_thickness
            r2 = inner_r + (layer + 1) * layer_thickness

            # 轻微缩小角度，避免相邻区域视觉粘连
            gap = 0.15 if idx != 3 else 0.0
            w = Wedge(
                (cx, cy),
                r2,
                theta1 + gap,
                theta2 - gap,
                width=r2 - r1,
                facecolor=colors[idx],
                edgecolor="#333866",
                linewidth=0.45,
            )
            ax.add_patch(w)

    # 中心留空
    ax.add_patch(Circle((cx, cy), inner_r, facecolor=bg, edgecolor="none"))

    # 标注线
    line_width = 0.8

    # [20,30)
    ax.plot([637, 672, 800], [271, 230, 230],
            color=colors[0], linewidth=line_width)
    ax.scatter([637], [271], s=28, color=colors[0], zorder=10)
    ax.text(700, 188, "[20,30)", color="#F2F2F2",
            fontsize=17, ha="left", va="bottom")
    ax.text(704, 210, "37.5%", color=colors[0],
            fontsize=17, fontweight="bold", ha="left", va="bottom")

    # [30,40)
    ax.plot([554, 582, 722], [554, 597, 597],
            color=colors[1], linewidth=line_width)
    ax.scatter([554], [554], s=28, color=colors[1], zorder=10)
    ax.text(633, 545, "[30,40)", color="#F2F2F2",
            fontsize=17, ha="left", va="bottom")
    ax.text(633, 569, "29.2%", color=colors[1],
            fontsize=17, fontweight="bold", ha="left", va="bottom")

    # [40,50)
    ax.plot([256, 227, 81], [356, 396, 396],
            color=colors[2], linewidth=line_width)
    ax.scatter([256], [356], s=28, color=colors[2], zorder=10)
    ax.text(130, 342, "[40,50)", color="#F2F2F2",
            fontsize=17, ha="left", va="bottom")
    ax.text(130, 366, "20.8%", color=colors[2],
            fontsize=17, fontweight="bold", ha="left", va="bottom")

    # >=50
    ax.plot([333, 309, 170], [235, 199, 199],
            color=colors[3], linewidth=line_width)
    ax.scatter([333], [235], s=28, color=colors[3], zorder=10)
    ax.text(227, 146, ">=50", color="#F2F2F2",
            fontsize=17, ha="left", va="bottom")
    ax.text(227, 169, "12.5%", color="#F2F2F2",
            fontsize=17, ha="left", va="bottom")

    # 底部注释
    ax.text(
        54, 609,
        "*注：数据来源于公司人力资源系统，统计日期截至2022.06.30",
        color="#F2F2F2",
        fontsize=15,
        ha="left",
        va="top",
    )

    # 保存图片
    DPI = 100
    BG = bg

    output_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "p20.png"
    )

    plt.savefig(
        output_file,
        dpi=DPI,
        facecolor=BG,
        edgecolor="none",
        pad_inches=0
    )

    plt.show()


if __name__ == "__main__":
    draw_chart()
