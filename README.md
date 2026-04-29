# ROS2 Automated Golf Ball Tee Feeder

## 📌 Overview
This project implements a **ROS2-based robotic system** that autonomously detects when a golf ball is missing from a tee and triggers a feeding mechanism to place a new ball.
The system follows a complete robotics pipeline:
**Sense → Decide → Act → Verify**

## 🎯 Key Features
- ROS2 multi-node architecture
- Event-driven system using publishers, subscribers, and timers
- Closed-loop feedback using actuator status and sensor verification
- Retry logic with failure handling
- Launch-based execution for full system orchestration
- Topic-based simulation (no blocking input)

## 🧠 System Architecture
### Nodes

|           Node           |                   Responsibility                    |
|--------------------------|-----------------------------------------------------|
| `tee_sensor_node`        | Publishes whether a ball is present on the tee      |
| `feeder_supervisor_node` | State machine that decides when to feed             |
| `actuator_node`          | Simulates servo-based feeder and reports completion |

### Topics

|         Topic       |   Type   |              Description             |
|---------------------|----------|--------------------------------------|
| `/tee/ball_present` | `Bool`   | Sensor state (ball present or not)   |
| `/feeder/command`   | `String` | Command to actuator (`FEED_ONE`)     |
| `/feeder/status`    | `String` | Actuator feedback (`DONE`)           |
| `/sim/toggle_ball`  | `Empty`  | Simulation trigger for ball state    |

## 🔁 System Behavior

1. **Idle State**
   - Ball is present on the tee

2. **Detection**
   - If ball is missing for 3 seconds → trigger feed

3. **Actuation**
   - Actuator simulates servo rotation (90°)
   - Publishes `"DONE"` after completion

4. **Verification**
   - Supervisor waits for sensor confirmation
   - If ball not detected → retry (max 3 attempts)

5. **Failure Handling**
   - After 3 failed attempts → system waits for manual intervention

## 🚀 Running the System
### 1. Build
```bash
colcon build --symlink-install
source install/setup.bash
```

### 2. Launch
```bash
ros2 launch ros2_golf_ball_feeder feeder_system.launch.py
```

### 3. Simulate Ball Events
To simulate the ball presence, the below is necessary to toggle whether the ball is on the tee.
When system is launched in a terminal, open another terminal and run:
```bash
ros2 topic pub --once /sim/toggle_ball std_msgs/msg/Empty "{}"
```
each time the ball presence state needs to be changed. (First call -> ball removed, second call -> ball placed)

## 🛠 Technologies Used
- ROS2 (rclpy)
- Python
- Publisher/Subscriber communication
- Timers and event-driven callbacks

## 💡 Key Takeaways
- Designed a modular ROS2 system with clear separation of concerns
- Implemented closed-loop control using feedback and verification
- Built a realistic failure-handling and retry mechanism

## 📈 Future Improvements
- Integrate real hardware (load cell + servo motor)
- Replace String messages with custom ROS2 message types
- Add visualization (RViz or state topic)
- Convert actuator node to C++ for performance realism