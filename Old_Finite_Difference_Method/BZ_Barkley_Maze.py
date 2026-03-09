import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools

# --- 1. 参数设置 (Barkley Model - 微调版) ---
# 保持你喜欢的“宽波”效果，视觉冲击力强
a = 0.75
b = 0.01   
epsilon = 0.02 
D = 1.0     
dx = 1.0 
dt = 0.05   

# 网格大小
size = 120

# 动画速度
steps_per_frame = 2

# --- 2. 迷宫设计 (手动绘制一个复杂迷宫) ---
maze = np.zeros((size, size))

# > 2.1 绘制四周边界
maze[0:5, :] = 1       # 上墙
maze[-5:, :] = 1       # 下墙
maze[:, 0:5] = 1       # 左墙
maze[:, -5:] = 1       # 右墙

# > 2.2 绘制内部障碍物 (构建迷宫路径)
# 障碍物 1: 长横墙 (迫使波向下走)
maze[30:35, 20:100] = 1

# 障碍物 2: U型陷阱 (制造死胡同)
maze[60:85, 40:45] = 1   # 竖
maze[60:85, 80:85] = 1   # 竖
maze[80:85, 40:85] = 1   # 横底
# (波进这里会死掉)

# 障碍物 3: 分隔墙
maze[30:80, 20:25] = 1

# 障碍物 4: 右侧阻挡
maze[50:100, 100:105] = 1

# 生成墙壁的布尔掩码
walls = (maze == 1)

# --- 3. 视觉优化：高亮白色墙壁 ---
wall_overlay = np.zeros((size, size, 4))
# 纯白色墙壁，不透明
wall_overlay[walls] = [1.0, 1.0, 1.0, 1.0] 

# --- 4. 初始化化学场 ---
U = np.zeros((size, size))
V = np.zeros((size, size))

# 【关键修改】设置入口 (Entrance)
# 我们把火点在左上角 (坐标约 15, 15)
# 波将从这里开始寻找出路
U[10:20, 10:20] = 1.0
V[10:20, 10:20] = 0.0

# --- 5. 核心计算 (不变) ---
def laplacian(Z):
    return (
        np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
        np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) -
        4 * Z
    ) / (dx ** 2)

def update(frame):
    global U, V
    
    for _ in range(steps_per_frame):
        Lu = laplacian(U)
        threshold = (V + b) / a
        reaction = (1 / epsilon) * U * (1 - U) * (U - threshold)
        
        delta_U = (D * Lu + reaction) * dt
        delta_V = (U - V) * dt
        
        U += delta_U
        V += delta_V
        
        # 强制墙壁处无化学物质 (吸收边界)
        U[walls] = 0
        V[walls] = 0

    im_wave.set_array(U)
    # 标题显示时间步
    ax.set_title(f"Chemical Maze Solver\nTime Step: {frame * steps_per_frame}", 
                 fontsize=12, color='white')
    return [im_wave, im_walls]

# --- 6. 绘图与显示 ---
fig, ax = plt.subplots(figsize=(6, 6), facecolor='#2b2b2b') 

# Layer 1: 化学波 (底层)
im_wave = ax.imshow(U, cmap='magma', vmin=0, vmax=0.9, interpolation='bicubic', zorder=1)

# Layer 2: 墙壁 (顶层)
im_walls = ax.imshow(wall_overlay, interpolation='nearest', zorder=2)

# 标记起点 (Start) 和 终点 (End)
ax.text(15, 25, "START", color="cyan", fontsize=10, fontweight='bold', ha='center')
ax.text(100, 110, "EXIT", color="lime", fontsize=10, fontweight='bold', ha='center')

ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=itertools.count(), interval=30, blit=True)

plt.show()

# ------------------------------------------------------------
# 文件说明（中文）：
# - 功能：在复杂迷宫布局上运行 Barkley 模型，展示化学/激发波如何在迷宫中传播以寻路或被困。
# - 描述的情形：通过手工绘制的迷宫（边界、障碍、死胡同等），从起点触发波，观察波在迷宫路径中传播、绕行或被墙体阻断的行为，配合起点/终点标注以便观察“求路”过程。
# - 模拟方法：与 Barkley 模型一致，使用离散拉普拉斯算子模拟扩散，非线性反应项为 `U*(1-U)*(U-threshold)` 的放缩形式，时间积分为显式步进。
#   在每步更新后，将墙体处的 `U`/`V` 强制为 0（吸收边界），并把墙体用 `wall_overlay` 覆盖为白色以便视觉辨识。
# - 可调项与应用：通过调整参数 `a, b, epsilon, D, dt` 和迷宫几何形状，可以让波呈现不同宽度/速度的传播；此类模型常用于研究化学波、神经媒体或用于“液体/化学求路”可视化实验。
# ------------------------------------------------------------