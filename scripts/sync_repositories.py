import os
import json
import urllib.request
import urllib.error

# Token can come from environment GITHUB_TOKEN (in GitHub Actions) or local gh CLI
token = os.environ.get("GITHUB_TOKEN")
if not token:
    try:
        import subprocess
        token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        token = None

headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Arkz-Lab-Sync"
}
if token:
    headers["Authorization"] = f"Bearer {token}"

# Curated metadata dictionary to enrich descriptions and tags for flagship repos
CURATED_METADATA = {
    "sih2026-isro-space-tech": {
        "title": "ASTRA: Space Rendezvous & Docking Digital Twin",
        "description": "Smart India Hackathon 2026 ISRO Space Tech challenge. Autonomous space rendezvous, proximity operations, gripper telemetry, and real-time 3D orbital inspection twin.",
        "category": "Hackathon Solutions",
        "tags": ["ROS 2", "TypeScript", "Three.js", "FastAPI", "Docker", "ISRO SIH 2026"],
        "highlight": "SIH ISRO Space Tech",
        "featured": True
    },
    "yuva-yodha-hackathon": {
        "title": "EcoCast AI: Melter Optimizer & Digital Twin",
        "description": "Schneider Electric Yuva Yodha Hackathon 2026. Predictive AI decision-support twin and energy melter optimizer with tactile telemetry dashboard.",
        "category": "Hackathon Solutions",
        "tags": ["Digital Twin", "Python", "React", "Render", "Optimization", "Schneider Electric"],
        "highlight": "Schneider Electric Finalist",
        "featured": True
    },
    "agentic-supply-chain": {
        "title": "Autonomous Multi-Agent Supply Chain Engine",
        "description": "Enterprise agentic AI orchestration for demand forecasting, supplier disruption analysis, dynamic routing, and automated inventory rebalancing.",
        "category": "AI & Multi-Agent Systems",
        "tags": ["Multi-Agent AI", "LangChain", "FastAPI", "Render", "Docker", "Python"],
        "highlight": "Agentic AI Platform",
        "featured": True
    },
    "agentic-graphrag-tigergraph": {
        "title": "Agentic GraphRAG Knowledge Platform",
        "description": "Next-generation Graph Retrieval-Augmented Generation utilizing TigerGraph knowledge graphs and multi-agent query synthesis.",
        "category": "AI & Multi-Agent Systems",
        "tags": ["GraphRAG", "TigerGraph", "Multi-Agent AI", "Python", "Streamlit"],
        "highlight": "TigerGraph GraphRAG",
        "featured": True
    },
    "twindeo": {
        "title": "Twindeo: 3D Industrial Digital Twin",
        "description": "Production-grade 3D WebGL industrial digital twin engine. Federated CAD strategy, AABB clash detection, real-time spatial analytics, and telemetry integration.",
        "category": "Digital Twins & 3D WebGL",
        "tags": ["React Three Fiber", "WebGL", "PostgreSQL", "Docker", "Express"],
        "highlight": "3D Industrial Twin",
        "featured": True
    },
    "AutoTwin-AI": {
        "title": "AutoTwin AI: Video Telemetry & Digital Twin",
        "description": "Vision-based digital twin platform streaming factory crane video telemetry, joint safety inspection, and synthetic dataset generation.",
        "category": "Digital Twins & 3D WebGL",
        "tags": ["Computer Vision", "Telemetry", "Digital Twin", "Python", "Streamlit"],
        "highlight": "Vision Digital Twin",
        "featured": True
    },
    "luminous-pdm-command-center": {
        "title": "Luminous Inverter PdM Command Center",
        "description": "BITS Pilani APOGEE 2026 Innovation Challenge. AI-driven Physics-of-Failure model predicting Remaining Useful Life (RUL) of inverter relays over MQTT & MODBUS.",
        "category": "Hackathon Solutions",
        "tags": ["Scikit-Learn", "MQTT", "MODBUS", "Streamlit", "Edge AI", "BITS Pilani"],
        "highlight": "BITS Pilani APOGEE",
        "featured": True
    },
    "Traffic-Management-System": {
        "title": "Dynamic AI Traffic Management System",
        "description": "Autonomous traffic signal optimization built for SIH. Deep Q-Network (DQN) reinforcement learning trained on SUMO traffic simulations.",
        "category": "AI & Multi-Agent Systems",
        "tags": ["PyTorch DQN", "SUMO Simulation", "Reinforcement Learning", "JavaScript"],
        "highlight": "SIH AI System",
        "featured": True
    },
    "wheeled_robot_ros2": {
        "title": "Autonomous 4WD Mobile Robot in Gazebo",
        "description": "Autonomous 4-wheel drive skid-steer robot simulation in Gazebo and ROS 2. Features ros_gz_bridge, 2D SLAM mapping, and a reactive FSM obstacle avoider.",
        "category": "Robotics & ROS 2",
        "tags": ["ROS 2 Humble", "Gazebo Sim", "FSM Navigation", "SLAM", "URDF", "LiDAR"],
        "highlight": "ROS 2 Autonomous Robot",
        "featured": True
    },
    "ros2-workspaces": {
        "title": "ROS 2 Robotics & Embedded Control Workspaces",
        "description": "Consolidated modular ROS 2 architecture: powertrain telemetry, PID motor controllers, custom state messages, distance actions, and rover SLAM navigation.",
        "category": "Robotics & ROS 2",
        "tags": ["ROS 2 Humble", "Motor Telemetry", "Custom Actions", "SLAM", "Colcon", "C++ / Python"],
        "highlight": "ROS 2 Suite",
        "featured": True
    },
    "oomwoo-clean-and-map-arkz": {
        "title": "Oomwoo Clean & Map: Vacuum Robot ROS 2",
        "description": "Autonomous vacuum robot clean & map ROS 2 navigation stack. Advanced morphological erosion for safe gap-fill coverage and dynamic SLAM mapping.",
        "category": "Robotics & ROS 2",
        "tags": ["ROS 2", "SLAM", "Coverage Path Planning", "Autonomous Robot", "C++"],
        "highlight": "Autonomous Cleaning Robot",
        "featured": True
    },
    "odom_monitor": {
        "title": "ROS 2 Odometry Drift Benchmark Monitor",
        "description": "Real-time ROS 2 package tracking odometry drift, evaluating wheel slippage error thresholds, and recording trajectory benchmarks.",
        "category": "Robotics & ROS 2",
        "tags": ["ROS 2", "Odometry", "Drift Benchmark", "Python", "Telemetry"],
        "highlight": "ROS 2 Package"
    },
    "medilong_decision_core": {
        "title": "Medilong Clinical Decision Intelligence",
        "description": "Diagnostic intelligence pipeline and predictive machine learning models supporting hospital clinical triage and clinical risk estimation.",
        "category": "AI & Multi-Agent Systems",
        "tags": ["Machine Learning", "Healthcare AI", "Python", "Jupyter", "Predictive Analytics"],
        "highlight": "Clinical Decision Core"
    },
    "Scholarship-Policy-Compliance-Bot": {
        "title": "Scholarship Policy Compliance & Fraud Guard",
        "description": "Rule-based and ML policy evaluation engine enforcing scholarship compliance criteria with anomaly detection fraud guard.",
        "category": "AI & Multi-Agent Systems",
        "tags": ["Rules Engine", "Fraud Guard", "Python", "Streamlit", "Automation"],
        "highlight": "Compliance Engine"
    },
    "Solution-Hackathon": {
        "title": "FallGuard: AI Real-Time Fall Detector",
        "description": "Computer vision fall detection monitoring system powered by multimodal Gemini AI and real-time alerts.",
        "category": "Hackathon Solutions",
        "tags": ["Computer Vision", "Gemini AI", "Streamlit", "Python", "Hackathon"],
        "highlight": "Hackathon Solution"
    },
    "Thamizhan_Skills": {
        "title": "Computer Vision & ROS Practical Collection",
        "description": "Extensive 8-project practical repository covering traffic signal classification, YOLOv8 tracking, ROS 2 hand gesture control, and deep learning.",
        "category": "Robotics & ROS 2",
        "tags": ["YOLOv8", "OpenCV", "ROS 2", "PyTorch", "Gesture Control"],
        "highlight": "Multi-Project Showcase"
    },
    "portfolio": {
        "title": "Deepak R: Engineering Portfolio",
        "description": "Personal developer portfolio and interactive engineering showcase built with modern React, TypeScript, and TailwindCSS.",
        "category": "Software & Systems",
        "tags": ["React", "TypeScript", "Next.js", "TailwindCSS"],
        "highlight": "Portfolio Web App"
    },
    "Arkz-Deepak": {
        "title": "GitHub Profile Engineering Hub",
        "description": "Official GitHub profile configuration and skills overview repository for Deepak R.",
        "category": "Software & Systems",
        "tags": ["GitHub Profile", "Markdown", "Engineering Skills"],
        "highlight": "Profile Hub"
    },
    "oomwoo": {
        "title": "Oomwoo Vacuum Cleaner (Upstream Fork)",
        "description": "Open-source vacuum robot cleaner hardware and firmware upstream repository.",
        "category": "Robotics & ROS 2",
        "tags": ["Hardware", "Robotics", "ROS 2", "Upstream Fork"],
        "highlight": "Hardware Upstream"
    },
    "moveit2": {
        "title": "MoveIt 2 for ROS 2 (Motion Planning)",
        "description": "MoveIt 2 motion planning framework repository for advanced manipulation, kinematics, and trajectory control.",
        "category": "Robotics & ROS 2",
        "tags": ["MoveIt 2", "C++", "Motion Planning", "Kinematics"],
        "highlight": "Robotics Manipulation"
    },
    "Decentralized-Mesh-Protocol": {
        "title": "Decentralized Mesh Protocol (ESP32 / LoRa)",
        "description": "Decentralized mesh networking protocol designed for off-grid resilient peer-to-peer IoT communications.",
        "category": "Software & Systems",
        "tags": ["Mesh Networking", "C++", "PlatformIO", "Embedded IoT"],
        "highlight": "IoT Mesh"
    }
}

