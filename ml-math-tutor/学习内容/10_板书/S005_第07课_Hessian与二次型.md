# 板书 · S005 · 第 07 课：Hessian 与二次型（Hessian & quadratic forms）

- 会话ID：`S005`
- 日期：2026-10-27
- 对应：L07 / M2
- 修订记录：（初版）2026-10-27；（v2）2026-10-27 修 7.2 例：原来把公式拆成两行写在行内 `$...$` 里，导致渲染成乱码，改为独立公式块，并把「12 与 21 位相同」改成「第 1 行第 2 列 = 第 2 行第 1 列」

---

## 0. 生活化引入

走到一个“看起来平”的地方，一阶导数为 $0$——但你分不清是**谷底**、**山顶**，还是**山口（马鞍）**。
要分清，只能蹲下来摸摸“**往两边弯不弯、往哪边弯**”。这就是**二阶导 / Hessian（海森矩阵）**。

---

## 1. 直觉

| 对象 | 一句话 | 比作 |
|---|---|---|
| 梯度 $\nabla f$ | 往哪走最陡 | 坡度、方向 |
| Hessian $\mathbf{H}$ | 每个方向“弯多少、朝哪弯” | 曲率、碗还是鞍 |

- $\mathbf{H}$ **正定** ⇒ 每个方向都向上弯 ⇒ **碗** ⇒ 局部最小。
- $\mathbf{H}$ **负定** ⇒ 每个方向都向下弯 ⇒ **倒扣的碗** ⇒ 局部最大。
- $\mathbf{H}$ **不定** ⇒ 有的方向向上、有的向下 ⇒ **马鞍** ⇒ 驻点但不是极值。

---

## 2. 几何

![二次型等高线：碗 / 鞍 / 谷](图片/fig_quadratic_contours.png)

**看图**（这张图 L05 用过，现在换个角度读）：

- ① 椭圆等高线 + 特征值 $3,1$ 全正 ⇒ $\mathbf{H}$ 正定 ⇒ 原点**最低**。
- ② 双曲线等高线 + 特征值 $3,-1$ 一正一负 ⇒ $\mathbf{H}$ **不定** ⇒ 原点**马鞍点**。
- ③ 平行直线 + 特征值 $2,0$ ⇒ **半正定** ⇒ 有一条“平的谷底”，不是严格极小。

> 一句话：**梯度和为 0 只找到“驻点”，Hessian 才能告诉你那是碗、鞍还是顶。**

---

## 3. 计算（公式卡片）

### 7.1 二阶偏导（second partial derivative）

$$
\frac{\partial^2 f}{\partial x_i\partial x_j}
=\frac{\partial}{\partial x_i}\left(\frac{\partial f}{\partial x_j}\right)
$$

- **符号**：先对 $x_j$ 求偏导，再对 $x_i$ 求；$i\ne j$ 时叫**混合偏导（mixed partial）**；结果是一个数。
- **例**：$f(x,y)=x^2y+3xy^2$。$f_x=2xy+3y^2$，再对 $y$ 求：$f_{xy}=2x+6y$；
  另一条路 $f_y=x^2+6xy$，再对 $x$ 求：$f_{yx}=2x+6y$。**两条路一样**。

### 7.2 Hessian 矩阵（Hessian matrix）

$$
\mathbf{H}(\mathbf{x})=\begin{bmatrix}
\dfrac{\partial^2 f}{\partial x_1^2} & \cdots & \dfrac{\partial^2 f}{\partial x_1\partial x_n}\\
\vdots & \ddots & \vdots\\
\dfrac{\partial^2 f}{\partial x_n\partial x_1} & \cdots & \dfrac{\partial^2 f}{\partial x_n^2}
\end{bmatrix},
\qquad
\mathbf{H}=\mathbf{H}^\top
$$

