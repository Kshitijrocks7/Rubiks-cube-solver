# Rubiks-cube-solver

!![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)



## 🧩 Project Overview
A 3D virtual Rubik’s Cube solver built with **Python** & **VPython** — scramble, visualize, and solve using **Kociemba’s algorithm**.  
**Shortlisted for AeroHack 2025 Face Off Round.**

This project simulates a **3×3 Rubik’s Cube** in 3D (VPython) and solves any valid scrambled state using the Kociemba two-phase algorithm. It includes:
- Interactive controls
- Scramble & solve functionality
- Animated moves for clear visualization

---

## 🚀 Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Kshitijrocks7/Rubiks-cube-solver.git
   cd Rubiks-cube-solver
   ```

2. **Create & activate virtual environment**
   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

> **Note:** VPython will open a browser window for the 3D view. If the window is blank, refresh or check your firewall settings.
## 🎥 Demo Video
[▶ Watch Demo on Google Drive](https://drive.google.com/uc?id=1coXM6EN4oZJLrDu7GL_sDZovCXRrh9Ad&export=download)


---

## 📂 Project Structure
```
Rubiks-cube-solver/
│── cube.py                # Cube logic and data structure
│── main.py                # Main application entry point
│── solve_rubiccs_cube.py  # Kociemba algorithm solver
│── requirements.txt       # Dependencies list
│── LICENSE                # Project license (MIT)
│── README.md              # This file
│── Presentation/          # AeroHack presentation slides
```

---

## 📊 Presentation

Download the AeroHack 2025 submission presentation:  
[📥 Click here to download](Presentation/Your_PPT_File_Name.pptx)

---

## 🛠 Dependencies

Main packages used:
- `vpython`
- `kociemba`
- `numpy`

Full list in: [`requirements.txt`](requirements.txt)

---

## 🏷 Topics
`rubiks-cube` `python` `vpython` `kociemba` `3d-visualization` `aerohack2025`

---

## 📜 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.  
Copyright © 2025 Kshitij Verma

---

## 💡 Troubleshooting
- Use Python 3.8+ for best compatibility
- If VPython graphics don’t appear, refresh the opened browser tab or try another browser
- For Windows users, run in `cmd` or `powershell`, not inside certain IDE consoles

---

## 🌟 Acknowledgments
- **Kociemba’s Algorithm** for efficient cube solving
- VPython community for interactive 3D graphics
- AeroHack 2025 organizers for the platform to showcase this work

---
