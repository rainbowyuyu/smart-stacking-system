from flask import Blueprint, request, jsonify
from models import Cargo, db
from datetime import datetime

cargo_bp = Blueprint('cargo', __name__)

@cargo_bp.route('/add', methods=['POST'])
def add_cargo():
    data = request.json
    
    # 检查必要字段
    required_fields = ['cargo_id', 'cargo_type', 'weight', 'dimensions']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # 处理日期字段
    if 'entry_time' in data:
        data['entry_time'] = datetime.strptime(data['entry_time'], '%Y-%m-%d %H:%M:%S')
    if 'expected_out_time' in data:
        data['expected_out_time'] = datetime.strptime(data['expected_out_time'], '%Y-%m-%d %H:%M:%S')
    
    # 创建新货物
    new_cargo = Cargo(**data)
    
    try:
        db.session.add(new_cargo)
        db.session.commit()
        return jsonify({'message': 'Cargo added successfully', 'cargo_id': new_cargo.cargo_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cargo_bp.route('/list', methods=['GET'])
def list_cargo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    cargo_list = Cargo.query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = {
        'items': [
            {
                'cargo_id': cargo.cargo_id,
                'cargo_type': cargo.cargo_type,
                'weight': cargo.weight,
                'dimensions': cargo.dimensions,
                'entry_time': cargo.entry_time.strftime('%Y-%m-%d %H:%M:%S') if cargo.entry_time else None,
                'current_location': cargo.current_location
            } for cargo in cargo_list.items
        ],
        'total_pages': cargo_list.pages,
        'total_items': cargo_list.total
    }
    
    return jsonify(result), 200

@cargo_bp.route('/<cargo_id>', methods=['GET'])
def get_cargo(cargo_id):
    cargo = Cargo.query.get_or_404(cargo_id)
    
    cargo_data = {
        'cargo_id': cargo.cargo_id,
        'cargo_type': cargo.cargo_type,
        'brand': cargo.brand,
        'weight': cargo.weight,
        'dimensions': cargo.dimensions,
        'stack_height_max': cargo.stack_height_max,
        'is_hazardous': cargo.is_hazardous,
        'hazard_class': cargo.hazard_class,
        'turnover_rate': cargo.turnover_rate,
        'entry_time': cargo.entry_time.strftime('%Y-%m-%d %H:%M:%S') if cargo.entry_time else None,
        'expected_out_time': cargo.expected_out_time.strftime('%Y-%m-%d %H:%M:%S') if cargo.expected_out_time else None,
        'current_location': cargo.current_location
    }
    
    return jsonify(cargo_data), 200

@cargo_bp.route('/<cargo_id>', methods=['PUT'])
def update_cargo(cargo_id):
    cargo = Cargo.query.get_or_404(cargo_id)
    data = request.json
    
    # 更新字段
    for key, value in data.items():
        if hasattr(cargo, key):
            if key in ['entry_time', 'expected_out_time'] and value:
                setattr(cargo, key, datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
            else:
                setattr(cargo, key, value)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Cargo updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cargo_bp.route('/<cargo_id>', methods=['DELETE'])
def delete_cargo(cargo_id):
    cargo = Cargo.query.get_or_404(cargo_id)
    
    try:
        db.session.delete(cargo)
        db.session.commit()
        return jsonify({'message': 'Cargo deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cargo_bp.route('/search', methods=['GET'])
def search_cargo():
    # 示例：按类型和周转率搜索
    cargo_type = request.args.get('type')
    turnover_rate = request.args.get('turnover_rate')
    
    query = Cargo.query
    
    if cargo_type:
        query = query.filter(Cargo.cargo_type == cargo_type)
    if turnover_rate:
        query = query.filter(Cargo.turnover_rate == turnover_rate)
    
    results = query.all()
    
    return jsonify([{
        'cargo_id': cargo.cargo_id,
        'cargo_type': cargo.cargo_type,
        'weight': cargo.weight,
        'turnover_rate': cargo.turnover_rate,
        'current_location': cargo.current_location
    } for cargo in results]), 200    