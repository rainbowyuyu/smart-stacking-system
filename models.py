from database import db
from datetime import datetime

class Cargo(db.Model):
    __tablename__ = 'cargo'
    cargo_id = db.Column(db.String(50), primary_key=True)
    cargo_type = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String(30))
    weight = db.Column(db.Float, nullable=False, default=0)
    dimensions = db.Column(db.String(50), nullable=False)
    stack_height_max = db.Column(db.Float, default=0)
    stack_compatibility = db.Column(db.String(100))
    is_hazardous = db.Column(db.Boolean, nullable=False, default=False)
    hazard_class = db.Column(db.String(10))
    storage_requirement = db.Column(db.String(50))
    turnover_rate = db.Column(db.String(10), nullable=False, default='中')
    next_destination = db.Column(db.String(50))
    expected_out_time = db.Column(db.DateTime)
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_window_priority = db.Column(db.Float, nullable=False, default=0.5)
    current_location = db.Column(db.String(50))
    actual_out_time = db.Column(db.DateTime)  # 实际出库时间，用于LSTM训练

class YardLocation(db.Model):
    __tablename__ = 'yard_location'
    location_id = db.Column(db.String(30), primary_key=True)
    parent_location_id = db.Column(db.String(20))
    sub_area_type = db.Column(db.String(20), nullable=False)
    area = db.Column(db.Float, nullable=False, default=0)
    load_capacity = db.Column(db.Float, nullable=False, default=0)
    max_stack_height = db.Column(db.Float, default=0)
    terrain_type = db.Column(db.String(20), nullable=False)
    access_distance = db.Column(db.Float, nullable=False, default=0)
    safety_zone = db.Column(db.String(50))
    weather_protection = db.Column(db.String(50))
    env_conditions = db.Column(db.String(50))
    coordinates = db.Column(db.String(50))
    current_load = db.Column(db.Float, default=0)  # 当前负载
    current_height = db.Column(db.Float, default=0)  # 当前堆高

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    warehouse_id = db.Column(db.String(30), primary_key=True)
    area = db.Column(db.Float, nullable=False, default=0)
    height = db.Column(db.Float, nullable=False, default=0)
    load_capacity = db.Column(db.Float, nullable=False, default=0)
    rack_type = db.Column(db.String(20))
    rack_height = db.Column(db.Float)
    aisle_width = db.Column(db.Float)
    access_distance = db.Column(db.Float, nullable=False, default=0)
    safety_zone = db.Column(db.String(50))
    env_conditions = db.Column(db.String(50))
    coordinates = db.Column(db.String(50))
    available_racks = db.Column(db.Integer, default=0)
    available_capacity = db.Column(db.Float, default=0)
    current_load = db.Column(db.Float, default=0)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipment_id = db.Column(db.String(20), primary_key=True)
    equipment_type = db.Column(db.String(20), nullable=False)
    load_capacity = db.Column(db.Float, nullable=False, default=0)
    max_height = db.Column(db.Float, default=0)
    power_type = db.Column(db.String(20), nullable=False)
    corrosion_resistance = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(10), nullable=False, default='闲置')
    last_maintenance = db.Column(db.DateTime)
    next_maintenance = db.Column(db.DateTime)    