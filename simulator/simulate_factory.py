#!/usr/bin/env python3
"""
Intelica Factory Simulator
Simulates sensor data from CNC, Injection Molding, and Conveyor machines
"""

import time
import json
import random
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt
import numpy as np

class MachineSimulator:
    """Base class for machine simulation"""
    
    def __init__(self, machine_id: str, machine_type: str):
        self.machine_id = machine_id
        self.machine_type = machine_type
        self.status = "running"
        
    def generate_sensor_data(self) -> dict:
        """Generate sensor data - to be overridden by subclasses"""
        raise NotImplementedError

class CNCSimulator(MachineSimulator):
    """CNC Machine Simulator"""
    
    def __init__(self, machine_id: str):
        super().__init__(machine_id, "CNC")
        self.spindle_temp_baseline = 70.0
        self.vibration_baseline = 0.01
        self.tool_wear = 0.0
        
    def generate_sensor_data(self) -> dict:
        # Normal operation with slight variations
        spindle_temp = self.spindle_temp_baseline + np.random.normal(0, 5)
        vibration_x = self.vibration_baseline + np.random.normal(0, 0.002)
        vibration_y = self.vibration_baseline + np.random.normal(0, 0.002)
        
        # Gradually increase tool wear
        self.tool_wear += 0.001
        
        # 5% chance of anomaly
        if random.random() < 0.05:
            spindle_temp += random.uniform(20, 40)
            vibration_x *= random.uniform(3, 5)
            vibration_y *= random.uniform(3, 5)
            
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "status": self.status,
            "sensors": {
                "spindle_temp": round(spindle_temp, 2),
                "vibration_x": round(vibration_x, 4),
                "vibration_y": round(vibration_y, 4),
                "spindle_speed": 2500,
                "feed_rate": 300,
                "tool_wear": round(self.tool_wear, 3),
                "torque": round(150 + np.random.normal(0, 10), 2)
            }
        }

class InjectionMoldingSimulator(MachineSimulator):
    """Injection Molding Machine Simulator"""
    
    def __init__(self, machine_id: str):
        super().__init__(machine_id, "Injection Molding")
        self.barrel_temp_baseline = 220.0
        self.cycle_count = 0
        
    def generate_sensor_data(self) -> dict:
        barrel_temp = self.barrel_temp_baseline + np.random.normal(0, 3)
        injection_pressure = 100 + np.random.normal(0, 5)
        cooling_time = 15 + np.random.normal(0, 1)
        
        self.cycle_count += 1
        
        # Occasional pressure spike
        if random.random() < 0.03:
            injection_pressure += random.uniform(20, 30)
            
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "status": self.status,
            "sensors": {
                "barrel_temp": round(barrel_temp, 2),
                "injection_pressure": round(injection_pressure, 2),
                "cooling_time": round(cooling_time, 2),
                "cycle_time": round(45 + np.random.normal(0, 2), 2),
                "cycle_count": self.cycle_count,
                "hydraulic_pressure": round(80 + np.random.normal(0, 5), 2)
            }
        }

class ConveyorSimulator(MachineSimulator):
    """Conveyor System Simulator"""
    
    def __init__(self, machine_id: str):
        super().__init__(machine_id, "Conveyor")
        self.motor_temp_baseline = 55.0
        
    def generate_sensor_data(self) -> dict:
        motor_temp = self.motor_temp_baseline + np.random.normal(0, 3)
        motor_current = 12 + np.random.normal(0, 1)
        speed = 1.5 + np.random.normal(0, 0.1)
        
        # Rare motor overload
        if random.random() < 0.02:
            motor_current += random.uniform(5, 10)
            motor_temp += random.uniform(10, 20)
            
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "status": self.status,
            "sensors": {
                "motor_temp": round(motor_temp, 2),
                "motor_current": round(motor_current, 2),
                "speed": round(speed, 2),
                "vibration": round(0.005 + np.random.normal(0, 0.001), 4),
                "belt_tension": round(150 + np.random.normal(0, 10), 2)
            }
        }

class FactorySimulator:
    """Main Factory Simulator"""
    
    def __init__(self, broker: str, port: int, num_machines: int = 3):
        self.broker = broker
        self.port = port
        
        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        # Create machine simulators
        self.machines = [
            CNCSimulator("CNC_001"),
            InjectionMoldingSimulator("INJ_001"),
            ConveyorSimulator("CONV_001")
        ][:num_machines]
        
        print(f"Initialized {len(self.machines)} machine simulators")
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
        else:
            print(f"Failed to connect, return code {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected from MQTT broker")
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            time.sleep(2)  # Wait for connection
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            raise
            
    def publish_sensor_data(self, machine: MachineSimulator):
        """Publish sensor data to MQTT"""
        data = machine.generate_sensor_data()
        topic = f"factory/{machine.machine_type}/{machine.machine_id}/sensors"
        
        payload = json.dumps(data)
        self.client.publish(topic, payload, qos=1)
        
        print(f"[{data['timestamp']}] {machine.machine_id}: "
              f"Published {len(data['sensors'])} sensor readings")
        
    def run(self, duration_hours: float = 24, update_interval: int = 2):
        """Run simulation"""
        print(f"Starting simulation for {duration_hours} hours...")
        print(f"Update interval: {update_interval} seconds")
        
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        try:
            while time.time() < end_time:
                for machine in self.machines:
                    self.publish_sensor_data(machine)
                    
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            print("\nSimulation stopped by user")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            print("Simulation ended")

def main():
    parser = argparse.ArgumentParser(description="Intellica Factory Simulator")
    parser.add_argument("--broker", default="rabbitmq", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--machines", type=int, default=3, help="Number of machines")
    parser.add_argument("--duration", default="24h", help="Simulation duration (e.g., 24h, 1d)")
    parser.add_argument("--interval", type=int, default=2, help="Update interval in seconds")
    
    args = parser.parse_args()
    
    # Parse duration
    if args.duration.endswith('h'):
        duration_hours = float(args.duration[:-1])
    elif args.duration.endswith('d'):
        duration_hours = float(args.duration[:-1]) * 24
    else:
        duration_hours = 24
        
    # Create and run simulator
    simulator = FactorySimulator(args.broker, args.port, args.machines)
    simulator.connect()
    simulator.run(duration_hours, args.interval)

if __name__ == "__main__":
    main()