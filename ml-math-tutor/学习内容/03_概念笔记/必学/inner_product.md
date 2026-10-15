---
id: inner_product
name: 内积（inner product / dot product）
priority: 必学
prereq: [vector]
next: [norm, orthogonal_projection, linear_model]
ml_usage: [线性回归 w·x, 神经网络加权和, 余弦相似度, 注意力机制]
status: 学习中
mastery: 0
next_review: 
---

# 内积（inner product / dot product）

## 1. 一句话定义
内积把**两个向量**压成**一个数**：对应位置相乘，再全部加起来。

## 2. 直白解释（它到底在干嘛）
给两样东西打分，看它们**有多"合拍"**：
- 你给一部电影打标签 (动作=5, 搞笑=1)；
- 我打标签 (动作=4, 搞笑=2)。
- 逐项相乘再相加 $\to$ 一个总分，衡量"我们口味像不像"。

## 3. 几何直觉
内积暗藏角度：
$$
\mathbf{a}\cdot\mathbf{b}=\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$
- $\|\mathbf{a}\|,\|\mathbf{b}\|$：两向量各自长度。
- $\theta$：夹角。
- 含义：把 $\mathbf{b}$ **投影**到 $\mathbf{a}$ 上，看"顺着 $\mathbf{a}$ 方向的分量有多大"，再乘以 $\|\mathbf{a}\|$。

三种极端情形：
- 方向相同 $\theta=0 \Rightarrow \cos\theta=1 \Rightarrow$ 内积最大（正）。
- 垂直 $\theta=90^\circ \Rightarrow \cos\theta=0 \Rightarrow$ 内积 $=0$（**正交 orthogonal**）。
- 方向相反 $\theta=180^\circ \Rightarrow$ 内积为负。

## 4. 数学形式与符号逐个解释
$$
\mathbf{a}\cdot\mathbf{b}=a_1b_1+a_2b_2+\dots+a_nb_n=\sum_{i=1}^{n}a_i b_i
$$
- $\mathbf{a}\cdot\mathbf{b}$：内积的写法（中间一个点）。
- $a_i$、$b_i$：第 $i$ 个分量。
- $\sum$：求和符号，把 $i$ 从 $1$ 到 $n$ 的每一项加起来。

## 5. 最小例子（手算，不跳步）
设 $\mathbf{a}=(1,2)$，$\mathbf{b}=(3,4)$：
$$
\mathbf{a}\cdot\mathbf{b}=1\times3+2\times4=3+8=11
$$
$$
\|\mathbf{a}\|=\sqrt{1^2+2^2}=\sqrt{5},\qquad \|\mathbf{b}\|=\sqrt{3^2+4^2}=5
$$
$$
\cos\theta=\frac{11}{\sqrt{5}\times5}=\frac{11}{11.18}\approx0.984
\quad\Rightarrow\quad \theta\approx10.3^\circ
$$

## 6. 机器学习中的应用
- **线性回归 / 神经网络**：$\hat{y}=\mathbf{w}\cdot\mathbf{x}+b$，内积就是"特征加权求和"。
- **余弦相似度**：$\cos\theta=\dfrac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$ 衡量文本/用户/商品相似度。
- **注意力机制**：用内积衡量 query 和 key 的匹配程度。
- **正交**是正交投影与最小二乘的直接基础。

## 7. 常见易错点
- **结果是标量（一个数），不是向量**。
- **维度必须相同**，否则不能逐位相乘。
- 内积为 $0$ $\ne$ 两个向量是零向量；只说明它们**垂直**。
- 别和"逐元素相乘（$\odot$）"混淆：内积最后要**求和**成一个数。

## 8. 与已学概念的关系
- 基于 `vector`；内积可推出 `norm`（$\|\mathbf{a}\|=\sqrt{\mathbf{a}\cdot\mathbf{a}}$）与 `orthogonal_projection`（投影）。

## 9. 对应习题
见 `学习内容/04_习题/必学/inner_product_习题.md`。

## 10. 批改与解析
（学生提交后填写）
