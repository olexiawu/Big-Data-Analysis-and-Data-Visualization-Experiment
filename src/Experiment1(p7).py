import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os


# 数据
regions = ["华东", "西北", "东北", "华北", "华南"]

data_2022 = [36, 31, 18, 13, 9]
data_2021 = [42, 26, 19, 12, 5]


# 画布
WIDTH = 930
HEIGHT = 177
DPI = 100

fig = plt.figure(
    figsize=(WIDTH / DPI, HEIGHT / DPI),
    dpi=DPI,
    facecolor="white"
)

ax = fig.add_axes([0, 0, 1, 1])

ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)

ax.set_facecolor("white")
ax.axis("off")


# 网格
grid_color = "#DDDDDD"

vertical_grid = [0, 79, 183, 287, 391, 495, 599, 703, 807, 911]
horizontal_grid = [0, 21, 45, 69, 94, 118, 143, 168]

for x in vertical_grid:
    ax.plot(
        [x, x],
        [0, HEIGHT],
        color=grid_color,
        linewidth=0.8,
        zorder=0
    )

for y in horizontal_grid:
    ax.plot(
        [0, WIDTH],
        [y, y],
        color=grid_color,
        linewidth=0.8,
        zorder=0
    )


# 深绿色细竖线
def draw_striped_bar(x_start, x_end, y, height):

    stripe_color = "#006400"
    stripe_width = 1.0
    stripe_gap = 4.0

    x = x_start

    while x <= x_end:

        ax.add_patch(
            Rectangle(
                (x, y),
                stripe_width,
                height,
                facecolor=stripe_color,
                edgecolor="none",
                zorder=2
            )
        )

        x += stripe_width + stripe_gap


# 条形参数
bar_height = 20

left_end = 387
right_start = 500

scale = 10


# 行位置
row_y = [
    24,
    52,
    80,
    108,
    136
]


# 2022年
for value, y in zip(data_2022, row_y):

    bar_width = value * scale

    x_start = left_end - bar_width

    draw_striped_bar(
        x_start,
        left_end,
        y,
        bar_height
    )


# 2021年
for value, y in zip(data_2021, row_y):

    bar_width = value * scale

    x_end = right_start + bar_width

    draw_striped_bar(
        right_start,
        x_end,
        y,
        bar_height
    )


# 保存
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p7.png"
)

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor="white",
    edgecolor="none",
    pad_inches=0
)

plt.show()

print("图片已生成：")
print(output_file)