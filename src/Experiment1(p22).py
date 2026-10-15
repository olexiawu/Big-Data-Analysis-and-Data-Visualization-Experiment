import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from pathlib import Path
import numpy as np

# ==================== 数据 ====================
min_value = 50
max_value = 150
pointer_value = 76

# ==================== 画布 ====================
fig, ax = plt.subplots(figsize=(8.67, 6.48), dpi=120)

background = "#191E48"
fig.patch.set_facecolor(background)
ax.set_facecolor(background)

# ==================== 标题 ====================
ax.text(
    0, 1.96,
    "2022年6月29公司整体运营指数良好",
    fontsize=23,
    fontweight="bold",
    color="white",
    ha="center",
    va="center",
    fontname="Microsoft YaHei"
)

# ==================== 仪表盘参数 ====================
cx, cy = 0, -0.10

# 270°刻度范围
start_angle = 225
end_angle = -45

# 外环
outer_radius = 1.58

# 内外环均按之前宽度的2/3处理
# 彩色内环宽度 = 0.22 × 2/3
color_width = 0.22 * 2 / 3

# 彩色内环外半径
color_outer = 1.40

# 彩色内环内半径
color_inner = color_outer - color_width

# 外环必须与内环完全贴合
# 外环内边缘 = 彩色内环外边缘 = 1.40
outer_width = outer_radius - color_outer

# ==================== 完整360°外环 ====================
ax.add_patch(
    Wedge(
        (cx, cy),
        outer_radius,
        0,
        360,
        width=outer_width,
        facecolor="#087CC4",
        edgecolor="none"
    )
)

# ==================== 数值转角度 ====================
def value_to_angle(value):
    return start_angle - (
        (value - min_value) / (max_value - min_value) * 270
    )


# ==================== 彩色内环 ====================

# 50～80：青绿色
ax.add_patch(
    Wedge(
        (cx, cy),
        color_outer,
        value_to_angle(80),
        value_to_angle(50),
        width=color_width,
        facecolor="#1599A2",
        edgecolor="none"
    )
)

# 80～120：黄色
ax.add_patch(
    Wedge(
        (cx, cy),
        color_outer,
        value_to_angle(120),
        value_to_angle(80),
        width=color_width,
        facecolor="#FFC34F",
        edgecolor="none"
    )
)

# 120～150：红色
ax.add_patch(
    Wedge(
        (cx, cy),
        color_outer,
        value_to_angle(150),
        value_to_angle(120),
        width=color_width,
        facecolor="#F34D69",
        edgecolor="none"
    )
)

# ==================== 刻度 ====================
tick_outer = color_outer
tick_inner = color_inner

for value in range(50, 151, 10):
    angle = np.deg2rad(value_to_angle(value))

    # 刻度线
    x1 = cx + tick_inner * np.cos(angle)
    y1 = cy + tick_inner * np.sin(angle)

    x2 = cx + tick_outer * np.cos(angle)
    y2 = cy + tick_outer * np.sin(angle)

    ax.plot(
        [x1, x2],
        [y1, y2],
        color="#182046",
        linewidth=0.9,
        zorder=8
    )

    # 刻度数字
    label_radius = 1.08

    tx = cx + label_radius * np.cos(angle)
    ty = cy + label_radius * np.sin(angle)

    ax.text(
        tx,
        ty,
        str(value),
        color="white",
        fontsize=11,
        ha="center",
        va="center",
        fontname="Microsoft YaHei",
        zorder=10
    )

# ==================== 指针 ====================
pointer_angle = np.deg2rad(value_to_angle(pointer_value))

pointer_length = 1.02

px = cx + pointer_length * np.cos(pointer_angle)
py = cy + pointer_length * np.sin(pointer_angle)

ax.plot(
    [cx, px],
    [cy, py],
    color="white",
    linewidth=2.0,
    solid_capstyle="round",
    zorder=15
)

# ==================== 中间数值 ====================
ax.text(
    cx,
    cy - 0.58,
    str(pointer_value),
    color="white",
    fontsize=31,
    ha="center",
    va="center",
    fontname="Microsoft YaHei",
    zorder=20
)

# ==================== 坐标设置 ====================
ax.set_xlim(-2.25, 2.25)
ax.set_ylim(-1.95, 2.30)
ax.set_aspect("equal")
ax.axis("off")

plt.subplots_adjust(
    left=0,
    right=1,
    top=1,
    bottom=0
)

# ==================== 保存 ====================
output_path = (
    Path(__file__).resolve().parent
    / "p22.png"
)

plt.savefig(
    output_path,
    dpi=150,
    facecolor=background,
    edgecolor="none",
    bbox_inches=None,
    pad_inches=0
)

# ==================== 显示 ====================
plt.show()
