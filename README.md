# RTAB-Map Robot SLAM Project

## Overview

This project implements SLAM (Simultaneous Localization and Mapping) using RTAB-Map for a differential drive robot. The system is designed to seamlessly switch between Isaac Sim simulation and real RealSense D455 camera hardware, providing robust mapping and navigation capabilities.

### Key Features
- **🤖 Unified Launch System**: Single command switches between simulation and real hardware
- **📷 Intel RealSense D455**: Optimized stereo SLAM with IMU integration
- **🎮 NVIDIA Isaac Sim**: GPU-accelerated simulation environment
- **⚡ RTX 4070 Optimized**: Hardware-accelerated processing for real-time SLAM
- **🧭 ROS2 Humble**: Modern robotics middleware

## Quick Start

### Basic Usage
```bash
# Simulation mode (default)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py

# Real robot with D455 camera
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
```

### Advanced Usage
```bash
# Simulation with custom parameters
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    vo:=rtabmap \
    rtabmap_viz:=true \
    image_width:=1280 \
    image_height:=720

# Real robot - just works out of the box
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
```

## Project Structure

```
rtabmap_isaacsim_d455/
├── launch/
│   ├── rtabmap_main.launch.py              # 🚀 Main unified launch file
│   ├── real_robot/
│   │   └── realsense_d455_stereo.launch.py # 📷 RealSense D455 SLAM setup
│   ├── simulation/
│   │   ├── isaac_sim.launch.py             # 🤖 Isaac Sim main launch
│   │   ├── stereo_image_processing.launch.py # 🖼️ Image processing for Isaac
│   │   └── isaac_visual_slam.launch.py     # 👁️ Isaac Visual SLAM integration
│   └── archive/                            # 📦 Archived/test launch files
├── config/                                 # ⚙️ Configuration files (future)
└── README.md                              # 📖 This documentation
```

## Hardware Requirements

### Minimum System
- **CPU**: Intel i5-8th gen or AMD Ryzen 5 3600+
- **GPU**: NVIDIA RTX 4070 or better (for optimal performance)
- **RAM**: 16GB (32GB recommended for large mapping)
- **Storage**: SSD with 50GB+ free space

### Camera Hardware
- **Intel RealSense D455**: USB 3.0+ connection required
- **Good lighting**: Essential for stereo vision quality

## Software Dependencies

### Install ROS2 Packages
```bash
# Core RTAB-Map packages
sudo apt install ros-humble-rtabmap-ros

# RealSense camera support
sudo apt install ros-humble-realsense2-camera

# IMU processing
sudo apt install ros-humble-imu-filter-madgwick

# Navigation (if needed)
sudo apt install ros-humble-nav2-bringup
```

### Isaac Sim Requirements
- NVIDIA Isaac Sim 2023.1.0 or later
- CUDA-compatible GPU (RTX series recommended)
- Omniverse Launcher installed
```

### Isaac ROS (for simulation)
```bash
# Follow NVIDIA Isaac ROS installation guide
sudo apt install ros-humble-isaac-ros-visual-slam
sudo apt install ros-humble-isaac-ros-image-proc
sudo apt install ros-humble-isaac-ros-stereo-image-proc
```

## Build Instructions

```bash
# Navigate to your ROS2 workspace
cd ~/robot_ws  # or your workspace path

# Build the package
colcon build --packages-select rtabmap_isaacsim_d455

# Source the workspace
source install/setup.bash
```

## Launch File Details

### Main Launch File: `rtabmap_main.launch.py`

This is your primary entry point. It automatically detects hardware configuration and launches appropriate subsystems.

**Parameters:**
- `d455` (default: `false`): Hardware selection
  - `true`: Launch with RealSense D455 camera
  - `false`: Launch with Isaac Sim simulation

**Simulation Parameters** (only used when `d455=false`):
- `rtabmap_viz` (default: `true`): Enable RTAB-Map visualization
- `localization` (default: `false`): Start in localization mode
- `vo` (default: `none`): Visual odometry method
  - `none`: No visual odometry
  - `rtabmap`: Use RTAB-Map's visual odometry
  - `isaac`: Use Isaac ROS visual SLAM
- `stereo` (default: `true`): Enable stereo camera mode
- `image_width` (default: `960`): Simulation image width
- `image_height` (default: `600`): Simulation image height

### Real Robot: `real_robot/realsense_d455_stereo.launch.py`

Configures RealSense D455 camera with optimized SLAM parameters.

**Features:**
- Stereo infrared camera setup
- IMU integration with Madgwick filter
- Optimized RTAB-Map parameters for D455
- Automatic IR emitter disabling for stereo

**Parameters:**
- `unite_imu_method` (default: `2`): IMU data processing
  - `0`: No IMU unification
  - `1`: Copy method
  - `2`: Linear interpolation (recommended)

### Simulation: `simulation/isaac_sim.launch.py`

Main Isaac Sim integration with conditional Isaac ROS support.

**Components:**
- Stereo image rectification
- Optional Isaac Visual SLAM
- Nav2 navigation integration
- RTAB-Map SLAM with simulation parameters

## Usage Examples

### Basic Workflow

#### 1. Real Robot Operation
```bash
# Connect your RealSense D455 camera
# Verify camera connection
realsense-viewer

