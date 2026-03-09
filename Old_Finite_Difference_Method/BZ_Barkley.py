import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools

# --- 1. 参数设置 (Barkley Model) ---
a = 0.75
b = 0.01   
epsilon = 0.02 
D = 1.0     
dx = 1.0 
dt = 0.05   

# 网格大小
size = 120

# 动画速度 (数值越大，每帧演化越快)
steps_per_frame = 2

# --- 2. 迷宫设计 ---
maze = np.zeros((size, size))

# 设计障碍物：一道横墙
maze[60:65, :] = 1 

# 在墙上开两个“门”
maze[60:65, 30:35] = 0   
maze[60:65, 85:90] = 0   

# 生成墙壁的布尔掩码
walls = (maze == 1)

# --- 3. 视觉优化：高亮白色墙壁 ---
# RGBA 矩阵
wall_overlay = np.zeros((size, size, 4))

# 【关键修改】把墙壁改成纯白色 [1.0, 1.0, 1.0]
# Alpha = 1.0 (不透明)
wall_overlay[walls] = [1.0, 1.0, 1.0, 1.0] 

# --- 4. 初始化化学场 ---
U = np.zeros((size, size))
V = np.zeros((size, size))

# 在下方中心点火
U[20:30, 55:65] = 1.0
V[20:30, 55:65] = 0.0

# --- 5. 核心计算 ---
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
        
        # 强制墙壁处无化学物质
        U[walls] = 0
        V[walls] = 0

    im_wave.set_array(U)
    # 标题也设为白色
    ax.set_title(f"Liquid Computing Simulation\nTime Step: {frame * steps_per_frame}", 
                 fontsize=12, color='white')
    return [im_wave, im_walls]

# --- 6. 绘图与显示 ---
# 深色背景 (Dark Gray)
fig, ax = plt.subplots(figsize=(6, 6), facecolor='#2b2b2b') 

# Layer 1: 化学波 (底层)
# vmin/vmax 控制亮度
im_wave = ax.imshow(U, cmap='magma', vmin=0, vmax=0.9, interpolation='bicubic', zorder=1)

# Layer 2: 墙壁 (顶层) - 现在是醒目的白色
im_walls = ax.imshow(wall_overlay, interpolation='nearest', zorder=2)

ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=itertools.count(), interval=30, blit=True)

plt.show()

# ------------------------------------------------------------
# 文件说明（中文）：
# - 功能：使用 Barkley 可激发模型在包含一条横墙（带两个门）的网格上模拟化学/激发波的传播，并可视化 U 场。
# - 描述的情形：在网格中设置一道障碍（墙），通过墙上的门让波传播，通过初始点火区域触发波动，观察波遇墙、绕行或被吸收的行为。
# - 模拟方法：使用离散拉普拉斯算子模拟扩散项，Barkley 模型的反应项为具有阈值和非线性项的三次多项式形式：
#   reaction = (1/epsilon) * U * (1-U) * (U - threshold)，其中 threshold = (V + b)/a。时间推进采用显式步长积累。
# - 墙体处理：在墙体位置强制将 `U` 和 `V` 设为 0（吸收边界），并用 `wall_overlay` 高亮显示墙面。
# - 可调项：参数 `a, b, epsilon, D, dx, dt` 及迷宫/墙体的形状影响波的宽度、速度和传播行为。
# ------------------------------------------------------------