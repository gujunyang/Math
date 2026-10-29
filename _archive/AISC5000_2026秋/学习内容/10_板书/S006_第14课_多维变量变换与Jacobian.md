# 板书 · S006 · 第 14 课：多维变量变换与 Jacobian

- 覆盖：原 L14｜公告依据：Ch2 §2.4；"Questions will be similar in style and difficulty to the homework problems."
- 会话批次：批 A（第 14–18 课）｜日期：2026-10-28｜修订记录：（初版）2026-10-28；v2 2026-10-28：审核修正 + 公式卡例细化（三段式，数字与 §4/§5 去重）

## 0. 生活化引入
把一张 A4 世界地图按"长 2 倍、宽 3 倍"拉伸，面积变成 6 倍，颜色被摊薄。
二维换坐标时，密度也要按"面积放大几倍"来折算——这就是 $|\det J|$。

## 1. 直觉
一维看区间长度被拉伸几倍；二维看**面积**被拉伸几倍。
概率是"质量"，换坐标不增不减；面积变大，密度就必须变小。

## 2. 几何
![一维的拉伸：同一块概率质量换坐标](图片/fig_change_of_vars.png)

**看图**：一维阴影面积不变、宽度变了，所以高度要反向变。
二维把"宽度"换成"面积"：单位正方形 $\to$ $2\times3$ 矩形，面积 $\times6$，密度 $\div6$。

## 3. 计算（公式卡片）
### 14.1 雅可比矩阵（Jacobian matrix）
$$
J=\frac{\partial\mathbf x}{\partial\mathbf y^\top}=
\begin{bmatrix}
\partial x_1/\partial y_1 & \partial x_1/\partial y_2\\
\partial x_2/\partial y_1 & \partial x_2/\partial y_2
\end{bmatrix}
$$
- **符号**：$\mathbf x=g(\mathbf y)$ 是新坐标到旧坐标的映射；$J$ 是 $D\times D$ 矩阵，第 $i$ 行第 $j$ 列 = $x_i$ 对 $y_j$ 的偏导。
- **意义与场景**：它是一张"局部换算表"——$y$ 动一点点，$x$ 各方向各动多少。做坐标变换（缩放、旋转、归一化）时先写它。
- **例（生活版）**：
  - **背景与题干**：把单位正方形地毯按 $x_1=2y_1+y_2$、$x_2=4y_2$ 拉伸；求 Jacobian 矩阵 $J$。
  - **解**：Step 1 $\partial x_1/\partial y_1=2$、$\partial x_1/\partial y_2=1$；Step 2 $\partial x_2/\partial y_1=0$、$\partial x_2/\partial y_2=4$；Step 3 拼成 $J=\begin{bmatrix}2&1\\0&4\end{bmatrix}$。
  - **解读**：上三角说明 $x_2$ 不受 $y_1$ 影响；非对角 $1$ 表示 $y_2$ 也会改 $x_1$。
### 14.2 体积元与行列式（volume element）
$$
\mathrm{Vol}(\Delta\mathbf x)\approx|\det J|\;\mathrm{Vol}(\Delta\mathbf y)
$$
- **符号**：$\Delta\mathbf y$ 是 $y$ 空间的小方块；$\Delta\mathbf x$ 是它被映射后的形状；$|\det J|$ 是面积/体积的放大倍数。
- **意义与场景**：行列式就是"面积尺子"。$\det J=2$ 表示面积变 2 倍；$\det J<0$ 只说明方向翻了，面积仍取正。
- **例（生活版）**：
  - **背景与题干**：同一变换 $x_1=2y_1+y_2,\ x_2=4y_2$；求面积放大倍数，并算 $1\,\mathrm{cm}^2$ 的新面积。
  - **解**：Step 1 $\det J=2\times4-1\times0=8$；Step 2 $|\det J|=8$；Step 3 $1\,\mathrm{cm}^2\to8\,\mathrm{cm}^2$。
  - **解读**：行列式就是“面积尺”；$\det<0$ 只说明方向翻转，面积仍取绝对值。
