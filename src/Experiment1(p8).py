import matplotlib.pyplot as plt
from matplotlib import font_manager
import os


# 数据
regions = ["华东", "西南", "西北", "东北", "华南", "华北"]
sales = [2109, 1369, 1872, 1536, 1946, 4321]
placeholder1 = [2212, 2952, 2449, 2785, 2375, 0]
placeholder2 = [1080, 1080, 1080, 1080, 1080, 1080]
yoy = ["-5.8%", "-17.9%", "-15.9%", "-9.3%", "-20.8%", "-13.6%"]


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
HEIGHT = 613
DPI = 100

BG = "#1A1E43"
DARK_BLUE = "#09387E"
LIGHT_BLUE = "#82ADD7"
RED = "#9B3D4F"
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
    55,
    68,
    "2021年各区域销量及同比情况",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=30,
    fontproperties=font_bold
)


# 副标题
ax.text(
    55,
    124,
    "各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=19,
    fontproperties=font_normal
)


# 图表参数
bar_left = 110
bar_right = 748
bar_width = bar_right - bar_left

bar_height = 48
row_gap = 14

first_y = 180


# 总长度对应：
# 最大销量4321 + 占位2 1080
max_sales = 4321
fixed_part = 1080
total_value = max_sales + fixed_part


# 绘制横向堆叠条
for i in range(len(regions)):

    y = first_y + i * (bar_height + row_gap)

    sales_width = (
        sales[i] / total_value
    ) * bar_width

    placeholder_width = (
        placeholder1[i] / total_value
    ) * bar_width

    red_width = (
        placeholder2[i] / total_value
    ) * bar_width


    # 区域名称
    ax.text(
        56,
        y + bar_height / 2,
        regions[i],
        ha="left",
        va="center",
        color=WHITE,
        fontsize=16,
        fontproperties=font_normal
    )


    # 深蓝：销量
    ax.add_patch(
        plt.Rectangle(
            (
                bar_left,
                y
            ),
            sales_width,
            bar_height,
            facecolor=DARK_BLUE,
            edgecolor="none"
        )
    )


    # 浅蓝：占位1
    ax.add_patch(
        plt.Rectangle(
            (
                bar_left + sales_width,
                y
            ),
            placeholder_width,
            bar_height,
            facecolor=LIGHT_BLUE,
            edgecolor="none"
        )
    )


    # 红色：占位2
    ax.add_patch(
        plt.Rectangle(
            (
                bar_left + sales_width + placeholder_width,
                y
            ),
            red_width,
            bar_height,
            facecolor=RED,
            edgecolor="none"
        )
    )


    # 销量数字
    if sales[i] > 0:
        ax.text(
            bar_left + sales_width - 12,
            y + bar_height / 2,
            str(sales[i]),
            ha="right",
            va="center",
            color=WHITE,
            fontsize=17,
            fontproperties=font_normal
        )


    # 同比去年
    ax.text(
        bar_left + sales_width + placeholder_width + red_width / 2,
        y + bar_height / 2,
        yoy[i],
        ha="center",
        va="center",
        color=WHITE,
        fontsize=15,
        fontproperties=font_normal
    )


# 底部备注
ax.text(
    47,
    579,
    "*注：数据来源于公司销售系统，统计日期截至2022.01.01",
    ha="left",
    va="center",
    color=WHITE,
    fontsize=14,
    fontproperties=font_normal
)


# 保存到当前代码所在文件夹
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "p8.png"
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