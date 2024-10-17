import numpy as np
import matplotlib.pyplot as plt

# 实验数据，每一行代表一次实验的结果 [正面次数, 反面次数]
data = np.array([
    [5, 5],  # 第一次实验：5次正面，5次反面
    [9, 1],  # 第二次实验：9次正面，1次反面
    [8, 2],  # 第三次实验：8次正面，2次反面
    [4, 6],  # 第四次实验：4次正面，6次反面
    [7, 3]  # 第五次实验：7次正面，3次反面
])

# 初始化参数：两个硬币正面出现的概率 p_A 和 p_B
p_A = 0.6  # 初始估计硬币A正面概率
p_B = 0.5  # 初始估计硬币B正面概率

# 保存每次迭代后 p_A 和 p_B 的值，用于画图
p_A_history = [p_A]
p_B_history = [p_B]

# EM算法迭代
for step in range(10):  # 迭代10次
    # E步: 计算隐变量（每次实验中硬币A和B的责任值）
    weights_A = []  # 记录硬币A的责任值
    weights_B = []  # 记录硬币B的责任值

    for heads, tails in data:
        # 计算硬币A产生这些数据的可能性
        likelihood_A = (p_A ** heads) * ((1 - p_A) ** tails)
        # 计算硬币B产生这些数据的可能性
        likelihood_B = (p_B ** heads) * ((1 - p_B) ** tails)

        # 归一化，计算硬币A和B的责任值
        weight_A = likelihood_A / (likelihood_A + likelihood_B)
        weight_B = likelihood_B / (likelihood_A + likelihood_B)

        weights_A.append(weight_A)
        weights_B.append(weight_B)

    # M步: 使用E步中计算的责任值更新参数 p_A 和 p_B
    total_heads_A = sum(weight_A * heads for weight_A, (heads, tails) in zip(weights_A, data))
    total_tails_A = sum(weight_A * tails for weight_A, (heads, tails) in zip(weights_A, data))

    total_heads_B = sum(weight_B * heads for weight_B, (heads, tails) in zip(weights_B, data))
    total_tails_B = sum(weight_B * tails for weight_B, (heads, tails) in zip(weights_B, data))

    # 更新p_A 和 p_B
    p_A = total_heads_A / (total_heads_A + total_tails_A)
    p_B = total_heads_B / (total_heads_B + total_tails_B)

    # 保存每次迭代后的 p_A 和 p_B
    p_A_history.append(p_A)
    p_B_history.append(p_B)

    print(f"Step {step + 1}: p_A = {p_A:.4f}, p_B = {p_B:.4f}")

# 最终的估计结果
final_p_A = p_A_history[-1]
final_p_B = p_B_history[-1]

# 画出 p_A 和 p_B 随着迭代次数的变化
plt.plot(range(11), p_A_history, label="p_A (Coin A)", marker='o')
plt.plot(range(11), p_B_history, label="p_B (Coin B)", marker='o')

# 标注最后的结果
plt.text(10, final_p_A, f'p_A = {final_p_A:.4f}', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(10, final_p_B, f'p_B = {final_p_B:.4f}', fontsize=12, verticalalignment='top', horizontalalignment='right')

plt.xlabel('Iteration Step')
plt.ylabel('Probability of Heads')
plt.title('EM Algorithm: Probability of Heads for Coin A and Coin B')
plt.legend()
plt.grid(True)
plt.show()

# 输出最后的结论
print(f"\nFinal estimated probability for Coin A (p_A): {final_p_A:.4f}")
print(f"Final estimated probability for Coin B (p_B): {final_p_B:.4f}")
