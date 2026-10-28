# 板书 · S006 · 第 11 课：Gaussian 与多维 Gaussian

- 会话ID：`S006`
- 日期：2026-10-28
- 对应：L11 / M3
- 修订记录：（初版）2026-10-28；v2 2026-10-28：按新标准（公式卡片加「意义与场景」、例题生活化 + 计算）重写 11.1–11.3 与第 4/5 节：身高 $\mathcal N(170,8^2)$、零件长宽误差 $\operatorname{diag}(4,1)$、糖袋 $\mathcal N(500,10^2)$；v3 2026-10-28：「意义与场景」按新要求扩到 1–5 句并加类比（钟形/点云/斜云的主轴）

---

## 0. 生活化引入

身高、测量误差、全班成绩——大多数"中间多、两头少"的量都长成**钟形**。
它只需要两个数就能说清：**中心在哪（$\mu$）、有多宽（$\sigma$）**。多维时把这两个数升级成**向量 $\boldsymbol\mu$** 和**矩阵 $\boldsymbol\Sigma$**。

---

## 1. 直觉

|           | 一元                   | 多维                                              |
| --------- | ---------------------- | ------------------------------------------------- |
| 位置      | $\mu$（一个数）      | $\boldsymbol\mu$（$n\times1$ 向量）           |
| 宽度/形状 | $\sigma^2$（一个数） | $\boldsymbol\Sigma$（$n\times n$ 协方差矩阵） |

一句话：**一元看一个数偏离中心多远，多维看一个点偏离中心"多远 + 朝哪个方向"。**

---

## 2. 几何

![Gaussian：μ 定位置，Σ 定椭圆](图片/fig_gaussian.png)

**看图**：

- 左图：曲线关于 $\mu$ 对称；$\mu\pm\sigma$ 之间占约 $68\%$，$\pm2\sigma$ 约 $95\%$。$\sigma$ 变大 ⇒ 变矮变宽（面积仍为 1）。
- 右图：二维时等高线是**椭圆**；椭圆的两根轴就是 $\boldsymbol\Sigma$ 的**特征方向**，半轴长 $\propto\sqrt{\lambda_i}$。
- 椭圆"斜着"说明两个分量相关；若 $\boldsymbol\Sigma$ 是对角阵，椭圆就正着放（轴与坐标轴平行）。

---

## 3. 计算（公式卡片）

### 11.1 一元 （univariate Gaussian）

$$
p(x)=\frac{1}{\sqrt{2\pi}\,\sigma}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

- **符号**：$\mu=E[X]$ 是中心；$\sigma^2=\operatorname{Var}(X)$ 是宽度，$\sigma>0$；前面那坨是**归一化常数**，保证积分为 1。
- **意义与场景**：它画的是生活里最常见的形状——大多数人在中间，越往两边越稀。身高、体重、测量误差、考试成绩，几乎都长这样。它也是后面一切“噪声”的默认模型：只要说“误差是随机的”，数学上通常就是在说它是 Gaussian。
- **例（生活版）**：某地成年男性身高 $\mu=170$ cm、$\sigma=8$ cm ⇒

$$
p(170)=\frac{1}{8\sqrt{2\pi}}\approx0.0499\ \text{每 cm}
$$

意思是身高落在 170–171 cm 之间的人约占 $0.0499\times1\approx5\%$。

### 11.2 多维 Gaussian 密度（multivariate Gaussian）

$$
p(\mathbf{x})=\frac{1}{(2\pi)^{n/2}\sqrt{\det\boldsymbol\Sigma}}
\exp\!\left(-\tfrac12(\mathbf{x}-\boldsymbol\mu)^\top
\boldsymbol\Sigma^{-1}(\mathbf{x}-\boldsymbol\mu)\right)
$$

