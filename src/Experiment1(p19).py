import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib import font_manager
import numpy as np
import os


# ==================== 数据 ====================

departments = [
    "销售部",
    "采购部",
    "工程部",
    "财务部",
    "行政部",
    "人力部"
]

percentages = [
    29.2,
    22.7,
    17.5,
    13.6,
    10.3,
    6.7
]


# ==================== 字体 ====================

def find_chinese_font(bold=False):
    if os.name == "nt":
        if bold:
            paths = [
                r"C:\Windows\Fonts\msyhbd.ttc",
                r"C:\Windows\Fonts\msyhbd.ttf",
                r"C:\Windows\Fonts\simhei.ttf"
            ]
        else:
            paths = [
                r"C:\Windows\Fonts\msyh.ttc",
                r"C:\Windows\Fonts\msyh.ttf",
                r"C:\Windows\Fonts\simhei.ttf"
            ]

        for path in paths:
            if os.path.exists(path):
                return font_manager.FontProperties(fname=path)

    for name in [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans CN"
    ]:
        try:
            path = font_manager.findfont(
                font_manager.FontProperties(family=name),
                fallback_to_default=False
            )

            if os.path.exists(path):
                return font_manager.FontProperties(fname=path)

        except Exception:
            pass

    return font_manager.FontProperties()


font_normal = find_chinese_font(False)
font_bold = find_chinese_font(True)


# ==================== 画布 ====================

WIDTH = 868
HEIGHT = 648
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"

fig = plt.figure(
    figsize=(WIDTH / DPI, HEIGHT / DPI),
    dpi=DPI,
    facecolor=BG
)

ax = fig.add_axes([0, 0, 1, 1])

ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)

ax.set_facecolor(BG)
ax.axis("off")


# ==================== 标题 ====================

ax.text(
    54,
    62,
    "2021年各部门人数分布",
    fontsize=31,
    fontproperties=font_bold,
    color=WHITE,
    ha="left",
    va="center"
)

ax.text(
    54,
    104,
    "公司总人数1664，销售部人数最多451，占比29.2%",
    fontsize=20,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# ==================== 饼图参数 ====================

center_x = 431
center_y = 381

radius = 226

colors = [
    "#E94D6A",   # 销售部
    "#F8C752",   # 采购部
    "#17A5AD",   # 工程部
    "#0878C1",   # 财务部
    "#3AA2D4",   # 行政部
    "#7431A6"    # 人力部
]


# ==================== 绘制扇区 ====================

start_angle = 90

wedges = []

for department, percentage, color in zip(
    departments,
    percentages,
    colors
):

    angle = percentage / 100 * 360

    end_angle = start_angle + angle

    wedge = Wedge(
        (center_x, center_y),
        radius,
        start_angle,
        end_angle,
        facecolor=color,
        edgecolor=BG,
        linewidth=0
    )

    ax.add_patch(wedge)

    wedges.append(
        (
            department,
            percentage,
            color,
            start_angle,
            end_angle
        )
    )

    start_angle = end_angle


# ==================== 引导线 ====================

# 手动调整标签位置，使整体布局接近参考图

label_positions = {
    "销售部": (650, 222),
    "采购部": (622, 550),
    "工程部": (140, 560),
    "财务部": (118, 410),
    "行政部": (165, 262),
    "人力部": (263, 230)
}


# 引导线颜色
line_colors = {
    "销售部": "#E94D6A",
    "采购部": "#F8C752",
    "工程部": "#17A5AD",
    "财务部": "#0878C1",
    "行政部": "#3AA2D4",
    "人力部": "#7431A6"
}


for department, percentage, color, start, end in wedges:

    mid_angle = (start + end) / 2

    # 计算圆周上的连接点
    angle_rad = np.deg2rad(mid_angle)

    x1 = center_x + radius * np.cos(angle_rad)
    y1 = center_y - radius * np.sin(angle_rad)

    # 第二个连接点
    connector_radius = radius + 27

    x2 = center_x + connector_radius * np.cos(angle_rad)
    y2 = center_y - connector_radius * np.sin(angle_rad)

    # 最终标签位置
    label_x, label_y = label_positions[department]

    # 水平引导线终点
    if label_x > center_x:
        x3 = label_x - 42
    else:
        x3 = label_x + 42

    y3 = y2

    # 第一段
    ax.plot(
        [x1, x2],
        [y1, y2],
        color=line_colors[department],
        linewidth=1.0
    )

    # 第二段
    ax.plot(
        [x2, x3],
        [y2, y3],
        color=line_colors[department],
        linewidth=1.0
    )

    # 圆点
    ax.scatter(
        [x2],
        [y2],
        s=26,
        color=line_colors[department],
        edgecolors="none",
        zorder=5
    )


# ==================== 标签文字 ====================

text_positions = {
    "销售部": (681, 222),
    "采购部": (620, 550),
    "工程部": (110, 560),
    "财务部": (90, 410),
    "行政部": (165, 262),
    "人力部": (300, 230)
}


for department, percentage in zip(
    departments,
    percentages
):

    x, y = text_positions[department]

    if x > center_x:
        ha = "left"
    else:
        ha = "right"

    ax.text(
        x,
        y,
        f"{department} {percentage:.1f}%",
        fontsize=14,
        fontproperties=font_normal,
        color=WHITE,
        ha=ha,
        va="center"
    )


# ==================== 底部备注 ====================

ax.text(
    55,
    616,
    "*注：数据来源于公司人力资源系统，统计日期截至2022.01.01",
    fontsize=14,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# ==================== 保存图片 ====================

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p19.png"
)

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)


# ==================== 显示图片 ====================

plt.show()

print("图片已生成：")
print(output_file)