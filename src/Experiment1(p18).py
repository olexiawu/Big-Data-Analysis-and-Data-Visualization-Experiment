import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib import font_manager
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

values = [
    451,
    326,
    293,
    238,
    226,
    130
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
HEIGHT = 612
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
    53,
    70,
    "2022年上半年各部门人数",
    fontsize=31,
    fontproperties=font_bold,
    color=WHITE,
    ha="left",
    va="center"
)

ax.text(
    53,
    122,
    "公司总人数1664，销售部人数最多451，占比27%",
    fontsize=20,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# ==================== 跑道参数 ====================

center_x = 390
center_y = 370

# 从画面正上方开始
start_angle = 270

# 最外层半径
outer_radius = 207

# 跑道宽度
track_width = 14

# 跑道之间的深蓝色间隔
track_gap = 7

# 六条跑道的颜色
colors = [
    "#ED4D6D",   # 销售部
    "#F7C95B",   # 采购部
    "#1AA7AD",   # 工程部
    "#38A5D8",   # 财务部
    "#167BC4",   # 行政部
    "#7542B7"    # 人力部
]


# ==================== 跑道长度 ====================

min_value = min(values)
max_value = max(values)

# 参考图中最长、最短跑道的角度范围
min_angle = 48
max_angle = 235

angles = []

for value in values:

    ratio = (value - min_value) / (max_value - min_value)

    angle = min_angle + ratio * (max_angle - min_angle)

    angles.append(angle)


# ==================== 绘制跑道 ====================

for i, (department, value, color, angle) in enumerate(
    zip(departments, values, colors, angles)
):

    # 每条跑道独立半径
    radius = (
        outer_radius
        - i * (track_width + track_gap)
    )

    end_angle = start_angle + angle

    arc = Arc(
        (
            center_x,
            center_y
        ),
        2 * radius,
        2 * radius,
        angle=0,
        theta1=start_angle,
        theta2=end_angle,
        linewidth=track_width,
        color=color,
        capstyle="butt"
    )

    ax.add_patch(arc)


# ==================== 部门文字 ====================

label_x = 312

label_y = [
    170,
    188,
    207,
    226,
    245,
    264
]

for department, value, y in zip(
    departments,
    values,
    label_y
):

    ax.text(
        label_x,
        y,
        f"{department} {value}",
        fontsize=13,
        fontproperties=font_normal,
        color=WHITE,
        ha="left",
        va="center"
    )


# ==================== 底部备注 ====================

ax.text(
    40,
    585,
    "注：数据来源于公司人力资源系统，统计日期截至2022.06.30",
    fontsize=14,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# ==================== 保存 ====================

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p18.png"
)

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)


# ==================== 显示 ====================

plt.show()

print("图片已生成：")
print(output_file)