- **符号**：$\mathbf{x},\boldsymbol\mu\in\mathbb{R}^{n\times1}$；$\boldsymbol\Sigma\in\mathbb{R}^{n\times n}$ 是协方差矩阵（对称、正定）；$\det\boldsymbol\Sigma$ 管"体积"，$\boldsymbol\Sigma^{-1}$ 管"形状"。
- **意义与场景**：现实里的量很少单独出现——一张图的两个像素、一个人的身高和体重、一个零件的长和宽，往往一起变。多维 Gaussian 就是给“一整组数”画一张联合的钟形地图；$\boldsymbol\Sigma$ 记下每个方向抖多大、彼此怎么牵连。所以它一次就能描述“一整团点云”的形状。
- **例（生活版）**：某零件的长、宽误差互不影响，方差为 $4$ 和 $1$（$\mathrm{mm}^2$），即 $\boldsymbol\Sigma=\operatorname{diag}(4,1)$。误差 $\mathbf{x}=(2,1)^\top$ 处：

$$
\text{指数}=-\tfrac12\Big(\tfrac{2^2}{4}+\tfrac{1^2}{1}\Big)=-1,\quad
\text{系数}=\frac{1}{2\pi\sqrt4}=0.0796,\quad
p=0.0796e^{-1}=0.0293
$$

### 11.3 $\boldsymbol\Sigma$ 为什么对称正定

$$
\boldsymbol\Sigma=E\big[(\mathbf{x}-\boldsymbol\mu)(\mathbf{x}-\boldsymbol\mu)^\top\big]
=\mathbf{Q}\boldsymbol\Lambda\mathbf{Q}^\top,\qquad \lambda_i>0
$$

- **符号**：$\lambda_i$ 是各主方向的方差，必须 $>0$（否则密度在某个方向"无限宽"、积分为 0）；$\mathbf{Q}$ 的列是椭圆的主轴方向。
- **意义与场景**：把 $\boldsymbol\Sigma$ 拆成“方向 + 长度”，就像把一团斜着的云看成一组长短不一的轴：轴的方向说明数据往哪边斜，轴的长短说明那个方向有多松。正定是一条底线——每个方向都必须有正的宽度，否则这团云会在某个方向摊平成一条线，密度就再也归一化不了。这套分解也是“白化”（把斜云转正、拉圆）和降维的起点。
- **例（生活版）**：零件长、宽误差会同向偏（一个大另一个也大），$\boldsymbol\Sigma=\begin{bmatrix}2&1\\1&2\end{bmatrix}$ ⇒ $\lambda=1,3$ ⇒ 椭圆半轴 $\sqrt1,\sqrt3$，方向 $(1,-1)$、$(1,1)$——也就是“长宽同时偏大/偏小”的方向最松。

---

## 4. 完整手算

**Example（身高）**：某地成年男性身高 $X\sim\mathcal N(170,8^2)$（单位 cm）。求 $p(170)$、$p(178)$、$p(186)$，并估计 170–171 cm 之间的人占多少。

1. 系数：$\dfrac{1}{8\sqrt{2\pi}}=\dfrac{1}{20.053}=0.0499$（单位：**每 cm**）。
2. $x=170$：指数为 $0$ ⇒ $p(170)=0.0499$。
3. $x=178$：$z=\dfrac{178-170}{8}=1$ ⇒ $p=0.0499e^{-1/2}=0.0499\times0.6065=0.0303$。
4. $x=186$：$z=2$ ⇒ $p=0.0499e^{-2}=0.0499\times0.1353=0.00675$。
5. 区间：$P(170<X<171)\approx p(170)\times1=0.0499\approx5\%$（密度 × 小区间长度 ≈ 概率）。
6. 读结论：每远离 $1\sigma$，密度乘 $e^{-1/2}\approx0.607$；远离 $2\sigma$ 乘 $e^{-2}\approx0.135$。**指数里的平方就是“钟形”的来源。**

---

## 5. 独立复现（先自己写，答案见第 9 节）

