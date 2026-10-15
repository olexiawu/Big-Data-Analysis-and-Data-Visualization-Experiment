import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle
import os
import math
from scipy.optimize import brentq


# 数据
completion = 65


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
WIDTH = 830
HEIGHT = 618
DPI = 100

BG = "#191D43"
WHITE = "#FFFFFF"
BLUE = "#087BC5"


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
    67,
    "2022年上半年目标完成率",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)

ax.text(
    58,
    121,
    "截至6月30日销售目标总体完成率达到65%",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=20,
    fontproperties=font_normal
)


# 圆形参数
center_x = 391
center_y = 352

outer_radius = 178
inner_radius = 163


# ==========================================================
# 计算从圆底部向上填充65%面积时的水平分界线
# ==========================================================

r = inner_radius

target_ratio = completion / 100


def bottom_area_ratio(y):
    """
    y：相对于圆心的纵坐标
    正数 = 圆心以下
    负数 = 圆心以上

    计算水平线 y 以下的圆形面积占比。
    """

    # 圆形下方弓形面积
    area = (
        r ** 2 * math.acos(y / r)
        - y * math.sqrt(r ** 2 - y ** 2)
    )

    return area / (math.pi * r ** 2)


# 求蓝色面积为65%时的分界线
relative_y = brentq(
    lambda y: bottom_area_ratio(y) - target_ratio,
    -r,
    r
)


# 转换为图像坐标
fill_y = center_y + relative_y


# ==========================================================
# 蓝色区域
# ==========================================================

inner_circle = Circle(
    (center_x, center_y),
    inner_radius,
    transform=ax.transData
)

blue_fill = Rectangle(
    (
        center_x - inner_radius,
        fill_y
    ),
    2 * inner_radius,
    center_y + inner_radius - fill_y,
    facecolor=BLUE,
    edgecolor="none",
    clip_path=inner_circle,
    zorder=2
)

ax.add_patch(blue_fill)


# ==========================================================
# 外圆
# ==========================================================

ax.add_patch(
    Circle(
        (center_x, center_y),
        outer_radius,
        fill=False,
        edgecolor=BLUE,
        linewidth=3.2,
        zorder=5
    )
)


# ==========================================================
# 内圆
# ==========================================================

ax.add_patch(
    Circle(
        (center_x, center_y),
        inner_radius,
        fill=False,
        edgecolor=BLUE,
        linewidth=3.2,
        zorder=6
    )
)


# ==========================================================
# 中间百分比
# ==========================================================

ax.text(
    center_x,
    center_y - 5,
    "65%",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=68,
    fontproperties=font_normal,
    zorder=7
)


# ==========================================================
# 底部备注
# ==========================================================

ax.text(
    48,
    587,
    "*注：数据来源于公司销售系统",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=15,
    fontproperties=font_normal
)


# 保存
output_file = "p15.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=BG,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：", output_file)
print(f"蓝色区域实际面积占比：{bottom_area_ratio(relative_y) * 100:.2f}%")
print(f"水平分界线相对于圆心的位置：{relative_y:.2f}px")