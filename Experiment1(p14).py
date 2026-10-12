import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Wedge
import os
import numpy as np


# 数据
completion = 85
remaining = 15


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
HEIGHT = 643
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"
UNFINISHED = "#30365D"

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
    52,
    67,
    "2022年上半年目标完成率",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)

ax.text(
    52,
    122,
    "截至6月30日销售目标总体完成率达到85%",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=20,
    fontproperties=font_normal
)


# 圆环参数
center_x = 441
center_y = 360

outer_radius = 181
inner_radius = 160


# 圆环起始位置
# 使用图像坐标：0°在右侧，角度顺时针增加
start_angle = 210

colored_angle = 360 * completion / 100
end_angle = start_angle + colored_angle


# 未完成部分
ax.add_patch(
    Wedge(
        (center_x, center_y),
        outer_radius,
        start_angle,
        start_angle + 360,
        width=outer_radius - inner_radius,
        facecolor=UNFINISHED,
        edgecolor="none"
    )
)


# 渐变颜色
start_color = np.array([
    134, 52, 180
]) / 255.0

middle_color = np.array([
    194, 58, 155
]) / 255.0

end_color = np.array([
    239, 74, 113
]) / 255.0


# 绘制85%的渐变圆环
segments = 500

angles = np.linspace(
    start_angle,
    end_angle,
    segments + 1
)

for i in range(segments):

    angle1 = angles[i]
    angle2 = angles[i + 1]

    t = i / (segments - 1)

    if t <= 0.55:
        local_t = t / 0.55

        color = (
            start_color * (1 - local_t)
            + middle_color * local_t
        )
    else:
        local_t = (t - 0.55) / 0.45

        color = (
            middle_color * (1 - local_t)
            + end_color * local_t
        )

    ax.add_patch(
        Wedge(
            (center_x, center_y),
            outer_radius,
            angle1,
            angle2,
            width=outer_radius - inner_radius,
            facecolor=color,
            edgecolor=color,
            linewidth=0
        )
    )


# 中央完成率
ax.text(
    center_x,
    342,
    "85%",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=64,
    fontproperties=font_normal
)


# 中央说明
ax.text(
    center_x,
    427,
    "目标完成率",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=22,
    fontproperties=font_normal
)


# 底部备注
ax.text(
    47,
    608,
    "注：数据来源于公司销售系统",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 保存
output_file = "p14.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：", output_file)