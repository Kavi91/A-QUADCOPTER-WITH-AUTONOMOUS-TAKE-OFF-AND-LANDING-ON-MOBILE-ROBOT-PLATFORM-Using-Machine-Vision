# A-QUADCOPTER-WITH-AUTONOMOUS-TAKE-OFF-AND-LANDING-ON-MOBILE-ROBOT-PLATFORM-Using-Machine-Vision
we propose an approach for automated and coordinated landing of an unmanned aerial vehicle on a mobile platform using Machine Vision

# Autonomous UAV Landing on a Mobile Platform

## Overview

Robotics represents the forefront of technological advancement, incorporating sophisticated designs and autonomous operations. Despite the absence of a universally accepted definition, a "Robot" often refers to a device capable of autonomous movement to fulfill specific objectives. Robotics applications span various fields, including unmanned vehicles, manufacturing, and healthcare. Among these, the integration of unmanned aerial vehicles (UAVs) with automated ground vehicles (AGVs) stands out as a key focus area, especially in the realm of coordinated operations.

This project introduces an innovative approach for the automated and coordinated landing of a UAV on a moving platform, employing a mobile manipulator as the landing station. Our goal is to develop an algorithm enabling autonomous vertical take-off and landing (VToL) capabilities for UAVs, incorporating obstacle avoidance on the mobile manipulator.

## Project Aim

The aim is to enhance UAV autonomy, particularly in VToL operations, through a dual-controller system and a computer vision-based algorithm for precise landing on a mobile platform, ensuring obstacle avoidance and accurate positioning.

## Methodology

Our UAV system incorporates two controllers:
- A default KK2 controller for basic flight control.
- A custom secondary controller for advanced operations, including input from analog proximity sensors (Sonar) and a 3-axis accelerometer for speed adjustments. PID controller parameters are simulated in MATLAB Simulink, with outputs encoded for a target microcontroller.

The mobile ground robot also features two controllers:
- A primary controller for intensive computations related to UAV flight.
- A secondary controller for mobile platform operations, such as obstacle avoidance, utilizing real-time and autonomous control via RF link.

A significant advancement is our computer vision algorithm, which enables the UAV to autonomously land on a moving platform by tracking, determining YAW orientation, and estimating vertical height.

## Key Features

- **Autonomous VToL with Obstacle Avoidance:** Enhances UAV capabilities for safer, more precise operations.
- **Dual-Controller System:** Ensures robust control over flight dynamics and platform operations.
- **Computer Vision for Landing:** Facilitates accurate landing on moving platforms, leveraging advanced algorithms.

## Contributions

This project is the culmination of efforts from a team with deep expertise and enthusiasm for unmanned robotics. From software simulation to real-world implementation, every member has significantly contributed to achieving the project's objectives.

## Future Work

Continued development will focus on refining the computer vision algorithm, enhancing controller efficiency, and expanding application areas for broader impact.

## Acknowledgements

We extend our gratitude to all team members, advisors, and supporters who have made this project possible.

## License

[MIT License](LICENSE)

## Contact

For inquiries or contributions, please contact us at [email@example.com](mailto:email@example.com).

---

Enjoy exploring our project, and we welcome any contributions or questions!
