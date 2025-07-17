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

## 🎯 Launch Arguments Reference

### Main Launch (`rtabmap_main.launch.py`)

| Argument | Default | Choices | Description |
|----------|---------|---------|-------------|
| `d455` | `false` | `true`, `false` | Hardware selection: true=RealSense D455, false=Isaac Sim |
| `rtabmap_viz` | `true` | `true`, `false` | Launch RTAB-Map visualization |
| `localization` | `false` | `true`, `false` | Start in localization mode (requires existing map) |
| `vo` | `none` | `none`, `rtabmap`, `isaac` | Visual odometry method |
| `stereo` | `true` | `true`, `false` | Use stereo camera mode |
| `image_width` | `960` | - | Simulation image width (pixels) |
| `image_height` | `600` | - | Simulation image height (pixels) |

### Real Robot Launch (`realsense_d455_stereo.launch.py`)

| Argument | Default | Description |
|----------|---------|-------------|
| `unite_imu_method` | `2` | IMU unite method: 0=None, 1=copy, 2=linear_interpolation |
| `enable_infra1` | `true` | Enable infrared camera 1 |
| `enable_infra2` | `true` | Enable infrared camera 2 |
| `enable_color` | `false` | Enable RGB camera |
| `enable_depth` | `false` | Enable depth stream |

## 📚 References and Documentation

- [RTABMap Documentation](http://introlab.github.io/rtabmap/)
- [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/)
- [RealSense ROS2 Package](https://github.com/IntelRealSense/realsense-ros)
- [Nav2 Navigation Stack](https://navigation.ros.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Mobile Robotics Engineer** - *Initial development and integration*

## 🙏 Acknowledgments

- NVIDIA Isaac ROS team for GPU-accelerated robotics
- RTABMap development team for robust SLAM algorithms
- Intel RealSense team for excellent depth camera technology
- ROS2 community for the modern robotics framework

---

**Happy SLAM-ming! 🤖📍**
