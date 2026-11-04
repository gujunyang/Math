#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 math-tutor-os 板书用的几何示意图（matplotlib，输出 PNG）。

用法（在 math-tutor-os 目录内）：
    python3 系统/05_工具/生成几何图.py

输出目录：学习内容/04_板书/图片/
说明：几何示意优先，配色统一（蓝=主向量，红=次向量，灰=辅助线）。
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "Microsoft YaHei", "SimHei",
                                  "Hiragino Sans GB", "Songti SC"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "学习内容", "04_板书", "图片")
os.makedirs(OUT, exist_ok=True)

BLUE = "#1f77b4"
RED = "#d62728"
GRAY = "#9aa0a6"
GREEN = "#2ca02c"


def arrow(ax, x, y, color=BLUE, lw=2.0, label=None, ls="-", zorder=5):
    ax.annotate(
        "",
        xy=(x, y),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls,
                        shrinkA=0, shrinkB=0),
        zorder=zorder,
    )
    if label:
        ax.text(x * 1.03, y * 1.03, label, color=color, fontsize=13, zorder=6)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("生成", os.path.relpath(path, ROOT))


# --- 图 1：向量与分量 -------------------------------------------------------
def fig_vector():
    fig, ax = plt.subplots(figsize=(5, 5))
    arrow(ax, 3, 4, BLUE, label=r"$\mathbf{a}=(3,4)$")
    ax.plot([3, 3], [0, 4], ls="--", color=GRAY, lw=1)
    ax.plot([0, 3], [4, 4], ls="--", color=GRAY, lw=1)
    ax.plot([0, 3], [0, 0], color=GRAY, lw=1)
    ax.plot([0, 0], [0, 4], color=GRAY, lw=1)
    ax.text(1.5, -0.45, r"$x_1=3$", ha="center", color=GRAY, fontsize=12)
    ax.text(-0.5, 2.0, r"$x_2=4$", va="center", color=GRAY, fontsize=12)
    ax.scatter([3], [4], color=BLUE, s=25, zorder=6)
    ax.set_title("向量的几何：一支从原点出发的箭")
    ax.set_axisbelow(True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5)
    ax.set_aspect("equal")
    save(fig, "fig_vector_components.png")


# --- 图 2：内积的几何意义（投影） ------------------------------------------
def fig_inner():
    fig, ax = plt.subplots(figsize=(5.4, 5))
    a = np.array([4.0, 1.0])
    b = np.array([1.5, 2.5])
    arrow(ax, *a, BLUE, label=r"$\mathbf{a}$")
    arrow(ax, *b, RED, label=r"$\mathbf{b}$")
    # 投影：b 在 a 方向上的投影点
    t = np.dot(b, a) / np.dot(a, a)
    proj = t * a
    ax.plot([b[0], proj[0]], [b[1], proj[1]], ls="--", color=GRAY, lw=1.2)
    ax.annotate("", xy=proj, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2))
    ax.text(proj[0] * 0.5 + 0.1, proj[1] * 0.5 - 0.35,
            r"$\|\mathbf{b}\|\cos\theta$", color=GREEN, fontsize=12)
    # 直角标记
    u = a / np.linalg.norm(a)
    n = b - proj
    n = n / np.linalg.norm(n)
    s = 0.25
    p1 = proj + s * n
    p2 = proj + s * (n - u)
    p3 = proj - s * u
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=GRAY, lw=1)
    ax.text(1.15, 0.15, r"$\theta$", color="k", fontsize=13)
    ax.set_title(r"内积 = $\mathbf{a}\cdot\mathbf{b}=\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta$")
    ax.set_axisbelow(True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 4)
    ax.set_aspect("equal")
    save(fig, "fig_inner_product_projection.png")


# --- 图 3：三种范数的单位球 -------------------------------------------------
def fig_norms():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7))
    th = np.linspace(0, 2 * np.pi, 400)
    # L2：圆
    axes[0].plot(np.cos(th), np.sin(th), color=BLUE, lw=2.2)
    axes[0].set_title(r"L2 范数：$\|\mathbf{x}\|_2=1$（圆）")
    # L1：菱形
    d = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 0]], float)
    axes[1].plot(d[:, 0], d[:, 1], color=RED, lw=2.2)
    axes[1].set_title(r"L1 范数：$\|\mathbf{x}\|_1=1$（菱形）")
    # Linf：正方形
    sq = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 1]], float)
    axes[2].plot(sq[:, 0], sq[:, 1], color=GREEN, lw=2.2)
    axes[2].set_title(r"L∞ 范数：$\|\mathbf{x}\|_\infty=1$（正方形）")
    for ax in axes:
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
    fig.suptitle("“到原点距离为 1”的点集：不同范数，形状不同", y=1.04)
    save(fig, "fig_norm_unit_balls.png")


# --- 图 4：距离 = 差向量的长度 ---------------------------------------------
def fig_distance():
    fig, ax = plt.subplots(figsize=(5.4, 5))
    A = np.array([1.0, 1.0])
    B = np.array([4.0, 5.0])
    ax.scatter(*A, color=BLUE, s=40, zorder=6)
    ax.scatter(*B, color=RED, s=40, zorder=6)
    ax.text(A[0] - 0.5, A[1] - 0.4, r"$\mathbf{a}$", color=BLUE, fontsize=13)
    ax.text(B[0] + 0.1, B[1] + 0.1, r"$\mathbf{b}$", color=RED, fontsize=13)
    arrow(ax, *A, color=BLUE, lw=1.6)
    arrow(ax, *B, color=RED, lw=1.6)
    # 差向量 a-b，平移到 b 处显示
    ax.annotate("", xy=A, xytext=B,
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
    mid = (A + B) / 2
    ax.text(mid[0] - 0.3, mid[1] + 0.15, r"$\mathbf{a}-\mathbf{b}$", color=GREEN,
            fontsize=12)
    ax.text(2.2, 0.55, r"$d=\|\mathbf{a}-\mathbf{b}\|=5$", color=GREEN, fontsize=12)
    ax.set_title("距离 = “差向量”的长度")
    ax.set_axisbelow(True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    save(fig, "fig_distance.png")


# --- 图 5：余弦相似度只看方向 ----------------------------------------------
def fig_cosine():
    fig, ax = plt.subplots(figsize=(5.6, 5))
    a = np.array([3.0, 0.0])
    b1 = np.array([1.0, 1.0])
    b2 = np.array([2.0, 2.0])  # 与 b1 同方向，长度翻倍
    arrow(ax, *a, BLUE, label=r"$\mathbf{a}=(1,0)$ 方向")
    arrow(ax, *b1, RED, label=r"$\mathbf{b}$")
    arrow(ax, *b2, RED, lw=1.4, ls="--")
    ax.text(2.1, 2.1, r"$\mathbf{b}'=2\mathbf{b}$", color=RED, fontsize=11)
    ax.text(1.5, 0.35, r"$\theta=45^\circ$", color="k", fontsize=12)
    ax.set_title(r"方向相同、长度不同 $\Rightarrow$ 余弦相似度相同（$0.707$）")
    ax.set_axisbelow(True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.4, 4)
    ax.set_ylim(-0.4, 3.2)
    ax.set_aspect("equal")
    save(fig, "fig_cosine_similarity.png")


# --- 图 6：矩阵 = 线性变换（网格变形） -------------------------------------
def fig_matrix():
    M = np.array([[1.0, 0.7], [0.0, 1.2]])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    panels = [
        (axes[0], np.eye(2), "原网格（单位方格）", GRAY),
        (axes[1], M, r"变换后：$\mathbf{x}\mapsto \mathbf{M}\mathbf{x}$", BLUE),
    ]
    for ax, mat, title, color in panels:
        for t in np.linspace(-3, 3, 13):
            seg = np.array([[t, -3], [t, 3]]) @ mat.T
            ax.plot(seg[:, 0], seg[:, 1], color=color, lw=0.7, alpha=0.7)
            seg2 = np.array([[-3, t], [3, t]]) @ mat.T
            ax.plot(seg2[:, 0], seg2[:, 1], color=color, lw=0.7, alpha=0.7)
        e1 = mat @ np.array([1, 0])
        e2 = mat @ np.array([0, 1])
        ax.annotate("", xy=e1, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
        ax.annotate("", xy=e2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 4.5)
    axes[0].text(1.05, 0.2, r"$e_1$", color=RED, fontsize=12)
    axes[0].text(0.15, 1.1, r"$e_2$", color=GREEN, fontsize=12)
    axes[1].text(M[0, 0] + 0.05, M[1, 0], r"$e_1'$", color=RED, fontsize=12)
    axes[1].text(M[0, 1] + 0.05, M[1, 1], r"$e_2'$", color=GREEN, fontsize=12)
    fig.suptitle("矩阵就是一个线性变换：把整个网格（连同基向量）一起搬走", y=1.02)
    save(fig, "fig_matrix_transform.png")


# --- 图 7：转置 = 沿主对角线翻折 -------------------------------------------
def fig_transpose():
    from matplotlib.patches import Rectangle

    A = [[1, 2, 3], [4, 5, 6]]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))

    def draw(ax, grid, rows, cols, title, highlight=None):
        for i in range(rows):
            for j in range(cols):
                face = "#dbeafe"
                if highlight and (i, j) == highlight:
                    face = "#fde68a"
                ax.add_patch(Rectangle((j, rows - 1 - i), 1, 1, facecolor=face,
                                       edgecolor="k", lw=1))
                ax.text(j + 0.5, rows - 1 - i + 0.5, str(grid[i][j]),
                        ha="center", va="center", fontsize=13)
        ax.set_xlim(-0.3, cols + 0.3)
        ax.set_ylim(-0.3, rows + 0.3)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=12)
        ax.axis("off")

    draw(axes[0], A, 2, 3, r"$\mathbf{A}$：$2\times3$", highlight=(0, 1))
    draw(axes[1], [[A[j][i] for j in range(2)] for i in range(3)], 3, 2,
         r"$\mathbf{A}^{\top}$：$3\times2$", highlight=(1, 0))
    axes[0].text(1.5, -0.75, "把 (第1行,第2列) 的 2", ha="center", color="#b45309", fontsize=10)
    axes[1].text(1.0, -0.75, "挪到 (第2行,第1列)", ha="center", color="#b45309", fontsize=10)
    axes[2].axis("off")
    axes[2].text(0.5, 0.6, "转置 =", ha="center", fontsize=14)
    axes[2].text(0.5, 0.38, "行↔列 互换", ha="center", fontsize=14, color=BLUE)
    axes[2].text(0.5, 0.16, "（沿主对角线翻折）", ha="center", fontsize=11, color=GRAY)
    axes[2].set_xlim(0, 1)
    axes[2].set_ylim(0, 1)
    fig.suptitle("转置（transpose）：下标 $a_{ij}\\to a_{ji}$", y=1.05)
    save(fig, "fig_transpose.png")


# --- 图 8：逆 = 把变换撤销 -------------------------------------------------
def fig_inverse():
    A = np.array([[1.5, 0.6], [0.0, 1.2]])
    Ainv = np.linalg.inv(A)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    panels = [
        (axes[0], np.eye(2), "① 原网格"),
        (axes[1], A, r"② 施加 $\mathbf{A}$：网格被拉伸+搓斜"),
        (axes[2], Ainv @ A, r"③ 再施加 $\mathbf{A}^{-1}$：回到原样"),
    ]
    for ax, mat, title in panels:
        for t in np.linspace(-2, 2, 9):
            seg = np.array([[t, -2], [t, 2]]) @ mat.T
            ax.plot(seg[:, 0], seg[:, 1], color=GRAY, lw=0.6, alpha=0.6)
            seg2 = np.array([[-2, t], [2, t]]) @ mat.T
            ax.plot(seg2[:, 0], seg2[:, 1], color=GRAY, lw=0.6, alpha=0.6)
        e1 = mat @ np.array([1, 0])
        e2 = mat @ np.array([0, 1])
        ax.annotate("", xy=e1, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.3))
        ax.annotate("", xy=e2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.3))
        ax.set_title(title, fontsize=11)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.15)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
    fig.suptitle("逆矩阵 = “撤销”这台机器", y=1.02)
    save(fig, "fig_inverse.png")


