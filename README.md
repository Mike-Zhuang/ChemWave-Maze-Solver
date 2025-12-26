# 🌊 ChemWave Maze Solver — Liquid Pathfinder

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Science](https://img.shields.io/badge/Reference-Science%201995-red.svg)](https://www.science.org/doi/10.1126/science.267.5199.868)
[![Repo](https://img.shields.io/badge/GitHub-ChemWave--Maze--Solver-black)](https://github.com/Mike-Zhuang/ChemWave-Maze-Solver)

> **"Chemistry is nature's original algorithm."**
> 
> **化学是自然界最原始的算法。**

A Digital Twin reproduction of the classic 1995 *Science* paper: *"Navigating Complex Labyrinths: Optimal Paths from Chemical Waves"*. Repository: Mike-Zhuang/ChemWave-Maze-Solver.

**数字孪生再现了1995年《科学》杂志的经典论文：** *《穿越复杂迷宫：化学波的最优路径》*。

---

## 📖 Introduction

**Liquid Pathfinder** is a simulation framework that explores the computational capabilities of reaction-diffusion systems. By simulating the **Barkley Model** of excitable media, this project demonstrates how chemical waves can perform massive parallel computing to find the optimal path through complex labyrinths.

**Liquid Pathfinder** 是一个模拟框架，用于探索反应扩散系统的计算能力。通过模拟可激发介质的 **Barkley 模型**，该项目展示了化学波如何通过大规模并行计算找到复杂迷宫中的最优路径。

### Key Highlights / 主要特点

1. **Explores in Parallel:** Waves propagate through all corridors simultaneously.  
   **并行探索：** 化学波同时传播到所有通道。
2. **Physical Selection:** Waves entering dead ends annihilate; waves on the shortest path arrive first.  
   **物理选择：** 进入死胡同的波会湮灭；最短路径上的波会最先到达。
3. **Digital Twin:** Uses **Computer Vision (CV)** to digitize any maze image into a physical simulation environment.  
   **数字孪生：** 使用 **计算机视觉 (CV)** 将任何迷宫图像数字化为物理模拟环境。

---

## ✨ Key Features / 功能亮点

- **⚡ Real-time Simulation:** Solves mazes using the reaction-diffusion dynamics (Barkley Model).  
  **实时模拟：** 使用反应扩散动力学（Barkley 模型）解决迷宫问题。
- **👁️ CV-Based Map Generation:** Automatically extracts maze structures from raw images (e.g., `3.jpg`) using OpenCV.  
  **基于 CV 的地图生成：** 使用 OpenCV 从原始图像（如 `3.jpg`）中自动提取迷宫结构。
- **🧠 Interactive Pathfinding:** Click anywhere on the map to instantly visualize the shortest path using **Time-Gradient Backtracking**.  
  **交互式路径查找：** 点击地图上的任意位置，使用 **时间梯度回溯** 即时可视化最短路径。
- **🌈 Visualization:** Dual-view display showing the **Live Wave Propagation** (Process) and the **Time-of-Arrival Map** (Result).  
  **可视化：** 双视图显示 **实时波传播**（过程）和 **到达时间图**（结果）。

---

## 🚀 Quick Start / 快速开始

### 1. Clone the repository / 克隆仓库
```bash
git clone https://github.com/Mike-Zhuang/ChemWave-Maze-Solver.git
cd ChemWave-Maze-Solver
```

### 2. Install dependencies / 安装依赖
```bash
pip install -r requirements.txt
```

### 3. Run the Digital Twin / 运行数字孪生
To run the full simulation with the complex 1664 Boeckler labyrinth (with CV extraction + interactive backtracking):  
运行复杂的 1664 Boeckler 迷宫（含图像识别 + 点击回溯寻路）的完整模拟：
```bash
python BZ_Barkley_Maze_Complicated.py
```

- **Left Screen:** Watch the chemical wave propagate in real-time.  
  **左屏幕：** 实时观察化学波的传播。
- **Right Screen:** See the time map building up.  
  **右屏幕：** 查看时间图的生成。
- **Interact:** Click any point on the right screen to reveal the optimal path!  
  **交互：** 点击右屏幕上的任意点以显示最优路径！

### 4. Other demos / 其它演示
- Barkley base model (two gates demo) / 基础 Barkley 模型（双门演示）
  ```bash
  python BZ_Barkley.py
  ```
- Hand-crafted maze (START/EXIT labels) / 手工复杂迷宫（带起终点标注）
  ```bash
  python BZ_Barkley_Maze.py
  ```
- Gray-Scott pattern formation / Gray-Scott 图灵花纹
  ```bash
  python BZ_Gray-Scott.py
  ```

---

## 📂 File Structure / 文件结构

- **BZ_Barkley_Maze_Complicated.py:** The advanced "Digital Twin" version. Includes CV maze extraction, dual-screen visualization, and interactive click-to-solve pathfinding.  
  **高级版：** 包含 CV 迷宫提取、双屏可视化和交互式点击求解路径。
- **BZ_Barkley.py:** A minimal Barkley excitable-media demo with a wall and two gates, good for learning the core dynamics before moving to full mazes.  
  **入门版：** 带“横墙 + 双门”的最小 Barkley 演示，适合先理解波传播与墙体吸收的核心机制。
- **BZ_Barkley_Maze.py:** A simplified version with a manually constructed U-trap maze, good for understanding the basic mechanism.  
  **简化版：** 包含手动构建的 U 型迷宫，适合理解基本机制。
- **BZ_Gray-Scott.py:** A fundamental demo of the Gray-Scott model, showcasing Turing patterns and self-catalysis ($U+2V \to 3V$).  
  **基础演示：** 展示 Gray-Scott 模型的图灵模式和自催化反应。
- **3.jpg:** The original maze image from the 1664 Boeckler design (and the 1995 Science paper).  
  **原始迷宫图：** 来自 1664 年 Boeckler 设计（以及 1995 年《科学》论文）。

> Note / 说明：`BZ_Barkley_Maze_Complicated.py` 默认读取 `3.jpg`（黑色为墙、白色为通道）。若缺失或读取失败，脚本会自动降级为内置备用迷宫，不会中断演示。

---

## ⚙️ Environment & Dependencies / 环境与依赖

- Python ≥ 3.8
- Packages: `numpy`, `matplotlib`, `opencv-python`（见 `requirements.txt`）

Optional tips / 建议：
- macOS 上若遇到 `matplotlib` 后端问题，可尝试：
  ```bash
  export MPLBACKEND=MacOSX
  ```
- OpenCV 读取迷宫的阈值目前在代码中固定为 `100`。对于不同风格的迷宫图，可在 `BZ_Barkley_Maze_Complicated.py` 中调整：
  ```python
  _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
  ```
  以获得更理想的二值化效果。

---

## 🧪 Parameters You Can Tweak / 可调参数

In Barkley-based scripts（`BZ_Barkley*.py`）you can tune:
- `epsilon`, `D`, `dt`: affect wave thickness, speed and stability.
- `steps_per_frame`: trade-off between visual smoothness and simulation speed.
- `sim_size` / `size`: resolution of the simulation grid.

在 Barkley 系脚本中可调整：
- `epsilon`、`D`、`dt`：影响波的厚度、速度与稳定性；
- `steps_per_frame`：在“流畅度”和“速度”之间折中；
- `sim_size` / `size`：模拟网格分辨率（越大越耗时）。

For the Digital Twin (`BZ_Barkley_Maze_Complicated.py`):
- Replace `3.jpg` with your own maze image, or modify `img_path` 指向你的图片路径；
- Ensure “walls = black, paths = white” for best results.

---

---

## 🔬 The Science Behind It / 背后的科学原理

### The Barkley Model / Barkley 模型
We simulate an excitable medium using the following partial differential equations:  
我们使用以下偏微分方程模拟可激发介质：

$$ \frac{\partial u}{\partial t} = D \nabla^2 u + \frac{1}{\epsilon} u (1-u) (u - \frac{v+b}{a}) $$
$$ \frac{\partial v}{\partial t} = u - v $$

Where:  
其中：
- $u$: The "propagator" species (the wave).  
  **传播者：** 波动。
- $v$: The "controller" species (the inhibitor).  
  **控制者：** 抑制剂。

Parameters: Tuned to $a=0.75, b=0.01$ (High contrast mode) vs original paper ($a=0.9, b=0.05$).  
参数：调整为 $a=0.75, b=0.01$（高对比模式），原始论文为 $a=0.9, b=0.05$。

### The Algorithm: Time-Gradient Backtracking / 算法：时间梯度回溯
The simulation builds a Time Map $T(x,y)$ recording when the wave reached each point. Finding the shortest path is reduced to a simple Gradient Descent problem:  
模拟生成一个时间图 $T(x,y)$，记录波到达每个点的时间。找到最短路径简化为一个梯度下降问题：

$$ Path = -\nabla T(x,y) $$

By tracing back from the destination to the source along the steepest descent of time, the optimal trajectory is mathematically guaranteed.  
通过沿时间最陡下降方向从终点回溯到起点，最优路径在数学上是有保证的。

---

## 🧰 Troubleshooting / 故障排查

- "找不到 3.jpg" 或图像提取效果差：
  - 程序会自动使用备用迷宫继续演示；
  - 调整 OpenCV 二值化阈值（见上文）；
  - 请确保迷宫图片为“黑墙白路”。
- 窗口卡顿或帧率低：
  - 降低分辨率（`sim_size`/`size`），或减少 `steps_per_frame`；
  - 关闭其他高负载任务。

---

---

## 📚 Reference / 参考文献

- **Original Paper:** Steinbock, O., Tóth, Á., & Showalter, K. (1995). Navigating complex labyrinths: Optimal paths from chemical waves. Science, 267(5199), 868-871.  
  **原始论文：** Steinbock, O., Tóth, Á., & Showalter, K. (1995)。穿越复杂迷宫：化学波的最优路径。《科学》，267(5199)，868-871。
- **Maze Design:** G. A. Boeckler (1664).  
  **迷宫设计：** G. A. Boeckler (1664)。

---

## 👨‍💻 Author / 作者

Zhuang Chengbo (Mike)  
庄程博（Mike）  
Future Technology Programme, Guohao College  
同济大学国豪学院未来技术班

---

## 🗂️ Repo Hygiene / 仓库规范

This repo ignores editor settings and OS artifacts to keep commits clean:

```
.vscode/
.DS_Store
```

除此之外，资源文件（如 `3.jpg`）与源码一并纳入版本管理，便于复现实验与演示。