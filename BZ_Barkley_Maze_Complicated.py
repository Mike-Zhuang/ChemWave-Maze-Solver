import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. 图像处理 ---
img_path = '3.jpg'  

try:
    img_origin = cv2.imread(img_path)
    if img_origin is None:
        raise FileNotFoundError("找不到 3.jpg")
    
    gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    
    sim_size = 200
    maze_resized = cv2.resize(binary, (sim_size, sim_size), interpolation=cv2.INTER_NEAREST)
    walls = (maze_resized < 50) 

except Exception as e:
    print(f"Error: {e}. 使用备用迷宫。")
    sim_size = 200
    walls = np.zeros((sim_size, sim_size), dtype=bool)
    walls[0:5, :] = True; walls[-5:, :] = True; walls[:, 0:5] = True; walls[:, -5:] = True
    walls[100, 50:150] = True

# --- 2. 墙壁图层 ---
wall_overlay = np.zeros((sim_size, sim_size, 4))
wall_overlay[walls] = [1.0, 1.0, 1.0, 1.0] 

# --- 3. 物理参数 (黄金均速版) ---
a = 0.75
b = 0.01
epsilon = 0.015
D = 1.0    # 保持较大的扩散系数，波形饱满
dx = 1.0 
dt = 0.04  
# 【关键修改】每帧计算 6 次 (原版2，极速版20)
# 这个速度既能展示细节，又不会让演示冷场
steps_per_frame = 6

# --- 4. 初始化 ---
U = np.zeros((sim_size, sim_size)) 
V = np.zeros((sim_size, sim_size)) 
arrival_times = np.full((sim_size, sim_size), np.inf) 

# 自动寻找起点
start_pos = None
for r in range(10, 50):
    for c in range(10, 50):
        if not walls[r, c]:
            start_pos = (r, c)
            U[r-5:r+5, c-5:c+5] = 1.0
            arrival_times[r-5:r+5, c-5:c+5] = 0 
            break
    if start_pos: break

path_overlay = np.zeros((sim_size, sim_size, 4))

# --- 5. 核心计算 ---
def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx**2)

def update(frame):
    global U, V, arrival_times
    
    for _ in range(steps_per_frame):
        Lu = laplacian(U)
        threshold = (V + b) / a
        reaction = (1 / epsilon) * U * (1 - U) * (U - threshold)
        
        delta_U = (D * Lu + reaction) * dt
        delta_V = (U - V) * dt
        
        U += delta_U; V += delta_V
        U[walls] = 0; V[walls] = 0
        
        mask_new = (U > 0.5) & (arrival_times == np.inf)
        arrival_times[mask_new] = frame * steps_per_frame

    im_wave.set_array(U)
    
    disp_map = arrival_times.copy()
    disp_map[disp_map == np.inf] = -100
    im_time.set_array(disp_map)
    
    title_text.set_text(f"Step: {frame*steps_per_frame}")
    
    return [im_wave, im_time, im_path, im_walls1, im_walls2, title_text]

# --- 6. 逆向寻路算法 ---
def find_shortest_path(end_r, end_c):
    if arrival_times[end_r, end_c] == np.inf:
        print("波还没传到这里，无法寻路！")
        return

    path_points = []
    curr_r, curr_c = end_r, end_c
    path_points.append((curr_r, curr_c))

    while arrival_times[curr_r, curr_c] > 0:
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < sim_size and 0 <= nc < sim_size:
                    neighbors.append((arrival_times[nr, nc], nr, nc))
        
        neighbors.sort(key=lambda x: x[0])
        best_val, best_r, best_c = neighbors[0]
        
        if best_val >= arrival_times[curr_r, curr_c]: break
        curr_r, curr_c = best_r, best_c
        path_points.append((curr_r, curr_c))
        if best_val == 0: break
            
    global path_overlay
    path_overlay.fill(0) 
    for r, c in path_points:
        # 洋红色高亮路径
        path_overlay[r-1:r+2, c-1:c+2] = [1.0, 0.0, 1.0, 1.0] 
    
    im_path.set_array(path_overlay)

def onclick(event):
    if event.inaxes == ax2 and event.xdata and event.ydata:
        find_shortest_path(int(event.ydata), int(event.xdata))

# --- 7. 绘图系统 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#2b2b2b')
fig.canvas.mpl_connect('button_press_event', onclick)

# 文字位置调整，防止遮挡
title_text = ax1.text(0.5, 1.15, "", transform=ax1.transAxes, ha='center', 
                      color='cyan', fontsize=12, fontweight='bold',
                      bbox=dict(facecolor='#2b2b2b', edgecolor='white', boxstyle='round,pad=0.3'))

# 左图
im_wave = ax1.imshow(U, cmap='magma', vmin=0, vmax=1.0, interpolation='bicubic', zorder=1)
im_walls1 = ax1.imshow(wall_overlay, interpolation='nearest', zorder=2) 
ax1.set_title("Live Wave (Real-time)", color='white', pad=10)
ax1.axis('off')

# 右图
cmap_time = plt.cm.jet_r
cmap_time.set_under('black')
im_time = ax2.imshow(arrival_times, cmap=cmap_time, vmin=0, vmax=3000, interpolation='nearest', zorder=1)
im_walls2 = ax2.imshow(wall_overlay, interpolation='nearest', zorder=2) 
im_path = ax2.imshow(path_overlay, interpolation='nearest', zorder=3)   

ax2.set_title("Time Map (Click to Find Path!)", color='white', pad=10)
ax2.axis('off')

ani = animation.FuncAnimation(fig, update, frames=2000, interval=20, blit=True)
plt.show()

# ------------------------------------------------------------
# 文件说明（中文）：
# - 功能：基于图像或备用迷宫运行 Barkley 可激发模型并可视化实时波形、到达时间图与反向寻路结果，支持点击选点查找路径。
# - 描述的情形：程序先尝试读取外部图片 `3.jpg` 并将其二值化为迷宫（黑色为墙），若读取失败则使用备用迷宫。
#   从自动选定的起点触发化学波，记录每个格子的到达时间（`arrival_times`），可交互地点击右侧时间图触发反向寻路并高亮最短路径。
# - 模拟方法：使用离散拉普拉斯算子模拟扩散，Barkley 型非线性反应项 `(1/epsilon)*U*(1-U)*(U-threshold)` 驱动激发波，
#   时间推进为显式步进（每帧内多次小步以提高稳定性）。墙体位置用 `walls` 掩码吸收化学场（设为 0）。
# - 附加机制：记录 `arrival_times` 用于绘制时间图并在右侧显示；`find_shortest_path` 使用邻域最小到达时间进行贪心反向回溯，从而恢复一条遵循波前传播的路径并以洋红色高亮。
# - 可调项与用途：可通过更换输入图片、调整 `epsilon, D, steps_per_frame` 等参数观察不同波形与寻路性能，适合用于演示化学波在复杂环境中的传播与基于波传播的路径恢复。
# ------------------------------------------------------------