# --- 图 9：可逆 vs 不可逆（行列式 = 面积伸缩） -----------------------------
def fig_determinant():
    unit = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], float)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    cases = [
        (axes[0], np.eye(2), "原单位正方形\n面积 = 1"),
        (axes[1], np.array([[1.2, 0.7], [0.4, 1.3]]), "可逆：变成平行四边形\n面积 = |det| ≈ 1.28"),
        (axes[2], np.array([[1.0, 2.0], [0.5, 1.0]]), "不可逆：压扁成一条线\n面积 = 0（det = 0）"),
    ]
    for ax, mat, title in cases:
        poly = unit @ mat.T
        ax.fill(poly[:, 0], poly[:, 1], color="#dbeafe", alpha=0.8, edgecolor=BLUE, lw=2)
        e1 = mat @ np.array([1, 0])
        e2 = mat @ np.array([0, 1])
        ax.annotate("", xy=e1, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
        ax.annotate("", xy=e2, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2))
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.set_title(title, fontsize=11)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 3.5)
    fig.suptitle("行列式 |det| = 单位正方形被放大/压扁后的面积", y=1.03)
    save(fig, "fig_determinant_invertibility.png")


# --- 图 10：张成（span）-----------------------------------------------------
def fig_span():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    # 面板1：一个向量 -> 张成一条直线
    v = np.array([1.0, 0.5])
    tt = np.linspace(-3, 3, 2)
    axes[0].plot(v[0] * tt, v[1] * tt, ls="--", color=GRAY, lw=1.2)
    for c in [-1.5, -0.5, 1.5, 2.5]:
        axes[0].annotate("", xy=c * v, xytext=(0, 0),
                         arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0, alpha=0.5))
    arrow(axes[0], *v, BLUE, lw=2.6, label=r"$\mathbf{v}$")
    axes[0].set_title("1 个向量 → 张成一条直线")

    # 面板2：两个不共线向量 -> 张成整个平面
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.4, 1.0])
    axes[1].set_facecolor("#eef4ff")
    for c1 in np.linspace(-3, 3, 13):
        for c2 in np.linspace(-3, 3, 13):
            p = c1 * v1 + c2 * v2
            axes[1].plot(p[0], p[1], ".", color="#9db8e8", ms=3)
    arrow(axes[1], *v1, RED, lw=2.6, label=r"$\mathbf{v}_1$")
    arrow(axes[1], *v2, GREEN, lw=2.6, label=r"$\mathbf{v}_2$")
    axes[1].set_title("2 个不共线向量 → 张成整个平面")

    # 面板3：两个共线向量 -> 仍是一条直线
    w1 = np.array([1.0, 0.5])
    w2 = np.array([2.0, 1.0])
    tt2 = np.linspace(-3, 3, 2)
    axes[2].plot(w1[0] * tt2, w1[1] * tt2, ls="--", color=GRAY, lw=1.2)
    arrow(axes[2], *w1, BLUE, lw=2.6, label=r"$\mathbf{w}_1$")
    arrow(axes[2], *w2, RED, lw=2.2, ls="--", label=r"$\mathbf{w}_2$")
    axes[2].set_title("2 个共线向量 → 还是一条直线")

    for ax in axes:
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-2.2, 3)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)
    fig.suptitle("张成（span）= 能由这些向量组合出来的所有点", y=1.03)
    save(fig, "fig_span.png")


# --- 图 11：线性无关 vs 线性相关 -------------------------------------------
def fig_independence():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    # 无关：两向量不共线
    v1 = np.array([1.2, 0.2])
    v2 = np.array([0.3, 1.2])
    arrow(axes[0], *v1, RED, lw=2.6, label=r"$\mathbf{v}_1$")
    arrow(axes[0], *v2, GREEN, lw=2.6, label=r"$\mathbf{v}_2$")
    axes[0].set_title("线性无关：谁也变不出另一个\n→ 张成整个平面（冗余为 0）")
    # 相关：共线
    w1 = np.array([1.0, 0.5])
    w2 = np.array([2.0, 1.0])
    arrow(axes[1], *w1, BLUE, lw=2.6, label=r"$\mathbf{w}_1$")
    arrow(axes[1], *w2, RED, lw=2.2, ls="--", label=r"$\mathbf{w}_2=2\mathbf{w}_1$")
    axes[1].set_title("线性相关：一个可由另一个得到\n→ 只能张成一条线（有冗余）")
    for ax in axes:
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.set_xlim(-0.6, 2.6)
        ax.set_ylim(-0.6, 2.6)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)
    fig.suptitle("线性无关 = “没有多余的方向”", y=1.02)
    save(fig, "fig_independence.png")


# --- 图 12：det = 两列张成的平行四边形面积（列相关则面积 0） ----------------
def fig_det_columns():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))

    def panel(ax, v1, v2, title, note, color):
        poly = np.array([[0, 0], v1, v1 + v2, v2, [0, 0]], float)
        ax.fill(poly[:, 0], poly[:, 1], color="#dbeafe", alpha=0.85,
                edgecolor=color, lw=2)
        arrow(ax, *v1, RED, lw=2.6, label=r"$\mathbf{v}_1$")
        arrow(ax, *v2, GREEN, lw=2.6, label=r"$\mathbf{v}_2$")
        ax.set_title(title, fontsize=11)
        ax.text(0.05, 0.03, note, transform=ax.transAxes, fontsize=12, color=color)
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.grid(True, alpha=0.2)
        ax.set_xlim(-0.4, 2.2)
        ax.set_ylim(-0.4, 2.2)
        ax.set_aspect("equal")

    v1 = np.array([1.2, 0.3])
    v2 = np.array([0.4, 1.1])
    panel(axes[0], v1, v2, "列不共线：平行四边形有面积\n(列线性无关)",
          r"$|\det|=|v_1\times v_2|=1.2\ne0$", BLUE)
    w1 = np.array([1.0, 0.5])
    w2 = np.array([0.6, 0.3])
    panel(axes[1], w1, w2, "列共线：被压扁成线段\n(列线性相关)",
          r"$|\det|=0$", RED)
    fig.suptitle(r"$\det$ 就是两列张成的平行四边形（带符号）面积", y=1.03)
    save(fig, "fig_det_columns.png")


# --- 图 13：正交 = 夹角 90°（点积为 0），夹角与点积符号 ---------------------
def fig_orthogonality():
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.3))
    a = np.array([2.2, 0.0])
    cases = [
        ("锐角：$\\mathbf{a}\\cdot\\mathbf{b}>0$", np.array([1.7, 1.5]), GREEN),
        ("直角：$\\mathbf{a}\\cdot\\mathbf{b}=0$（正交）", np.array([0.0, 2.2]), RED),
        ("钝角：$\\mathbf{a}\\cdot\\mathbf{b}<0$", np.array([-1.2, 1.6]), GRAY),
    ]
    for ax, (title, b, color) in zip(axes, cases):
        arrow(ax, *a, BLUE, lw=2.4, label=r"$\mathbf{a}$")
        arrow(ax, *b, color, lw=2.4, label=r"$\mathbf{b}$")
        # 直角标记（仅中间的"正交"图）
        if abs(np.dot(a, b)) < 1e-12:
            u = b / np.linalg.norm(b)
            v = a / np.linalg.norm(a)
            s = 0.3
            pts = np.array([u * s, u * s + v * s, v * s])
            ax.plot(pts[:, 0], pts[:, 1], color="k", lw=1.2)
            ax.text(0.1, 0.55, r"$90^\circ$", fontsize=12)
            ax.text(0.7, 1.0, r"$\mathbf{a}^{\top}\mathbf{b}=0$", color=RED, fontsize=12)
        ax.set_title(title, fontsize=11)
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.set_xlim(-2.2, 3.0)
        ax.set_ylim(-0.8, 2.8)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.2)
        ax.legend(loc="lower right", fontsize=10, frameon=False)
    fig.suptitle("正交 = 夹角 90° = 内积为 0；内积的符号就是夹角的锐/直/钝",
                 y=1.03)
    save(fig, "fig_orthogonality.png")


# --- 图 14：投影到一条直线 = 拆成"平行分量 + 垂直分量" ----------------------
def fig_projection_line():
    fig, ax = plt.subplots(figsize=(6.0, 5.4))
    a = np.array([3.0, 4.0])
    b = np.array([4.0, 2.0])
    t = np.dot(a, b) / np.dot(a, a)          # = 0.8
    p = t * a                                # (2.4, 3.2)
    e = b - p                                # (1.6, -1.2)

    # 直线 span{a}
    tt = np.linspace(-0.6, 2.2, 2)
    ax.plot(a[0] * tt, a[1] * tt, ls="--", color=GRAY, lw=1.2,
            label=r"直线 $\mathrm{span}\{\mathbf{a}\}$")
    ax.annotate("", xy=a, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    ax.text(a[0] * 1.02, a[1] * 1.02, r"$\mathbf{a}$", color=BLUE, fontsize=13)
    ax.annotate("", xy=b, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax.text(b[0] + 0.08, b[1] + 0.08, r"$\mathbf{b}$", color=RED, fontsize=13)
    # 投影 p 与残差 e
    ax.annotate("", xy=p, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.6))
    ax.text(p[0] - 1.35, p[1] + 0.45, r"$\mathbf{p}=\mathrm{proj}_{\mathbf{a}}\mathbf{b}$",
            color=GREEN, fontsize=12)
    ax.annotate("", xy=b, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color="#8c564b", lw=2.0))
    ax.text((p[0] + b[0]) / 2 + 0.05, (p[1] + b[1]) / 2 - 0.35,
            r"$\mathbf{e}=\mathbf{b}-\mathbf{p}$", color="#8c564b", fontsize=12)
    # 直角标记
    u = a / np.linalg.norm(a)
    n = e / np.linalg.norm(e)
    s = 0.28
    pts = np.array([p + n * s, p + n * s + u * s, p + u * s])
    ax.plot(pts[:, 0], pts[:, 1], color="k", lw=1.1)
    ax.scatter([p[0]], [p[1]], color=GREEN, s=30, zorder=6)
    ax.text(0.02, 0.96, r"$\mathbf{p}=t\,\mathbf{a},\quad t=\dfrac{\mathbf{a}^{\top}\mathbf{b}}{\mathbf{a}^{\top}\mathbf{a}}=0.8$",
            transform=ax.transAxes, va="top", fontsize=12)
    ax.set_title("投影 = 只保留 $\\mathbf{b}$ 沿 $\\mathbf{a}$ 方向的分量", fontsize=12)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.set_xlim(-1.0, 5.4)
    ax.set_ylim(-1.0, 5.2)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    save(fig, "fig_projection_line.png")