### 14.3 多维密度变换（change of variables in $\mathbb R^D$）
$$
p_Y(\mathbf y)=p_X\big(g(\mathbf y)\big)\,|\det J|,
\qquad J=\frac{\partial\mathbf x}{\partial\mathbf y^\top}
$$
- **符号**：$p_X$ 是旧密度；$p_Y$ 是新密度；$g(\mathbf y)$ 把新坐标送回旧坐标；$|\det J|$ 是面积折算率。
- **意义与场景**：和汇率一样：同样的钱（概率），换成"面积更小的币种"（坐标），每单位面值就变大。二维 Gaussian 做线性变换仍是 Gaussian，就是它在撑腰。
- **例（生活版）**：
  - **背景与题干**：大图（$x$ 空间）浓度 $0.125/\mathrm{cm}^2$、总质量 $1$；小图面积只有它的 $1/8$，求小图浓度。
  - **解**：Step 1 $|\det J|=8$；Step 2 $p_Y=p_X\cdot|\det J|=0.125\times8=1.0/\mathrm{cm}^2$；Step 3 验证 $1.0\times\frac18=0.125$，概率质量守恒。
  - **解读**：面积缩小、浓度变大；密度不是概率，可以大于 $1$。

## 4. 完整手算
**Example.** Let $x_1=2y_1,\ x_2=3y_2$, and let $\mathbf X$ be uniform on $[0,2]\times[0,3]$. Find $p_Y$.
1. **Range.** $0<x_1<2,\ 0<x_2<3\Rightarrow 0<y_1<1,\ 0<y_2<1$.
2. **Jacobian.** $J=\begin{bmatrix}2&0\\0&3\end{bmatrix}$, so $|\det J|=6$.
3. **Old density.** Area $=2\times3=6$, uniform $\Rightarrow p_X=1/6$.
4. **Transform.** $p_Y=p_X\cdot|\det J|=\frac16\cdot6=1$ on the unit square.
5. **Check.** $\int_0^1\int_0^1 1\,dy_1dy_2=1$ ✓

面积放大 6 倍、密度缩小 6 倍，正好抵消；所以新密度是常数 1。

## 5. 独立复现
**Exercise.** $x_1=y_1,\ x_2=2y_2$, $\mathbf X$ uniform on the unit square. Find $p_Y$ and verify it integrates to 1.

## 6. 易错点
1. 用了 $\partial\mathbf y/\partial\mathbf x$ 的行列式，却忘了它是 $J$ 的倒数。
2. 忘记绝对值：$\det J<0$ 时密度会变负。
3. 变换后没重算支撑域（$y$ 的范围不是原来的 $x$ 范围）。

## 7. 与已学关系
L13 的 $|dx/dy|$ 是 $1\times1$ 的 $|\det J|$；L11 的多维 Gaussian 做线性变换仍 Gaussian，就是 14.3 的直接应用。

**考场第一步**：先写 $\mathbf x=g(\mathbf y)$，再写 $J=\partial\mathbf x/\partial\mathbf y^\top$，最后取 $|\det J|$。

## 8. 作业（答案在第 9 节，先做完再看）
**Q1 (concept).** True or false? One line why.
(a) In 2D the factor is $|\det J|$, not $|J|$. (b) If a map stretches area, the density decreases. (c) For $\mathbf x=g(\mathbf y)$, use $J=\partial\mathbf y/\partial\mathbf x^\top$. (d) A negative determinant makes the density negative.

**Q2 (exam-style, HW2 Q2 II style).** Let $x_1=3y_1,\ x_2=y_1+2y_2$, with $\mathbf y$ uniform on $[0,1]^2$ and $p_X=1/6$ on the image. Find $p_Y(y_1,y_2)$.

**Q3 (self-test).** Why must the Jacobian factor be inside an absolute value?

**Q4 (self-test).** What goes wrong if $\det J=0$?

## 9. 答案（先做完再看）
**A1.** (a) True. $|J|$ is not a thing for matrices. (b) True. Mass is fixed, area grows. (c) False. Use $\partial\mathbf x/\partial\mathbf y^\top$. (d) False. Area uses $|\det J|$.
**A2.** $J=\begin{bmatrix}3&0\\1&2\end{bmatrix}$, $|\det J|=6$; hence $p_Y=\frac16\cdot6=1$ on the image $\{0<x_1<3,\ x_1/3<x_2<x_1/3+2\}$（平行四边形，不是外接矩形）.
**A3.** Interval lengths and areas are nonnegative; $\det J<0$ only means orientation flips.
**A4.** The map collapses area, so it is not invertible; the density transform is undefined.
**A5（第 5 节）.** $x_1=y_1,\ x_2=2y_2\Rightarrow|\det J|=2$; $p_Y=1\cdot2=2$ on $[0,1]\times[0,\tfrac12]$; $\int_0^{1/2}\int_0^1 2\,dy_1dy_2=1$ ✓
