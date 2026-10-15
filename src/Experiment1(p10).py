import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager
from datetime import datetime
import os


# ============================================================
# 1. 数据
# ============================================================

data = [
    {"name": "制定计划", "start": "2022/3/1",  "days": 11, "progress": 51},
    {"name": "方案设计", "start": "2022/3/13", "days": 8,  "progress": 32},
    {"name": "资源调配", "start": "2022/3/22", "days": 10, "progress": 21},
    {"name": "第一阶段", "start": "2022/4/2",  "days": 13, "progress": 85},
    {"name": "第二阶段", "start": "2022/4/16", "days": 24, "progress": 36},
    {"name": "第三阶段", "start": "2022/5/11", "days": 14, "progress": 68},
    {"name": "项目总结", "start": "2022/5/26", "days": 7,  "progress": 68},
]


# ============================================================
# 2. 自动寻找中文字体
# ============================================================

def find_chinese_font(bold=False):

    if os.name == "nt":

        if bold:
            windows_fonts = [
                r"C:\Windows\Fonts\msyhbd.ttc",
                r"C:\Windows\Fonts\msyhbd.ttf",
                r"C:\Windows\Fonts\simhei.ttf",
            ]
        else:
            windows_fonts = [
                r"C:\Windows\Fonts\msyh.ttc",
                r"C:\Windows\Fonts\msyh.ttf",
                r"C:\Windows\Fonts\simhei.ttf",
            ]

        for path in windows_fonts:
            if os.path.exists(path):
                return font_manager.FontProperties(fname=path)

    candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans CN",
        "WenQuanYi Zen Hei",
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


# ============================================================
# 3. 创建画布
# ============================================================

WIDTH = 923
HEIGHT = 613
DPI = 100

fig = plt.figure(
    figsize=(WIDTH / DPI, HEIGHT / DPI),
    dpi=DPI,
    facecolor="#1A1E43"
)

ax = fig.add_axes([0, 0, 1, 1])

ax.set_facecolor("#1A1E43")

ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0)

ax.axis("off")


# ============================================================
# 4. 颜色
# ============================================================

background_color = "#1A1E43"

progress_color = "#00A3E6"

remaining_color = "#0070C0"

white = "#FFFFFF"

grid_color = "#717389"


# ============================================================
# 5. 标题
# ============================================================

ax.text(
    461.5,
    40,
    "2022年化妆品类目采购项目进度",
    ha="center",
    va="center",
    color=white,
    fontsize=32,
    fontproperties=font_bold
)


# ============================================================
# 6. 日期刻度
# ============================================================

tick_dates = [
    "2022/3/1",
    "2022/3/16",
    "2022/3/31",
    "2022/4/15",
    "2022/4/30",
    "2022/5/15",
    "2022/5/30",
    "2022/6/14",
]

tick_x = [
    153,
    251,
    349,
    447,
    545,
    643,
    741,
    839,
]

for x, text in zip(tick_x, tick_dates):

    ax.text(
        x,
        113,
        text,
        ha="center",
        va="center",
        color=white,
        fontsize=13,       # 日期字体缩小
        fontproperties=font_normal
    )


# ============================================================
# 7. 绘制纵向虚线
# ============================================================

for x in tick_x:

    ax.plot(
        [x, x],
        [137, 578],
        color=grid_color,
        linewidth=0.8,
        linestyle=(0, (6, 4)),
        solid_capstyle="butt",
        zorder=1
    )


# ============================================================
# 8. 日期 -> X 坐标
# ============================================================

base_date = datetime.strptime(
    "2022/3/1",
    "%Y/%m/%d"
)

PIXELS_PER_DAY = 98 / 15


def date_to_x(date_string):

    current_date = datetime.strptime(
        date_string,
        "%Y/%m/%d"
    )

    days = (current_date - base_date).days

    return 153 + days * PIXELS_PER_DAY


# ============================================================
# 9. 绘制项目名称和进度条
# ============================================================

bar_top_positions = [
    153,
    216,
    279,
    342,
    404,
    467,
    530,
]

BAR_HEIGHT = 32


for item, y in zip(data, bar_top_positions):

    # 项目名称
    ax.text(
        136,
        y + BAR_HEIGHT / 2,
        item["name"],
        ha="right",
        va="center",
        color=white,
        fontsize=18,
        fontproperties=font_normal
    )

    # 开始位置
    start_x = date_to_x(item["start"])

    # 总长度
    total_width = item["days"] * PIXELS_PER_DAY

    # 已完成长度
    progress_width = (
        total_width * item["progress"] / 100
    )

    # 未完成长度
    remaining_width = (
        total_width - progress_width
    )

    # 已完成部分
    ax.add_patch(
        Rectangle(
            (start_x, y),
            progress_width,
            BAR_HEIGHT,
            facecolor=progress_color,
            edgecolor="none",
            zorder=3
        )
    )

    # 未完成部分
    ax.add_patch(
        Rectangle(
            (
                start_x + progress_width,
                y
            ),
            remaining_width,
            BAR_HEIGHT,
            facecolor=remaining_color,
            edgecolor="none",
            zorder=3
        )
    )

    # 百分比
    ax.text(
        start_x + total_width / 2,
        y + BAR_HEIGHT / 2,
        f"{item['progress']}%",
        ha="center",
        va="center",
        color=white,
        fontsize=16,
        fontproperties=font_normal,
        zorder=4
    )


# ============================================================
# 10. 保存图片
# ============================================================

output_file = "p10.png"

plt.savefig(
    output_file,
    dpi=DPI,
    facecolor=background_color,
    edgecolor="none",
    pad_inches=0
)

plt.show()

print(f"图片已生成：{output_file}")