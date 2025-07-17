# RTAB-Map Isaac Sim D455 Integration

A comprehensive ROS2 package for SLAM (Simultaneous Localization and Mapping) that seamlessly integrates RTAB-Map with both NVIDIA Isaac Sim simulation and Intel RealSense D455 camera hardware. This unified system enables robust mapping, localization, and autonomous navigation for differential drive robots.

## 🎯 Key Features

- **🔄 Unified Launch System**: Single command interface that automatically switches between simulation and real hardware
- **📷 Intel RealSense D455**: Optimized stereo vision SLAM with IMU sensor fusion
- **🎮 NVIDIA Isaac Sim**: GPU-accelerated simulation with realistic sensor modeling
- **🧠 RTABMap Integration**: Advanced visual SLAM with loop closure detection
- **🧭 Nav2 Navigation**: Full autonomous navigation stack integration
- **⚡ Hardware Acceleration**: Optimized for NVIDIA RTX GPUs
- **🔧 ROS2 Humble**: Modern robotics middleware with real-time capabilities

## 🚀 Quick Start

### Basic Usage
```bash
# Launch in simulation mode (default)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py

# Launch with real RealSense D455 camera
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
```

### Advanced Configuration
```bash
# Simulation with RTABMap visual odometry
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    vo:=rtabmap \
    rtabmap_viz:=true \
    image_width:=1280 \
    image_height:=720

# Simulation with Isaac Visual SLAM
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    vo:=isaac \
    stereo:=true

# Localization mode (requires existing map)
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    localization:=true
```

## 🔥 NEW: Optimized D455 RGBD Mode

### Why RGBD Mode is Superior for D455
The D455 is an RGBD camera (RGB + Depth) that provides much better performance than stereo infrared mode:

**✅ RGBD Advantages:**
- **Rich RGB features**: Color imagery provides 10x more visual features than IR
- **Hardware depth**: Active IR depth sensor more accurate than stereo computation  
- **Better floor detection**: Direct depth data enables precise ground plane detection
- **Lower CPU usage**: No stereo matching computation required
- **Improved tracking**: RGB features don't suffer from "image sticking" issues

**❌ Stereo IR Issues:**
- Limited features on smooth surfaces
- Computational overhead of stereo matching
- Poor performance in low-texture environments  
- Inconsistent tracking leading to "image sticking"

### RGBD Quick Start
```bash
# Test the optimized RGBD configuration
./test_d455_rgbd.sh

# Or launch directly with different resolutions
ros2 launch rtabmap_isaacsim_d455 d455_rgbd_optimized.launch.py resolution:=640x480
ros2 launch rtabmap_isaacsim_d455 d455_rgbd_optimized.launch.py resolution:=848x480  
ros2 launch rtabmap_isaacsim_d455 d455_rgbd_optimized.launch.py resolution:=1280x720
```

### RGBD Configuration Features
- **RGB Camera**: 640x480, 848x480, or 1280x720 @ 30fps
- **Depth Alignment**: Depth automatically aligned to RGB frame
- **IMU Integration**: 6-DOF sensor fusion with Madgwick filter
- **Enhanced Floor Detection**: Optimized Grid parameters for ground plane
- **Visual Odometry**: RGBD-based tracking with 1000+ features
- **Loop Closure**: RGB-based place recognition
- **Real-time Mapping**: Occupancy grid generation from depth data

## 📁 Project Architecture

```
rtabmap_isaacsim_d455/
├── launch/
│   ├── rtabmap_main.launch.py                    # 🚀 Main unified launcher
│   ├── real_robot/
│   │   └── realsense_d455_stereo.launch.py       # 📷 Real hardware configuration
│   ├── simulation/
│   │   ├── isaac_sim.launch.py                   # 🤖 Isaac Sim integration
│   │   ├── stereo_image_processing.launch.py     # 🖼️ GPU-accelerated image processing
│   │   └── isaac_visual_slam.launch.py           # 👁️ Isaac Visual SLAM
│   └── archive/                                  # 📦 Legacy/experimental launches
├── config/
│   ├── nav2_rtabmap_params.yaml                  # 🧭 Navigation parameters
│   └── rtabmap.rviz                              # 📊 Visualization configuration
├── package.xml                                   # 📋 Package dependencies
└── CMakeLists.txt                                # 🔧 Build configuration
```