# --- 图 15：投影到一个平面（列空间）—— 残差垂直平面 = 最小二乘的几何 --------
def fig_projection_subspace():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    fig = plt.figure(figsize=(6.6, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    # 平面：span{e1, e2} = 列空间
    g = np.linspace(-0.3, 2.6, 2)
    GX, GY = np.meshgrid(g, g)
    ax.plot_surface(GX, GY, np.zeros_like(GX), color="#cfe3ff", alpha=0.45,
                    edgecolor=GRAY, linewidth=0.4)
    y = np.array([1.4, 1.0, 2.0])
    p = np.array([1.4, 1.0, 0.0])
    r = y - p
    ax.quiver(0, 0, 0, *y, color=RED, lw=2.4, arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, *p, color=BLUE, lw=2.4, arrow_length_ratio=0.08)
    ax.quiver(p[0], p[1], p[2], *r, color=GREEN, lw=2.4, arrow_length_ratio=0.12)
    ax.text(*(y * 1.04), r"$\mathbf{y}$", color=RED, fontsize=13)
    ax.text(*(p * 1.03 + np.array([0, 0, 0.08])), r"$\hat{\mathbf{y}}$", color=BLUE, fontsize=13)
    ax.text(*(p + r / 2 + np.array([0.1, 0.05, 0.0])), r"$\mathbf{r}=\mathbf{y}-\hat{\mathbf{y}}$",
            color=GREEN, fontsize=11)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_zlabel(r"$x_3$")
    ax.set_title("投影到子空间：残差 $\\mathbf{r}\\perp$ 列空间\n（最小二乘就是找平面上离 $\\mathbf{y}$ 最近的点）",
                 fontsize=11)
    ax.set_xlim(0, 2.4)
    ax.set_ylim(0, 2.4)
    ax.set_zlim(0, 2.4)
    ax.view_init(elev=20, azim=-58)
    save(fig, "fig_projection_subspace.png")


# --- 图 16：特征向量（方向不变） -------------------------------------------
def fig_eigen():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    fig, ax = plt.subplots(figsize=(6.2, 5.6))

    # 单位圆 -> 椭圆（矩阵把圆拉成椭圆）
    th = np.linspace(0, 2 * np.pi, 400)
    circle = np.vstack([np.cos(th), np.sin(th)])
    ell = A @ circle
    ax.plot(circle[0], circle[1], color=GRAY, ls="--", lw=1.2,
            label=r"单位圆 $\|\mathbf{x}\|=1$")
    ax.plot(ell[0], ell[1], color=BLUE, lw=2.2,
            label=r"像椭圆 $\mathbf{A}\mathbf{x}$")

    # 两条特征方向（虚线辅助线）
    for d, c in [(np.array([1.0, 1.0]), RED), (np.array([1.0, -1.0]), GREEN)]:
        t = np.linspace(-3.6, 3.6, 2)
        ax.plot(d[0] * t, d[1] * t, color=c, ls=":", lw=1.0, alpha=0.7, zorder=1)

    # v1 -> A v1 = 3 v1（同向，变长）
    v1 = np.array([1.0, 1.0])
    arrow(ax, *v1, RED, lw=2.0, label=r"$\mathbf{v}_1$")
    arrow(ax, *(A @ v1), RED, lw=2.0, ls="--")
    ax.text(3.15, 3.15, r"$\mathbf{A}\mathbf{v}_1=3\mathbf{v}_1$", color=RED, fontsize=12)

    # v2 -> A v2 = v2（同向，长度不变）
    v2 = np.array([1.0, -1.0])
    arrow(ax, *v2, GREEN, lw=2.0, label=r"$\mathbf{v}_2$")
    arrow(ax, *(A @ v2), GREEN, lw=3.2, ls="--")
    ax.text(1.05, -1.55, r"$\mathbf{A}\mathbf{v}_2=1\cdot\mathbf{v}_2$", color=GREEN, fontsize=12)

    # 一般向量：方向会转
    u = np.array([1.6, 0.4])
    arrow(ax, *u, GRAY, lw=1.8, ls="-.")
    arrow(ax, *(A @ u), GRAY, lw=1.8, ls=":")
    ax.text(2.0, 1.0, r"一般向量：方向会变", color=GRAY, fontsize=10)

    ax.set_title(r"特征向量：$A\mathbf{v}=\lambda\mathbf{v}$ —— 方向不变，只被拉伸 $\lambda$ 倍")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(0, color=GRAY, lw=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(-4, 4.2)
    ax.set_ylim(-4, 4.2)
    ax.set_aspect("equal")
    ax.legend(loc="lower right", fontsize=9)
    save(fig, "fig_eigen_direction.png")


# --- 图 17：谱分解三步 —— 换坐标 → 拉伸 → 转回来 ---------------------------
def fig_spectral_steps():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    Q = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
    Lam = np.diag([3.0, 1.0])
    steps = [
        (np.eye(2), "① 原图：单位圆 + 标准网格\n（蓝 = 单位圆）"),
        (Q.T, "② 乘 $\\mathbf{Q}^\\top$：换到特征坐标\n（网格转到特征方向，圆还是圆）"),
        (Lam @ Q.T, "③ 乘 $\\boldsymbol{\\Lambda}$：沿两条特征轴\n分别拉伸 3 倍、1 倍"),
        (Q @ Lam @ Q.T, "④ 乘 $\\mathbf{Q}$：转回原坐标\n→ 半轴 3 和 1 的椭圆"),
    ]
    th = np.linspace(0, 2 * np.pi, 400)
    circle = np.vstack([np.cos(th), np.sin(th)])
    q1 = Q[:, 0]
    q2 = Q[:, 1]

    fig, axes = plt.subplots(1, 4, figsize=(17, 4.4))
    for ax, (M, title) in zip(axes, steps):
        # 网格
        for t in np.linspace(-4, 4, 17):
            for seg in (np.array([[t, -4], [t, 4]]), np.array([[-4, t], [4, t]])):
                p = seg @ M.T
                ax.plot(p[:, 0], p[:, 1], color=GRAY, lw=0.6, alpha=0.6)
        # 单位圆的像
        img = M @ circle
        ax.plot(img[0], img[1], color=BLUE, lw=2.2)
        # 两条特征方向在这个视角下的样子
        for vec, color, name in [(q1, RED, r"$\mathbf{q}_1$"), (q2, GREEN, r"$\mathbf{q}_2$")]:
            w = M @ vec
            ax.annotate("", xy=w, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2))
            ax.text(w[0] * 1.06 + 0.06, w[1] * 1.06 + 0.06, name, color=color, fontsize=12)
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.set_title(title, fontsize=10.5)
        ax.set_xlim(-3.6, 3.6)
        ax.set_ylim(-3.6, 3.6)
        ax.set_aspect("equal")
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
    fig.suptitle(r"$\mathbf{A}=\mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^\top$：换个坐标系说话 → 各方向拉伸 → 换回来说",
                 y=1.03, fontsize=13)
    save(fig, "fig_spectral_steps.png")


# --- 图 18：二次型的等高线 —— 椭圆（碗）/ 双曲线（鞍）/ 平行线（谷） --------
def fig_quadratic_contours():
    x = np.linspace(-2.4, 2.4, 500)
    X, Y = np.meshgrid(x, x)
    cases = [
        (np.array([[2.0, 1.0], [1.0, 2.0]]),
         "① 正定（" + r"$\lambda=3,\,1$" + "）\n等高线是椭圆：碗，原点最低"),
        (np.array([[1.0, 2.0], [2.0, 1.0]]),
         "② 不定（" + r"$\lambda=3,\,-1$" + "）\n等高线是双曲线：马鞍"),
        (np.array([[1.0, 1.0], [1.0, 1.0]]),
         "③ 半正定（" + r"$\lambda=2,\,0$" + "）\n等高线是平行直线：山谷"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, (M, title) in zip(axes, cases):
        Q = M[0, 0] * X ** 2 + (M[0, 1] + M[1, 0]) * X * Y + M[1, 1] * Y ** 2
        ax.contour(X, Y, Q, levels=[1, 2, 4, 8], colors=[BLUE], linewidths=1.6)
        ax.contour(X, Y, Q, levels=[-8, -4, -2, -1], colors=[RED], linewidths=1.6,
                   linestyles="--")
        # 特征方向
        w, V = np.linalg.eigh(M)
        for k, color in [(0, GREEN), (1, RED)]:
            v = V[:, k]
            ax.annotate("", xy=v * 2.2, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, ls=":"))
            ax.text(v[0] * 2.35, v[1] * 2.35, rf"$\lambda={w[k]:.0f}$", color=color,
                    fontsize=11)
        ax.scatter([0], [0], color="k", s=22, zorder=6)
        ax.text(0.06, -0.28, "原点", fontsize=10)
        ax.set_title(title, fontsize=11)
        ax.axhline(0, color=GRAY, lw=0.7)
        ax.axvline(0, color=GRAY, lw=0.7)
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.4, 2.4)
        ax.set_aspect("equal")
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([-2, 0, 2])
    fig.suptitle(r"二次型 $q(\mathbf{x})=\mathbf{x}^\top\mathbf{A}\mathbf{x}$ 的等高线：蓝 = 正值，红虚线 = 负值",
                 y=1.03, fontsize=13)
    save(fig, "fig_quadratic_contours.png")


# --- 图 19：梯度 ⟂ 等高线，指向上升最快方向 --------------------------------
def fig_gradient_contour():
    from matplotlib.lines import Line2D

    x = np.linspace(-2.6, 2.6, 500)
    X, Y = np.meshgrid(x, x)
    F = X ** 2 + 2 * Y ** 2

    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    cs = ax.contour(X, Y, F, levels=[0.5, 1, 2, 4, 8], colors=[GRAY],
                    linewidths=1.3)
    ax.clabel(cs, fmt="f=%.1f", fontsize=9, inline=True)

    def grad(p):
        return np.array([2 * p[0], 4 * p[1]])

    # 蓝色：梯度（最陡上升）
    for p in [np.array([1.45, 0.75]), np.array([-1.3, 1.1]),
              np.array([-1.5, -0.75]), np.array([0.95, -1.35])]:
        g = grad(p)
        g = g / np.linalg.norm(g) * 0.75
        ax.annotate("", xy=p + g, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0))

    # 绿色：负梯度（最陡下降）
    p0 = np.array([-1.3, 1.1])
    g0 = grad(p0)
    g0 = -g0 / np.linalg.norm(g0) * 0.75
    ax.annotate("", xy=p0 + g0, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2))
    ax.text(p0[0] - 0.95, p0[1] - 0.55, r"$-\nabla f$（下山）", color=GREEN, fontsize=11)

    # 直角标记：梯度 ⟂ 切线
    p = np.array([1.2, 1.0])
    g = grad(p)
    u1 = g / np.linalg.norm(g)
    u2 = np.array([-u1[1], u1[0]])
    s = 0.3
    ax.plot(*np.array([p - s * u2, p + s * u2]).T, color=GRAY, lw=1.4, ls="--")
    k = 0.18
    sq = np.array([p + k * u1, p + k * u1 + k * u2, p + k * u2])
    ax.plot(sq[:, 0], sq[:, 1], color="k", lw=1.1)
    ax.scatter([p[0]], [p[1]], color="k", s=24, zorder=6)
    ax.annotate("", xy=p + u1 * 0.85, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.6))

    ax.set_title(r"梯度 $\nabla f$ 垂直于等高线，指向 $f$ 增大最快的方向", fontsize=12)
    ax.axhline(0, color=GRAY, lw=0.7)
    ax.axvline(0, color=GRAY, lw=0.7)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_aspect("equal")
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.legend(handles=[
        Line2D([], [], color=BLUE, lw=2, label=r"$\nabla f$：最陡上升"),
        Line2D([], [], color=GREEN, lw=2, label=r"$-\nabla f$：最陡下降"),
        Line2D([], [], color=GRAY, lw=1.3, ls="--", label="切线 = 等高线方向"),
        Line2D([], [], color=GRAY, lw=1.3, label="等高线 $f=c$"),
    ], loc="lower right", fontsize=9, frameon=False)
    save(fig, "fig_gradient_contour.png")


# --- 图 20：二阶 Taylor = 在一点贴一条抛物线 --------------------------------
def fig_taylor_parabola():
    w = np.linspace(-0.95, 1.2, 500)
    L = 0.5 * (w * np.exp(w) - 2) ** 2
    tan = 2.0 - 2.0 * w                 # 一阶 Taylor
    par = 2.0 - 2.0 * w - 1.5 * w ** 2  # 二阶 Taylor（L''(0) = -3）

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    ax.plot(w, L, color=BLUE, lw=2.6, label=r"$L(w)=\frac{1}{2}(we^w-2)^2$")
    ax.plot(w, tan, color=GRAY, lw=1.6, ls="--", label=r"一阶：切线 $L(0)+L'(0)w$")
    ax.plot(w, par, color=RED, lw=2.0, ls="-",
            label=r"二阶：抛物线 $L(0)+L'(0)w+\frac{L''(0)}{2}w^2$")

    ax.scatter([0], [2], color="k", s=40, zorder=6)
    ax.text(-0.92, 0.55, r"$w_0=0$：" + "\n" + r"$L=2,\ L'=-2,\ L''=-3$",
            fontsize=10, bbox=dict(boxstyle="round", fc="white", ec=GRAY, alpha=0.9))

    ws = 0.8526
    ax.scatter([ws], [0], color=GREEN, s=40, zorder=6)
    ax.annotate(r"真正的最小 $w\approx0.85$", xy=(ws, 0.03), xytext=(0.40, 0.62),
                fontsize=10, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))

    ax.set_title("局部二次近似：值、斜率、曲率三样都对上", fontsize=12)
    ax.set_xlabel(r"$w$")
    ax.set_ylabel(r"$L(w)$")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(-0.95, 1.2)
    ax.set_ylim(-0.3, 3.4)
    ax.legend(loc="upper center", fontsize=9, frameon=False)
    save(fig, "fig_taylor_parabola.png")