# Launch RTAB-Map SLAM
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true

# In another terminal, control robot
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

#### 2. Simulation Operation
```bash
# Start Isaac Sim with your robot scene
# Then launch RTAB-Map
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py

# For Isaac Visual SLAM instead of RTAB-Map
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py vo:=isaac
```

### Advanced Examples

#### High-Quality Mapping (Real Robot)
```bash
# Full resolution with visualization
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
```

#### Simulation Development
```bash
# Custom image resolution for simulation
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    image_width:=1280 \
    image_height:=720 \
    vo:=rtabmap \
    rtabmap_viz:=true
```

#### Localization Mode (using existing map)
```bash
# Real robot localization
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    d455:=true \
    localization:=true

# Simulation localization
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    localization:=true
```
sudo apt install ros-humble-rqt-robot-monitor
```

## Quick Start Guide

### 🚀 Launch with RealSense D455 (Real Robot)

```bash
# Basic SLAM with D455
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true

# With visual odometry for better accuracy
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true vo:=rtabmap

# Localization mode (requires existing map)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true localization:=true
```

### 🤖 Launch with Isaac Simulator

**Step 1**: Start Isaac Sim
1. Launch NVIDIA Isaac Sim
2. Open: `Isaac Examples → ROS2 → Navigation → Carter Navigation`
3. In Stage tab, enable stereo cameras:
   - Navigate to `World → Nova_Carter_ROS → front_hawk → left_camera_render_product`
   - Under `Property → Isaac Create Render Product Node → Inputs`, check "Enabled"
   - Set `height=600` and `width=960` for better performance
   - Repeat for `right_camera_render_product`

**Step 2**: Launch RTAB-Map
```bash
# Basic simulation SLAM
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=false

# With Isaac visual odometry (disable wheel odom TF first!)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=false vo:=isaac

# Custom image resolution
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=false image_width:=1280 image_height:=720
```

## Launch Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `d455` | bool | `false` | Use RealSense D455 instead of Isaac Sim |
| `rtabmap_viz` | bool | `true` | Launch RTAB-Map visualization GUI |
| `localization` | bool | `false` | Run in localization mode (map must exist) |
| `vo` | string | `none` | Visual odometry: `none`, `rtabmap`, `isaac` |
| `stereo` | bool | `true` | Use stereo vision instead of RGB+Depth |
| `image_width` | int | `960` | Image width for Isaac Sim processing |
| `image_height` | int | `600` | Image height for Isaac Sim processing |

## Advanced Usage Examples

### 🎯 High-Accuracy Mapping
```bash
# D455 with visual odometry and stereo
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true vo:=rtabmap stereo:=true

# Simulation with higher resolution
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=false image_width:=1280 image_height:=720 vo:=rtabmap
```

### 🧭 Navigation Only (Localization)
```bash
# Use existing map for navigation
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true localization:=true

# Disable visualization for headless operation
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true localization:=true rtabmap_viz:=false
```

### 🔄 Different Sensor Modes
```bash
# RGB+Depth mode instead of stereo
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true stereo:=false

