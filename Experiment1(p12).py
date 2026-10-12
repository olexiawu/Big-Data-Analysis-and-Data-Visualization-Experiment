import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import numpy as np


# 数据
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"]
rates = [53.60, 49.80, 52.70, 70.80, 60.90, 49.60, 58.60, 70.40]


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
WIDTH = 867
HEIGHT = 614
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"
PINK = "#FF496B"
BASELINE = "#777A91"


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
    58,
    65,
    "2022年1-8月公司计划完成率",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)

# 副标题
ax.text(
    58,
    123,
    "公司整体完成率55%，4月和8月超过70%，2月和6月较低未过半",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=19,
    fontproperties=font_normal
)


# 坐标
x_positions = np.linspace(117, 773, 8)

baseline_y = 506

min_height = 208
max_height = 297

heights = [
    min_height + (rate - 49) / (71 - 49) * (max_height - min_height)
    for rate in rates
]

top_positions = [
    baseline_y - height
    for height in heights
]


# 基准线
ax.plot(
    [69, 819],
    [baseline_y, baseline_y],
    color=BASELINE,
    linewidth=0.8
)


# 竖线、菱形、数据标签
for x, rate, top_y, month in zip(
    x_positions,
    rates,
    top_positions,
    months
):

    # 竖线
    ax.plot(
        [x, x],
        [baseline_y, top_y],
        color=PINK,
        linewidth=1.6,
        zorder=2
    )

    # 菱形
    ax.scatter(
        x,
        top_y,
        marker="D",
        s=62,
        facecolors=BG,
        edgecolors=PINK,
        linewidths=1.5,
        zorder=3
    )

    # 完成率
    ax.text(
        x,
        top_y - 27,
        f"{rate:.2f}%",
        ha="center",
        va="center",
        color=WHITE,
        fontsize=15,
        fontproperties=font_normal
    )

    # 月份
    ax.text(
        x,
        533,
        month,
        ha="center",
        va="center",
        color=WHITE,
        fontsize=16,
        fontproperties=font_normal
    )


# 底部备注
ax.text(
    60,
    580,
    "注：数据来源于公司销售系统，统计日期截至2022.08.31",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 保存
output_file = "p12.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：", output_file)