- **符号**：$\mathbf{H}$ 是 $n\times n$ **对称**矩阵（因为 $f_{x_ix_j}=f_{x_jx_i}$，Schwarz 定理）；第 $(i,j)$ 元 = 先对 $x_j$ 再对 $x_i$。
- **例**：上面的 $f$：

$$
\mathbf{H}=\begin{bmatrix}f_{xx}&f_{xy}\\f_{yx}&f_{yy}\end{bmatrix}
=\begin{bmatrix}2y&2x+6y\\2x+6y&6x\end{bmatrix}
$$

  明显对称（第 1 行第 2 列 = 第 2 行第 1 列，都是 $2x+6y$）。

### 7.3 二次型的梯度（gradient of a quadratic form）

$$
f(\mathbf{x})=\mathbf{x}^\top\mathbf{A}\mathbf{x}
\quad\Longrightarrow\quad
\nabla f=(\mathbf{A}+\mathbf{A}^\top)\mathbf{x}
$$

- **符号**：$\mathbf{A}$ 是 $n\times n$（**不必对称**）；$\nabla f$ 是 $n\times1$；若 $\mathbf{A}=\mathbf{A}^\top$ 则化简为 $2\mathbf{A}\mathbf{x}$。
- **例**：$\mathbf{A}=\begin{bmatrix}1&2\\3&4\end{bmatrix}$（不对称）、$\mathbf{x}=(1,1)^\top$。
  $\mathbf{A}+\mathbf{A}^\top=\begin{bmatrix}2&5\\5&8\end{bmatrix}$ ⇒ $\nabla f=(7,13)^\top$。
  直接展开 $f=x_1^2+5x_1x_2+4x_2^2$：$f_{x_1}=2x_1+5x_2=7$，$f_{x_2}=5x_1+8x_2=13$ ✓

### 7.4 二次型的 Hessian

$$
f(\mathbf{x})=\mathbf{x}^\top\mathbf{A}\mathbf{x}
\quad\Longrightarrow\quad
\mathbf{H}=\mathbf{A}+\mathbf{A}^\top;
\qquad
\mathbf{A}=\mathbf{A}^\top\ \Rightarrow\ \mathbf{H}=2\mathbf{A}
$$

- **符号**：梯度是**线性**的，再求一次导就回到常数矩阵；$\mathbf{H}$ 一定对称。
- **例**：上例 $\mathbf{H}=\begin{bmatrix}2&5\\5&8\end{bmatrix}$。直接算 $f_{x_1x_1}=2$、$f_{x_1x_2}=5$、$f_{x_2x_2}=8$ ✓

### 7.5 最小二乘目标的梯度与 Hessian

$$
J(\mathbf{w})=\tfrac12\|\mathbf{X}\mathbf{w}-\mathbf{y}\|^2
\quad\Longrightarrow\quad
\nabla J=\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y}),
\qquad
\mathbf{H}_J=\mathbf{X}^\top\mathbf{X}
$$

- **符号**：$\mathbf{X}\in\mathbb{R}^{m\times n}$、$\mathbf{w}\in\mathbb{R}^{n\times1}$；$\mathbf{X}^\top\mathbf{X}$ 是 $n\times n$ **对称半正定**；加正则后 $\mathbf{H}=\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I}$ 正定（$\lambda>0$）。
- **例**：$\mathbf{X}=\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix}$，$\mathbf{X}^\top\mathbf{X}=\begin{bmatrix}3&3\\3&5\end{bmatrix}$，
  $\mathbf{H}=\begin{bmatrix}3&3\\3&5\end{bmatrix}$，$\operatorname{tr}=8$、$\det=6>0$ ⇒ 正定。

### 7.6 驻点分类（second-order test）

$$
\nabla f(\mathbf{x}_0)=\mathbf{0}
\ \Longrightarrow\
\begin{cases}
\mathbf{H}\succ\mathbf{0} & \text{局部最小（local min）}\\
\mathbf{H}\prec\mathbf{0} & \text{局部最大（local max）}\\
\mathbf{H}\ \text{不定} & \text{鞍点（saddle）}\\
\mathbf{H}\ \text{半定} & \text{判不了，需更高阶}
\end{cases}
$$

