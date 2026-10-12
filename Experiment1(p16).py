import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path
import numpy as np
import os


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
WIDTH = 834
HEIGHT = 622
DPI = 100

BG = "#191D43"
BLUE = "#087BC5"
DARK_BLUE = "#102B55"
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
    72,
    "本科及以上学历占比",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)


# 副标题
ax.text(
    53,
    129,
    "6月30日最新统计数据本科及以上员工占比65%",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=20,
    fontproperties=font_normal
)


# 圆形参数
center_x = 431
center_y = 356

# 外部边缘线
outer_radius = 190

# 内部水面区域
water_radius = 174


# ==========================================================
# 波浪线
# ==========================================================

x = np.linspace(
    center_x - water_radius,
    center_x + water_radius,
    600
)

wave_center = center_y - 27

wave = (
    13 * np.sin(
        (x - center_x) / water_radius * np.pi * 1.25
        + 0.25
    )
    +
    5 * np.sin(
        (x - center_x) / water_radius * np.pi * 2.3
        + 1.0
    )
)

wave_y = wave_center + wave


# ==========================================================
# 水面区域路径
# ==========================================================

vertices = []

for xi, yi in zip(x, wave_y):
    vertices.append((xi, yi))

vertices.append(
    (center_x + water_radius, center_y + water_radius)
)

vertices.append(
    (center_x - water_radius, center_y + water_radius)
)

vertices.append(
    (x[0], wave_y[0])
)

codes = (
    [Path.MOVETO]
    + [Path.LINETO] * (len(x) - 1)
    + [Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
)

water_path = Path(vertices, codes)


# ==========================================================
# 水面裁剪区域
# ==========================================================

water_clip = Circle(
    (center_x, center_y),
    water_radius,
    transform=ax.transData
)


# ==========================================================
# 深色边缘
# ==========================================================

dark_water = PathPatch(
    water_path,
    facecolor=DARK_BLUE,
    edgecolor="none",
    clip_path=water_clip,
    zorder=2
)

ax.add_patch(dark_water)


# ==========================================================
# 蓝色主体
# ==========================================================

blue_vertices = []

for xi, yi in zip(x, wave_y - 2):
    blue_vertices.append((xi, yi))

blue_vertices.append(
    (center_x + water_radius, center_y + water_radius)
)

blue_vertices.append(
    (center_x - water_radius, center_y + water_radius)
)

blue_vertices.append(
    (x[0], wave_y[0] - 2)
)

blue_path = Path(
    blue_vertices,
    codes
)

blue_water = PathPatch(
    blue_path,
    facecolor=BLUE,
    edgecolor="none",
    clip_path=water_clip,
    zorder=3
)

ax.add_patch(blue_water)


# ==========================================================
# 外部圆形边缘线
# ==========================================================

ax.add_patch(
    Circle(
        (center_x, center_y),
        outer_radius,
        fill=False,
        edgecolor=BLUE,
        linewidth=2.8,
        zorder=5
    )
)


# ==========================================================
# 中间百分比
# ==========================================================

ax.text(
    center_x,
    center_y - 5,
    f"{completion}%",
    ha="center",
    va="center",
    color=WHITE,
    fontsize=68,
    fontproperties=font_normal,
    zorder=6
)


# ==========================================================
# 底部备注
# ==========================================================

ax.text(
    52,
    589,
    "*注：数据来源于公司人力资源系统",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=14,
    fontproperties=font_normal
)


# 保存
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p16.png"
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