**Exercise.** 一袋糖标称 $500$ g，实际重量 $X\sim\mathcal N(500,10^2)$。求 $p(500)$、$p(510)$，并说明 $p(510)/p(500)$ 等于多少。

---

## 6. 易错点

1. **漏掉归一化系数** $\dfrac{1}{\sqrt{2\pi}\sigma}$（多维是 $(2\pi)^{n/2}\sqrt{\det\boldsymbol\Sigma}$）。漏了就不是密度。
2. **指数漏平方或漏 $\frac12$**：是 $-\dfrac{(x-\mu)^2}{2\sigma^2}$，不是 $-\dfrac{x-\mu}{2\sigma}$。
3. **把 $\sigma$ 和 $\sigma^2$ 混用**：公式分母是 $\sigma^2$，前置系数是 $\sigma$。
4. **把 $\boldsymbol\Sigma$ 当方差向量**：它是矩阵；对角元才是各分量的方差，非对角元是协方差。

---

## 7. 与已学关系

L10 的 $E[X],\operatorname{Var}(X)$ 就是 Gaussian 的两个参数；L09 的独立性在多维里表现为 $\boldsymbol\Sigma$ 对角。往后：L12 对 $\ln p$ 求导得 MLE，L17 用 "Gaussian noise ⇒ 平方损失" 接回 SSE。

---

## 8. 作业

**Q1 (concept).** True or false? One line why.

(a) Increasing $\sigma^2$ makes the curve wider and lower.
(b) The maximum of a univariate Gaussian density is $\dfrac{1}{\sqrt{2\pi}\sigma}$.
(c) $\boldsymbol\Sigma$ must be symmetric positive definite.
(d) If $\boldsymbol\Sigma$ is diagonal, the components are independent.
(e) The mode of a univariate Gaussian is at $x=\mu$.

**Q2 (compute).** $X\sim\mathcal N(-1,4)$。求 $p(-1)$ 与 $p(1)$。

**Q3 (compute).** $\mathbf{x}\sim\mathcal N(\mathbf{0},\operatorname{diag}(4,1))$。求 $\mathbf{x}=(2,2)^\top$ 处的密度。

**Q4 (why).** 为什么多维密度里会出现 $\det\boldsymbol\Sigma$，而一元里对应的是 $\sigma$？

---

## 9. 答案（先做完再看）

**A1.**

(a) True. 面积固定为 1，变宽必须变矮。
(b) True. 在 $x=\mu$ 处指数为 0。
(c) True. 协方差矩阵对称；正定保证每个方向方差为正、密度可归一化。
(d) True. 对角 ⇒ 联合密度可拆成各分量密度的乘积。
(e) True. 众数、均值、中位数三者重合。

**A2.** $\sigma=2$，系数 $=1/(2\sqrt{2\pi})=0.1995$：

$$
p(-1)=0.1995,\qquad p(1)=0.1995e^{-1/2}=0.1210
$$

**A3.** 系数 $=\dfrac{1}{2\pi\sqrt{4}}=0.0796$；指数 $=-\frac12\left(\frac{4}{4}+\frac{4}{1}\right)=-2.5$：

$$
p=0.0796\,e^{-2.5}=0.0796\times0.0821=0.00653
$$

**A4.** 一维里"宽度"是长度 $\sigma$；$n$ 维里"体积"要乘各主方向的长度，等于 $\sqrt{\lambda_1\cdots\lambda_n}=\sqrt{\det\boldsymbol\Sigma}$。所以 $\sigma$ 的位置被 $\sqrt{\det\boldsymbol\Sigma}$ 取代。

**A5（第 5 节独立复现）.** 系数 $=1/(10\sqrt{2\pi})=0.0399$：

$$
p(500)=0.0399,\qquad p(510)=0.0399e^{-1/2}=0.0242,\qquad
\frac{p(510)}{p(500)}=e^{-1/2}\approx0.607
$$
