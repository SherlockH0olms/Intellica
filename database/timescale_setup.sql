-- TimescaleDB Hypertable Setup for Time-Series Data

-- Sensor data hypertable
CREATE TABLE IF NOT EXISTS sensor_data (
    time TIMESTAMPTZ NOT NULL,
    machine_id UUID NOT NULL,
    sensor_name VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20)
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_sensor_data_machine_time 
ON sensor_data (machine_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_name 
ON sensor_data (sensor_name, time DESC);

-- Continuous aggregate for 5-minute intervals
CREATE MATERIALIZED VIEW IF NOT EXISTS sensor_data_5min
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('5 minutes', time) AS bucket,
    machine_id,
    sensor_name,
    AVG(value) as avg_value,
    MAX(value) as max_value,
    MIN(value) as min_value,
    STDDEV(value) as stddev_value,
    COUNT(*) as sample_count
FROM sensor_data
GROUP BY bucket, machine_id, sensor_name;

-- Continuous aggregate for 1-hour intervals
CREATE MATERIALIZED VIEW IF NOT EXISTS sensor_data_1hour
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS bucket,
    machine_id,
    sensor_name,
    AVG(value) as avg_value,
    MAX(value) as max_value,
    MIN(value) as min_value,
    STDDEV(value) as stddev_value,
    COUNT(*) as sample_count
FROM sensor_data
GROUP BY bucket, machine_id, sensor_name;

-- Data retention policy (keep raw data for 30 days)
SELECT add_retention_policy('sensor_data', INTERVAL '30 days', if_not_exists => TRUE);

-- Compression policy (compress data older than 7 days)
ALTER TABLE sensor_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'machine_id, sensor_name'
);

SELECT add_compression_policy('sensor_data', INTERVAL '7 days', if_not_exists => TRUE);