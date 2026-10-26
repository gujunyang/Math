# 板书 · S005 · 第 08 课：乘积/链式法则与二阶 Taylor

- 会话ID：`S005`
- 日期：2026-10-27
- 对应：L08 / M2
- 修订记录：（初版）2026-10-27

---

## 0. 生活化引入

拧音量旋钮，声音经过“功放”再经过“喇叭”，最后才到耳朵。
**旋钮转一点，中间每一层都放大一次**——这就是**链式法则**。
而“我只需在当前位置附近估个值”，用一条抛物线贴住曲线就够了——这就是**二阶 Taylor**。

---

## 1. 直觉

| 工具 | 一句话 | 什么时候用 |
|---|---|---|
| 乘积法则（product rule） | 两个因子都在变，**各管一半再相加** | $(we^w)'$、$\|\mathbf{X}\mathbf{w}-\mathbf{y}\|^2$ 展开时 |
| 链式法则（chain rule） | **外层导数 × 内层导数**，一层层剥 | $e^{2w}$、$(3w+1)^4$、$J(\mathbf{w})$ |
| 二阶 Taylor | 用**值 + 斜率 + 曲率**贴一条抛物线 | 估附近的值、判极值、看收敛 |

一句话：**乘积法则管“并列”，链式法则管“套娃”，Taylor 管“以点代面”。**

---

## 2. 几何

![二阶 Taylor = 贴一条抛物线](图片/fig_taylor_parabola.png)

**看图**（$L(w)=\frac12(we^w-2)^2$，在 $w_0=0$ 处展开）：

- 蓝线是真函数；灰虚线是**一阶**近似（切线），只在 $w_0$ 附近贴合，走远就偏。
- 红线是**二阶**近似（抛物线），在 $w_0$ 附近**几乎与蓝线重合**——因为它的值、斜率、曲率三样都和真函数一样。
- 但注意：这条抛物线**开口向下**（$L''(0)=-3<0$），说明从 $0$ 往右走 $L$ 会**下降**——
  真正的最小点在 $w\approx0.85$，离展开点不算近，所以抛物线走远就失效（红线穿到 0 以下）。
- **教训**：Taylor 是“局部”的，只在展开点附近可信。

> 一句话：**一阶近似给方向，二阶近似给弯曲；越远越不准。**

---

## 3. 计算（公式卡片）

### 8.1 乘积法则（product rule）

$$
\big(u(w)v(w)\big)'=u'(w)v(w)+u(w)v'(w)
$$

- **符号**：$u,v$ 都是 $w$ 的函数；“$u'v$”= 只有 $u$ 变，“$uv'$”= 只有 $v$ 变，两部分相加。
- **例**：$\big(we^w\big)'=1\cdot e^w+w\cdot e^w=e^w(1+w)$。

### 8.2 链式法则·一元（chain rule）

$$
\big(f(g(w))\big)'=f'(g(w))\cdot g'(w)
$$

- **符号**：$g$ 是内层（先算），$f$ 是外层（后算）；**别忘了乘 $g'(w)$**。
- **例**：$\big(e^{2w}\big)'=e^{2w}\cdot2=2e^{2w}$；$\big((3w+1)^4\big)'=4(3w+1)^3\cdot3=12(3w+1)^3$。

**常用导数小表**

| $f(w)$ | $f'(w)$ |
|---|---|
| $w^n$ | $nw^{n-1}$ |
| $e^{w}$ | $e^{w}$ |
| $\ln w$ | $1/w$ |
| $\sigma(w)=\dfrac{1}{1+e^{-w}}$ | $\sigma(w)\big(1-\sigma(w)\big)$ |

### 8.3 一阶 Taylor（linear approximation）

$$
f(w)\approx f(w_0)+f'(w_0)(w-w_0)
$$

- **符号**：$w_0$ 是展开点（必须靠近你要估的点）；$(w-w_0)$ 是**位移**，不是 $w$。
- **例**：$f(w)=e^w$ 在 $w_0=0$：$e^w\approx1+w$；估 $e^{0.1}\approx1.1$（真值 $1.1052$）。

### 8.4 二阶 Taylor·一元（quadratic approximation）

$$
f(w)\approx f(w_0)+f'(w_0)(w-w_0)+\frac{f''(w_0)}{2}(w-w_0)^2
$$

- **符号**：第三项带 $\dfrac{1}{2}$（不能丢）；$f''(w_0)>0$ 开口向上（谷），$<0$ 开口向下（峰）。
- **例**：$\ln(1+w)$ 在 $0$：$f(0)=0$、$f'(0)=1$、$f''(0)=-1$ ⇒ $\ln(1+w)\approx w-\dfrac{w^2}{2}$；
  估 $\ln1.1\approx0.1-0.005=0.095$（真值 $0.09531$）。

### 8.5 二阶 Taylor·多元（向量形式）

