# Fuzzy Logic Based Vehicle Speed Controller

Fuzzy logic based vehicle speed, braking and steering control using Python.

## Overview
This project implements a **Fuzzy Logic Based Vehicle Speed Controller**
using Python and the `scikit-fuzzy` library.

The controller dynamically adjusts:
- 🚦 Braking Force
- 🧭 Steering Angle
- ⚡ Acceleration

based on real-world inputs such as:
- Vehicle speed
- Road conditions
- Distance to obstacles

This approach mimics **human-like decision making** and performs better
than traditional rigid controllers in uncertain environments.

---

## Features
- Mamdani-type Fuzzy Inference System
- Smooth braking and acceleration control
- Adaptive steering based on road condition
- Graphical visualization of membership functions
- 3D surface plot for braking behavior

---

## Technologies Used
- Python
- NumPy
- Matplotlib
- scikit-fuzzy

---

## Input Variables
- **Vehicle Speed** (Slow, Moderate, Fast)
- **Road Conditions** (Poor, Average, Good)
- **Distance to Obstacle** (Close, Medium, Far)

---

## Output Variables
- **Braking Force (%)**
- **Steering Angle (degrees)**
- **Acceleration (m/s²)**

---

## How to Run

1. Clone or download the repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   
3. Run the program:
```bash
python fuzzy_vehicle_control.py
```




  


  

   
   







   
   


