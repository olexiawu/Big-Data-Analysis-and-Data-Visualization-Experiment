import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

# ===== 解决中文显示为方框的警告 =====
# 直接加载系统中文字体文件，而不是靠字体名查找（最可靠）
_font_candidates = [
    r'C:\Windows\Fonts\msyh.ttc',    # 微软雅黑（Windows 自带）
    r'C:\Windows\Fonts\msyh.ttf',
    r'C:\Windows\Fonts\simhei.ttf',  # 黑体
    r'C:\Windows\Fonts\simsun.ttc',  # 宋体
]
_zh_font = None
for _fp in _font_candidates:
    if os.path.exists(_fp):
        fm.fontManager.addfont(_fp)          # 注册字体文件
        _zh_font = fm.FontProperties(fname=_fp).get_name()
        break

if _zh_font:
    plt.rcParams['font.sans-serif'] = [_zh_font]
else:
    # 兜底：让 matplotlib 自己从系统里找
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号

# ===== 数据 =====
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales   = [2354, 1902, 3524, 2698, 2896, 2563]

# ===== 配色（参照图一）=====
bg_color      = '#1a1a3e'   # 深蓝紫背景
bar_top_color = '#006fd6'   # 柱子顶部深蓝
bar_bot_color = '#00d4ff'   # 柱子底部亮青

# ===== 画布 =====
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=100)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 渐变 colormap：底部亮青 -> 顶部深蓝
cmap = LinearSegmentedColormap.from_list(
    'bar_grad', [bar_bot_color, bar_top_color]
)

x = np.arange(len(regions))
bar_width = 0.5  # 所有柱子统一宽度

# ===== 逐柱绘制渐变 =====
for xi, val in zip(x, sales):
    left, right = xi - bar_width / 2, xi + bar_width / 2
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(gradient,
              extent=[left, right, 0, val],
              aspect='auto', cmap=cmap,
              zorder=2, origin='lower')

# ===== 柱顶数值标签 =====
for xi, val in zip(x, sales):
    ax.text(xi, val + 90, str(val),
            ha='center', va='bottom',
            color='white', fontsize=13, fontweight='bold')

# ===== 坐标轴 =====
ax.set_xticks(x)
ax.set_xticklabels(regions, color='white', fontsize=14)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1000', '2000', '3000', '4000'],
                   color='white', fontsize=13)
ax.set_ylim(0, 4300)
ax.set_xlim(-0.7, len(regions) - 0.3)

# ===== 水平虚线网格 =====
ax.grid(axis='y', color='white', alpha=0.22,
        linestyle='--', linewidth=1, zorder=1)
ax.set_axisbelow(True)

# ===== 隐藏边框与刻度线 =====
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
ax.tick_params(axis='both', length=0)

# ===== 标题 / 副标题 =====
fig.text(0.06, 0.925, '3月各区域销量分布',
         color='white', fontsize=27, fontweight='bold')
fig.text(0.06, 0.865, '东北销量最多占总销量的22%，华南销量最低',
         color='white', fontsize=17)

# ===== 左下角注释 =====
fig.text(0.06, 0.035,
         '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='#aaaaaa', fontsize=12)

plt.tight_layout(rect=[0, 0.06, 1, 0.84])
plt.savefig('gradient_bar.png', dpi=100,
            facecolor=bg_color, bbox_inches='tight')
plt.show()
print('done')
