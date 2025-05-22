from app import db
from models import Cargo, YardLocation, Warehouse, Equipment
from datetime import datetime, timedelta

def initialize_database():
    # 创建所有表
    db.create_all()
    
    # 添加示例堆场位置
    yard_locations = [
        YardLocation(
            location_id="YARD_A1",
            sub_area_type="高周转",
            area=1000,
            load_capacity=5000,
            max_stack_height=10,
            terrain_type="平坦",
            access_distance=10,
            safety_zone="普通",
            weather_protection="露天",
            env_conditions="干燥",
            coordinates="10,20"
        ),
        YardLocation(
            location_id="YARD_A2",
            sub_area_type="高周转",
            area=800,
            load_capacity=4000,
            max_stack_height=8,
            terrain_type="平坦",
            access_distance=15,
            safety_zone="普通",
            weather_protection="露天",
            env_conditions="干燥",
            coordinates="30,20"
        ),
        YardLocation(
            location_id="YARD_B1",
            sub_area_type="中周转",
            area=1200,
            load_capacity=6000,
            max_stack_height=12,
            terrain_type="平坦",
            access_distance=20,
            safety_zone="普通",
            weather_protection="露天",
            env_conditions="干燥",
            coordinates="10,50"
        ),
        YardLocation(
            location_id="YARD_C1",
            sub_area_type="低周转",
            area=1500,
            load_capacity=8000,
            max_stack_height=15,
            terrain_type="平坦",
            access_distance=30,
            safety_zone="普通",
            weather_protection="露天",
            env_conditions="干燥",
            coordinates="50,50"
        ),
        YardLocation(
            location_id="YARD_H1",
            sub_area_type="危险品",
            area=300,
            load_capacity=1000,
            max_stack_height=5,
            terrain_type="平坦",
            access_distance=40,
            safety_zone="隔离区",
            weather_protection="半封闭",
            env_conditions="通风",
            coordinates="70,10"
        )
    ]
    
    # 添加示例仓库
    warehouses = [
        Warehouse(
            warehouse_id="WAREHOUSE_1",
            area=2000,
            height=15,
            load_capacity=10000,
            rack_type="重型货架",
            rack_height=10,
            aisle_width=3,
            access_distance=15,
            safety_zone="普通",
            env_conditions="常温",
            coordinates="20,80",
            available_racks=50,
            available_capacity=1500
        ),
        Warehouse(
            warehouse_id="WAREHOUSE_2",
            area=1500,
            height=10,
            load_capacity=8000,
            rack_type="中型货架",
            rack_height=6,
            aisle_width=2.5,
            access_distance=25,
            safety_zone="普通",
            env_conditions="常温",
            coordinates="60,80",
            available_racks=30,
            available_capacity=1000
        ),
        Warehouse(
            warehouse_id="WAREHOUSE_COLD",
            area=500,
            height=8,
            load_capacity=3000,
            rack_type="冷藏货架",
            rack_height=4,
            aisle_width=2,
            access_distance=30,
            safety_zone="普通",
            env_conditions="冷藏(-20℃)",
            coordinates="80,40",
            available_racks=10,
            available_capacity=200
        )
    ]
    
    # 添加示例设备
    equipment = [
        Equipment(
            equipment_id="FORKLIFT_01",
            equipment_type="叉车",
            load_capacity=5,
            max_height=7,
            power_type="柴油",
            corrosion_resistance=False,
            status="闲置",
            last_maintenance=datetime.now() - timedelta(days=30),
            next_maintenance=datetime.now() + timedelta(days=60)
        ),
        Equipment(
            equipment_id="FORKLIFT_02",
            equipment_type="叉车",
            load_capacity=3,
            max_height=5,
            power_type="电动",
            corrosion_resistance=False,
            status="闲置",
            last_maintenance=datetime.now() - timedelta(days=45),
            next_maintenance=datetime.now() + timedelta(days=45)
        ),
        Equipment(
            equipment_id="CRANE_01",
            equipment_type="起重机",
            load_capacity=20,
            max_height=15,
            power_type="电动",
            corrosion_resistance=True,
            status="工作中",
            last_maintenance=datetime.now() - timedelta(days=60),
            next_maintenance=datetime.now() + timedelta(days=30)
        ),
        Equipment(
            equipment_id="REACH_TRUCK_01",
            equipment_type="前移式叉车",
            load_capacity=2,
            max_height=10,
            power_type="电动",
            corrosion_resistance=False,
            status="闲置",
            last_maintenance=datetime.now() - timedelta(days=15),
            next_maintenance=datetime.now() + timedelta(days=75)
        )
    ]
    
    # 添加示例货物（在初始化时不添加，因为会在运行时动态添加）
    
    # 将所有对象添加到数据库
    db.session.add_all(yard_locations)
    db.session.add_all(warehouses)
    db.session.add_all(equipment)
    
    # 提交更改
    db.session.commit()
    
    print("数据库初始化完成！")

if __name__ == '__main__':
    initialize_database()    