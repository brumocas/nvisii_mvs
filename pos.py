import yaml
import numpy as np
import random

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        bounding_box = yaml.safe_load(file)['BoundingBox']
    return {'Min': bounding_box['Min'], 'Max': bounding_box['Max']}

def compute_bounding_box_in_space(min_coords, max_coords, position):
    min_coords = np.array([min_coords['x'], min_coords['y'], min_coords['z']])
    max_coords = np.array([max_coords['x'], max_coords['y'], max_coords['z']])
    position = np.array([position['x'], position['y'], position['z']])
    global_min = min_coords + position
    global_max = max_coords + position
    return {
        'Min': {'x': global_min[0], 'y': global_min[1], 'z': global_min[2]},
        'Max': {'x': global_max[0], 'y': global_max[1], 'z': global_max[2]}
    }

def generate_random_position(x_range, y_range, z_range):
    return {
        'x': random.uniform(*x_range),
        'y': random.uniform(*y_range),
        'z': random.uniform(*z_range)
    }

def generate_random_rotation():
    
    # X rotation not working
    #rand = random.randint(1, 2)
    rand = random.randint(1, 2)
    if rand == 0:
        rotation = random.uniform(0, 3.14)  # Random angle in radians
        unit_vector = {"x": 1, "y": 0, "z": 0}
    elif rand == 1:
        rotation = 3.14
        unit_vector = {"x": 0, "y": 1, "z": 0}
    else:
        rotation = 1.57
        unit_vector = {"x": 0, "y": 0, "z": 1}

    return {"rotation": rotation, "vector": unit_vector}

def apply_rotation(bounding_box, rotation, unit_vector):
    """
    Apply rotation to the bounding box around the given axis.
    This is a simplified rotation that uses 2D rotation in the plane orthogonal to the axis.
    """
    min_coords = np.array([bounding_box['Min']['x'], bounding_box['Min']['y'], bounding_box['Min']['z']])
    max_coords = np.array([bounding_box['Max']['x'], bounding_box['Max']['y'], bounding_box['Max']['z']])

    # Rotation matrices for each axis
    if unit_vector["x"] == 1:
        # Rotate around the x-axis (y, z plane)
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(rotation), -np.sin(rotation)],
                                    [0, np.sin(rotation), np.cos(rotation)]])
    elif unit_vector["y"] == 1:
        # Rotate around the y-axis (x, z plane)
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
    else:
        # Rotate around the z-axis (x, y plane)
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])

    min_rotated = np.dot(rotation_matrix, min_coords)
    max_rotated = np.dot(rotation_matrix, max_coords)

    return {
        'Min': {'x': min_rotated[0], 'y': min_rotated[1], 'z': min_rotated[2]},
        'Max': {'x': max_rotated[0], 'y': max_rotated[1], 'z': max_rotated[2]}
    }

def check_bounding_box_collision(box1, box2, threshold=0.00):
    x_collision = not (box1['Max']['x'] + threshold < box2['Min']['x'] or box1['Min']['x'] - threshold > box2['Max']['x'])
    y_collision = not (box1['Max']['y'] + threshold < box2['Min']['y'] or box1['Min']['y'] - threshold > box2['Max']['y'])
    z_collision = not (box1['Max']['z'] + threshold < box2['Min']['z'] or box1['Min']['z'] - threshold > box2['Max']['z'])
    return x_collision and y_collision and z_collision

def generate_positions_with_rotations_and_collisions(bounding_box_data, num_positions, x_range, y_range, z_range):
    positions = []
    generated_boxes = []

    for _ in range(num_positions):
        while True:
            # Generate random position and rotation
            random_position = generate_random_position(x_range, y_range, z_range)
            random_rotation = generate_random_rotation()
            
            # Compute the bounding box in space for this position
            global_box = compute_bounding_box_in_space(
                bounding_box_data['Min'], bounding_box_data['Max'], random_position
            )
            
            # Apply rotation to the bounding box
            rotated_box = apply_rotation(global_box, random_rotation['rotation'], random_rotation['vector'])
            
            # Check for collisions with previously generated bounding boxes
            collision_detected = False
            for box in generated_boxes:
                if check_bounding_box_collision(rotated_box, box):
                    collision_detected = True
                    break
            
            # If no collision is detected, add this box to the list
            if not collision_detected:
                formatted_position = {
                    "position": [random_position['x'], random_position['y'], random_position['z']],
                    "rotation": random_rotation["rotation"],
                    "axis": random_rotation["vector"]
                }
                positions.append(formatted_position)
                generated_boxes.append(rotated_box)
                break  # Move to generating the next position

    return positions