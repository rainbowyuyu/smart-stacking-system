from app import db
from models import Cargo
from datetime import datetime, timedelta
import random

def populate_sample_data(num_cargos=50):
    # 货物类型
    cargo_types = ["集装箱", "散货", "件杂货", "液体货物", "冷冻货物"]
    
    # 品牌
    brands = ["ABC", "XYZ", "DEF", "GHI", "JKL", "MNO"]
    
    # 周转率
    turnover_rates = ["高", "中", "低"]
    
    # 下一个目的地
    destinations = ["港口A", "港口B", "港口C", "仓库1", "仓库2", "工厂1", "工厂2"]
    
    # 随机生成货物数据
    for i in range(1, num_cargos + 1):
        cargo_id = f"CARGO_{i:03d}"
        cargo_type = random.choice(cargo_types)
        brand = random.choice(brands)
        weight = round(random.uniform(1, 50), 2)  # 1-50吨
        
        # 根据货物类型生成不同的尺寸
        if cargo_type == "集装箱":
            length = round(random.uniform(2, 12), 2)  # 20英尺或40英尺集装箱
            width = 2.44  # 标准宽度
            height = round(random.uniform(2.5, 2.9), 2)  # 标准高度
        elif cargo_type == "散货":
            length = round(random.uniform(1, 5), 2)
            width = round(random.uniform(1, 5), 2)
            height = round(random.uniform(0.5, 3), 2)
        else:
            length = round(random.uniform(0.5, 3), 2)
            width = round(random.uniform(0.5, 3), 2)
            height = round(random.uniform(0.5, 3), 2)
        
        dimensions = f"{length}x{width}x{height}"
        
        # 堆高限制
        stack_height_max = height * random.randint(1, 5)
        
        # 是否危险品
        is_hazardous = random.random() < 0.1  # 10%的概率是危险品
        hazard_class = random.choice(["爆炸品", "易燃液体", "氧化剂", "有毒物质", None]) if is_hazardous else None
        
        # 存储要求
        storage_requirement = None
        if cargo_type == "冷冻货物":
            storage_requirement = "冷藏"
        elif is_hazardous:
            storage_requirement = "隔离存放"
        
        # 周转率
        turnover_rate = random.choice(turnover_rates)
        
        # 下一个目的地
        next_destination = random.choice(destinations)
        
        # 入库时间（过去30天内的随机时间）
        entry_time = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # 预期出库时间（入库时间+1-60天）
        expected_out_time = entry_time + timedelta(days=random.randint(1, 60))
        
        # 时间窗口优先级
        time_window_priority = round(random.uniform(0.1, 0.9), 2)
        
        # 实际出库时间（有些货物已经出库）
        actual_out_time = None
        if random.random() < 0.3:  # 30%的货物已经出库
            actual_out_time = entry_time + timedelta(days=random.randint(1, (expected_out_time - entry_time).days + 5))
        
        # 创建货物对象
        cargo = Cargo(
            cargo_id=cargo_id,
            cargo_type=cargo_type,
            brand=brand,
            weight=weight,
            dimensions=dimensions,
            stack_height_max=stack_height_max,
            stack_compatibility=None,
            is_hazardous=is_hazardous,
            hazard_class=hazard_class,
            storage_requirement=storage_requirement,
            turnover_rate=turnover_rate,
            next_destination=next_destination,
            expected_out_time=expected_out_time,
            entry_time=entry_time,
            time_window_priority=time_window_priority,
            actual_out_time=actual_out_time
        )
        
        db.session.add(cargo)
    
    # 提交更改
    db.session.commit()
    
    print(f"已成功添加{num_cargos}条示例货物数据！")

if __name__ == '__main__':
    populate_sample_data(50)    