## 🛠️ System Architecture

### Core Components

#### 1. Main Launch Controller (`rtabmap_main.launch.py`)
The unified entry point that intelligently routes to either simulation or real hardware based on the `d455` parameter:

- **Simulation Mode** (`d455:=false`): Launches Isaac Sim integration with GPU-accelerated image processing
- **Real Hardware Mode** (`d455:=true`): Configures RealSense D455 camera with optimized stereo SLAM settings

#### 2. Simulation Pipeline (`simulation/`)
- **Isaac Sim Integration**: Connects to NVIDIA Isaac Sim for realistic robot simulation
- **Stereo Image Processing**: GPU-accelerated image rectification and resizing using Isaac ROS
- **Visual Odometry Options**: 
  - `vo:=none` - No visual odometry (wheel odometry only)
  - `vo:=rtabmap` - RTABMap's built-in visual odometry
  - `vo:=isaac` - Isaac Visual SLAM integration

#### 3. Real Hardware Pipeline (`real_robot/`)
- **RealSense D455 Configuration**: Optimized parameters for stereo vision and IMU fusion
- **Topic Remapping**: Automatic mapping from D455 infrared cameras to RTABMap inputs
- **IMU Integration**: Madgwick filter for sensor fusion and improved odometry

#### 4. Navigation Stack Integration
- **Nav2 Integration**: Full autonomous navigation with dynamic obstacle avoidance
- **Custom Parameters**: Optimized for differential drive robots (TurtleBot3-style)
- **Real-time Path Planning**: Global and local planners with recovery behaviors

## 🔧 Technical Details

### Sensor Configuration

#### RealSense D455 Setup
```yaml
Camera Configuration:
  - Infrared Stereo: 848x480 @ 30fps
  - IMU: 6-DOF (gyroscope + accelerometer)
  - Depth Range: 0.2m - 10m
  - Field of View: 87° × 58°

RTABMap Parameters:
  - Frame ID: camera_link
  - Stereo Mode: True
  - IMU Integration: Linear interpolation
  - Loop Closure: Visual bag-of-words
```

#### Isaac Sim Configuration
```yaml
Virtual Camera:
  - Resolution: Configurable (default 960x600)
  - Stereo Baseline: Realistic camera separation
  - GPU Acceleration: CUDA-enabled image processing
  - Physics Simulation: Real-time sensor modeling
```

### Visual Odometry Modes

#### 1. No Visual Odometry (`vo:=none`)
- **Best for**: Testing wheel odometry, simple environments
- **Odometry Source**: Robot base encoders only
- **Performance**: Lowest computational load
- **Accuracy**: Depends on wheel slip and surface conditions

#### 2. RTABMap Visual Odometry (`vo:=rtabmap`)
- **Best for**: General purpose SLAM, loop closure detection
- **Features**: ORB feature detection, stereo matching
- **Performance**: Moderate computational load
- **Accuracy**: High accuracy with good texture environments

#### 3. Isaac Visual SLAM (`vo:=isaac`)
- **Best for**: GPU-accelerated processing, simulation environments
- **Features**: NVIDIA cuVSLAM, hardware acceleration
- **Performance**: High frame rate processing
- **Accuracy**: Excellent with NVIDIA RTX GPUs

### Navigation Architecture

```
Robot Base Controller → Sensor Data → Hardware Type Decision
                                           ↓
                               ┌─────────────────┐
                               │   d455:=true    │   d455:=false
                               │                 │
                         RealSense D455    Isaac Sim
                               │                 │
                         Stereo + IMU    Virtual Stereo
                               │                 │
                               └─────────────────┘
                                       ↓
                                RTABMap SLAM
                                       ↓
                             Map + Localization
                                       ↓
                               Nav2 Planning
                                       ↓
                              Cmd_vel Commands
                                       ↓
                            Robot Base Controller
```

