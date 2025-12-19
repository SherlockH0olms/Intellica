-- Seed Data for Intellica Demo

-- Insert sample machines
INSERT INTO machines (id, name, type, manufacturer, model, location_x, location_y, protocol, status) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'CNC_001', 'CNC', 'Fanuc', 'Robodrill D21LIA5', 150, 200, 'MQTT', 'running'),
('550e8400-e29b-41d4-a716-446655440002', 'INJ_001', 'Injection Molding', 'Engel', 'e-victory 200', 400, 250, 'OPC-UA', 'running'),
('550e8400-e29b-41d4-a716-446655440003', 'CONV_001', 'Conveyor', 'Siemens', 'Simatic S7', 650, 200, 'Modbus', 'idle')
ON CONFLICT (id) DO NOTHING;

-- Insert sample users
INSERT INTO users (username, email, hashed_password, role, full_name) VALUES
('admin', 'admin@intellica.az', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsKEYw8h.W1K', 'admin', 'System Administrator'),
('operator1', 'operator1@intellica.az', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsKEYw8h.W1K', 'operator', 'Operator User'),
('viewer1', 'viewer1@intellica.az', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsKEYw8h.W1K', 'viewer', 'Viewer User')
ON CONFLICT (username) DO NOTHING;

-- Insert sample sensor data (last 1 hour)
INSERT INTO sensor_data (time, machine_id, sensor_name, value, unit)
SELECT 
    NOW() - (random() * INTERVAL '1 hour'),
    '550e8400-e29b-41d4-a716-446655440001',
    'spindle_temp',
    70 + (random() * 10),
    'celsius'
FROM generate_series(1, 100);

INSERT INTO sensor_data (time, machine_id, sensor_name, value, unit)
SELECT 
    NOW() - (random() * INTERVAL '1 hour'),
    '550e8400-e29b-41d4-a716-446655440001',
    'vibration_x',
    0.01 + (random() * 0.005),
    'mm/s'
FROM generate_series(1, 100);

-- Insert sample alerts
INSERT INTO alerts (machine_id, alert_type, severity, description, status) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'anomaly', 'warning', 'Elevated vibration detected', 'open'),
('550e8400-e29b-41d4-a716-446655440002', 'predictive_maintenance', 'info', 'Maintenance recommended in 5 days', 'open');

-- Insert sample defects
INSERT INTO defects (product_id, machine_id, defect_type, confidence, bbox) VALUES
('PROD_2025_001234', '550e8400-e29b-41d4-a716-446655440001', 'scratch', 0.92, '{"x1": 120, "y1": 80, "x2": 240, "y2": 200}'),
('PROD_2025_001235', '550e8400-e29b-41d4-a716-446655440002', 'crack', 0.87, '{"x1": 150, "y1": 100, "x2": 300, "y2": 250}');

COMMIT;