# 习题 · 向量与内积（vector / inner product）

> 会话 S002 · 2026-10-15 · 状态：已布置，待批改
> 规则：先自己做完，再看文末答案区。

## 作业（先做完再看答案）

**Q1（概念）** 判断对错，并说明理由：
- (a) 两个向量的内积结果还是一个向量。
- (b) 若 $\mathbf{a}\cdot\mathbf{b}=0$，则 $\mathbf{a}$ 和 $\mathbf{b}$ 中至少有一个是零向量。
- (c) 向量 $(1,2,3)$ 和 $(3,2,1)$ 的内积与顺序无关。

**Q2（手算，写完整步骤）** 设 $\mathbf{a}=(-1,3,2)$，$\mathbf{b}=(2,0,4)$。
- (a) 求 $\mathbf{a}+\mathbf{b}$
- (b) 求 $3\mathbf{a}$
- (c) 求 $\mathbf{a}\cdot\mathbf{b}$
- (d) 求 $\|\mathbf{a}\|$（$\mathbf{a}$ 的长度）

**Q3（几何）**
- (a) $\mathbf{a}=(1,0)$，$\mathbf{b}=(0,1)$。求 $\mathbf{a}\cdot\mathbf{b}$ 以及夹角。
- (b) $\mathbf{a}=(1,0)$，$\mathbf{c}=(1,1)$。求 $\mathbf{a}\cdot\mathbf{c}$ 和 $\|\mathbf{c}\|$，再用 $\cos\theta=\dfrac{\mathbf{a}\cdot\mathbf{c}}{\|\mathbf{a}\|\,\|\mathbf{c}\|}$ 求夹角。

**Q4（机器学习联系）** 预测房价，特征 $\mathbf{x}=(\text{面积}, \text{房间数})=(100,3)$，权重 $\mathbf{w}=(2,50)$，偏置 $b=20$。预测值 $\hat{y}=\mathbf{w}\cdot\mathbf{x}+b$。
- (a) 算出 $\hat{y}$。
- (b) 用一句话说明"$\mathbf{w}\cdot\mathbf{x}$"在这个模型里代表什么。

---

## 答案区（先自己做完再看）

**Q1**
- (a) **错**。内积是逐位相乘再求和，结果是**一个标量**。
- (b) **错**。$\mathbf{a}\cdot\mathbf{b}=0$ 只说明两向量**垂直**，比如 $\mathbf{a}=(1,0)$、$\mathbf{b}=(0,1)$ 都不是零向量但内积为 $0$。
- (c) **对**。内积满足交换律：$1\times3+2\times2+3\times1=10$，交换也一样。

**Q2** $\mathbf{a}=(-1,3,2)$，$\mathbf{b}=(2,0,4)$
- (a) $\mathbf{a}+\mathbf{b}=(-1+2,\ 3+0,\ 2+4)=(1,3,6)$
- (b) $3\mathbf{a}=(3\times(-1),\ 3\times3,\ 3\times2)=(-3,9,6)$
- (c) $\mathbf{a}\cdot\mathbf{b}=(-1)(2)+(3)(0)+(2)(4)=-2+0+8=6$
- (d) $\|\mathbf{a}\|=\sqrt{(-1)^2+3^2+2^2}=\sqrt{1+9+4}=\sqrt{14}\approx3.74$

**Q3**
- (a) $\mathbf{a}\cdot\mathbf{b}=1\times0+0\times1=0 \Rightarrow$ 垂直，夹角 $90^\circ$。
- (b) $\mathbf{a}\cdot\mathbf{c}=1\times1+0\times1=1$；$\|\mathbf{c}\|=\sqrt{1^2+1^2}=\sqrt{2}$；$\|\mathbf{a}\|=1$。
  $\cos\theta=\dfrac{1}{1\times\sqrt{2}}=\dfrac{1}{\sqrt{2}}\approx0.707 \Rightarrow \theta=45^\circ$。

**Q4**
- (a) $\mathbf{w}\cdot\mathbf{x}=2\times100+50\times3=200+150=350$；$\hat{y}=350+20=370$。
- (b) "$\mathbf{w}\cdot\mathbf{x}$" = 把每个特征乘上它的**权重**再求和，即"各特征对预测的**加权贡献**之和"。
  （面积每多 $1$ 贡献 $2$，房间每多 $1$ 贡献 $50$。）