- **符号**：$\succ\mathbf{0}$ 读作“正定”（$\lambda_i>0$）；前提是 $\mathbf{H}$ 对称——这总成立。
- **例**：$f=x^2+2xy+3y^2$，$\mathbf{H}=\begin{bmatrix}2&2\\2&6\end{bmatrix}$，$\lambda=4\pm2\sqrt2\approx6.83,\,1.17>0$ ⇒ 最小。

### 7.7 二阶判别法（$2\times2$ 版本，考试最快）

$$
\det\mathbf{H}=f_{xx}f_{yy}-f_{xy}^2
$$

- **符号**：$\det\mathbf{H}=\lambda_1\lambda_2$，$f_{xx}$ 与 $\lambda_1\lambda_2$ 的符号一起决定类型。
- **例**：

| $\det\mathbf{H}$ | $f_{xx}$ | 结论 |
|---|---|---|
| $>0$ | $>0$ | 局部最小 |
| $>0$ | $<0$ | 局部最大 |
| $<0$ | 任意 | 鞍点 |
| $=0$ | 任意 | 失效 |

---

## 4. 完整手算

**Example.** Let $\mathbf{X}=\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix}$，$\mathbf{y}=\begin{bmatrix}1\\2\\2\end{bmatrix}$，
$J(\mathbf{w})=\tfrac12\|\mathbf{X}\mathbf{w}-\mathbf{y}\|^2+\tfrac{\lambda}{2}\|\mathbf{w}\|^2$（取 $\lambda=0$）。
Find $\nabla J$、$\mathbf{H}_J$，判其正定性，并求驻点。

1. 先算两个“零件”：

$$
\mathbf{X}^\top\mathbf{X}
=\begin{bmatrix}1&1&1\\0&1&2\end{bmatrix}\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix}
=\begin{bmatrix}3&3\\3&5\end{bmatrix},
\qquad
\mathbf{X}^\top\mathbf{y}
=\begin{bmatrix}1&1&1\\0&1&2\end{bmatrix}\begin{bmatrix}1\\2\\2\end{bmatrix}
=\begin{bmatrix}5\\6\end{bmatrix}
$$

2. 梯度：

$$
\nabla J=\mathbf{X}^\top\mathbf{X}\mathbf{w}-\mathbf{X}^\top\mathbf{y}
=\begin{bmatrix}3w_1+3w_2-5\\3w_1+5w_2-6\end{bmatrix}
\in\mathbb{R}^{2\times1}\ \checkmark
$$

3. Hessian：

$$
\mathbf{H}_J=\mathbf{X}^\top\mathbf{X}=\begin{bmatrix}3&3\\3&5\end{bmatrix}
\quad(\text{对称}\ \checkmark)
$$

4. 正定性：$\operatorname{tr}=8>0$，$\det=15-9=6>0$ ⇒ 两个特征值同号且和为正 ⇒ 都正 ⇒ **正定**。

$$
\lambda=\frac{8\pm\sqrt{64-24}}{2}=\frac{8\pm\sqrt{40}}{2}=4\pm\sqrt{10}\approx7.16,\ 0.84
$$

5. 驻点（$\nabla J=\mathbf{0}$）：

$$
\begin{cases}3w_1+3w_2=5\\3w_1+5w_2=6\end{cases}
\ \Rightarrow\
w_2=\tfrac12,\quad w_1=\tfrac{7}{6}
$$

6. 结论：$\mathbf{H}$ 正定 ⇒ 这个驻点是**唯一的全局最小**（凸二次函数，只有一个碗底）。

> 中文：这题就是 HW1 Q4 的骨架——“$\nabla$ 写成 $n\times1$，$\mathbf{H}$ 写成 $n\times n$ 且对称”，
> 再用 $\operatorname{tr}$/$\det$ 或特征值判正定。

