from flask import Blueprint, request, jsonify
from models import Warehouse, YardLocation, db

warehouse_bp = Blueprint('warehouse', __name__)

@warehouse_bp.route('/add', methods=['POST'])
def add_warehouse():
    data = request.json
    
    new_warehouse = Warehouse(
        warehouse_id=data['warehouse_id'],
        area=data['area'],
        height=data['height'],
        load_capacity=data['load_capacity'],
        rack_type=data.get('rack_type'),
        rack_height=data.get('rack_height'),
        aisle_width=data.get('aisle_width'),
        access_distance=data.get('access_distance', 0),
        safety_zone=data.get('safety_zone'),
        env_conditions=data.get('env_conditions'),
        coordinates=data.get('coordinates'),
        available_racks=data.get('available_racks', 0),
        available_capacity=data.get('available_capacity', 0),
        current_load=data.get('current_load', 0)
    )
    
    try:
        db.session.add(new_warehouse)
        db.session.commit()
        return jsonify({'message': 'Warehouse added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@warehouse_bp.route('/list', methods=['GET'])
def list_warehouses():
    warehouses = Warehouse.query.all()
    
    result = [
        {
            'warehouse_id': warehouse.warehouse_id,
            'area': warehouse.area,
            'height': warehouse.height,
            'load_capacity': warehouse.load_capacity,
            'rack_type': warehouse.rack_type,
            'available_racks': warehouse.available_racks,
            'available_capacity': warehouse.available_capacity,
            'current_load': warehouse.current_load
        } for warehouse in warehouses
    ]
    
    return jsonify(result), 200

@warehouse_bp.route('/<warehouse_id>', methods=['GET'])
def get_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    warehouse_data = {
        'warehouse_id': warehouse.warehouse_id,
        'area': warehouse.area,
        'height': warehouse.height,
        'load_capacity': warehouse.load_capacity,
        'rack_type': warehouse.rack_type,
        'rack_height': warehouse.rack_height,
        'aisle_width': warehouse.aisle_width,
        'access_distance': warehouse.access_distance,
        'safety_zone': warehouse.safety_zone,
        'env_conditions': warehouse.env_conditions,
        'coordinates': warehouse.coordinates,
        'available_racks': warehouse.available_racks,
        'available_capacity': warehouse.available_capacity,
        'current_load': warehouse.current_load
    }
    
    return jsonify(warehouse_data), 200

@warehouse_bp.route('/<warehouse_id>', methods=['PUT'])
def update_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(warehouse, key):
            setattr(warehouse, key, value)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Warehouse updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@warehouse_bp.route('/<warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    try:
        db.session.delete(warehouse)
        db.session.commit()
        return jsonify({'message': 'Warehouse deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@warehouse_bp.route('/available', methods=['GET'])
def get_available_warehouses():
    min_capacity = request.args.get('min_capacity', type=float)
    
    if min_capacity:
        warehouses = Warehouse.query.filter(Warehouse.available_capacity >= min_capacity).all()
    else:
        warehouses = Warehouse.query.filter(Warehouse.available_capacity > 0).all()
    
    result = [
        {
            'warehouse_id': warehouse.warehouse_id,
            'available_capacity': warehouse.available_capacity,
            'load_capacity': warehouse.load_capacity,
            'rack_type': warehouse.rack_type,
            'env_conditions': warehouse.env_conditions
        } for warehouse in warehouses
    ]
    
    return jsonify(result), 200    