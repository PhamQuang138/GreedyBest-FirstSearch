import math

# Hàm tính khoảng cách Euclidean
def euclidean_distance(p1, p2, coord_dict):
    x1, y1 = coord_dict[p1]
    x2, y2 = coord_dict[p2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Hàm heuristic chính
def heuristic(current_id, unvisited, coord_dict, depot_id=0):
    """
    - current_id: diem hien tai (int)
    - unvisited: diem chua giao (list of int)
    - coord_dict: dict chua toa do {id: (x, y)}
    - depot_id: dia chi kho (0,0)
    """
    if not unvisited:
        # Nếu giao xong → quay về kho
        return euclidean_distance(current_id, depot_id, coord_dict)
    # Khoảng cách đến điểm gần nhất
    return min(
        euclidean_distance(current_id, p, coord_dict)
        for p in unvisited
    )