$$
f(\mathbf{x}_0+\mathbf{d})\approx f(\mathbf{x}_0)+\nabla f(\mathbf{x}_0)^\top\mathbf{d}
+\frac12\,\mathbf{d}^\top\mathbf{H}(\mathbf{x}_0)\,\mathbf{d}
$$

- **符号**：$\mathbf{d}=\mathbf{x}-\mathbf{x}_0\in\mathbb{R}^{n\times1}$ 是位移；第一项是数，第二项 $(\nabla f)^\top\mathbf{d}$ 是数，第三项是二次型（也是数）。
- **例**：$\mathbf{x}_0=(0,0)$、$f=x^2+2xy+3y^2$：$\nabla f(\mathbf{0})=\mathbf{0}$，$\mathbf{H}=\begin{bmatrix}2&2\\2&6\end{bmatrix}$ ⇒ $f\approx\frac12\mathbf{d}^\top\mathbf{H}\mathbf{d}=d_1^2+2d_1d_2+3d_2^2$（二次函数，Taylor 精确）。

### 8.6 梯度下降一步（gradient-descent update）

$$
\mathbf{w}_{k+1}=\mathbf{w}_k-\eta\,\nabla f(\mathbf{w}_k)
$$

- **符号**：$\eta>0$ 是步长（learning rate）；**减号**因为要往下降方向走；$\nabla f$ 与 $\mathbf{w}$ 同形。
- **例**：$f(w)=w^2$、$w_0=1$、$\eta=0.1$：$w_1=1-0.1\cdot2=0.8$，$w_2=0.8-0.1\cdot1.6=0.64$。

---

## 4. 完整手算

**Example.** $L(w)=\frac12(we^w-2)^2$。求 $L'(0)$、$L''(0)$、$w_0=0$ 处的二阶 Taylor，并从 $w_0=0$ 走一步 GD（$\eta=0.1$）。

1. 拆层：令 $u=we^w-2$，则 $L=\frac12u^2$。

2. 内层用乘积法则：

$$
u'=1\cdot e^w+w\cdot e^w=e^w(1+w)
$$

3. 外层用链式：

$$
L'(w)=u\cdot u'=(we^w-2)\,e^w(1+w)
$$

4. 代 $w=0$：$u(0)=0-2=-2$，$u'(0)=1$ ⇒

$$
L'(0)=(-2)\cdot1=-2
$$