## 📦 Dependencies

### Required ROS2 Packages
```xml
<!-- Core RTABMap packages -->
rtabmap_slam, rtabmap_odom, rtabmap_util, rtabmap_viz
rtabmap_msgs, rtabmap_sync, rtabmap_demos

<!-- Navigation -->
nav2_bringup

<!-- Camera and sensors -->
realsense2_camera, image_transport, imu_filter_madgwick

<!-- Isaac ROS (for simulation) -->
isaac_ros_visual_slam, isaac_ros_image_proc, isaac_ros_stereo_image_proc

<!-- Visualization and utilities -->
rviz2, teleop_twist_keyboard, robot_state_publisher, tf2_ros
```

### System Requirements

#### For Real Hardware:
- **Camera**: Intel RealSense D455
- **OS**: Ubuntu 22.04 LTS
- **ROS**: ROS2 Humble
- **CPU**: Intel i5+ or AMD Ryzen 5+ (recommended)
- **RAM**: 8GB minimum, 16GB recommended

#### For Simulation:
- **GPU**: NVIDIA RTX series (RTX 4070+ recommended)
- **CUDA**: 11.8 or newer
- **Isaac Sim**: 2023.1.1 or newer
- **VRAM**: 8GB minimum, 12GB+ recommended

## 🚀 Installation Guide

### 1. Install ROS2 Humble
```bash
# Add ROS2 repository
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Humble
sudo apt update
sudo apt install ros-humble-desktop
```

### 2. Install RTABMap and Dependencies
```bash
# Install RTABMap packages
sudo apt install ros-humble-rtabmap-*

# Install navigation stack
sudo apt install ros-humble-nav2-*

# Install camera and sensor packages
sudo apt install ros-humble-realsense2-camera
sudo apt install ros-humble-imu-filter-madgwick
sudo apt install ros-humble-image-transport-plugins

# Install utilities
sudo apt install ros-humble-teleop-twist-keyboard
sudo apt install ros-humble-robot-state-publisher
```

### 3. Install Isaac ROS (for simulation)
```bash
# Install Isaac ROS packages
sudo apt install ros-humble-isaac-ros-*

# Or build from source for latest features
cd ~/ros2_ws/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline.git
```

### 4. Build the Package
```bash
# Clone this repository
cd ~/ros2_ws/src
git clone <repository-url> rtabmap_isaacsim_d455

# Build the workspace
cd ~/ros2_ws
colcon build --packages-select rtabmap_isaacsim_d455

# Source the workspace
source install/setup.bash
```

## 🎮 Usage Examples

### Basic Mapping
```bash
# Start mapping with real D455 camera
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true

# Control the robot manually
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Advanced Simulation
```bash
# High-resolution mapping with RTABMap VO
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    vo:=rtabmap \
    image_width:=1280 \
    image_height:=720 \
    rtabmap_viz:=true

# GPU-accelerated with Isaac Visual SLAM
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    vo:=isaac \
    stereo:=true
```

### Autonomous Navigation
```bash
# Start mapping mode
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true

# In another terminal, send navigation goals
ros2 topic pub /goal_pose geometry_msgs/PoseStamped '{
  header: {frame_id: "map"},
  pose: {
    position: {x: 2.0, y: 1.0, z: 0.0},
    orientation: {w: 1.0}
  }
}'
```

### Map Management
```bash
# Save current map
ros2 service call /rtabmap/set_mode_localization std_srvs/Empty

# Load existing map for localization
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    d455:=true \
    localization:=true
