import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import numpy as np
from scipy.interpolate import CubicSpline


# 数据
months = [
    "5月", "6月", "7月", "8月", "9月",
    "10月", "11月", "12月", "1月", "2月", "3月"
]

sales = [
    146, 198, 296, 412, 506,
    615, 789, 1021, 3782, 3215, 2936
]


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

    candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans CN"
    ]

    for name in candidates:
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
HEIGHT = 642
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"
ORANGE = "#FF6B3D"
YEAR_2021 = "#65C8D9"
YEAR_2022 = "#F6C34F"

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
    45,
    58,
    "化妆品品类月度销量走势",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=34,
    fontproperties=font_bold
)

ax.text(
    45,
    114,
    "2022年销量迅速增加，1月最高，销量达到3782",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=25,
    fontproperties=font_normal
)


# 坐标区域
x_left = 100
x_right = 832
y_axis = 489
y_top = 185
max_value = 4000

x_positions = np.linspace(
    x_left,
    x_right,
    len(months)
)


def value_to_y(value):
    return y_axis - (
        value / max_value
    ) * (y_axis - y_top)


y_positions = np.array([
    value_to_y(value)
    for value in sales
])


# Y轴刻度
for value in [0, 1000, 2000, 3000, 4000]:
    y = value_to_y(value)

    ax.text(
        82,
        y,
        f"{value:,}",
        ha="right",
        va="center",
        color=ORANGE,
        fontsize=14,
        fontproperties=font_normal
    )


# X轴
ax.plot(
    [x_left, x_right],
    [y_axis, y_axis],
    color=WHITE,
    linewidth=1
)

for x, month in zip(x_positions, months):
    ax.plot(
        [x, x],
        [y_axis, y_axis + 7],
        color=WHITE,
        linewidth=0.8
    )

    ax.text(
        x,
        514,
        month,
        ha="center",
        va="center",
        color=WHITE,
        fontsize=16,
        fontproperties=font_normal
    )


# 平滑曲线
spline = CubicSpline(
    x_positions,
    y_positions,
    bc_type="natural"
)

smooth_x = np.linspace(
    x_positions[0],
    x_positions[-1],
    2000
)

smooth_y = spline(smooth_x)

ax.plot(
    smooth_x,
    smooth_y,
    color=ORANGE,
    linewidth=2,
    solid_capstyle="round",
    solid_joinstyle="round",
    zorder=3
)


# 找到曲线实际最高点
peak_index = np.argmin(smooth_y)

peak_x = smooth_x[peak_index]
peak_y = smooth_y[peak_index]


# 最高点虚线
ax.plot(
    [peak_x, peak_x],
    [peak_y, y_axis],
    color=ORANGE,
    linewidth=1,
    linestyle=(0, (7, 5)),
    alpha=0.8,
    zorder=2
)


# 最高值
ax.text(
    peak_x - 8,
    peak_y - 12,
    "3782",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 年份区域
year_y = 535
year_height = 35

year_2021_left = 80
year_2021_right = 635

ax.add_patch(
    plt.Rectangle(
        (
            year_2021_left,
            year_y
        ),
        year_2021_right - year_2021_left,
        year_height,
        facecolor=YEAR_2021,
        edgecolor="none"
    )
)

year_2022_left = 643
year_2022_right = 846

ax.add_patch(
    plt.Rectangle(
        (
            year_2022_left,
            year_y
        ),
        year_2022_right - year_2022_left,
        year_height,
        facecolor=YEAR_2022,
        edgecolor="none"
    )
)


# 年份文字
ax.text(
    (year_2021_left + year_2021_right) / 2,
    year_y + year_height / 2,
    "2021",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=18,
    fontproperties=font_normal
)

ax.text(
    (year_2022_left + year_2022_right) / 2,
    year_y + year_height / 2,
    "2022",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=18,
    fontproperties=font_normal
)


# 备注
ax.text(
    39,
    607,
    "注：数据来源于公司销售系统，统计日期截至2022.03.31",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 保存
output_file = "p11.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：", output_file)