# --- 图 21：概率规则 = 面积（Venn + Bayes 先验→后验） ----------------------
def fig_prob_rules():
    from matplotlib.patches import Circle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.6))

    # 左：Venn 图（并 = 相加后减去重叠）
    ax1.add_patch(Circle((0.40, 0.57), 0.27, facecolor=BLUE, alpha=0.26,
                         edgecolor=BLUE, lw=2))
    ax1.add_patch(Circle((0.63, 0.47), 0.22, facecolor=RED, alpha=0.26,
                         edgecolor=RED, lw=2))
    ax1.text(0.24, 0.82, r"$A$", color=BLUE, fontsize=15, ha="center")
    ax1.text(0.81, 0.66, r"$B$", color=RED, fontsize=15, ha="center")
    ax1.annotate(r"$A\cap B$", xy=(0.53, 0.52), xytext=(0.53, 0.22),
                 ha="center", fontsize=11, color="#5b2d8e",
                 arrowprops=dict(arrowstyle="->", color="#5b2d8e", lw=1.0))
    ax1.text(0.5, 0.02, r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$",
             ha="center", fontsize=10.5)
    ax1.text(0.5, -0.10, r"$P(A\,|\,B)=\dfrac{P(A\cap B)}{P(B)}$",
             ha="center", fontsize=11)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.16, 1.0)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("概率 = 面积：条件化 = 换一个分母", fontsize=11.5)

    # 右：Bayes = 先验 → 后验（同一条 [0,1]，面积重新分配）
    ax2.barh(1, 0.02, height=0.32, color=BLUE, edgecolor="white")
    ax2.barh(1, 0.98, left=0.02, height=0.32, color=RED, alpha=0.75,
             edgecolor="white")
    ax2.barh(0, 0.3265, height=0.32, color=BLUE, edgecolor="white")
    ax2.barh(0, 0.6735, left=0.3265, height=0.32, color=RED, alpha=0.75,
             edgecolor="white")

    ax2.text(-0.02, 1, r"先验 $P(C)$", ha="right", va="center", fontsize=10.5)
    ax2.text(-0.02, 0, r"后验 $P(C\,|\,T{=}1)$", ha="right", va="center",
             fontsize=10.5)
    ax2.text(0.01, 1.26, r"$2\%$", color=BLUE, fontsize=11)
    ax2.text(0.50, 1.0, r"$98\%$", color="white", ha="center", va="center",
             fontsize=11)
    ax2.text(0.163, 0.0, r"$32.6\%$", color="white", ha="center", va="center",
             fontsize=11)
    ax2.text(0.67, 0.0, r"$67.4\%$", color="white", ha="center", va="center",
             fontsize=11)

    ax2.annotate("证据把 2% 抬到 32.6%\n（仍然不到一半）",
                 xy=(0.10, -0.19), xytext=(0.30, -0.46), fontsize=10.5,
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
    ax2.text(0.02, -0.80,
             r"$P(C{=}1\,|\,T{=}1)=\dfrac{0.019}{0.019+0.0392}=0.326$",
             fontsize=10.5)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.95, 1.45)
    ax2.set_yticks([])
    ax2.set_xlabel("概率质量（面积）")
    ax2.set_title("Bayes：先验 → 后验，分母是全概率", fontsize=11.5)
    ax2.grid(True, axis="x", alpha=0.2)

    save(fig, "fig_prob_rules.png")


# --- 图 22：密度 = 高度，概率 = 面积；CDF = 累积面积 ------------------------
def fig_density_cdf():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2))

    # 左：p(x)=2x，阴影面积 = P(X<1/2)
    x = np.linspace(0, 1, 200)
    ax1.plot(x, 2 * x, color=BLUE, lw=2.2, label=r"$p(x)=2x$")
    xs = np.linspace(0, 0.5, 100)
    ax1.fill_between(xs, 0, 2 * xs, color=BLUE, alpha=0.28)
    ax1.plot([0.5, 0.5], [0, 1.0], ls="--", color=GRAY, lw=1)
    ax1.text(0.22, 0.30, r"面积 $=P(X<1/2)=\frac{1}{4}$", fontsize=10.5, color=BLUE)
    ax1.annotate("", xy=(1.0, 2.0), xytext=(1.0, 0.0),
                 arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1))
    ax1.text(1.02, 0.9, "总面积\n$=1$", fontsize=10, color=GRAY, va="center")
    ax1.set_xlim(0, 1.18)
    ax1.set_ylim(0, 2.25)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$p(x)$")
    ax1.set_title("密度是「高度」，概率是「面积」", fontsize=11.5)
    ax1.grid(True, alpha=0.25)

    # 右：F(x)=x^2
    xx = np.linspace(-0.25, 1.25, 500)
    F = np.where(xx < 0, 0.0, np.where(xx > 1, 1.0, xx ** 2))
    ax2.plot(xx, F, color=GREEN, lw=2.2, label=r"$F(x)=P(X\le x)$")
    ax2.plot([0.5, 0.5], [0, 0.25], ls="--", color=GRAY, lw=1)
    ax2.plot([0, 0.5], [0.25, 0.25], ls="--", color=GRAY, lw=1)
    ax2.scatter([0.5], [0.25], color=GREEN, s=35, zorder=6)
    ax2.text(0.55, 0.16, r"$F(0.5)=0.5^2=0.25$", fontsize=10.2, color=GREEN)
    ax2.text(-0.22, 1.04, r"$F=1$", fontsize=10, color=GRAY)
    ax2.text(-0.22, -0.10, r"$F=0$", fontsize=10, color=GRAY)
    ax2.set_xlim(-0.28, 1.28)
    ax2.set_ylim(-0.18, 1.18)
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$F(x)$")
    ax2.set_title("CDF = 从左往右累积的面积", fontsize=11.5)
    ax2.grid(True, alpha=0.25)

    save(fig, "fig_density_cdf.png")


# --- 图 23：Gaussian：μ 定位置、σ 定宽度；Σ 定椭圆 ------------------------
def fig_gaussian():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.3))

    # 左：一元正态
    x = np.linspace(-4, 4, 400)
    y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    ax1.plot(x, y, color=BLUE, lw=2.2)
    xs = np.linspace(-1, 1, 200)
    ax1.fill_between(xs, 0, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi),
                     color=BLUE, alpha=0.25)
    ax1.plot([0, 0], [0, 1 / np.sqrt(2 * np.pi)], ls="--", color=GRAY, lw=1)
    ax1.text(0, 0.05, r"$\mu$", ha="center", color=GRAY, fontsize=12)
    ax1.annotate(r"$\mu\pm\sigma$：约 $68\%$", xy=(0.55, 0.16),
                 xytext=(1.2, 0.24), fontsize=10, color=BLUE,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1))
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(0, 0.46)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$p(x)$")
    ax1.set_title(r"一元：$\mu$ 定位置，$\sigma$ 定宽度", fontsize=11.5)
    ax1.grid(True, alpha=0.25)

    # 右：二维相关正态的椭圆等高线 + 主轴
    S = np.array([[1.6, 0.9], [0.9, 1.0]])
    w, V = np.linalg.eigh(S)
    gx = np.linspace(-3.2, 3.2, 260)
    X, Y = np.meshgrid(gx, gx)
    Si = np.linalg.inv(S)
    Z = np.exp(-0.5 * (Si[0, 0] * X ** 2 + 2 * Si[0, 1] * X * Y
                       + Si[1, 1] * Y ** 2))
    ax2.contour(X, Y, Z, levels=[0.15, 0.4, 0.7, 0.9], colors=[BLUE],
                linewidths=1.6, alpha=0.8)
    for i in range(2):
        v = V[:, i] * 2.2 * np.sqrt(w[i])
        ax2.annotate("", xy=(v[0], v[1]), xytext=(0, 0),
                     arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
        ax2.text(v[0] * 1.08, v[1] * 1.08,
                 r"$\sqrt{\lambda_%d}$" % (i + 1), color=RED, fontsize=11)
    ax2.set_xlim(-3.2, 3.2)
    ax2.set_ylim(-3.2, 3.2)
    ax2.set_aspect("equal")
    ax2.set_xlabel(r"$x_1$")
    ax2.set_ylabel(r"$x_2$")
    ax2.set_title(r"多维：$\Sigma$ 定椭圆（轴 = 特征方向）", fontsize=11.5)
    ax2.grid(True, alpha=0.2)

    save(fig, "fig_gaussian.png")


# --- 图 24：MLE：对数似然的峰值 -------------------------------------------
def fig_mle():
    x = np.array([498.0, 502.0, 500.0, 504.0, 496.0])
    N = x.size
    S = float(np.sum((x - x.mean()) ** 2))  # 40

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.0))

    # 左：ℓ(μ)，σ² 固定为 8
    mu = np.linspace(494, 506, 400)
    ll_mu = -(N / 2) * np.log(2 * np.pi * 8) - np.sum(
        (x[None, :] - mu[:, None]) ** 2, axis=1) / (2 * 8)
    ax1.plot(mu, ll_mu, color=BLUE, lw=2.2)
    ax1.axvline(x.mean(), ls="--", color=GRAY, lw=1)
    ax1.scatter([x.mean()], [ll_mu.max()], color=RED, s=40, zorder=6)
    ax1.annotate(r"$\hat\mu=\bar x=500$", xy=(500, ll_mu.max()),
                 xytext=(501.2, ll_mu.max() - 1.6), fontsize=10.5,
                 color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1))
    ax1.set_xlabel(r"$\mu$")
    ax1.set_ylabel(r"$\ell(\mu)$")
    ax1.set_title(r"固定 $\sigma^2$：$\ell$ 的峰在样本均值", fontsize=11.5)
    ax1.grid(True, alpha=0.25)

    # 右：ℓ(σ²)，μ 固定为 500
    v = np.linspace(2, 20, 400)
    ll_v = -(N / 2) * np.log(v) - S / (2 * v)
    ax2.plot(v, ll_v, color=BLUE, lw=2.2, label=r"$\ell(\sigma^2)$")
    ax2.axvline(S / N, ls="--", color=RED, lw=1.5)
    ax2.axvline(S / (N - 1), ls=":", color=GREEN, lw=1.6)
    ax2.text(S / N + 0.3, ll_v.min() + 0.6,
             r"ML: $40/5=8$", color=RED, fontsize=10.5)
    ax2.text(S / (N - 1) + 0.3, ll_v.min() + 1.8,
             r"无偏: $40/4=10$", color=GREEN, fontsize=10.5)
    ax2.set_xlabel(r"$\sigma^2$")
    ax2.set_ylabel(r"$\ell(\sigma^2)$")
    ax2.set_title(r"固定 $\mu$：峰在 $\sigma^2=S/N$，不是 $S/(N-1)$", fontsize=11.5)
    ax2.grid(True, alpha=0.25)

    save(fig, "fig_mle.png")


