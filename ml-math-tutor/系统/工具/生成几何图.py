#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 ml-math-tutor 板书用的几何示意图（matplotlib，输出 PNG）。

用法（在 ml-math-tutor 目录内）：
    python3 系统/工具/生成几何图.py

输出目录：学习内容/10_板书/图片/
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
OUT = os.path.join(ROOT, "学习内容", "10_板书", "图片")
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
    fig_quadratic_contours()
    fig_gradient_contour()
    fig_taylor_parabola()
    print("全部完成 ->", os.path.relpath(OUT, ROOT))