---

## 5. 独立复现（先自己写，答案见第 9 节）

**Exercise.** $f(x,y)=x^3-3xy+y^2$。求所有驻点，并用 $\mathbf{H}$ 分类。

---

## 6. 易错点

1. **Hessian 不是“梯度的梯度”向量，而是 $n\times n$ 矩阵**；写成一列 $n$ 个数就错了。
2. **$\nabla(\mathbf{x}^\top\mathbf{A}\mathbf{x})=2\mathbf{A}\mathbf{x}$ 只在 $\mathbf{A}$ 对称时成立**；一般情形是 $(\mathbf{A}+\mathbf{A}^\top)\mathbf{x}$。
3. **$\nabla f=\mathbf{0}$ 不能直接说是最小**。$f=x^2-y^2$ 在原点梯度为 $0$，但 $\mathbf{H}=\operatorname{diag}(2,-2)$ 不定 ⇒ 鞍点。
4. **$\det\mathbf{H}<0$ 是鞍点，不是最大**。最大要求 $\det>0$ 且 $f_{xx}<0$。

---

## 7. 与已学关系

L05 的“正定”原来只是一个矩阵性质，现在有了归宿：**Hessian 正定 ⇔ 局部最小**。
L06 的梯度是一阶信息（往哪走），本课的 Hessian 是二阶信息（走一步会怎样变）；L08 的二阶 Taylor 把两者拼成一条公式。

---

## 8. 作业

**Q1 (concept).** True or false? One line why.

(a) For a twice continuously differentiable $f$, the Hessian is symmetric.
(b) If $\mathbf{H}$ is positive definite at a stationary point, that point is a local minimum.
(c) In 2D, $\det\mathbf{H}<0$ at a stationary point means a local maximum.
(d) For symmetric $\mathbf{A}$, $\nabla(\mathbf{x}^\top\mathbf{A}\mathbf{x})=2\mathbf{A}\mathbf{x}$ and $\mathbf{H}=2\mathbf{A}$.
(e) If $\mathbf{H}=\mathbf{0}$ at a stationary point, the point is neither a max nor a min.

**Q2 (compute).** Find $\nabla f$ and $\mathbf{H}$; state shapes.

(a) $f(x,y)=x^2y+3xy^2$
(b) $f(\mathbf{x})=3x_1^2+2x_1x_2+x_2^2$
(c) $f(\mathbf{x})=x_1^2+2x_2^2+3x_3^2+x_1x_2$

**Q3 (classify).** At a stationary point the Hessian is

(i) $\begin{bmatrix}2&1\\1&2\end{bmatrix}$，(ii) $\begin{bmatrix}-2&1\\1&-2\end{bmatrix}$，(iii) $\begin{bmatrix}1&3\\3&1\end{bmatrix}$。

Classify each as min / max / saddle. (Eigenvalues or $\operatorname{tr}$/$\det$ both fine.)

**Q4 (ML).** $J(\mathbf{w})=\tfrac12\|\mathbf{X}\mathbf{w}-\mathbf{y}\|^2+\tfrac{\lambda}{2}\|\mathbf{w}\|^2$，$\mathbf{X}\in\mathbb{R}^{m\times n}$。

(a) Write $\nabla J$ and $\mathbf{H}_J$; give shapes.
(b) Explain why $\mathbf{H}_J$ is positive definite when $\lambda>0$.
(c) For $\mathbf{X}^\top\mathbf{X}=\begin{bmatrix}3&3\\3&5\end{bmatrix}$、$\lambda=0$，compute the eigenvalues of $\mathbf{H}_J$ and the condition number $\kappa=\lambda_{\max}/\lambda_{\min}$.

---

## 9. 作业答案（先做完再看）

**A1.**

