# KITA CUMA PAKAI NUMPY YA GUYS YAK, ga pakai training data
import numpy as np

def get_dist(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    centered = b - a
    dist = np.sqrt(np.sum(np.pow(centered, 2)))
    return dist

def get_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.float64: # b nya sudutnya dicari
    A = get_dist(b, c)
    B = get_dist(a, c)
    C = get_dist(a, b)

    res_angle = np.arccos( (np.pow(A, 2) + np.pow(C, 2) - np.pow(B, 2)) / (2 * A * C) ) / np.pi * 180
    return res_angle

def get_equil_height(a: np.ndarray, b: np.ndarray) -> np.float64:
    dist = get_dist(a, b)

    res_equil_height = dist / 2 * np.sqrt(3)
    return res_equil_height

def get_center(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    res_center = (a + b) / 2
    return res_center

def normalize(a: np.ndarray):
    res_norm = a / get_dist(np.array([0, 0]), a)
    return res_norm

def get_dir_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray: # dari a ke b
    centered_vec = b - a

    result_dir = normalize(centered_vec)
    return result_dir

def rotate_90_deg(a: np.ndarray) -> np.ndarray: # ini berlawanan arah jarum jam
    a[0], a[1] = -a[1], a[0]
    return a

def equil_point_two_cases(a: np.ndarray, b: np.ndarray) -> np.ndarray: # 2D array
    if b[0] < a[0]:
        a, b = b, a
    
    center = get_center(a, b)

    dir = get_dir_vec(a, b)
    dir_rotated_90_deg = rotate_90_deg(dir)

    equil_height = get_equil_height(a, b)

    # DUA KASUS
    # case 1
    case_1 = center + (dir_rotated_90_deg * equil_height)
    # case 2
    case_2 = center + (-dir_rotated_90_deg * equil_height)

    return np.array([case_1, case_2])

def equil_opposite_point(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray: # b adalah titik fokus, mengcover collinear juga
    two_cases = equil_point_two_cases(a, c)

    # jarak dua kasus terhadap b dan pilih paling besar
    dist_1 = get_dist(b, two_cases[0])
    dist_2 = get_dist(b, two_cases[1])

    if dist_1 > dist_2:
        return two_cases[0]
    else:
        return two_cases[1]

def get_line_eq(a: np.ndarray, b: np.ndarray) -> np.ndarray: # dengan format [m, b], m adalah gradien dan b adalah y intersection
    slope = (b[1] - a[1]) / (b[0] - a[0])
    bias = a[1] - slope * a[0]

    return np.array([slope, bias])

def solve_two_lines(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    line_1 = get_line_eq(a, b)
    line_2 = get_line_eq(c, d)

    x_res = (line_1[1] - line_2[1]) / (line_2[0] - line_1[0])
    y_res = line_1[0] * x_res + line_1[1]

    return np.array([x_res, y_res])

def get_minimum_distance(row):
    coords = np.array([
        [row['X1'], row['Y1']],
        [row['X2'], row['Y2']],
        [row['X3'], row['Y3']]
    ])
    a, b, c = coords[0, :], coords[1, :], coords[2, :]
    A, B, C = get_angle(b, a, c), get_angle(a, b, c), get_angle(a, c, b)

    if A >= 120.0:
        return get_dist(a, b) + get_dist(a, c)
    elif B >= 120.0:
        return get_dist(b, a) + get_dist(b, c)
    elif C >= 120.0:
        return get_dist(c, a) + get_dist(c, b)
    
    ext_a = equil_opposite_point(b, a, c)
    ext_b = equil_opposite_point(a, b, c)

    fermat_point = solve_two_lines(a, ext_a, b, ext_b)

    final_distance = get_dist(fermat_point, a) + get_dist(fermat_point, b) + get_dist(fermat_point, c)
    return final_distance