from flask import Blueprint, request, jsonify
from models import Equipment, db
from datetime import datetime

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route('/add', methods=['POST'])
def add_equipment():
    data = request.json
    
    # 处理日期字段
    if 'last_maintenance' in data:
        data['last_maintenance'] = datetime.strptime(data['last_maintenance'], '%Y-%m-%d')
    if 'next_maintenance' in data:
        data['next_maintenance'] = datetime.strptime(data['next_maintenance'], '%Y-%m-%d')
    
    new_equipment = Equipment(
        equipment_id=data['equipment_id'],
        equipment_type=data['equipment_type'],
        load_capacity=data['load_capacity'],
        max_height=data.get('max_height', 0),
        power_type=data['power_type'],
        corrosion_resistance=data.get('corrosion_resistance', False),
        status=data.get('status', '闲置'),
        last_maintenance=data.get('last_maintenance'),
        next_maintenance=data.get('next_maintenance')
    )
    
    try:
        db.session.add(new_equipment)
        db.session.commit()
        return jsonify({'message': 'Equipment added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@equipment_bp.route('/list', methods=['GET'])
def list_equipment():
    equipment_list = Equipment.query.all()
    
    result = [
        {
            'equipment_id': equipment.equipment_id,
            'equipment_type': equipment.equipment_type,
            'load_capacity': equipment.load_capacity,
            'max_height': equipment.max_height,
            'power_type': equipment.power_type,
            'status': equipment.status,
            'last_maintenance': equipment.last_maintenance.strftime('%Y-%m-%d') if equipment.last_maintenance else None,
            'next_maintenance': equipment.next_maintenance.strftime('%Y-%m-%d') if equipment.next_maintenance else None
        } for equipment in equipment_list
    ]
    
    return jsonify(result), 200

@equipment_bp.route('/<equipment_id>', methods=['GET'])
def get_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    
    equipment_data = {
        'equipment_id': equipment.equipment_id,
        'equipment_type': equipment.equipment_type,
        'load_capacity': equipment.load_capacity,
        'max_height': equipment.max_height,
        'power_type': equipment.power_type,
        'corrosion_resistance': equipment.corrosion_resistance,
        'status': equipment.status,
        'last_maintenance': equipment.last_maintenance.strftime('%Y-%m-%d') if equipment.last_maintenance else None,
        'next_maintenance': equipment.next_maintenance.strftime('%Y-%m-%d') if equipment.next_maintenance else None
    }
    
    return jsonify(equipment_data), 200

@equipment_bp.route('/<equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    data = request.json
    
    # 更新字段
    for key, value in data.items():
        if hasattr(equipment, key):
            if key in ['last_maintenance', 'next_maintenance'] and value:
                setattr(equipment, key, datetime.strptime(value, '%Y-%m-%d'))
            else:
                setattr(equipment, key, value)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Equipment updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@equipment_bp.route('/<equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    
    try:
        db.session.delete(equipment)
        db.session.commit()
        return jsonify({'message': 'Equipment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@equipment_bp.route('/available', methods=['GET'])
def get_available_equipment():
    equipment_type = request.args.get('type')
    min_capacity = request.args.get('min_capacity', type=float)
    
    query = Equipment.query.filter_by(status='闲置')
    
    if equipment_type:
        query = query.filter(Equipment.equipment_type == equipment_type)
    if min_capacity:
        query = query.filter(Equipment.load_capacity >= min_capacity)
    
    available_equipment = query.all()
    
    return jsonify([{
        'equipment_id': eq.equipment_id,
        'equipment_type': eq.equipment_type,
        'load_capacity': eq.load_capacity,
        'max_height': eq.max_height,
        'power_type': eq.power_type
    } for eq in available_equipment]), 200

@equipment_bp.route('/maintenance', methods=['GET'])
def get_equipment_needing_maintenance():
    today = datetime.now().date()
    
    # 查询需要维护的设备（维护日期已过或即将到期）
    equipment_list = Equipment.query.filter(
        (Equipment.next_maintenance <= today) | 
        ((Equipment.next_maintenance - today).days <= 7)  # 即将到期（7天内）
    ).all()
    
    return jsonify([{
        'equipment_id': eq.equipment_id,
        'equipment_type': eq.equipment_type,
        'last_maintenance': eq.last_maintenance.strftime('%Y-%m-%d') if eq.last_maintenance else None,
        'next_maintenance': eq.next_maintenance.strftime('%Y-%m-%d') if eq.next_maintenance else None,
        'days_until_maintenance': (eq.next_maintenance.date() - today).days if eq.next_maintenance else None
    } for eq in equipment_list]), 200    