(a) True. Mixed partials commute (Schwarz), so $h_{ij}=h_{ji}$.
(b) True. Positive curvature in every direction ⇒ strict local minimum.
(c) False. $\det\mathbf{H}<0$ ⇒ one eigenvalue positive, one negative ⇒ **saddle**.
(d) True. $\mathbf{A}+\mathbf{A}^\top=2\mathbf{A}$ when symmetric.
(e) False. It is **undetermined** by the second-order test; you need higher-order terms (e.g. $f=x^4$ at $0$ is a min with $\mathbf{H}=0$).

**A2.**

(a) $\nabla f=\begin{bmatrix}2xy+3y^2\\x^2+6xy\end{bmatrix}$，$2\times1$；

$$
\mathbf{H}=\begin{bmatrix}2y&2x+6y\\2x+6y&6x\end{bmatrix},\quad 2\times2\ \checkmark
$$

(b) $\nabla f=\begin{bmatrix}6x_1+2x_2\\2x_1+2x_2\end{bmatrix}$，$2\times1$；$\mathbf{H}=\begin{bmatrix}6&2\\2&2\end{bmatrix}$。
$\det=12-4=8>0$、$f_{xx}=6>0$ ⇒ 正定（处处）。
(c) $\nabla f=\begin{bmatrix}2x_1+x_2\\4x_2+x_1\\6x_3\end{bmatrix}$，$3\times1$；

$$
\mathbf{H}=\begin{bmatrix}2&1&0\\1&4&0\\0&0&6\end{bmatrix},\quad 3\times3\ \checkmark
$$

**A3.**

(i) $\operatorname{tr}=4$、$\det=3$ ⇒ $\lambda=3,1>0$ ⇒ **min**。
(ii) $\operatorname{tr}=-4$、$\det=3$ ⇒ $\lambda=-1,-3<0$ ⇒ **max**。
(iii) $\operatorname{tr}=2$、$\det=1-9=-8<0$ ⇒ 异号 ⇒ **saddle**。

**A4.**

(a)

$$
\nabla J=\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y})+\lambda\mathbf{w}\in\mathbb{R}^{n\times1},
\qquad
\mathbf{H}_J=\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I}\in\mathbb{R}^{n\times n}
$$

(b) 对任意 $\mathbf{w}\ne\mathbf{0}$：

$$
\mathbf{w}^\top\mathbf{H}_J\mathbf{w}=\|\mathbf{X}\mathbf{w}\|^2+\lambda\|\mathbf{w}\|^2>0
$$

因为 $\lambda>0$ 且 $\|\mathbf{w}\|^2>0$（第一项 $\ge0$ 不破坏）⇒ 正定 ⇒ 唯一全局最小。

(c) $\operatorname{tr}=8$、$\det=6$ ⇒

$$
\lambda=\frac{8\pm\sqrt{64-24}}{2}=4\pm\sqrt{10}\approx7.16,\ 0.84,
\qquad
\kappa=\frac{4+\sqrt{10}}{4-\sqrt{10}}\approx8.5
$$

**A5（第 5 节独立复现）.**

$\nabla f=(3x^2-3y,\ -3x+2y)$。令其为零：$y=x^2$ 且 $-3x+2x^2=0$ ⇒ $x=0$ 或 $x=\tfrac32$。

驻点：$(0,0)$ 与 $\left(\tfrac32,\tfrac94\right)$。

$$
\mathbf{H}=\begin{bmatrix}6x&-3\\-3&2\end{bmatrix}
$$

- $(0,0)$：$\mathbf{H}=\begin{bmatrix}0&-3\\-3&2\end{bmatrix}$，$\det=0-9=-9<0$ ⇒ **鞍点**。
- $\left(\tfrac32,\tfrac94\right)$：$\mathbf{H}=\begin{bmatrix}9&-3\\-3&2\end{bmatrix}$，$\det=18-9=9>0$、$f_{xx}=9>0$ ⇒ **局部最小**。