# --- 图 25：变量变换：同一块概率质量被拉伸 ---------------------------------
def fig_change_of_vars():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.1))

    # 左：p_X(x)=2x，阴影 x∈[0.4,0.6]
    x = np.linspace(0, 1, 300)
    ax1.plot(x, 2 * x, color=BLUE, lw=2.2)
    xs = np.linspace(0.4, 0.6, 120)
    ax1.fill_between(xs, 0, 2 * xs, color=BLUE, alpha=0.28)
    ax1.text(0.5, 1.80, r"$x\in[0.4,\,0.6]$", ha="center", fontsize=10.5)
    ax1.text(0.5, 0.42, "面积 $=0.2$", ha="center", fontsize=10.5, color=BLUE)
    ax1.set_xlim(0, 1.05)
    ax1.set_ylim(0, 2.2)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$p_X(x)=2x$")
    ax1.set_title("变换前：边长越长越常见", fontsize=11.5)
    ax1.grid(True, alpha=0.25)

    # 右：p_Y(y)=1，阴影 y∈[0.16,0.36]
    y = np.linspace(0, 1, 300)
    ax2.plot(y, np.ones_like(y), color=GREEN, lw=2.2)
    ys = np.linspace(0.16, 0.36, 120)
    ax2.fill_between(ys, 0, 1, color=GREEN, alpha=0.28)
    ax2.text(0.26, 1.42, r"$y\in[0.16,\,0.36]$", ha="center", fontsize=10.5)
    ax2.text(0.26, 0.45, "面积 $=0.2$", ha="center", fontsize=10.5, color=GREEN)
    ax2.set_xlim(0, 1.05)
    ax2.set_ylim(0, 1.75)
    ax2.set_xlabel(r"$y=x^2$")
    ax2.set_ylabel(r"$p_Y(y)=1$")
    ax2.set_title("变换后：面积反而完全均匀", fontsize=11.5)
    ax2.grid(True, alpha=0.25)

    fig.subplots_adjust(bottom=0.24, wspace=0.25)
    fig.text(0.5, 0.04, "同一块概率质量换了个坐标：宽度被拉伸，高度就必须压扁——面积不变。",
             ha="center", fontsize=10.5, color=GRAY)
    save(fig, "fig_change_of_vars.png")


# --- 图 26：线性判别的决策边界、法向量与 signed distance -------------------
def fig_decision_boundary():
    w = np.array([3.0, 4.0])
    w0 = -6.0
    nrm = np.linalg.norm(w)
    nhat = w / nrm
    foot = -w0 * w / (nrm ** 2)            # 原点到边界的垂足 (0.72, 0.96)
    r0 = -w0 / nrm                          # 1.2
    xa = np.array([4.0, 2.0])
    ra = (w @ xa + w0) / nrm                # 2.8
    pa = xa - ra * nhat                     # 边界上的垂足

    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    xs = np.linspace(-1.0, 5.5, 200)
    ys = (-w0 - w[0] * xs) / w[1]           # 边界 3x+4y=6
    ax.plot(xs, ys, color=BLUE, lw=2.2, label=r"决策边界 $y(\mathbf{x})=0$")

    # 两个半平面
    ylo, yhi = -1.2, 6.0
    ax.fill_between(xs, ys, yhi, color=BLUE, alpha=0.10)
    ax.fill_between(xs, ylo, ys, color=RED, alpha=0.08)
    ax.text(3.6, 5.0, r"$C_1:\ y>0$", color=BLUE, fontsize=12)
    ax.text(-0.75, 0.9, r"$C_2:\ y<0$", color=RED, fontsize=12)

    # 法向量：从垂足出发
    ax.annotate("", xy=foot + 2.0 * nhat, xytext=foot,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    ax.text(*(foot + 2.1 * nhat), r"$\mathbf{w}$（法向）", color=BLUE, fontsize=12)

    # r0：原点到边界的 signed distance
    ax.annotate("", xy=foot, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.0))
    ax.text(0.10, 0.35, r"$r_0=1.2$", color=GREEN, fontsize=11.5)

    # x_A 与它到边界的距离
    ax.scatter([xa[0]], [xa[1]], color=RED, s=42, zorder=6)
    ax.text(xa[0] + 0.10, xa[1] + 0.15, r"$\mathbf{x}_A=(4,2)$", color=RED, fontsize=11.5)
    ax.plot([xa[0], pa[0]], [xa[1], pa[1]], ls="--", color=RED, lw=1.6)
    ax.text((xa[0] + pa[0]) / 2 + 0.12, (xa[1] + pa[1]) / 2 + 0.18,
            r"$r_A=2.8$", color=RED, fontsize=11.5)
    ax.scatter([pa[0]], [pa[1]], color=RED, s=24, zorder=6)

    ax.set_title(r"$\mathbf{w}$ 垂直边界；$r_0=-w_0/\|\mathbf{w}\|$ 是原点到边界的距离", fontsize=11.5)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_xlim(-1.0, 5.5)
    ax.set_ylim(-1.2, 6.0)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.legend(loc="lower left", fontsize=9, frameon=False)
    save(fig, "fig_decision_boundary.png")


# --- 图 27：误差面、等高线与梯度下降的 zig-zag ------------------------------
def fig_error_surface():
    fig = plt.figure(figsize=(11.6, 4.6))
    w1 = np.linspace(-2.2, 2.2, 160)
    w2 = np.linspace(-2.2, 2.2, 160)
    W1, W2 = np.meshgrid(w1, w2)
    E = 0.5 * (4.0 * W1 ** 2 + 1.0 * W2 ** 2)

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(W1, W2, E, cmap="viridis", alpha=0.9, linewidth=0, antialiased=True)
    ax1.contour(W1, W2, E, levels=8, zdir="z", offset=0, cmap="viridis", linewidths=1.0)
    ax1.scatter([0], [0], [0], color=RED, s=30)
    ax1.text(0.1, 0.1, 1.2, r"$\nabla E=0$", color=RED, fontsize=11)
    ax1.set_xlabel(r"$w_1$")
    ax1.set_ylabel(r"$w_2$")
    ax1.set_zlabel(r"$E(\mathbf{w})$")
    ax1.set_title("误差面：驻点处梯度为 0", fontsize=11.5)
    ax1.view_init(elev=28, azim=-125)

    # 右：等高线 + GD 轨迹（λ1=4, λ2=1, η=0.4）
    ax2 = fig.add_subplot(1, 2, 2)
    cs = ax2.contour(W1, W2, E, levels=10, cmap="viridis")
    ax2.clabel(cs, inline=True, fontsize=8)
    pts = [(2.0, 2.0)]
    for _ in range(6):
        a, b = pts[-1]
        pts.append((a - 0.4 * 4.0 * a, b - 0.4 * 1.0 * b))
    pts = np.array(pts)
    ax2.plot(pts[:, 0], pts[:, 1], "-o", color=RED, lw=1.8, ms=4,
             label=r"GD：$\eta=0.4$")
    ax2.scatter([0], [0], color=BLUE, s=36, zorder=6)
    ax2.text(0.08, 0.12, r"$w^\star$", color=BLUE, fontsize=12)
    ax2.text(0.55, 0.96, "陡方向 $w_1$：$\\lambda_{\\max}=4$", transform=ax2.transAxes,
             ha="center", va="top", fontsize=10, color=GRAY)
    ax2.text(0.55, 0.06, "平方向 $w_2$：$\\lambda_{\\min}=1$", transform=ax2.transAxes,
             ha="center", va="bottom", fontsize=10, color=GRAY)
    ax2.set_xlabel(r"$w_1$")
    ax2.set_ylabel(r"$w_2$")
    ax2.set_title("等高线是椭圆：陡方向来回抖，平方向走得慢", fontsize=11.5)
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.2)
    ax2.legend(loc="lower right", fontsize=9, frameon=False)

    fig.subplots_adjust(bottom=0.14, wspace=0.28)
    fig.text(0.5, 0.03, "误差面像地形图：梯度指上坡，负梯度指下坡；等高线越扁，越容易 zig-zag。",
             ha="center", fontsize=10.5, color=GRAY)
    save(fig, "fig_error_surface.png")


# --- 图 28：过拟合：M=1/3/9 的拟合与训练/测试误差 ---------------------------
def fig_overfit_M():
    import warnings

    rng = np.random.default_rng(4)
    x = np.linspace(0.0, 1.0, 10)
    t = np.sin(2 * np.pi * x) + rng.normal(0, 0.18, size=x.size)
    xs = np.linspace(0.0, 1.0, 400)
    true = np.sin(2 * np.pi * xs)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.4))
    ax1.scatter(x, t, color=GRAY, s=24, zorder=5, label="训练数据")
    ax1.plot(xs, true, ls="--", color=GRAY, lw=1.0, label=r"真实曲线 $\sin 2\pi x$")
    styles = {1: (BLUE, r"$M=1$：欠拟合"),
              3: (RED, r"$M=3$：合适"),
              9: (GREEN, r"$M=9$：过拟合")}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for M, (c, lab) in styles.items():
            coef = np.polyfit(x, t, M)
            ax1.plot(xs, np.polyval(coef, xs), color=c, lw=1.8, label=lab)
    ax1.set_ylim(-1.9, 2.7)
    ax1.set_xlabel("x")
    ax1.set_ylabel("t")
    ax1.set_title("同一批点，三种弯曲程度", fontsize=11.5)
    ax1.legend(fontsize=8.5, frameon=False, loc="lower left")
    ax1.grid(True, alpha=0.2)

    Ms = list(range(0, 10))
    train, test = [], []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for M in Ms:
            coef = np.polyfit(x, t, M)
            train.append(np.mean((np.polyval(coef, x) - t) ** 2))
            test.append(np.mean((np.polyval(coef, xs) - true) ** 2))
    ax2.semilogy(Ms, train, "-o", color=BLUE, ms=4, label="训练误差")
    ax2.semilogy(Ms, test, "-s", color=RED, ms=4, label="测试误差")
    ax2.set_ylim(1e-6, 1.0)
    ax2.set_xlabel(r"多项式阶数 $M$")
    ax2.set_ylabel("均方误差（对数轴）")
    ax2.set_title("训练误差一路降，测试误差先降后升", fontsize=11.5)
    ax2.legend(fontsize=9, frameon=False)
    ax2.grid(True, alpha=0.2, which="both")

    fig.subplots_adjust(bottom=0.2, wspace=0.25)
    fig.text(0.5, 0.03,
             "M 越大越能穿过训练点，但点与点之间开始乱摆——训练误差降、测试误差升，就是过拟合。",
             ha="center", fontsize=10.5, color=GRAY)
    save(fig, "fig_overfit_M.png")


# --- 图 29：激活函数与导数（饱和） -----------------------------------------
def fig_activation():
    a = np.linspace(-5.0, 5.0, 500)
    sig = 1.0 / (1.0 + np.exp(-a))
    th = np.tanh(a)
    relu = np.maximum(0.0, a)
    leaky = np.where(a < 0, 0.1 * a, a)
    soft = np.log1p(np.exp(a))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3))
    ax1.plot(a, sig, color=BLUE, lw=2.0, label=r"$\sigma$（sigmoid）")
    ax1.plot(a, th, color=RED, lw=2.0, label=r"$\tanh$")
    ax1.plot(a, relu, color=GREEN, lw=2.0, label="ReLU")
    ax1.plot(a, leaky, color=GRAY, lw=1.4, ls="--", label="leaky ReLU")
    ax1.plot(a, soft, color="#ff7f0e", lw=1.4, ls=":", label="softplus")
    ax1.axhline(0.0, color=GRAY, lw=0.8)
    ax1.axhline(1.0, color=GRAY, lw=0.8, ls=":")
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-1.6, 5.2)
    ax1.set_xlabel("a")
    ax1.set_ylabel("h(a)")
    ax1.set_title("激活函数：中段近似线性，两端压平", fontsize=11.5)
    ax1.legend(fontsize=8.5, frameon=False, loc="upper left")
    ax1.grid(True, alpha=0.2)

    ax2.plot(a, sig * (1 - sig), color=BLUE, lw=2.0, label=r"$\sigma'=\sigma(1-\sigma)$")
    ax2.plot(a, 1 - th ** 2, color=RED, lw=2.0, label=r"$\tanh'=1-\tanh^2$")
    ax2.plot(a, (a > 0).astype(float), color=GREEN, lw=1.6, label="ReLU'")
    ax2.plot(a, sig, color=GRAY, lw=1.2, ls="--", label=r"softplus$'=\sigma$")
    ax2.axvline(5, color=GRAY, lw=0.8, ls=":")
    ax2.text(2.6, 0.12, r"$\sigma'(5)\approx0.0067$", fontsize=9.5, color=BLUE)
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_xlabel("a")
    ax2.set_ylabel("h'(a)")
    ax2.set_title("导数：两端趋 0（饱和）", fontsize=11.5)
    ax2.legend(fontsize=8.5, frameon=False, loc="upper left")
    ax2.grid(True, alpha=0.2)

    fig.subplots_adjust(bottom=0.2, wspace=0.25)
    fig.text(0.5, 0.03,
             "饱和 = 曲线被压平 = 导数趋 0；反向传播每层都乘 h'，多层连乘就梯度消失。",
             ha="center", fontsize=10.5, color=GRAY)
    save(fig, "fig_activation.png")