def api_get(endpoint):
    url = f"https://api.github.com/{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def sync():
    repos = api_get("users/Arkz-Deepak/repos?per_page=100&sort=pushed")
    if isinstance(repos, dict) and "error" in repos:
        print(f"Failed to fetch repositories: {repos['error']}")
        return

    projects = []
    
    for r in repos:
        name = r.get("name")
        # Exclude self and archived
        if name == "Arkz-Deepak.github.io" or r.get("archived", False):
            continue

        pages_info = api_get(f"repos/Arkz-Deepak/{name}/pages")
        has_pages = "error" not in pages_info and pages_info.get("status") is not None
        pages_url = pages_info.get("html_url") if has_pages else f"http://lab.deepak-arkz.me/{name}/"
        
        # Check curated metadata
        meta = CURATED_METADATA.get(name, {})
        title = meta.get("title") or name.replace("-", " ").replace("_", " ").title()
        desc = meta.get("description") or r.get("description") or "Active open-source robotics and AI engineering project."
        category = meta.get("category") or "Software & Systems"
        tags = meta.get("tags") or r.get("topics") or ["Robotics", "Python"]
        highlight = meta.get("highlight") or ("Live Docs" if has_pages else "Active Repo")
        featured = meta.get("featured", False)

        projects.append({
            "name": name,
            "title": title,
            "description": desc,
            "category": category,
            "tags": tags,
            "highlight": highlight,
            "featured": featured,
            "has_pages": has_pages,
            "pages_url": pages_url,
            "github_url": r.get("html_url", f"https://github.com/Arkz-Deepak/{name}"),
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "pushed_at": (r.get("pushed_at") or "")[:10],
            "language": r.get("language") or "Python",
            "is_fork": r.get("fork", False)
        })

    # Sort featured first, then with pages, then by push date
    projects.sort(key=lambda p: (not p["featured"], not p["has_pages"], p["name"]))

    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "repositories.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    print(f"Successfully synced {len(projects)} repositories to {output_file}")
    return projects

if __name__ == "__main__":
    sync()
