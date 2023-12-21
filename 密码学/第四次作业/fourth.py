import numpy as np
from scipy import stats


def single_bit_frequency_test(sequence):
    """
    单比特频率检测
    检测序列中0和1的频率是否接近50%
    """
    n = len(sequence)
    s = sum(sequence)
    p_value = stats.norm.sf(abs(s - n / 2) / np.sqrt(n / 4)) * 2  # 双尾检验
    return p_value


def runs_test(sequence):
    """
    游程分布检测
    检测连续的0和1游程的分布是否符合随机性
    """
    n = len(sequence)
    pi = sum(sequence) / n
    tau = 2 / np.sqrt(n)

    if abs(pi - 0.5) >= tau:
        return 0.0  # 不满足游程检测前提条件

    vobs = 1
    for i in range(1, n):
        if sequence[i] != sequence[i - 1]:
            vobs += 1

    p_value = stats.norm.sf(abs(vobs - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(2 * n) * pi * (1 - pi))) * 2
    return p_value


def autocorrelation_test(sequence, d):
    """
    自相关检测
    检测给定位移d下序列的自相关性
    """
    n = len(sequence)
    adj_n = n - d
    ad = sum([sequence[i] for i in range(d, n)] != sequence[i - d] for i in range(d, n))
    p_value = stats.norm.sf(abs(ad - adj_n / 2) / np.sqrt(adj_n / 4)) * 2
    return p_value


# Example sequence (randomly generated for demonstration)
sequence = np.random.choice([0, 1], 1000)

# Perform tests
p_value_frequency = single_bit_frequency_test(sequence)
p_value_runs = runs_test(sequence)
p_value_autocorrelation = autocorrelation_test(sequence, 2)  # 自相关检测位移设为2

p_value_frequency, p_value_runs, p_value_autocorrelation