```

## 📊 Performance Optimization

### GPU Acceleration
- **Isaac ROS**: Leverages CUDA for image processing
- **RTX Optimization**: Designed for NVIDIA RTX 4070+ performance
- **Memory Management**: Efficient GPU memory usage for real-time operation

### Parameter Tuning
```yaml
# High-performance settings (config/nav2_rtabmap_params.yaml)
rtabmap:
  Mem/ReduceGraph: "false"          # Keep full graph for accuracy
  RGBD/OptimizeMaxError: "0.1"      # Strict optimization threshold
  Vis/MaxFeatures: "1000"           # High feature count for rich environments
  
nav2:
  max_vel_x: 1.5                    # Aggressive velocity for simulation
  inflation_radius: 0.2             # Tight obstacle avoidance
```

## 🐛 Troubleshooting

### Common Issues

#### 1. RealSense D455 Not Detected
```bash
# Check USB connection
lsusb | grep Intel

# Install latest RealSense SDK
sudo apt install librealsense2-*

# Check camera permissions
sudo usermod -a -G dialout $USER
```

#### 2. Isaac Sim Connection Issues
```bash
# Verify Isaac Sim is running
ps aux | grep isaac

# Check ROS bridge
ros2 topic list | grep isaac

# Restart Isaac Sim ROS2 bridge
```

#### 3. RTABMap Memory Issues
```bash
# Clear RTABMap database
rm ~/.ros/rtabmap.db

# Reduce memory usage
ros2 param set /rtabmap/rtabmap Mem/ReduceGraph true
```

#### 4. Navigation Stack Problems
```bash
# Check TF tree
ros2 run tf2_tools view_frames

# Verify static transforms
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link camera_link

# Reset navigation
ros2 service call /reinitialize_global_localization std_srvs/Empty
```

### Performance Tips

1. **GPU Memory**: Monitor VRAM usage with `nvidia-smi`
2. **CPU Load**: Use `htop` to monitor processing load
3. **Network**: Ensure low-latency connection for Isaac Sim
4. **Storage**: Use SSD for RTABMap database storage

## 🔬 Advanced Configuration

### Unified Parameter System

This package includes a **unified parameter configuration** that ensures consistent mapping behavior between Isaac Sim and RealSense D455:

#### Key Unified Features:
- **Visual-Only Odometry**: Both systems use camera-based odometry only (no wheel dependency)
- **Identical RTABMap Settings**: Same feature detection, loop closure, and optimization parameters
- **Consistent 2D Mapping**: Unified grid generation and floor detection settings
- **Robust Real Sensor Support**: Parameters tuned for sensor noise and real-world conditions

#### Testing Unified Parameters:
```bash
# Run the included test script
./test_unified_mapping.sh

# Or test manually:

# Isaac Sim with unified parameters
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    d455:=false \
    vo:=rtabmap \
    rtabmap_viz:=true

# D455 with identical parameters
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    d455:=true \
    vo:=rtabmap \
    rtabmap_viz:=true
```

#### Monitoring Map Quality:
```bash
# Check feature detection consistency
ros2 topic echo /rtabmap/info --field data.features

# Monitor odometry quality
ros2 topic echo /rtabmap/odom --field pose.covariance

# Verify loop closures
ros2 topic echo /rtabmap/info --field data.loop_closure_id
```

### Floor Detection Improvements

The unified parameters include special optimizations for floor detection:

```yaml
# Floor-optimized grid settings
Grid/FromDepth: "true"                # Generate from stereo depth
Grid/MaxGroundHeight: "0.05"          # Very low ground threshold  
Grid/MinGroundHeight: "-0.05"         # Allow slight variations
Grid/GroundIsObstacle: "false"        # Don't mark ground as obstacle
Grid/FlatObstacleDetected: "true"     # Detect flat surfaces
Grid/RayTracing: "true"               # Fill unknown space
```

### Isaac Sim Realism Mode

To make Isaac Sim behave more like real hardware:

1. **Disable Perfect Sensors**: The updated launch files remove dependency on perfect wheel odometry
2. **Visual-Only Mapping**: Both systems use only camera and IMU data
3. **Consistent Parameters**: Same RTABMap configuration for both platforms

### Custom Robot Integration
To integrate with your own robot, modify these key files:

1. **Robot Description**: Update TF frames in launch files
2. **Sensor Topics**: Modify topic remappings for your sensor setup
3. **Navigation Parameters**: Tune `nav2_rtabmap_params.yaml` for your robot's kinematics

### Multi-Robot Setup
```bash
# Launch multiple instances with namespaces
ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    namespace:=robot1 \
    d455:=true

ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py \
    namespace:=robot2 \
    d455:=true
