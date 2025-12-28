import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define fuzzy variables

road_conditions = ctrl.Antecedent(np.arange(0, 101, 1), 'road_conditions')
vehicle_speed = ctrl.Antecedent(np.arange(0, 101, 1), 'vehicle_speed')
distance_to_obstacle = ctrl.Antecedent(np.arange(0, 51, 1), 'distance_to_obstacle')

braking_force = ctrl.Consequent(np.arange(0, 101, 1), 'braking_force')
steering_angle = ctrl.Consequent(np.arange(-90, 91, 1), 'steering_angle')
acceleration = ctrl.Consequent(np.arange(-10, 11, 1), 'acceleration')

# Membership functions
# Road conditions

road_conditions['poor'] = fuzz.trimf(road_conditions.universe, [0, 0, 30])
road_conditions['average'] = fuzz.trimf(road_conditions.universe, [20, 50, 80])
road_conditions['good'] = fuzz.trimf(road_conditions.universe, [70, 100, 100])

# Vehicle speed
vehicle_speed['slow'] = fuzz.trimf(vehicle_speed.universe, [0, 0, 40])
vehicle_speed['moderate'] = fuzz.trimf(vehicle_speed.universe, [30, 60, 90])
vehicle_speed['fast'] = fuzz.trimf(vehicle_speed.universe, [80, 100, 100])

# Distance to obstacle
distance_to_obstacle['close'] = fuzz.trimf(distance_to_obstacle.universe, [0, 0, 10])
distance_to_obstacle['medium'] = fuzz.trimf(distance_to_obstacle.universe, [5, 20, 35])
distance_to_obstacle['far'] = fuzz.trimf(distance_to_obstacle.universe, [30, 50, 50])

# Braking force
braking_force['low'] = fuzz.trimf(braking_force.universe, [0, 0, 30])
braking_force['moderate'] = fuzz.trimf(braking_force.universe, [20, 50, 80])
braking_force['high'] = fuzz.trimf(braking_force.universe, [70, 100, 100])

# Steering angle
steering_angle['sharp_left'] = fuzz.trimf(steering_angle.universe, [-90, -90, -45])
steering_angle['slight_left'] = fuzz.trimf(steering_angle.universe, [-60, -30, 0])
steering_angle['straight'] = fuzz.trimf(steering_angle.universe, [-15, 0, 15])
steering_angle['slight_right'] = fuzz.trimf(steering_angle.universe, [0, 30, 60])
steering_angle['sharp_right'] = fuzz.trimf(steering_angle.universe, [45, 90, 90])

# Acceleration
acceleration['decelerate'] = fuzz.trimf(acceleration.universe, [-10, -10, -5])
acceleration['maintain'] = fuzz.trimf(acceleration.universe, [-5, 0, 5])
acceleration['accelerate'] = fuzz.trimf(acceleration.universe, [5, 10, 10])

# Fuzzy rules – Braking

rule1 = ctrl.Rule(distance_to_obstacle['close'] & vehicle_speed['fast'], braking_force['high'])
rule2 = ctrl.Rule(distance_to_obstacle['medium'] & vehicle_speed['moderate'], braking_force['moderate'])
rule3 = ctrl.Rule(distance_to_obstacle['far'] & vehicle_speed['slow'], braking_force['low'])

# Coverage rules
rule3a = ctrl.Rule(distance_to_obstacle['close'], braking_force['high'])
rule3b = ctrl.Rule(distance_to_obstacle['medium'], braking_force['moderate'])
rule3c = ctrl.Rule(distance_to_obstacle['far'], braking_force['low'])
rule3d = ctrl.Rule(vehicle_speed['fast'], braking_force['moderate'])
rule3e = ctrl.Rule(vehicle_speed['moderate'], braking_force['moderate'])
rule3f = ctrl.Rule(vehicle_speed['slow'], braking_force['low'])


# Fuzzy rules – Steering


rule4 = ctrl.Rule(road_conditions['poor'], steering_angle['slight_left'])
rule5 = ctrl.Rule(road_conditions['good'], steering_angle['straight'])
rule5a = ctrl.Rule(road_conditions['average'], steering_angle['straight'])


# Fuzzy rules – Acceleration

rule6 = ctrl.Rule(vehicle_speed['slow'] & road_conditions['poor'], acceleration['maintain'])
rule7 = ctrl.Rule(vehicle_speed['fast'] & road_conditions['good'], acceleration['accelerate'])

