from flask import Blueprint, request, jsonify
from models import Cargo, YardLocation, Warehouse, Equipment, db
from algorithms.nsga3_optimizer import optimize_stacking
from algorithms.topsis import evaluate_solutions
from algorithms.lstm_model import predict_out_time
import numpy as np
from datetime import timedelta

optimization_bp = Blueprint('optimization', __name__)

@optimization_bp.route('/generate_optimization', methods=['POST'])
def generate_optimization():
    data = request.json

    # 获取货物信息（可以是单个货物或多个货物）
    if 'cargo_ids' in data:
        cargo_list = Cargo.query.filter(Cargo.cargo_id.in_(data['cargo_ids'])).all()
    elif 'cargo_type' in data:
        cargo_list = Cargo.query.filter_by(cargo_type=data['cargo_type']).all()
    else:
        return jsonify({'error': 'No cargo specified'}), 400

    if not cargo_list:
        return jsonify({'error': 'No cargo found'}), 404

    # 获取可用的堆场位置
    yard_locations = YardLocation.query.filter(
        YardLocation.current_load < YardLocation.load_capacity,
        YardLocation.current_height < YardLocation.max_stack_height
    ).all()

    # 获取可用的仓库
    warehouses = Warehouse.query.filter(
        Warehouse.available_capacity > 0
    ).all()

    # 获取可用的设备
    equipment = Equipment.query.filter_by(status='闲置').all()

    # 预测每个货物的出库时间（使用LSTM模型）
    for cargo in cargo_list:
        if not cargo.expected_out_time:
            # 从数据库获取历史数据进行预测
            # 实际应用中可能需要更复杂的特征工程
            features = get_cargo_features(cargo)
            predicted_days = predict_out_time(features)
            cargo.expected_out_time = cargo.entry_time + timedelta(days=predicted_days)

    # 运行NSGA-III优化算法
    solutions = optimize_stacking(
        cargo_list=cargo_list,
        yard_locations=yard_locations,
        warehouses=warehouses,
        equipment=equipment
    )

    # 使用TOPSIS评估最优方案
    best_solution = evaluate_solutions(solutions)

    # 应用最优方案（更新数据库）
    apply_optimization_solution(best_solution)

    return jsonify({
        'message': 'Optimization completed successfully',
        'solution': best_solution
    }), 200

def get_cargo_features(cargo):
    # 从数据库获取特征，用于LSTM预测
    # 实际应用中可能需要更复杂的特征工程
    return np.array([[
        cargo.weight,
        cargo.dimensions.split('x')[0],  # 长度
        cargo.dimensions.split('x')[1],  # 宽度
        cargo.dimensions.split('x')[2],  # 高度
        1 if cargo.is_hazardous else 0
    ]])

def apply_optimization_solution(solution):
    # 将优化方案应用到数据库
    for assignment in solution['assignments']:
        cargo = Cargo.query.get(assignment['cargo_id'])
        location = assignment['location']

        if location.startswith('YARD_'):
            # 更新堆场位置
            yard = YardLocation.query.get(location)
            yard.current_load += cargo.weight
            yard.current_height = max(yard.current_height, assignment.get('stack_height', 0))
            cargo.current_location = location
        elif location.startswith('WAREHOUSE_'):
            # 更新仓库位置
            warehouse = Warehouse.query.get(location)
            warehouse.current_load += cargo.weight
            warehouse.available_capacity -= (cargo.dimensions.split('x')[0] *
                                           cargo.dimensions.split('x')[1] *
                                           cargo.dimensions.split('x')[2]) / 1000  # 转换为立方米
            cargo.current_location = location

    db.session.commit()