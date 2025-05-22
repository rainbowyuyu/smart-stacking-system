import numpy as np

def evaluate_solutions(solutions, weights=None, criteria_types=None):
    """
    使用TOPSIS方法评估多目标优化的解决方案
    
    参数:
    - solutions: 包含多个解决方案的列表，每个解决方案包含多个目标值
    - weights: 每个目标的权重，默认为等权重
    - criteria_types: 每个目标的类型（'max'表示越大越好，'min'表示越小越好），默认为全部最大化
    
    返回:
    - 最佳解决方案及其排名
    """
    # 提取目标值矩阵
    objectives = np.array([list(sol['objectives'].values()) for sol in solutions])
    
    # 如果没有提供权重，使用等权重
    if weights is None:
        weights = np.ones(objectives.shape[1]) / objectives.shape[1]
    else:
        weights = np.array(weights) / sum(weights)  # 归一化权重
    
    # 如果没有提供标准类型，默认为全部最大化
    if criteria_types is None:
        criteria_types = ['max'] * objectives.shape[1]
    
    # 1. 归一化决策矩阵
    norm_matrix = objectives / np.sqrt(np.sum(objectives**2, axis=0))
    
    # 2. 加权归一化决策矩阵
    weighted_matrix = norm_matrix * weights
    
    # 3. 确定理想解和负理想解
    ideal_best = np.array([
        np.max(weighted_matrix[:, i]) if criteria_types[i] == 'max' else np.min(weighted_matrix[:, i])
        for i in range(weighted_matrix.shape[1])
    ])
    
    ideal_worst = np.array([
        np.min(weighted_matrix[:, i]) if criteria_types[i] == 'max' else np.max(weighted_matrix[:, i])
        for i in range(weighted_matrix.shape[1])
    ])
    
    # 4. 计算每个方案到理想解和负理想解的距离
    s_best = np.sqrt(np.sum((weighted_matrix - ideal_best)**2, axis=1))
    s_worst = np.sqrt(np.sum((weighted_matrix - ideal_worst)**2, axis=1))
    
    # 5. 计算相对接近度
    relative_closeness = s_worst / (s_best + s_worst)
    
    # 6. 确定最佳方案
    best_index = np.argmax(relative_closeness)
    
    # 7. 为解决方案添加排名信息
    rankings = np.argsort(-relative_closeness)  # 降序排列
    for i, sol in enumerate(solutions):
        sol['rank'] = int(np.where(rankings == i)[0][0]) + 1
        sol['relative_closeness'] = float(relative_closeness[i])
    
    # 返回最佳解决方案
    return solutions[best_index]

# 示例使用
if __name__ == "__main__":
    # 示例解决方案
    example_solutions = [
        {
            'objectives': {
                '出库效率': 0.85,
                '空间利用率': 0.72,
                '安全性': 0.90
            }
        },
        {
            'objectives': {
                '出库效率': 0.92,
                '空间利用率': 0.65,
                '安全性': 0.85
            }
        },
        {
            'objectives': {
                '出库效率': 0.78,
                '空间利用率': 0.88,
                '安全性': 0.82
            }
        }
    ]
    
    # 设置权重（出库效率、空间利用率、安全性）
    weights = [0.4, 0.3, 0.3]
    
    # 设置标准类型（全部为最大化）
    criteria_types = ['max', 'max', 'max']
    
    # 评估解决方案
    best_solution = evaluate_solutions(example_solutions, weights, criteria_types)
    
    print("最佳解决方案:")
    print(f"排名: {best_solution['rank']}")
    print(f"相对接近度: {best_solution['relative_closeness']:.4f}")
    print("目标值:", best_solution['objectives'])    