```

# Comparison of Launch Files for RealSense D435i

This document provides a comparison of three launch files designed for the RealSense D435i camera:

1. **_realsense_d435i_color.launch.py**
2. **_realsense_d435i_infra.launch.py**
3. **_realsense_d435i_stereo.launch.py**

## Overview

All three launch files are designed to work with the RealSense D435i camera and integrate with RTAB-Map for SLAM and odometry. They share common features such as IMU integration, remapping of topics, and launching RTAB-Map nodes. However, they differ in the type of data they process and the configuration of the camera.

---

## Key Differences

### 1. **_realsense_d435i_color.launch.py**
- **Purpose**: Processes RGB color images and aligned depth data.
- **Remappings**:
  - `rgb/image`: `/camera/color/image_raw`
  - `rgb/camera_info`: `/camera/color/camera_info`
  - `depth/image`: `/camera/aligned_depth_to_color/image_raw`
- **Camera Settings**:
  - `rgb_camera.profile`: `640x360x30`
- **IR Emitter**: Enabled (`depth_module.emitter_enabled = 1`).

### 2. **_realsense_d435i_infra.launch.py**
- **Purpose**: Processes infrared images and depth data.
- **Remappings**:
  - `rgb/image`: `/camera/infra1/image_rect_raw`
  - `rgb/camera_info`: `/camera/infra1/camera_info`
  - `depth/image`: `/camera/depth/image_rect_raw`
- **Camera Settings**:
  - Infrared cameras enabled (`enable_infra1` and `enable_infra2`).
- **IR Emitter**: Disabled (`depth_module.emitter_enabled = 0`).

### 3. **_realsense_d435i_stereo.launch.py**
- **Purpose**: Processes stereo infrared images for depth computation.
- **Remappings**:
  - `left/image_rect`: `/camera/infra1/image_rect_raw`
  - `left/camera_info`: `/camera/infra1/camera_info`
  - `right/image_rect`: `/camera/infra2/image_rect_raw`
  - `right/camera_info`: `/camera/infra2/camera_info`
- **Camera Settings**:
  - Stereo mode enabled (`subscribe_stereo = True`).
- **IR Emitter**: Disabled (`depth_module.emitter_enabled = 0`).

---

## Common Features

- **IMU Integration**:
  - All launch files include the IMU filter node (`imu_filter_madgwick`) to compute quaternion data.
  - IMU remapping: `imu/data_raw` → `/camera/imu`.
- **RTAB-Map Nodes**:
  - `rtabmap_odom`: For odometry.
  - `rtabmap_slam`: For SLAM.
  - `rtabmap_viz`: For visualization.
- **Launch Arguments**:
  - `unite_imu_method`: Default value is `2` (linear interpolation).

---

## Summary

| Feature                  | Color Launch File       | Infra Launch File       | Stereo Launch File      |
|--------------------------|-------------------------|-------------------------|-------------------------|
| **Image Type**           | RGB Color              | Infrared                | Stereo Infrared         |
| **Depth Source**         | Aligned Depth          | Depth                   | Stereo Depth            |
| **IR Emitter**           | Enabled                | Disabled                | Disabled                |
| **IMU Integration**      | Yes                    | Yes                    | Yes                    |
| **RTAB-Map Nodes**       | Yes                    | Yes                    | Yes                    |

---

## Conclusion

Each launch file is tailored for specific use cases:
- **Color Launch File**: Ideal for applications requiring RGB color images.
- **Infra Launch File**: Suitable for infrared-based applications.
- **Stereo Launch File**: Best for stereo depth computation.

Choose the appropriate launch file based on your application's requirements.
