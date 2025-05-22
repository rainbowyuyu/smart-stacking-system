-- 批量插入更多堆场位置数据
INSERT IGNORE INTO yard_location (location_id, sub_area_type, area, load_capacity, max_stack_height, terrain_type, access_distance, safety_zone, weather_protection, env_conditions, coordinates) VALUES
('YARD_A3', '高周转', 900, 4500, 9, '平坦', 12, '普通', '露天', '干燥', '15,25'),
('YARD_B2', '中周转', 1100, 5500, 11, '平坦', 18, '普通', '露天', '干燥', '20,45'),
('YARD_C2', '低周转', 1600, 8500, 16, '平坦', 35, '普通', '露天', '干燥', '55,55'),
('YARD_H2', '危险品', 350, 1200, 6, '平坦', 42, '隔离区', '半封闭', '通风', '72,12'),
('YARD_D1', '特种', 400, 2000, 7, '起伏', 25, '普通', '封闭', '干燥', '40,60');

-- 批量插入更多仓库数据
INSERT IGNORE INTO warehouse (warehouse_id, area, height, load_capacity, rack_type, rack_height, aisle_width, access_distance, safety_zone, env_conditions, coordinates, available_racks, available_capacity) VALUES
('WAREHOUSE_3', 1800, 12, 9000, '轻型货架', 7, 2.8, 20, '普通', '常温', '25,85', 40, 1200),
('WAREHOUSE_COLD2', 600, 9, 3500, '冷藏货架', 5, 2.2, 28, '普通', '冷藏(-18℃)', '85,45', 12, 250),
('WAREHOUSE_SPECIAL', 700, 11, 4000, '防爆货架', 6, 3, 30, '隔离区', '防爆', '90,50', 15, 300);

-- 批量插入更多设备数据
INSERT IGNORE INTO equipment (equipment_id, equipment_type, load_capacity, max_height, power_type, corrosion_resistance, status, last_maintenance, next_maintenance) VALUES
('FORKLIFT_03', '叉车', 4, 6, '电动', 0, '闲置', DATE_SUB(NOW(), INTERVAL 20 DAY), DATE_ADD(NOW(), INTERVAL 70 DAY)),
('CRANE_02', '起重机', 25, 18, '柴油', 1, '工作中', DATE_SUB(NOW(), INTERVAL 50 DAY), DATE_ADD(NOW(), INTERVAL 40 DAY)),
('REACH_TRUCK_02', '前移式叉车', 3, 9, '电动', 0, '维修中', DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_ADD(NOW(), INTERVAL 90 DAY)),
('CONVEYOR_01', '输送机', 2, 0, '电动', 0, '闲置', DATE_SUB(NOW(), INTERVAL 60 DAY), DATE_ADD(NOW(), INTERVAL 30 DAY));

-- 批量插入部分货物数据示例
INSERT IGNORE INTO cargo (cargo_id, name, weight, volume, type, storage_requirements, handling_requirements, priority, entry_date, expected_departure_date, actual_departure_date, current_location, status, stackable, max_stack_height, stack_position, special_notes, is_hazardous, hazard_class, temperature_requirement, humidity_requirement, storage_location_id) VALUES
('CARGO_001', '电子元件', 500, 2, '电子', '防静电', '轻拿轻放', 1, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), NULL, 'WAREHOUSE_1', '存储中', TRUE, 5, 1, '', FALSE, NULL, '常温', '低湿', 'YARD_A1'),
('CARGO_002', '钢材', 2000, 10, '金属', '防雨', '机械搬运', 2, NOW(), DATE_ADD(NOW(), INTERVAL 60 DAY), NULL, 'YARD_B1', '存储中', FALSE, NULL, NULL, '注意防锈', FALSE, NULL, '露天', '干燥', 'YARD_B1'),
('CARGO_003', '化学品', 300, 1.5, '危险品', '防爆', '需专业操作', 1, NOW(), DATE_ADD(NOW(), INTERVAL 20 DAY), NULL, 'YARD_H1', '存储中', FALSE, NULL, NULL, '易燃易爆', TRUE, '易燃液体', '常温', '通风', 'YARD_H1');
