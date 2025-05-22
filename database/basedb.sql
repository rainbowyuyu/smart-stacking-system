-- 创建堆场位置表
CREATE TABLE IF NOT EXISTS yard_location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    location_id VARCHAR(255) NOT NULL UNIQUE,
    sub_area_type VARCHAR(255) NOT NULL,
    area FLOAT NOT NULL,
    load_capacity FLOAT NOT NULL,
    max_stack_height INT NOT NULL,
    terrain_type VARCHAR(255) NOT NULL,
    access_distance INT NOT NULL,
    safety_zone VARCHAR(255) NOT NULL,
    weather_protection VARCHAR(255) NOT NULL,
    env_conditions VARCHAR(255) NOT NULL,
    coordinates VARCHAR(255) NOT NULL
);

-- 创建仓库表
CREATE TABLE IF NOT EXISTS warehouse (
    id INT PRIMARY KEY AUTO_INCREMENT,
    warehouse_id VARCHAR(255) NOT NULL UNIQUE,
    area FLOAT NOT NULL,
    height FLOAT NOT NULL,
    load_capacity FLOAT NOT NULL,
    rack_type VARCHAR(255) NOT NULL,
    rack_height FLOAT NOT NULL,
    aisle_width FLOAT NOT NULL,
    access_distance INT NOT NULL,
    safety_zone VARCHAR(255) NOT NULL,
    env_conditions VARCHAR(255) NOT NULL,
    coordinates VARCHAR(255) NOT NULL,
    available_racks INT NOT NULL,
    available_capacity FLOAT NOT NULL
);

-- 创建设备表
CREATE TABLE IF NOT EXISTS equipment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    equipment_id VARCHAR(255) NOT NULL UNIQUE,
    equipment_type VARCHAR(255) NOT NULL,
    load_capacity FLOAT NOT NULL,
    max_height FLOAT NOT NULL,
    power_type VARCHAR(255) NOT NULL,
    corrosion_resistance BOOLEAN NOT NULL,
    status VARCHAR(255) NOT NULL,
    last_maintenance DATETIME NOT NULL,
    next_maintenance DATETIME NOT NULL
);

-- 创建货物表
CREATE TABLE IF NOT EXISTS cargo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cargo_id VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    weight FLOAT NOT NULL,
    volume FLOAT NOT NULL,
    type VARCHAR(255) NOT NULL,
    storage_requirements VARCHAR(255) NOT NULL,
    handling_requirements VARCHAR(255) NOT NULL,
    priority INT NOT NULL,
    entry_date DATETIME NOT NULL,
    expected_departure_date DATETIME,
    actual_departure_date DATETIME,
    current_location VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    stackable BOOLEAN NOT NULL,
    max_stack_height INT,
    stack_position INT,
    special_notes VARCHAR(255),
    is_hazardous BOOLEAN NOT NULL,
    hazard_class VARCHAR(255),
    temperature_requirement VARCHAR(255),
    humidity_requirement VARCHAR(255),
    storage_location_id VARCHAR(255),
    FOREIGN KEY (storage_location_id) REFERENCES yard_location (location_id)
);

-- 开始事务
START TRANSACTION;

-- 插入示例堆场位置数据 (使用 INSERT IGNORE)
INSERT IGNORE INTO yard_location (location_id, sub_area_type, area, load_capacity, max_stack_height, terrain_type, access_distance, safety_zone, weather_protection, env_conditions, coordinates) VALUES
('YARD_A1', '高周转', 1000, 5000, 10, '平坦', 10, '普通', '露天', '干燥', '10,20'),
('YARD_A2', '高周转', 800, 4000, 8, '平坦', 15, '普通', '露天', '干燥', '30,20'),
('YARD_B1', '中周转', 1200, 6000, 12, '平坦', 20, '普通', '露天', '干燥', '10,50'),
('YARD_C1', '低周转', 1500, 8000, 15, '平坦', 30, '普通', '露天', '干燥', '50,50'),
('YARD_H1', '危险品', 300, 1000, 5, '平坦', 40, '隔离区', '半封闭', '通风', '70,10');


-- 插入示例仓库数据
INSERT IGNORE INTO warehouse (warehouse_id, area, height, load_capacity, rack_type, rack_height, aisle_width, access_distance, safety_zone, env_conditions, coordinates, available_racks, available_capacity) VALUES
('WAREHOUSE_1', 2000, 15, 10000, '重型货架', 10, 3, 15, '普通', '常温', '20,80', 50, 1500),
('WAREHOUSE_2', 1500, 10, 8000, '中型货架', 6, 2.5, 25, '普通', '常温', '60,80', 30, 1000),
('WAREHOUSE_COLD', 500, 8, 3000, '冷藏货架', 4, 2, 30, '普通', '冷藏(-20℃)', '80,40', 10, 200);

-- 插入示例设备数据
INSERT IGNORE INTO equipment (equipment_id, equipment_type, load_capacity, max_height, power_type, corrosion_resistance, status, last_maintenance, next_maintenance) VALUES
('FORKLIFT_01', '叉车', 5, 7, '柴油', 0, '闲置', DATE_SUB(NOW(), INTERVAL 30 DAY), DATE_ADD(NOW(), INTERVAL 60 DAY)),
('FORKLIFT_02', '叉车', 3, 5, '电动', 0, '闲置', DATE_SUB(NOW(), INTERVAL 45 DAY), DATE_ADD(NOW(), INTERVAL 45 DAY)),
('CRANE_01', '起重机', 20, 15, '电动', 1, '工作中', DATE_SUB(NOW(), INTERVAL 60 DAY), DATE_ADD(NOW(), INTERVAL 30 DAY)),
('REACH_TRUCK_01', '前移式叉车', 2, 10, '电动', 0, '闲置', DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_ADD(NOW(), INTERVAL 75 DAY));

-- 提交事务
COMMIT;

-- 显示初始化完成信息
SELECT '数据库初始化完成！' AS message;
