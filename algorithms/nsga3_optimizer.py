import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.factory import get_reference_directions
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.util.display import Display
from datetime import datetime, timedelta
import random

class StackingProblem(Problem):
    def __init__(self, cargo_list, yard_locations, warehouses, equipment):
        # 决策变量：每个货物分配到哪个位置
        n_var = len(cargo_list)  # 每个货物一个决策变量

        # 计算可能的位置总数（堆场位置 + 仓库位置）
        all_locations = yard_locations + warehouses
        n_locations = len(all_locations)

        # 目标函数：3个（出库效率、空间利用率、安全性）
        n_obj = 3

        # 约束条件：承重限制、堆高限制等
        n_constr = 2  # 示例：承重约束和堆高约束

        super().__init__(
            n_var=n_var,
            n_obj=n_obj,
            n_constr=n_constr,
            xl=np.zeros(n_var),  # 决策变量下界（位置索引从0开始）
            xu=np.ones(n_var) * (n_locations - 1),  # 决策变量上界
            type_var=int  # 决策变量为整数（位置索引）
        )

        self.cargo_list = cargo_list
        self.yard_locations = yard_locations
        self.warehouses = warehouses
        self.all_locations = all_locations
        self.equipment = equipment

    def _evaluate(self, X, out, *args, **kwargs):
        # 初始化目标函数值和约束值
        F = np.zeros((X.shape[0], self.n_obj))
        G = np.zeros((X.shape[0], self.n_constr))

        for i in range(X.shape[0]):  # 对每个个体（解决方案）
            # 初始化目标函数
            出库效率 = 0
            空间利用率 = 0
            安全性 = 0

            # 初始化约束条件
            承重约束 = 0
            堆高约束 = 0

            # 记录每个位置的总重量和堆高
            location_weights = {loc.location_id: 0 for loc in self.all_locations}
            location_heights = {loc.location_id: 0 for loc in self.all_locations}

            for j in range(self.n_var):  # 对每个货物
                cargo = self.cargo_list[j]
                location_idx = int(X[i, j])
                location = self.all_locations[location_idx]

                # 计算出库效率（基于时间窗口和搬运距离）
                if cargo.expected_out_time:
                    current_time = datetime.now()
                    days_to_out = (cargo.expected_out_time - current_time).days
                    # 时间窗口优先级：越接近出库时间，优先级越高
                    time_priority = 1 - (days_to_out / 30) if days_to_out > 0 else 1
                    # 搬运距离：假设位置索引越小越靠近出口
                    distance_priority = 1 - (location_idx / len(self.all_locations))
                    出库效率 += time_priority * distance_priority

                # 计算空间利用率
                if location.location_id.startswith('YARD_'):
                    # 堆场空间利用率
                    空间利用率 += (cargo.weight / location.load_capacity) * 0.7
                    空间利用率 += (float(cargo.dimensions.split('x')[2]) / location.max_stack_height) * 0.3
                else:
                    # 仓库空间利用率
                    volume = float(cargo.dimensions.split('x')[0]) * \
                             float(cargo.dimensions.split('x')[1]) * \
                             float(cargo.dimensions.split('x')[2]) / 1000  # 转换为立方米
                    空间利用率 += (volume / location.available_capacity)

                # 计算安全性
                if cargo.is_hazardous:
                    # 危险品需要特殊处理
                    if hasattr(location, 'hazardous_safe') and location.hazardous_safe:
                        安全性 += 1
                    else:
                        安全性 -= 0.5
                else:
                    安全性 += 0.8  # 普通货物基本安全分

                # 更新位置重量和堆高
                location_weights[location.location_id] += cargo.weight
                if location.location_id.startswith('YARD_'):
                    # 堆高约束（假设每件货物堆叠）
                    location_heights[location.location_id] = max(
                        location_heights[location.location_id],
                        float(cargo.dimensions.split('x')[2])
                    )

            # 归一化目标函数
            F[i, 0] = -出库效率  # 最大化出库效率（取负因为NSGA-III默认最小化）
            F[i, 1] = -空间利用率  # 最大化空间利用率
            F[i, 2] = -安全性  # 最大化安全性

            # 计算约束条件（假设所有约束都是<=0的形式）
            for loc_id, weight in location_weights.items():
                loc = next((l for l in self.all_locations if l.location_id == loc_id), None)
                if loc:
                    承重约束 += max(0, weight - loc.load_capacity)

            for loc_id, height in location_heights.items():
                loc = next((l for l in self.all_locations if l.location_id == loc_id), None)
                if loc and loc_id.startswith('YARD_'):
                    堆高约束 += max(0, height - loc.max_stack_height)

            G[i, 0] = 承重约束
            G[i, 1] = 堆高约束

        out["F"] = F
        out["G"] = G

class CustomDisplay(Display):
    def _do(self, problem, evaluator, algorithm):
        super()._do(problem, evaluator, algorithm)
        self.output.append("出库效率", -algorithm.pop.get("F")[:, 0].mean())
        self.output.append("空间利用率", -algorithm.pop.get("F")[:, 1].mean())
        self.output.append("安全性", -algorithm.pop.get("F")[:, 2].mean())

def optimize_stacking(cargo_list, yard_locations, warehouses, equipment):
    # 创建问题实例
    problem = StackingProblem(cargo_list, yard_locations, warehouses, equipment)

    # 创建NSGA-III算法实例
    ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)
    algorithm = NSGA3(
        pop_size=100,
        ref_dirs=ref_dirs,
        display=CustomDisplay()
    )

    # 运行优化
    res = minimize(
        problem,
        algorithm,
        termination=('n_gen', 50),
        seed=1,
        verbose=True
    )

    # 提取最优解
    solutions = []
    for i in range(len(res.X)):
        solution = {
            'objectives': {
                '出库效率': -res.F[i, 0],
                '空间利用率': -res.F[i, 1],
                '安全性': -res.F[i, 2]
            },
            'assignments': []
        }

        for j in range(len(res.X[i])):
            cargo = cargo_list[j]
            location_idx = int(res.X[i, j])
            location = problem.all_locations[location_idx]

            solution['assignments'].append({
                'cargo_id': cargo.cargo_id,
                'location': location.location_id,
                'location_type': '堆场' if location.location_id.startswith('YARD_') else '仓库',
                'stack_height': float(cargo.dimensions.split('x')[2]) if location.location_id.startswith('YARD_') else 0
            })

        solutions.append(solution)

    return solutions