# --- 图 30：SVD —— 单位圆 → 椭圆，右/左奇异向量两组正交方向 ----------------
def fig_svd():
    A = np.array([[2.0, 1.0], [0.0, 1.5]])
    U, S, Vt = np.linalg.svd(A)
    th = np.linspace(0, 2 * np.pi, 400)
    circle = np.vstack([np.cos(th), np.sin(th)])
    ellipse = A @ circle

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8))

    # 左：定义域的单位圆 + 右奇异向量 v1, v2
    axes[0].plot(circle[0], circle[1], color=GRAY, lw=1.6, ls="--",
                 label=r"单位圆 $\|\mathbf{x}\|=1$")
    for k, color, lab in [(0, RED, r"$\mathbf{v}_1$"),
                          (1, GREEN, r"$\mathbf{v}_2$")]:
        v = Vt.T[:, k]
        arrow(axes[0], *v, color, lw=2.4, label=lab)
    axes[0].set_title("定义域：$\\mathbf{v}_1\\perp\\mathbf{v}_2$", fontsize=11.5)

    # 右：像椭圆 + 左奇异向量 u1, u2（长度 = 奇异值）
    axes[1].plot(ellipse[0], ellipse[1], color=BLUE, lw=2.2,
                 label=r"像 $\mathbf{A}\mathbf{x}$")
    for k, color in [(0, RED), (1, GREEN)]:
        vec = U[:, k] * S[k]
        arrow(axes[1], *vec, color, lw=2.4)
        axes[1].text(vec[0] * 1.05 + 0.06, vec[1] * 1.05 + 0.06,
                     rf"$\sigma_{k + 1}\mathbf{{u}}_{k + 1}$",
                     color=color, fontsize=12)
        axes[1].plot([vec[0], vec[0]], [0, vec[1]], ls=":", color=GRAY, lw=0.9)
        axes[1].plot([0, vec[0]], [vec[1], vec[1]], ls=":", color=GRAY, lw=0.9)

    for ax in axes:
        ax.axhline(0, color=GRAY, lw=0.8)
        ax.axvline(0, color=GRAY, lw=0.8)
        ax.grid(True, alpha=0.2)
        ax.set_aspect("equal")
        ax.legend(loc="lower right", fontsize=9, frameon=False)
    axes[0].set_xlim(-1.5, 1.5)
    axes[0].set_ylim(-1.5, 1.5)
    axes[1].set_xlim(-2.8, 2.8)
    axes[1].set_ylim(-2.4, 2.4)
    fig.suptitle(r"SVD：$\mathbf{A}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$，"
                 "先把正交方向转好，再沿两个正交方向分别拉伸", y=1.03, fontsize=12.5)
    save(fig, "fig_svd.png")


# --- 图 31：图 Laplacian —— 星形图、L 矩阵、特征值 --------------------------
def fig_graph_laplacian():
    pos = {0: (0.0, 0.0), 1: (-1.15, 1.15), 2: (1.15, 1.15), 3: (0.0, -1.5)}
    edges = [(0, 1), (0, 2), (0, 3)]
    L = np.array([[3, -1, -1, -1],
                  [-1, 1, 0, 0],
                  [-1, 0, 1, 0],
                  [-1, 0, 0, 1]])

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3))

    ax = axes[0]
    for i, j in edges:
        ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]],
                color=GRAY, lw=2.2, zorder=1)
    for k, (x, y) in pos.items():
        ax.scatter([x], [y], s=520, color=BLUE if k == 0 else "#dbeafe",
                   edgecolor=BLUE, linewidth=2, zorder=2)
        ax.text(x, y, rf"$v_{k + 1}$", ha="center", va="center",
                fontsize=12, color="white" if k == 0 else BLUE, zorder=3)
    ax.set_title(r"星形图 $K_{1,3}$：中心 $v_1$ 连三个叶子", fontsize=11.5)
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.9, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")

    ax = axes[1]
    im = ax.imshow(L, cmap="RdBu_r", vmin=-3, vmax=3)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, str(L[i, j]), ha="center", va="center", fontsize=12,
                    color="white" if abs(L[i, j]) >= 2 else "black")
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels([rf"$v_{k + 1}$" for k in range(4)])
    ax.set_yticklabels([rf"$v_{k + 1}$" for k in range(4)])
    ax.set_title(r"$\mathbf{L}=\mathbf{D}-\mathbf{A}$：对角线是度数，边上是 $-1$", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[2]
    vals = [0, 1, 1, 4]
    colors = [GRAY, BLUE, BLUE, GREEN]
    ax.bar(range(4), vals, color=colors, width=0.62)
    for k, v in enumerate(vals):
        ax.text(k, v + 0.08, str(v), ha="center", fontsize=12)
    ax.annotate(r"$\lambda_2=1$（代数连通度）", xy=(1, 1), xytext=(1.2, 2.6),
                fontsize=10, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1))
    ax.annotate(r"$\lambda_{\max}=4$", xy=(3, 4), xytext=(2.2, 4.5),
                fontsize=10, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.set_xticks(range(4))
    ax.set_xticklabels([r"$\lambda_1$", r"$\lambda_2$", r"$\lambda_3$", r"$\lambda_4$"])
    ax.set_ylim(0, 5.2)
    ax.set_ylabel("特征值")
    ax.set_title("谱：一个 0（连通）+ 两个 1 + 一个 4", fontsize=11.5)
    ax.grid(True, axis="y", alpha=0.2)

    fig.suptitle("图 Laplacian：把“节点上的数”变成“邻居之间的差异”", y=1.03, fontsize=12.5)
    fig.subplots_adjust(wspace=0.35)
    save(fig, "fig_graph_laplacian.png")


# --- 图 32：计算图前向 / 反向（z=wx+b, L=(z-t)^2） ------------------------
def fig_computation_graph():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.6))
    nodes = {
        "w": (0.0, 3.2, "w=2"),
        "x": (0.0, 2.1, "x=3"),
        "b": (0.0, 1.0, "b=1"),
        "z": (2.3, 2.1, "z=wx+b=7"),
        "t": (2.3, 0.55, "t=5"),
        "L": (4.7, 1.5, "L=(z-t)^2=4"),
    }
    edges = [("w", "z"), ("x", "z"), ("b", "z"), ("z", "L"), ("t", "L")]

    def draw(ax, backward=False):
        for a, c in edges:
            x1, y1, _ = nodes[a]
            x2, y2, _ = nodes[c]
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", lw=2.0,
                                        color=(RED if backward else GRAY),
                                        linestyle=("-" if not backward else "--"),
                                        shrinkA=32, shrinkB=32))
        for key, (x, y, lab) in nodes.items():
            ax.text(x, y, lab, ha="center", va="center", fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.45",
                              fc=("#fde8e8" if backward else "#e8f0fe"),
                              ec=(RED if backward else BLUE), lw=1.8))

    draw(axes[0], backward=False)
    axes[0].set_title("① 前向：从输入算到损失", fontsize=12)
    axes[0].text(0.5, 0.02, "z = 2×3 + 1 = 7\nL = (7 − 5)² = 4",
                 transform=axes[0].transAxes, ha="center", fontsize=10.5, color=GRAY)

    draw(axes[1], backward=True)
    axes[1].text(1.25, 1.85, r"$\partial L/\partial z=4$", color=RED, fontsize=10.5)
    axes[1].text(0.62, 2.85, r"$\partial L/\partial w=12$", color=RED, fontsize=10.5)
    axes[1].text(0.62, 2.15, r"$\partial L/\partial x=8$", color=RED, fontsize=10.5)
    axes[1].text(0.62, 1.25, r"$\partial L/\partial b=4$", color=RED, fontsize=10.5)
    axes[1].text(3.65, 1.78, r"$\partial L/\partial L=1$", color=RED, fontsize=10.5)
    axes[1].set_title("② 反向：从损失把梯度传回去", fontsize=12)
    axes[1].text(0.5, 0.02,
                 r"$\partial L/\partial z=2(z-t)=4$；再乘 $\partial z/\partial w=x$ 得 12",
                 transform=axes[1].transAxes, ha="center", fontsize=10.5, color=GRAY)

    for ax in axes:
        ax.set_xlim(-1.0, 5.9)
        ax.set_ylim(-0.1, 4.0)
        ax.axis("off")
    fig.suptitle("计算图：前向存中间值，反向用链式法则逐个乘回来", y=1.02, fontsize=12.5)
    save(fig, "fig_computation_graph.png")


# --- 图 33：联合密度 → 切片 → 条件密度 ------------------------------------
def fig_joint_conditional():
    rho = 0.7
    x = np.linspace(-3.2, 3.2, 400)
    y = np.linspace(-3.2, 3.2, 400)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X ** 2 - 2 * rho * X * Y + Y ** 2) / (2 * (1 - rho ** 2)))
    Z /= (2 * np.pi * np.sqrt(1 - rho ** 2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.6))
    cs = ax1.contour(X, Y, Z, levels=8, colors=[BLUE], linewidths=1.3)
    ax1.clabel(cs, inline=True, fontsize=7)
    ax1.axvline(1.0, color=RED, lw=2.2, ls="--")
    ax1.text(1.08, 2.65, r"切片 $x=1$", color=RED, fontsize=11)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title("联合密度 $p(x,y)$：椭圆等高线", fontsize=11.5)
    ax1.set_aspect("equal")
    ax1.grid(True, alpha=0.2)

    mu = rho * 1.0
    sd = np.sqrt(1 - rho ** 2)
    cond = np.exp(-(y - mu) ** 2 / (2 * sd ** 2)) / (sd * np.sqrt(2 * np.pi))
    marg = np.exp(-y ** 2 / 2) / np.sqrt(2 * np.pi)
    ax2.plot(y, marg, color=GRAY, lw=2.0, ls="--", label=r"边缘 $p(y)$")
    ax2.plot(y, cond, color=RED, lw=2.6, label=r"条件 $p(y\mid x=1)$")
    ax2.axvline(mu, color=RED, lw=0.9, ls=":")
    ax2.text(mu + 0.08, cond.max() * 0.9, r"均值 $\rho x=0.7$", color=RED, fontsize=10.5)
    ax2.set_xlabel(r"$y$")
    ax2.set_ylabel("密度")
    ax2.set_title("条件密度：切片后再归一化", fontsize=11.5)
    ax2.legend(fontsize=9.5, frameon=False)
    ax2.grid(True, alpha=0.2)

    fig.suptitle("联合 → 固定 $x$ 切一刀 → 条件分布；把所有 $x$ 平均掉 → 边缘分布",
                 y=1.03, fontsize=11.5)
    save(fig, "fig_joint_conditional.png")


