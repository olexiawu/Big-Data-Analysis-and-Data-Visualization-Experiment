import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import numpy as np


# 数据
months = ["1月", "2月", "3月", "4月", "5月", "6月"]
data_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
data_2022 = [1385, 1846, 1654, 1936, 2564, 2236]


# 中文字体
def find_chinese_font(bold=False):
    if os.name == "nt":
        if bold:
            fonts = [
                r"C:\Windows\Fonts\msyhbd.ttc",
                r"C:\Windows\Fonts\msyhbd.ttf",
                r"C:\Windows\Fonts\simhei.ttf"
            ]
        else:
            fonts = [
                r"C:\Windows\Fonts\msyh.ttc",
                r"C:\Windows\Fonts\msyh.ttf",
                r"C:\Windows\Fonts\simhei.ttf"
            ]

        for path in fonts:
            if os.path.exists(path):
                return font_manager.FontProperties(fname=path)

    fonts = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans CN"
    ]

    for name in fonts:
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
WIDTH = 866
HEIGHT = 649
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"
PINK = "#F54C6C"
BLUE = "#0079C8"
GRID = "#555A78"


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
    55,
    65,
    "2022年上半年各月同比去年销量",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)

ax.text(
    55,
    123,
    "上半年同比去年增长明显，5月份同比增长最多，增长近40%",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=18,
    fontproperties=font_normal
)


# 图表区域
x_positions = np.linspace(171, 758, 6)

y_top = 232
y_bottom = 550
max_value = 3000


def value_to_y(value):
    return y_bottom - (
        value / max_value
    ) * (y_bottom - y_top)


# Y轴刻度
for value in [0, 500, 1000, 1500, 2000, 2500, 3000]:

    y = value_to_y(value)

    ax.text(
        95,
        y,
        str(value),
        ha="right",
        va="center",
        color=WHITE,
        fontsize=15,
        fontproperties=font_normal
    )

    ax.plot(
        [112, 818],
        [y, y],
        color=GRID,
        linewidth=0.8,
        linestyle=(0, (7, 5)),
        alpha=0.8
    )


# X轴月份
for x, month in zip(x_positions, months):

    ax.text(
        x,
        575,
        month,
        ha="center",
        va="center",
        color=WHITE,
        fontsize=16,
        fontproperties=font_normal
    )


# 两条折线
y_2021 = [value_to_y(v) for v in data_2021]
y_2022 = [value_to_y(v) for v in data_2022]


ax.plot(
    x_positions,
    y_2021,
    color=PINK,
    linewidth=2.5,
    marker="o",
    markersize=6,
    markerfacecolor=PINK,
    markeredgecolor=PINK,
    solid_capstyle="round",
    solid_joinstyle="round",
    zorder=3
)

ax.plot(
    x_positions,
    y_2022,
    color=BLUE,
    linewidth=2.5,
    marker="o",
    markersize=6,
    markerfacecolor=BLUE,
    markeredgecolor=BLUE,
    solid_capstyle="round",
    solid_joinstyle="round",
    zorder=3
)


# 数据标签
for i, (x, y, value) in enumerate(
    zip(x_positions, y_2021, data_2021)
):

    if i in [0, 2, 3, 4]:
        label_y = y - 25
    elif i == 1:
        label_y = y + 27
    else:
        label_y = y + 30

    ax.text(
        x,
        label_y,
        str(value),
        ha="center",
        va="center",
        color=WHITE,
        fontsize=15,
        fontproperties=font_normal
    )


for i, (x, y, value) in enumerate(
    zip(x_positions, y_2022, data_2022)
):

    if i in [0, 2]:
        label_y = y + 35
    elif i in [1, 3, 4]:
        label_y = y - 25
    else:
        label_y = y - 25

    ax.text(
        x,
        label_y,
        str(value),
        ha="center",
        va="center",
        color=WHITE,
        fontsize=15,
        fontproperties=font_normal
    )


# 图例
legend_y = 193

ax.plot(
    [577, 616],
    [legend_y, legend_y],
    color=PINK,
    linewidth=2.5
)

ax.scatter(
    597,
    legend_y,
    s=35,
    color=PINK,
    zorder=4
)

ax.text(
    622,
    legend_y,
    "2021年",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)

ax.plot(
    [699, 738],
    [legend_y, legend_y],
    color=BLUE,
    linewidth=2.5
)

ax.scatter(
    719,
    legend_y,
    s=35,
    color=BLUE,
    zorder=4
)

ax.text(
    744,
    legend_y,
    "2022年",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 备注
ax.text(
    55,
    616,
    "注：数据来源于公司销售系统，统计日期截至2022.06.30",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 保存
output_file = "p13.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：", output_file)