import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from pathlib import Path
import numpy as np

# ==================== 数据 ====================
departments = ["销售部", "采购部", "工程部", "财务部", "行政部", "人力部"]
values = [29.20, 22.70, 17.50, 13.60, 10.30, 5.00]

# ==================== 颜色 ====================
colors = [
    "#E84D69",  # 销售部
    "#F6C44F",  # 采购部
    "#14A6AD",  # 工程部
    "#39A3D5",  # 财务部
    "#087CC3",  # 行政部
    "#7836A0",  # 人力部
]

background = "#1A1F48"

# ==================== 画布 ====================
fig, ax = plt.subplots(figsize=(8.40, 6.24), dpi=120)
fig.patch.set_facecolor(background)
ax.set_facecolor(background)

# ==================== 标题 ====================
ax.text(
    -2.42, 2.02,
    "2021年各部门人数分布",
    fontsize=23,
    fontweight="bold",
    color="white",
    ha="left",
    va="top",
    fontname="Microsoft YaHei"
)

# 副标题
ax.text(
    -2.42, 1.67,
    "公司总人数1664，销售部人数最多451，占比29.2%",
    fontsize=15,
    color="white",
    ha="left",
    va="top",
    fontname="Microsoft YaHei"
)

# ==================== 南丁格尔玫瑰图 ====================
cx, cy = 0.05, -0.12
max_radius = 1.58
max_value = max(values)

total = sum(values)
start_angle = 90
current_angle = start_angle

for value, color in zip(values, colors):
    angle = value / total * 360

    theta1 = current_angle - angle
    theta2 = current_angle

    # 半径按照占比变化
    radius = max_radius * value / max_value

    wedge = Wedge(
        (cx, cy),
        radius,
        theta1,
        theta2,
        facecolor=color,
        edgecolor="none"
    )

    ax.add_patch(wedge)
    current_angle = theta1

# ==================== 引导线 ====================
# 起点、折点、终点均按照参考图位置设置
line_data = [
    # 销售部
    (colors[0], (1.45, 0.90), (1.76, 1.38), (2.48, 1.38)),
    # 采购部
    (colors[1], (1.05, -1.05), (1.30, -1.48), (2.05, -1.48)),
    # 工程部
    (colors[2], (-0.98, -1.10), (-1.48, -1.55), (-2.35, -1.55)),
    # 财务部
    (colors[3], (-1.12, -0.03), (-1.55, -0.60), (-2.48, -0.60)),
    # 行政部
    (colors[4], (-0.63, 0.92), (-1.08, 1.42), (-2.08, 1.42)),
    # 人力部
    (colors[5], (-0.10, 1.15), (-0.54, 1.69), (-1.34, 1.69)),
]

for color, p1, p2, p3 in line_data:
    ax.plot(
        [p1[0], p2[0], p3[0]],
        [p1[1], p2[1], p3[1]],
        color=color,
        linewidth=0.75,
        solid_capstyle="round"
    )

    # 引导线起点圆点
    ax.scatter(
        p1[0],
        p1[1],
        s=25,
        color=color,
        edgecolors="none",
        zorder=10
    )

# ==================== 底部注释 ====================
ax.text(
    -2.47, -1.99,
    "*注：数据来源于公司人力资源系统，统计日期截至2022.01.01",
    fontsize=10.5,
    color="white",
    alpha=0.92,
    ha="left",
    va="bottom",
    fontname="Microsoft YaHei"
)

# ==================== 坐标设置 ====================
ax.set_xlim(-2.72, 2.72)
ax.set_ylim(-2.18, 2.25)

ax.set_aspect("equal")
ax.axis("off")

plt.subplots_adjust(
    left=0,
    right=1,
    top=1,
    bottom=0
)

# ==================== 保存 ====================
output_path = Path(__file__).resolve().parent / "p21.png"

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

