import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. 物理参数设置 (可微调以改变花纹) ---
# 模拟 U 和 V 两种物质：U 是“食物”，V 是“催化剂”
Du, Dv = 0.16, 0.08    # 扩散系数 (Diffusion rates)
f, k = 0.055, 0.062    # f: 进料率(Feed), k: 移除率(Kill)

# 网格设置
size = 200             # 网格分辨率
dt = 1.0               # 时间步长

# --- 2. 初始化化学场 ---
U = np.ones((size, size))      # U 初始充满全场
V = np.zeros((size, size))     # V 初始为 0

# 在中心放入一点 V (扰动，启动反应)
r = 10
mid = size // 2
V[mid-r:mid+r, mid-r:mid+r] = 0.25

# 加入一点随机噪声，模拟真实世界的非理想环境
U += np.random.rand(size, size) * 0.01
V += np.random.rand(size, size) * 0.01

# --- 3. 核心数学运算：拉普拉斯算子 (模拟扩散) ---
# 利用卷积原理计算物质如何向四周流动
def laplacian(Z):
    return (
        np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
        np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) -
        4 * Z
    )

# --- 4. 模拟循环更新 ---
def update(frame):
    global U, V
    # 为了动画流畅，每帧更新多次数据（数值越大，演化越快）
    for _ in range(20):
        Lu = laplacian(U)
        Lv = laplacian(V)
        
        # Gray-Scott 反应扩散方程 (Reaction-Diffusion Equation)
        # dU/dt = Du*Lap(U) - U*V^2 + f*(1-U)
        # dV/dt = Dv*Lap(V) + U*V^2 - (f+k)*V
        reaction = U * V * V
        U += (Du * Lu - reaction + f * (1 - U)) * dt
        V += (Dv * Lv + reaction - (f + k) * V) * dt

    im.set_array(V)
    return [im]

# --- 5. 可视化 ---
fig, ax = plt.subplots(figsize=(6, 6))
# 使用 'magma' 或 'inferno' 配色，模仿 B-Z 反应的红/蓝/黑效果
im = ax.imshow(V, cmap='magma', interpolation='bicubic')
ax.set_title("Chemical Computing Simulation\nReaction-Diffusion System (Gray-Scott Model)")
ax.axis('off')

# 生成动画
ani = animation.FuncAnimation(fig, update, frames=200, interval=12, blit=True)
plt.show()