rule7a = ctrl.Rule(vehicle_speed['moderate'] & road_conditions['average'], acceleration['maintain'])
rule7b = ctrl.Rule(vehicle_speed['slow'], acceleration['accelerate'])
rule7c = ctrl.Rule(vehicle_speed['moderate'], acceleration['maintain'])
rule7d = ctrl.Rule(vehicle_speed['fast'], acceleration['decelerate'])
rule7e = ctrl.Rule(road_conditions['poor'], acceleration['maintain'])
rule7f = ctrl.Rule(road_conditions['average'], acceleration['maintain'])
rule7g = ctrl.Rule(road_conditions['good'], acceleration['accelerate'])

# Control systems

braking_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3,
    rule3a, rule3b, rule3c, rule3d, rule3e, rule3f
])

steering_ctrl = ctrl.ControlSystem([rule4, rule5, rule5a])

acceleration_ctrl = ctrl.ControlSystem([
    rule6, rule7, rule7a, rule7b, rule7c, rule7d, rule7e, rule7f, rule7g
])


# Simulations

braking_simulation = ctrl.ControlSystemSimulation(braking_ctrl)
steering_simulation = ctrl.ControlSystemSimulation(steering_ctrl)
acceleration_simulation = ctrl.ControlSystemSimulation(acceleration_ctrl)

# Inputs
braking_simulation.input['distance_to_obstacle'] = 15
braking_simulation.input['vehicle_speed'] = 60

steering_simulation.input['road_conditions'] = 75

acceleration_simulation.input['vehicle_speed'] = 30
acceleration_simulation.input['road_conditions'] = 50

# Compute outputs

try:
    braking_simulation.compute()
    braking_force_output = braking_simulation.output['braking_force']
except Exception as e:
    print(f"Error in braking calculation: {e}")
    braking_force_output = None

try:
    steering_simulation.compute()
    steering_angle_output = steering_simulation.output['steering_angle']
except Exception as e:
    print(f"Error in steering calculation: {e}")
    steering_angle_output = None

try:
    acceleration_simulation.compute()
    acceleration_output = acceleration_simulation.output['acceleration']
except Exception as e:
    print(f"Error in acceleration calculation: {e}")
    acceleration_output = None

print(f"Braking Force: {braking_force_output}%")
print(f"Steering Angle: {steering_angle_output} degrees")
print(f"Acceleration: {acceleration_output} m/s^2")

# Visualization

plt.figure(figsize=(15, 10))

plt.subplot(3, 2, 1)
for label, mf in road_conditions.terms.items():
    plt.plot(road_conditions.universe, mf.mf, label=label)
plt.title('Road Conditions')
plt.legend()

plt.subplot(3, 2, 2)
for label, mf in vehicle_speed.terms.items():
    plt.plot(vehicle_speed.universe, mf.mf, label=label)
plt.title('Vehicle Speed')
plt.legend()

plt.subplot(3, 2, 3)
for label, mf in distance_to_obstacle.terms.items():
    plt.plot(distance_to_obstacle.universe, mf.mf, label=label)
plt.title('Distance to Obstacle')
plt.legend()

plt.subplot(3, 2, 4)
for label, mf in braking_force.terms.items():
    plt.plot(braking_force.universe, mf.mf, label=label)
plt.title('Braking Force')
plt.legend()

plt.subplot(3, 2, 6)
for label, mf in acceleration.terms.items():
    plt.plot(acceleration.universe, mf.mf, label=label)
plt.title('Acceleration')
plt.legend()

plt.tight_layout()
plt.show()

# 3D Surface Plot – Braking

try:
    x_braking, y_braking = np.meshgrid(
        np.linspace(0, 50, 21),
        np.linspace(0, 100, 21)
    )
    z_braking = np.zeros_like(x_braking)

    for i in range(x_braking.shape[0]):
        for j in range(x_braking.shape[1]):
            braking_simulation.input['distance_to_obstacle'] = x_braking[i, j]
            braking_simulation.input['vehicle_speed'] = y_braking[i, j]
            braking_simulation.compute()
            z_braking[i, j] = braking_simulation.output['braking_force']

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x_braking, y_braking, z_braking, cmap='viridis')

    ax.set_xlabel('Distance to Obstacle (m)')
    ax.set_ylabel('Vehicle Speed (km/h)')
    ax.set_zlabel('Braking Force (%)')
    ax.set_title('Fuzzy Control Surface for Braking')
    fig.colorbar(surf)

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error generating 3D surface plot: {e}")
