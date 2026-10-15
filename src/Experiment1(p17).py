import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib import font_manager
import os


# 数据
labels = [
    "[20,30)",
    "[30,40)",
    "[40,50)",
    ">=50"
]

percentages = [37.5, 29.2, 20.8, 12.5]


# 字体
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


# 画布
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


# 标题
ax.text(
    53,
    70,
    "2022年上半年龄分布",
    fontsize=31,
    fontproperties=font_bold,
    color=WHITE,
    ha="left",
    va="center"
)

ax.text(
    53,
    121,
    "公司平均年龄32.5，23-30员工比例最高",
    fontsize=20,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# 玉玦图参数
center_x = 438
center_y = 360

outer_radius = 187
ring_width = 28
ring_gap = 2

colors = [
    "#38A5D8",
    "#1DA6AD",
    "#F7C95B",
    "#ED4D6D"
]

radii = [
    outer_radius - 3 * (ring_width + ring_gap),
    outer_radius - 2 * (ring_width + ring_gap),
    outer_radius - 1 * (ring_width + ring_gap),
    outer_radius
]


# 累计占比
cumulative = []

total = 0

for value in percentages:
    total += value
    cumulative.append(total)


# 绘制玉玦
available_angle = 270

# 从正上方开始，彩色部分向右、向下、向左延伸
# 因为画布Y轴向下，所以270°对应画面正上方
start_angle = 270

for radius, color, cum_value in zip(
    radii,
    colors,
    cumulative
):

    arc_angle = available_angle * cum_value / 100

    end_angle = start_angle + arc_angle

    wedge = Wedge(
        (center_x, center_y),
        radius,
        start_angle,
        end_angle,
        width=ring_width,
        facecolor=color,
        edgecolor=BG,
        linewidth=2
    )

    ax.add_patch(wedge)


# 年龄区间文字
label_x = 365

label_y = [
    184,
    216,
    248,
    280
]

for label, y in zip(labels, label_y):

    ax.text(
        label_x,
        y,
        label,
        fontsize=18,
        fontproperties=font_normal,
        color=WHITE,
        ha="left",
        va="center"
    )


# 百分比文字
ax.text(
    270,
    338,
    "37.5%",
    fontsize=16,
    fontproperties=font_normal,
    color=WHITE,
    ha="center",
    va="center"
)

ax.text(
    356,
    466,
    "29.2%",
    fontsize=16,
    fontproperties=font_normal,
    color=WHITE,
    ha="center",
    va="center"
)

ax.text(
    469,
    465,
    "20.8%",
    fontsize=16,
    fontproperties=font_normal,
    color=WHITE,
    ha="center",
    va="center"
)

ax.text(
    513,
    378,
    "12.5%",
    fontsize=16,
    fontproperties=font_normal,
    color=WHITE,
    ha="center",
    va="center"
)


# 底部备注
ax.text(
    53,
    587,
    "*注：数据来源于公司人力资源系统，统计日期截至2022.06.30",
    fontsize=14,
    fontproperties=font_normal,
    color=WHITE,
    ha="left",
    va="center"
)


# 保存
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p17.png"
)

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：")
print(output_file)