# Pure wheel odometry (no visual odometry)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true vo:=none
```

## Configuration Files

### RTAB-Map Parameters (`config/rtabmap_params.yaml`)

The configuration includes optimized parameters for:

- **Loop Closure Detection**: Aggressive loop closure with `Rtabmap/DetectionRate: 1.0`
- **Memory Management**: Balanced STM/LTM with `Mem/STMSize: 30`
- **Visual Features**: GFTT detector with 400 max features for speed
- **Registration**: 3DoF mode optimized for differential robots
- **Grid Mapping**: 5cm resolution occupancy grids
- **GPU Optimization**: CUDA-accelerated stereo processing

Key optimizations for RTX 4070:
```yaml
Kp/DetectorStrategy: 6           # GFTT for speed
Kp/MaxFeatures: 400              # Balanced feature count
Vis/MaxFeatures: 1000            # High-quality matching
Grid/CellSize: 0.05              # 5cm grid resolution
Reg/Force3DoF: true              # 2D robot constraint
```

### Nav2 Parameters (`config/nav2_rtabmap_params.yaml`)

Optimized for differential drive robots with:
- **DWB Local Planner**: Smooth path following
- **Costmap Integration**: RTAB-Map point cloud obstacles
- **Velocity Limits**: Conservative for safety (`max_vel_x: 0.26`)
- **Recovery Behaviors**: Spin, backup, and wait actions

## Robot Control

### Manual Teleoperation
```bash
# Keyboard control
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# Gamepad control (if available)
ros2 launch teleop_twist_joy teleop-launch.py
```

### Autonomous Navigation
1. **Set Initial Pose**: Use RViz "2D Pose Estimate" tool
2. **Send Goal**: Use RViz "Nav2 Goal" tool
3. **Monitor Progress**: Check `/cmd_vel` and navigation status

## Monitoring and Debugging

### Essential Topics
```bash
# Check camera topics
ros2 topic list | grep camera

# Monitor RTAB-Map status
ros2 topic echo /rtabmap/info

# Check navigation status
ros2 topic echo /navigation_result

# View point clouds
ros2 topic echo /rtabmap/cloud_map
```

### Diagnostic Tools
```bash
# System monitor
ros2 run rqt_robot_monitor rqt_robot_monitor

# TF tree visualization
ros2 run rqt_tf_tree rqt_tf_tree

# Topic frequency check
ros2 topic hz /front_stereo_camera/left/image_raw
```

## Topic Information

### Real Robot Topics (RealSense D455)
```bash
# Camera topics
/camera/infra1/image_rect_raw    # Left infrared image
/camera/infra2/image_rect_raw    # Right infrared image
/camera/infra1/camera_info       # Left camera info
/camera/infra2/camera_info       # Right camera info
/camera/imu                      # Raw IMU data
/imu/data                        # Filtered IMU data

# RTAB-Map topics
/rtabmap/map                     # Occupancy grid map
/rtabmap/grid_map                # Grid map
/rtabmap/mapGraph                # Graph structure
/odom                            # Visual odometry
```

### Simulation Topics (Isaac Sim)
```bash
# Isaac Sim camera topics
/rgb_left                       # Left RGB camera
/rgb_right                       # Right RGB camera
/camera_info_left                # Left camera info
/camera_info_right               # Right camera info

# Processed topics
/left/image_rect                 # Rectified left image
/right/image_rect                # Rectified right image
```

## Troubleshooting

### Common Issues

#### RealSense D455 Problems
```bash
# Camera not detected
# 1. Check USB connection (USB 3.0+ required)
# 2. Verify permissions
sudo usermod -a -G dialout $USER
# 3. Reboot and try
realsense-viewer

# Poor stereo quality
# - Ensure good lighting conditions
# - Check camera calibration
# - Verify IR emitter is disabled
```

#### Isaac Sim Integration
```bash
# Isaac Sim not connecting
# 1. Verify Isaac Sim is running
# 2. Check ROS bridge is active
# 3. Verify topic names match

# Performance issues
# - Reduce image resolution
# - Check GPU memory usage
# - Monitor CPU usage
```

#### RTAB-Map Issues
```bash
# No loop closures
# - Increase visual features in scene
# - Check camera calibration
# - Verify stereo baseline

# Poor mapping quality
# - Slow down robot movement
# - Improve lighting conditions
# - Check IMU calibration
```

### Diagnostic Commands
```bash
# Check topics
ros2 topic list

# Monitor camera data
ros2 topic echo /camera/infra1/image_rect_raw

# Check RTAB-Map status
ros2 topic echo /rtabmap/info

# Verify transforms
ros2 run tf2_tools view_frames
```

## Performance Optimization

### For RTX 4070 Laptops
- Enable GPU acceleration in RTAB-Map parameters
- Use optimal image resolution (960x600 for real-time)
- Monitor thermal throttling during long mapping sessions

### Memory Management
- Clear RTAB-Map database periodically with `-d` argument
- Monitor RAM usage during large mapping sessions
- Use localization mode for navigation after mapping

## Contributing

1. Follow ROS2 coding standards
2. Test with both simulation and real hardware
3. Update documentation for new features
4. Ensure backward compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check this README troubleshooting section
2. Verify all dependencies are installed
3. Test with minimal configuration first
4. Open an issue with detailed logs

---

**Happy SLAM-ming! 🤖📍**