5. 再求一次导，用乘积法则 $(u u')'=(u')^2+u\,u''$：

$$
u''=\big(e^w(1+w)\big)'=e^w(1+w)+e^w=e^w(2+w)
$$

$$
L''(w)=(u')^2+u\,u''
$$

6. 代 $w=0$：$u'(0)=1$、$u(0)=-2$、$u''(0)=2$ ⇒

$$
L''(0)=1^2+(-2)\cdot2=1-4=-3
$$

7. 二阶 Taylor：

$$
L(w)\approx L(0)+L'(0)w+\frac{L''(0)}{2}w^2
=2-2w-\frac32w^2
$$

8. 验算 $w=0.2$：Taylor 给 $2-0.4-0.06=1.54$；
   真值 $L(0.2)=\frac12(0.2e^{0.2}-2)^2$，$e^{0.2}\approx1.2214$ ⇒ $0.2\cdot1.2214=0.2443$，
   $(-1.7557)^2=3.0825$，$L\approx1.5413$。**误差 $0.0013$** ✓

9. 走一步 GD：$w_1=w_0-\eta L'(0)=0-0.1\cdot(-2)=0.2$。

10. 读结论：$L''(0)=-3<0$ ⇒ 抛物线开口向下 ⇒ $0$ 处**不是**最小，往右走 $L$ 下降，与图里真正最小 $w\approx0.85$ 一致。

> 中文：这题就是 HW1 Q3(b)：先“拆层”再“乘积/链式”，二阶导再用一次乘积法则；Taylor 只代三个数。

---

## 5. 独立复现（先自己写，答案见第 9 节）

**Exercise.** $f(w)=w^2e^w$。求 $f'(w)$、$f''(w)$，写出 $w_0=1$ 处的二阶 Taylor，并给出一步 GD（$\eta=0.05$）。

---

## 6. 易错点

1. **乘积法则写成 $u'v'$**。必须 $u'v+uv'$，两项都不能少。
2. **链式法则忘乘内层导数**：$(e^{2w})'=2e^{2w}$，不是 $e^{2w}$；$(3w+1)^4$ 的导数是 $12(3w+1)^3$。
3. **Taylor 丢 $\frac12$**：二阶项是 $\frac{f''(w_0)}{2}(w-w_0)^2$；多元版是 $\frac12\mathbf{d}^\top\mathbf{H}\mathbf{d}$。
4. **GD 符号写反**：是 $-\eta\nabla f$；写成 $+$ 就是**上坡**，$L$ 会越来越大。
5. **GD 卡在驻点**：$\nabla f=\mathbf{0}$ 时无论 $\eta$ 多大都动不了——它只保证收敛到**驻点**，不保证是最小。

---

## 7. 与已学关系

L06 的 $\nabla f$ 是 Taylor 的第二项，L07 的 $\mathbf{H}$ 是第三项；L05 的“正定”现在有了几何含义：
$\mathbf{H}\succ\mathbf{0}$ ⇒ 抛物线开口向上 ⇒ 极小。L28 的误差面、L30 的收敛速度都从这条抛物线出发。

---

## 8. 作业

**Q1 (concept).** True or false? One line why.

(a) $(uv)'=u'v'$.
(b) $\dfrac{d}{dw}e^{2w}=2e^{2w}$.
(c) The second-order Taylor expansion matches $f$, $f'$, and $f''$ at the expansion point.
(d) If $f'(x_0)=0$ and $f''(x_0)>0$, then $x_0$ is a local minimum.
(e) The update $w_{k+1}=w_k+\eta f'(w_k)$ makes $f$ decrease for small $\eta>0$.

**Q2 (compute).** Find $f'$ (and $f''$ where asked).

(a) $f(w)=w^2e^w$ — find $f'$ and $f''$.
(b) $f(w)=(3w+1)^4$ — find $f'$.
(c) $f(w)=\ln(1+e^w)$ — find $f'$, and show it equals the sigmoid $\sigma(w)$.
(d) $J(\mathbf{w})=\frac12\|\mathbf{X}\mathbf{w}-\mathbf{y}\|^2+\frac{\lambda}{2}\|\mathbf{w}\|^2$ — find $\nabla J$.

**Q3 (Taylor).** Expand $f(w)=\ln(1+w)$ at $w_0=0$ up to second order, and estimate $\ln(1.1)$.

**Q4 (ML).** $f(w)=(w^2-1)^2$.

(a) Find $f'(w)$ and $f''(w)$.
(b) Write the second-order Taylor expansion at $w_0=0$.
(c) Starting at $w_0=0$ with $\eta=0.1$, compute $w_1$. What happens, and what does it teach about gradient descent?

---

## 9. 作业答案（先做完再看）

**A1.**

(a) False. It is $u'v+uv'$; the product rule has two terms.
(b) True. Chain rule with inner $2w$.
(c) True. By construction the first three terms are chosen to match those three quantities.
(d) True. Zero slope + positive curvature ⇒ bowl ⇒ local min.
(e) False. The minus sign is essential; with $+$ you move uphill.

**A2.**

(a) $f'=2we^w+w^2e^w=e^w(w^2+2w)$；

$$
f''=e^w(w^2+2w)+e^w(2w+2)=e^w(w^2+4w+2)
$$

(b) $f'=4(3w+1)^3\cdot3=12(3w+1)^3$.
(c) $f'=\dfrac{e^w}{1+e^w}=\dfrac{1}{1+e^{-w}}=\sigma(w)$（分子分母同除 $e^w$）。
(d) $\nabla J=\mathbf{X}^\top(\mathbf{X}\mathbf{w}-\mathbf{y})+\lambda\mathbf{w}$，形状 $n\times1$。

**A3.** $f(0)=0$，$f'(w)=\frac{1}{1+w}\Rightarrow f'(0)=1$，$f''(w)=-\frac{1}{(1+w)^2}\Rightarrow f''(0)=-1$。

$$
\ln(1+w)\approx w-\frac{w^2}{2}
\quad\Longrightarrow\quad
\ln(1.1)\approx0.1-0.005=0.095
$$

（真值 $0.09531$，误差约 $3\times10^{-4}$。）

**A4.**

(a) $f'=2(w^2-1)\cdot2w=4w^3-4w$；$f''=12w^2-4$。
(b) $f(0)=1$、$f'(0)=0$、$f''(0)=-4$ ⇒

$$
f(w)\approx1-2w^2
$$

(c) $w_1=w_0-\eta f'(0)=0-0.1\cdot0=0$。**卡住不动**。
因为 $w=0$ 是驻点（其实是**局部最大**：$f(0)=1$，两侧都下降到 $0$）。
教训：**梯度下降只保证到驻点，不保证到最小**；遇到鞍点/极大也会停。

**A5（第 5 节独立复现）.**

$f=w^2e^w$：$f'=e^w(w^2+2w)$，$f''=e^w(w^2+4w+2)$。

在 $w_0=1$：$f(1)=e$，$f'(1)=3e$，$f''(1)=7e$，

$$
f(w)\approx e+3e\,(w-1)+\frac{7e}{2}(w-1)^2
$$

一步 GD（$\eta=0.05$）：

$$
w_1=1-0.05\cdot3e=1-0.15e\approx1-0.4077=0.5923
$$
