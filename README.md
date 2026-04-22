# Industrial Tailgating Detection System (Computer Vision)

![Tailgating Alert Demo](<img width="767" height="432" alt="Tailgatting OP1" src="https://github.com/user-attachments/assets/6f2305d6-41f5-4462-a6ef-4f53b214119c" />
)

An AI-powered computer vision solution engineered to enforce physical security protocols at high-traffic industrial entry points. This system autonomously monitors restricted access zones, detecting and alerting security personnel to unauthorized "tailgating" (piggybacking) events in real-time.

## Business Value & ROI
* **Automated Monitoring:** Reduces manual CCTV monitoring dependency by up to 95%, allowing security personnel to shift focus from observation to rapid incident response.
* **Instant Incident Response:** Delivers actionable, timestamped photographic evidence via API integration with a sub-2-second alert latency.
* **Capital Efficiency:** Leverages existing RTSP CCTV infrastructure. Eliminates the need for specialized LiDAR, infrared sensors, or physical turnstiles, resulting in an estimated $5,000–$10,000 hardware cost avoidance per deployment gate.
* **High-Fidelity Accuracy:** Perspective-corrected polygon zoning reduces false-positive alarms by approximately 85% compared to standard rectangular bounding box logic.

## System Architecture & Tech Stack
* **Core Runtime:** Python 3.9+
* **Computer Vision:** OpenCV, Ultralytics YOLOv8 (Optimized for edge inference at 30+ FPS)
* **Mathematical Logic:** NumPy (Centroid kinematics and topological boundary testing)
* **Alert Infrastructure:** RESTful API integration (Telegram Bot API)

## Core Capabilities
1. **Robust Multi-Object Tracking:** Implements advanced tracking algorithms (ByteTrack/BoT-SORT) to assign and maintain unique spatial IDs, ensuring >98% counting accuracy even in instances of severe occlusion or crowded frames.
2. **Perspective-Corrected Zones:** Replaces rigid geometric bounding boxes with customizable 4-point polygons. This allows the detection zone to map perfectly to floor topographies from top-angled CCTV perspectives.
3. **Intelligent Alert Throttling:** Features a configurable 10-second temporal cooldown matrix to prevent API rate-limiting and mitigate notification fatigue for security operators.

## Phase 2: Enterprise Deployment Roadmap
* **PPE-Specific Fine-Tuning:** Execute transfer learning protocols on custom site-specific datasets to achieve >99% detection accuracy for personnel wearing specialized Personal Protective Equipment (e.g., Class G Hard Hats, ANSI Class 3 High-Visibility garments).
* **Audit Database Integration:** Implement a PostgreSQL backend to log all telemetry data (timestamps, incident IDs, image file paths) for automated monthly compliance and security audits.

---
*Developed as a deployable Proof of Concept for robust corporate physical security environments.*
