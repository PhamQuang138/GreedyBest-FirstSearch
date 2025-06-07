from heapq import heappush, heappop
from algorithms.Heuristic import euclidean_distance


def a_star_single_vehicle(start_id, unvisited, coord_dict, max_customers, depot_id=0):
    """
    Thuật toán A* để tìm tuyếnCHF cho một xe bắt đầu từ depot.
    f(n) = g(n) + h(n), trong đó g(n) là chi phí thực tế, h(n) là chi phí ước lượng (khoảng cách đến depot)
    """
    route = [start_id]  # Khởi tạo tuyến đường với điểm bắt đầu (depot)
    current_id = start_id  # Điểm hiện tại là điểm bắt đầu
    unvisited = unvisited.copy()  # Sao chép tập hợp các điểm chưa thăm để không ảnh hưởng tập gốc

    for _ in range(max_customers):  # Lặp tối đa số khách hàng cho phép
        if not unvisited:  # Nếu không còn điểm chưa thăm, thoát
            break

        # Hàng đợi ưu tiên cho A* (f_score, current_id)
        open_set = []
        for next_id in unvisited:  # Duyệt qua các điểm chưa thăm
            g_score = euclidean_distance(current_id, next_id, coord_dict)  # Tính chi phí thực tế
            h_score = euclidean_distance(next_id, depot_id, coord_dict)  # Ước lượng chi phí đến depot
            f_score = g_score + h_score  # Tổng chi phí ước lượng
            heappush(open_set, (f_score, next_id))  # Đưa vào hàng đợi ưu tiên

        if not open_set:  # Nếu không có điểm nào để chọn, thoát
            break

        # Lấy điểm có f_score nhỏ nhất
        _, next_id = heappop(open_set)
        route.append(next_id)  # Thêm điểm vào tuyến đường
        unvisited.remove(next_id)  # Xóa điểm khỏi tập chưa thăm
        current_id = next_id  # Cập nhật điểm hiện tại

    route.append(depot_id)  # Thêm depot vào cuối tuyến đường (quay lại)
    return route  # Trả về tuyến đường của xe


def a_star_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4):
    """
    Thuật toán A* cho nhiều xe, mỗi xe phục vụ tối đa max_customers_per_vehicle khách hàng.
    """
    unvisited = set(coord_dict.keys()) - {0}  # Loại bỏ depot khỏi tập các điểm chưa thăm
    vehicle_routes = []  # Danh sách lưu tuyến đường của các xe

    for _ in range(num_vehicles):  # Lặp cho số lượng xe
        if not unvisited:  # Nếu không còn điểm chưa thăm, thoát
            break
        # Bắt đầu từ depot, tìm tuyến đường cho một xe bằng A*
        route = a_star_single_vehicle(0, unvisited, coord_dict, max_customers_per_vehicle)
        # Xóa các điểm đã thăm khỏi tập unvisited
        for point in route[1:-1]:  # Bỏ qua depot ở đầu và cuối
            if point in unvisited:
                unvisited.remove(point)
        vehicle_routes.append(route)  # Thêm tuyến đường vào danh sách

    return vehicle_routes  # Trả về danh sách các tuyến đường