# --- 图 34：全期望 / 全方差 -------------------------------------------------
def fig_total_expectation_variance():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.4))

    # 左：两个条件分布 + 混合分布
    yy = np.linspace(-4, 7, 500)
    f0 = np.exp(-(yy - 0) ** 2 / 2) / np.sqrt(2 * np.pi)
    f1 = np.exp(-(yy - 3) ** 2 / 2) / np.sqrt(2 * np.pi)
    mix = 0.5 * f0 + 0.5 * f1
    ax1.plot(yy, f0, color=BLUE, lw=1.8, ls="--", label=r"$p(y\mid x=0)$")
    ax1.plot(yy, f1, color=GREEN, lw=1.8, ls="--", label=r"$p(y\mid x=1)$")
    ax1.plot(yy, mix, color=RED, lw=2.4, label=r"混合 $p(y)$")
    ax1.axvline(0, color=BLUE, lw=1.0, ls=":")
    ax1.axvline(3, color=GREEN, lw=1.0, ls=":")
    ax1.axvline(1.5, color=RED, lw=1.4, ls=":")
    ax1.text(0.05, 0.40, r"$E[Y\mid X{=}0]=0$", color=BLUE, fontsize=9.5)
    ax1.text(2.0, 0.40, r"$E[Y\mid X{=}1]=3$", color=GREEN, fontsize=9.5)
    ax1.text(1.55, 0.22, r"$E[Y]=1.5$", color=RED, fontsize=9.5)
    ax1.set_title("全期望：组内均值按权重平均", fontsize=11.5)
    ax1.set_xlabel(r"$y$")
    ax1.set_ylabel("密度")
    ax1.legend(fontsize=8.5, frameon=False, loc="upper right")
    ax1.grid(True, alpha=0.2)

    # 右：方差分解堆叠柱
    within = 1.0
    between = 2.25
    total = within + between
    ax2.bar([0], [within], width=0.45, color=BLUE, label=r"$E[\mathrm{Var}(Y\mid X)]=1$")
    ax2.bar([0], [between], bottom=[within], width=0.45, color=GREEN,
            label=r"$\mathrm{Var}(E[Y\mid X])=2.25$")
    ax2.text(0, within / 2, "组内\n1.00", ha="center", va="center", color="white", fontsize=10.5)
    ax2.text(0, within + between / 2, "组间\n2.25", ha="center", va="center", color="white", fontsize=10.5)
    ax2.text(0, total + 0.12, r"总方差 $=3.25$", ha="center", fontsize=11)
    ax2.set_xticks([0])
    ax2.set_xticklabels(["$\\mathrm{Var}(Y)$"])
    ax2.set_ylim(0, 3.9)
    ax2.set_ylabel("方差")
    ax2.set_title(r"全方差：$\mathrm{Var}(Y)=E[\mathrm{Var}(Y\mid X)]+\mathrm{Var}(E[Y\mid X])$",
                  fontsize=10.5)
    ax2.legend(fontsize=8.5, frameon=False, loc="upper right")
    ax2.grid(True, axis="y", alpha=0.2)

    fig.suptitle("全期望/全方差：先把组内算清楚，再按组间权重汇总", y=1.03, fontsize=12)
    save(fig, "fig_total_expectation_variance.png")


# --- 图 35：熵、交叉熵、KL --------------------------------------------------
def fig_entropy_kl():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.4))

    p = np.linspace(0.001, 0.999, 400)
    H = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    ax1.plot(p, H, color=BLUE, lw=2.4)
    ax1.scatter([0.5], [1.0], color=RED, s=40, zorder=5)
    ax1.annotate(r"$p=0.5$：$H=1$ bit（最不确定）", xy=(0.5, 1.0), xytext=(0.56, 0.82),
                 fontsize=10, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax1.set_xlabel(r"$p=P(X=1)$")
    ax1.set_ylabel(r"$H(p)$（bit）")
    ax1.set_title("伯努利熵：越接近 0.5 越不确定", fontsize=11.5)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1.08)
    ax1.grid(True, alpha=0.25)

    Hp = -(0.9 * np.log2(0.9) + 0.1 * np.log2(0.1))
    CE = -(0.9 * np.log2(0.5) + 0.1 * np.log2(0.5))
    KL = CE - Hp
    ax2.bar([0], [Hp], width=0.42, color=BLUE, label=r"$H(p)=0.469$")
    ax2.bar([0], [KL], bottom=[Hp], width=0.42, color=RED, label=r"$D(p\|q)=0.531$")
    ax2.text(0, Hp / 2, "H(p)", ha="center", va="center", color="white", fontsize=11)
    ax2.text(0, Hp + KL / 2, "KL", ha="center", va="center", color="white", fontsize=11)
    ax2.text(0, CE + 0.05, r"$H(p,q)=1$ bit", ha="center", fontsize=11)
    ax2.set_xticks([0])
    ax2.set_xticklabels([r"$p=(0.9,0.1)$, $q=(0.5,0.5)$"])
    ax2.set_ylim(0, 1.25)
    ax2.set_ylabel("bit")
    ax2.set_title(r"交叉熵 $=H(p)+D(p\|q)$", fontsize=11.5)
    ax2.legend(fontsize=9, frameon=False, loc="upper right")
    ax2.grid(True, axis="y", alpha=0.2)

    fig.suptitle("熵 = 自己的不确定；KL = 用错分布多付的代价；交叉熵 = 两者之和",
                 y=1.03, fontsize=11.5)
    save(fig, "fig_entropy_kl.png")


# --- 图 36：Fano 不等式：信息 → 误差下界 / 猜错时的候选集 ----------------
def fig_fano():
    from matplotlib.patches import Rectangle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.6))

    # 左：误差下界随 H(X|Y) 变化（弱化形式）
    for M, color, ls, lab in [(8, BLUE, "-", r"$|\mathcal{X}|=8$"),
                              (4, RED, "--", r"$|\mathcal{X}|=4$"),
                              (2, GREEN, ":", r"$|\mathcal{X}|=2$")]:
        hmax = np.log2(M)
        hh = np.linspace(0, hmax, 400)
        pe = np.maximum(0.0, (hh - 1.0) / hmax)
        ax1.plot(hh, pe, color=color, lw=2.2, ls=ls, label=lab)
    ax1.scatter([3.0], [2.0 / 3.0], color=RED, s=48, zorder=6)
    ax1.annotate(r"$H=3,\ |\mathcal{X}|=8$" + "\n" + r"$\Rightarrow P_e\geq 2/3$",
                 xy=(2.98, 2.0 / 3.0), xytext=(1.45, 0.70), fontsize=10.5, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax1.axhline(0.0, color=GRAY, lw=0.9)
    ax1.set_xlabel(r"$H(X\mid Y)$（bit）")
    ax1.set_ylabel(r"$P_e$ 的下界")
    ax1.set_title(r"$P_e\ \geq\ \frac{H(X\mid Y)-1}{\log_2|\mathcal{X}|}$", fontsize=12.5)
    ax1.set_xlim(0, 3.08)
    ax1.set_ylim(-0.03, 1.02)
    ax1.grid(True, alpha=0.25)
    ax1.legend(fontsize=9.5, frameon=False, loc="lower right")
    ax1.text(0.04, 0.93, r"$H(X\mid Y)\leq 1$ 时界为负 $\Rightarrow$ 不约束",
             transform=ax1.transAxes, fontsize=9.5, color=GRAY, va="top")

    # 右：猜错时还剩哪些候选（|X|-1 个）
    true_x, est = 3, 6
    for i in range(1, 9):
        col = i - 1
        if i == true_x:
            face, edge, lw = "#cfe3ff", BLUE, 2.4
        elif i == est:
            face, edge, lw = "#fde2e2", RED, 2.4
        else:
            face, edge, lw = "#eef2f7", GRAY, 1.6
        ax2.add_patch(Rectangle((col * 0.98, 1.05), 0.84, 0.72, facecolor=face,
                                edgecolor=edge, lw=lw))
        ax2.text(col * 0.98 + 0.42, 1.41, str(i), ha="center", va="center",
                 fontsize=13, color="#333333")
    ax2.annotate(r"真实 $X$", xy=(true_x * 0.98 + 0.42, 1.80), xytext=(0.55, 2.10),
                 fontsize=11, color=BLUE,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
    ax2.annotate(r"估计 $\hat{X}$", xy=(est * 0.98 + 0.42, 1.79), xytext=(5.15, 2.10),
                 fontsize=11, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax2.text(3.92, 0.62,
             r"猜错（$E=1$）：只知 $X\neq\hat{X}$ $\Rightarrow$ 还剩 $|\mathcal{X}|-1=7$ 个候选",
             ha="center", fontsize=10.5, color="#444444")
    ax2.text(3.92, 0.20,
             r"最坏情况是 7 个候选等可能：$H\leq\log_2 7\leq\log_2 8=3$ bit",
             ha="center", fontsize=10.5, color=GRAY)
    ax2.set_xlim(-0.15, 7.9)
    ax2.set_ylim(0.0, 2.35)
    ax2.axis("off")
    ax2.set_title("为什么是 $|\\mathcal{X}|-1$：错的时候排除了自己的答案", fontsize=12)

    fig.suptitle("Fano 不等式：看完 $Y$ 剩下的不确定，最多是「1 bit 的错/对」+「猜错时挑哪一个」",
                 y=1.04, fontsize=11.5)
    save(fig, "fig_fano.png")


# --- 图 37：MLE vs MAP：似然峰与后验峰 --------------------------------------
def fig_mle_map():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.4))

    n, k = 10, 7
    p = np.linspace(0.02, 0.98, 500)
    ll = k * np.log(p) + (n - k) * np.log(1 - p)
    ll -= ll.max()
    # Beta(2,2) prior: log p + log(1-p)
    lp = ll + np.log(p) + np.log(1 - p)
    lp -= lp.max()

    ax1.plot(p, ll, color=BLUE, lw=2.4, label=r"对数似然 $\ell(p)$")
    ax1.plot(p, lp, color=RED, lw=2.2, ls="--", label=r"对数后验（Beta(2,2) 先验）")
    ax1.axvline(k / n, color=BLUE, ls=":", lw=1.2)
    ax1.axvline((k + 1) / (n + 2), color=RED, ls=":", lw=1.2)
    ax1.scatter([k / n], [0], color=BLUE, s=40, zorder=6)
    ax1.scatter([(k + 1) / (n + 2)], [lp.max()], color=RED, s=40, zorder=6)
    ax1.annotate(r"MLE $=0.700$", xy=(k / n, 0), xytext=(0.74, -0.55),
                 fontsize=10, color=BLUE,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
    ax1.annotate(r"MAP $=0.667$", xy=((k + 1) / (n + 2), lp.max()),
                 xytext=(0.34, -0.35), fontsize=10, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax1.set_xlabel(r"$p$")
    ax1.set_ylabel("对数密度（已平移到峰值 0）")
    ax1.set_title("先验把峰往 0.5 拉：MAP 在 MLE 左边", fontsize=11.5)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-3.2, 0.35)
    ax1.grid(True, alpha=0.25)
    ax1.legend(fontsize=9, frameon=False, loc="lower left")

    vals = [k / n, (k + 1) / (n + 2), (k + 2) / (n + 4)]
    names = ["MLE", "MAP\n(Beta(2,2))", "后验均值\n(Beta(2,2))"]
    colors = [BLUE, RED, GREEN]
    bars = ax2.bar(names, vals, color=colors, width=0.55, alpha=0.85)
    for b, v in zip(bars, vals):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}",
                 ha="center", fontsize=11)
    ax2.axhline(0.5, color=GRAY, ls="--", lw=1.0)
    ax2.text(0.02, 0.52, r"先验均值 $0.5$", color=GRAY, fontsize=9.5, ha="left")
    ax2.set_ylim(0, 0.8)
    ax2.set_ylabel(r"对 $p$ 的估计")
    ax2.set_title("同一批数据：三种点估计，先验越强越靠近 0.5", fontsize=11.5)
    ax2.grid(True, axis="y", alpha=0.2)

    fig.suptitle(r"数据 $7$ 正 $3$ 负：MLE 只看数据，MAP 兼顾先验", y=1.03, fontsize=12)
    save(fig, "fig_mle_map.png")


