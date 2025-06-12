import math

# Hàm tính khoảng cách Euclidean
def euclidean_distance(p1, p2, coord_dict):
    x1, y1 = coord_dict[p1]
    x2, y2 = coord_dict[p2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def enhanced_heuristic(current_id, unvisited, coord_dict, time_dict=None, demand_dict=None, current_time=None, depot_id=0,
                       alpha=1.0, beta=0.0, gamma=0.0):
    if not unvisited:
        return depot_id
    return min(unvisited, key=lambda p: euclidean_distance(current_id, p, coord_dict))