# --- 图 38：Fisher 信息 = 对数似然的曲率；CRLB 随 n 收缩 ---------------------
def fig_fisher():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.4))

    th = np.linspace(-2.5, 2.5, 500)
    for I, color, lab in [(2, BLUE, r"$I=2$（平）"),
                          (8, RED, r"$I=8$（中）"),
                          (32, GREEN, r"$I=32$（尖）")]:
        ax1.plot(th, -0.5 * I * th ** 2, color=color, lw=2.4, label=lab)
        ax1.plot(th, -0.5 * I * th ** 2, color=color, lw=2.4)
    ax1.axhline(0, color=GRAY, lw=0.8)
    ax1.axvline(0, color=GRAY, lw=0.8)
    ax1.set_xlabel(r"$\theta-\hat\theta$")
    ax1.set_ylabel(r"$\ell(\theta)-\ell(\hat\theta)$")
    ax1.set_title("峰越尖 = 曲率越大 = Fisher 信息越大", fontsize=11.5)
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-12, 0.6)
    ax1.grid(True, alpha=0.25)
    ax1.legend(fontsize=9.5, frameon=False, loc="lower center")

    ns = np.arange(1, 101)
    I0 = 4.0  # Bernoulli, theta=0.5
    ax2.plot(ns, 1 / np.sqrt(ns * I0), color=BLUE, lw=2.4,
             label=r"CRLB 标准差 $1/\sqrt{nI(\theta)}$")
    ax2.scatter([10], [1 / np.sqrt(10 * I0)], color=RED, s=45, zorder=6)
    ax2.annotate(r"$n=10$：$1/\sqrt{40}=0.158$", xy=(10, 1 / np.sqrt(40)),
                 xytext=(18, 0.30), fontsize=10, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax2.set_xlabel(r"样本量 $n$")
    ax2.set_ylabel("标准差下界")
    ax2.set_title(r"数据越多，方差地板越低（$I(\theta)=4$）", fontsize=11.5)
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 0.55)
    ax2.grid(True, alpha=0.25)
    ax2.legend(fontsize=9.5, frameon=False, loc="upper right")

    fig.suptitle("Fisher 信息：不是「知道多少」，而是「数据对参数有多敏感」", y=1.03, fontsize=12)
    save(fig, "fig_fisher.png")


# --- 图 39：贝叶斯网络的三种三节点结构 --------------------------------------
def fig_bayes_net():
    from matplotlib.patches import Circle

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3))

    def node(ax, x, y, label, shaded=False):
        ax.add_patch(Circle((x, y), 0.30, facecolor=("#d9d9d9" if shaded else "white"),
                            edgecolor=(GRAY if shaded else BLUE), lw=2.2, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=14, zorder=4)

    def edge(ax, x1, y1, x2, y2, color=BLUE):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0,
                                    shrinkA=18, shrinkB=18), zorder=2)

    # 链
    ax = axes[0]
    node(ax, 0.0, 1.0, "A"); node(ax, 1.2, 1.0, "B"); node(ax, 2.4, 1.0, "C")
    edge(ax, 0.0, 1.0, 1.2, 1.0); edge(ax, 1.2, 1.0, 2.4, 1.0)
    ax.set_title("链 chain：A → B → C", fontsize=12)
    ax.text(1.2, 0.25, "B 未观测：通路开（A、C 相关）", ha="center", fontsize=9.5, color=RED)
    ax.text(1.2, -0.22, "B 观测：通路断（条件独立）", ha="center", fontsize=9.5, color=GREEN)

    # 叉
    ax = axes[1]
    node(ax, 1.2, 1.5, "B"); node(ax, 0.0, 0.5, "A"); node(ax, 2.4, 0.5, "C")
    edge(ax, 1.2, 1.5, 0.0, 0.5); edge(ax, 1.2, 1.5, 2.4, 0.5)
    ax.set_title("叉 fork：A ← B → C", fontsize=12)
    ax.text(1.2, -0.25, "B 未观测：通路开（A、C 相关）", ha="center", fontsize=9.5, color=RED)
    ax.text(1.2, -0.72, "B 观测：通路断（条件独立）", ha="center", fontsize=9.5, color=GREEN)

    # 碰撞
    ax = axes[2]
    node(ax, 0.0, 0.5, "A"); node(ax, 2.4, 0.5, "C"); node(ax, 1.2, 1.5, "B")
    edge(ax, 0.0, 0.5, 1.2, 1.5); edge(ax, 2.4, 0.5, 1.2, 1.5)
    ax.add_patch(Circle((1.2, 1.5), 0.30, facecolor="white", edgecolor=RED, lw=2.2, zorder=3))
    ax.text(1.2, 1.5, "B", ha="center", va="center", fontsize=14, zorder=4)
    ax.set_title("碰撞 collider：A → B ← C", fontsize=12)
    ax.text(1.2, -0.25, "B 未观测：通路断（A、C 独立）", ha="center", fontsize=9.5, color=GREEN)
    ax.text(1.2, -0.72, "B（或后代）观测：通路开（相关）", ha="center", fontsize=9.5, color=RED)

    for ax in axes:
        ax.set_xlim(-0.7, 3.1)
        ax.set_ylim(-0.95, 2.1)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("三节点结构：链/叉「观测中间就断」，碰撞「观测中间反而通」", y=1.03, fontsize=12.5)
    save(fig, "fig_bayes_net.png")


# --- 图 40：五个 Hint 的关系地图 --------------------------------------------
def fig_hint_map():
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(9.2, 4.6))

    def box(x, y, w, h, title, formula, color):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.06", facecolor="white",
                                    edgecolor=color, lw=2.0, zorder=3))
        ax.text(x, y + 0.28, title, ha="center", va="center", fontsize=11.5,
                color=color, zorder=4)
        ax.text(x, y - 0.22, formula, ha="center", va="center", fontsize=9.6,
                zorder=4)

    box(1.7, 3.35, 2.6, 1.05, "全期望（TLE）",
        r"$E[Y]=E[\,E[Y\mid X]\,]$", BLUE)
    box(5.0, 3.35, 2.6, 1.05, "全方差（TLV）",
        r"$\mathrm{Var}(Y)=E[\mathrm{Var}(Y\mid X)]$" + "\n" + r"$+\ \mathrm{Var}(E[Y\mid X])$", BLUE)
    ax.annotate("", xy=(3.68, 3.35), xytext=(3.02, 3.35),
                arrowprops=dict(arrowstyle="<|-|>", color=GREEN, lw=1.8), zorder=2)
    ax.text(3.35, 3.62, "同源", color=GREEN, fontsize=9.5, ha="center")

    box(1.55, 1.25, 2.5, 1.05, "Fisher 信息",
        r"$I(\theta)=E[(\partial_\theta\ln p)^2]$", RED)
    box(5.25, 1.25, 2.6, 1.05, "共轭先验",
        r"$p(\theta\mid y)\propto p(y\mid\theta)p(\theta)$", RED)
    ax.annotate("", xy=(3.92, 1.25), xytext=(2.83, 1.25),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8), zorder=2)
    ax.text(3.38, 1.60, "Jeffreys\n" + r"$p(\theta)\propto\sqrt{I(\theta)}$",
            color=RED, fontsize=8.8, ha="center")

    box(7.95, 2.30, 2.5, 1.05, "Fano 不等式",
        r"$P_e\geq\frac{H(X\mid Y)-1}{\log_2|\mathcal{X}|}$", "#7b3fa0")

    ax.set_xlim(0.15, 9.35)
    ax.set_ylim(0.45, 4.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("五个 Hint 一张图：左边两对同源，右边 Fano 独立", fontsize=12.5)
    fig.text(0.5, 0.02,
             "考场串法：TLE/TLV 常同一题；Conjugate 常与 Fisher（Jeffreys）连考；Fano 用条件熵直接套。",
             ha="center", fontsize=9.5, color=GRAY)
    save(fig, "fig_hint_map.png")


# --- 图 41：联合 → 条件 → 条件期望 ------------------------------------------
def fig_conditional_expectation():
    P = np.array([[0.30, 0.10, 0.10],
                  [0.05, 0.15, 0.30]])  # 行：X=0 雨、X=1 晴；列：Y=1,2,3
    cond = P / P.sum(axis=1, keepdims=True)
    ey = cond @ np.array([1, 2, 3])
    eY = float(P.sum(axis=0) @ np.array([1, 2, 3]))

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.4))

    # 左：联合分布热图
    ax = axes[0]
    im = ax.imshow(P, cmap="Blues", vmin=0, vmax=0.35)
    for i in range(2):
        for j in range(3):
            ax.text(j, i, f"{P[i, j]:.2f}", ha="center", va="center",
                    fontsize=13, color=("white" if P[i, j] > 0.22 else "#1f2937"))
    ax.set_xticks(range(3)); ax.set_xticklabels([r"$Y=1$", r"$Y=2$", r"$Y=3$"])
    ax.set_yticks(range(2)); ax.set_yticklabels([r"$X=0$ 雨", r"$X=1$ 晴"])
    ax.set_title("① 联合分布 $P(X,Y)$：每个格子是一个概率", fontsize=11.5)

    # 中：条件分布（行归一化）
    ax = axes[1]
    idx = np.arange(3)
    ax.bar(idx - 0.19, cond[0], width=0.36, color=BLUE, label=r"$P(Y\mid X=0)$")
    ax.bar(idx + 0.19, cond[1], width=0.36, color=RED, label=r"$P(Y\mid X=1)$")
    for i in range(3):
        ax.text(i - 0.19, cond[0, i] + 0.02, f"{cond[0, i]:.2f}", ha="center", fontsize=8.5)
        ax.text(i + 0.19, cond[1, i] + 0.02, f"{cond[1, i]:.2f}", ha="center", fontsize=8.5)
    ax.set_xticks(idx); ax.set_xticklabels([r"$Y=1$", r"$Y=2$", r"$Y=3$"])
    ax.set_ylim(0, 0.75)
    ax.set_ylabel("条件概率")
    ax.set_title("② 条件分布：每行除以行和（重新归一化）", fontsize=11.5)
    ax.legend(fontsize=9, frameon=False)
    ax.grid(True, axis="y", alpha=0.2)

    # 右：条件期望是 x 的函数
    ax = axes[2]
    ax.plot([0, 1], ey, "-o", color=GREEN, lw=2.4, ms=8, zorder=5,
            label=r"$E[Y\mid X=x]$")
    ax.axhline(eY, color=GRAY, ls="--", lw=1.4,
               label=r"$E[Y]=2.05$（加权平均）")
    ax.scatter([0.5], [eY], color=GRAY, s=45, zorder=6)
    ax.annotate(r"$1.6$", xy=(0, ey[0]), xytext=(0.05, 1.35), fontsize=11, color=GREEN)
    ax.annotate(r"$2.5$", xy=(1, ey[1]), xytext=(0.78, 2.65), fontsize=11, color=GREEN)
    ax.text(0.5, 1.78, r"$E[Y]=0.5\times1.6+0.5\times2.5$", ha="center", fontsize=10, color=GRAY)
    ax.set_xticks([0, 1]); ax.set_xticklabels([r"$X=0$ 雨", r"$X=1$ 晴"])
    ax.set_xlim(-0.25, 1.25)
    ax.set_ylim(1.2, 2.8)
    ax.set_ylabel(r"$Y$ 的条件均值")
    ax.set_title("③ $E[Y\\mid X]$ 是随机变量：随 $X$ 变，均值回到 $E[Y]$", fontsize=11.5)
    ax.legend(fontsize=9, frameon=False, loc="lower right")
    ax.grid(True, alpha=0.2)

    fig.suptitle("联合 → 条件 → 条件期望：先用 $X$ 切一刀，再在切片里求平均", y=1.04, fontsize=12.5)
    save(fig, "fig_conditional_expectation.png")


if __name__ == "__main__":
    fig_vector()
    fig_inner()
    fig_norms()
    fig_distance()
    fig_cosine()
    fig_matrix()
    fig_transpose()
    fig_inverse()
    fig_determinant()
    fig_span()
    fig_independence()
    fig_det_columns()
    fig_orthogonality()
    fig_projection_line()
    fig_projection_subspace()
    fig_eigen()
    fig_spectral_steps()
    fig_svd()
    fig_graph_laplacian()
    fig_computation_graph()
    fig_joint_conditional()
    fig_total_expectation_variance()
    fig_entropy_kl()
    fig_fano()
    fig_mle_map()
    fig_fisher()
    fig_bayes_net()
    fig_hint_map()
    fig_conditional_expectation()
    fig_quadratic_contours()
    fig_gradient_contour()
    fig_taylor_parabola()
    fig_prob_rules()
    fig_overfit_M()
    fig_activation()
    print("全部完成 ->", os.path.relpath(OUT, ROOT))
