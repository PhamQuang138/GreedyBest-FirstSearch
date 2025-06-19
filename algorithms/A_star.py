from heapq import heappush, heappop
from algorithms.Heuristic import euclidean_distance
import os
from datetime import datetime


def a_star_single_vehicle(start_id, unvisited, coord_dict, time_dict, max_customers, speed, depot_id=0,
                          alpha=0.5, beta=0.5, due_date_dict=None, service_time_dict=None,
                          default_service_time=90, vehicle_report=None):


    route = [start_id]
    current_id = start_id
    current_time = 0
    customers_served = 0
    unvisited = unvisited.copy()
    while customers_served < max_customers and unvisited:
        open_set = []  # Hàng đợi ưu tiên cho A*

        # Danh sách xếp hạng để ưu tiên giống như bên GBFS
        distance_ranks = sorted(unvisited, key=lambda p: euclidean_distance(current_id, p, coord_dict))
        distance_rank_dict = {p: i for i, p in enumerate(distance_ranks)}
        due_date_ranks = sorted(unvisited, key=lambda p: time_dict[p][1])
        due_date_rank_dict = {p: i for i, p in enumerate(due_date_ranks)}

        # Tìm các điểm khả thi
        for next_id in unvisited:
            distance = euclidean_distance(current_id, next_id, coord_dict)
            travel_time = distance / speed
            arrival_time = current_time + travel_time
            service_time = service_time_dict.get(next_id, default_service_time)
            total_time = arrival_time + service_time

            if total_time <= due_date_dict[next_id]:
                # Tính g_score và h_score dựa trên khoảng cách và thời hạn
                rank_distance = distance_rank_dict[next_id]
                rank_due_date = due_date_rank_dict[next_id]
                g_score = alpha * rank_distance + beta * rank_due_date
                h_score = euclidean_distance(next_id, depot_id, coord_dict) / speed
                f_score = g_score + h_score  # Tổng chi phí
                heappush(open_set, (f_score, next_id, travel_time, service_time))

        if not open_set:
            break

        # Chọn điểm có f_score nhỏ nhất
        _, next_id, travel_time, service_time = heappop(open_set)

        # Cập nhật trạng thái
        arrival_time = current_time + travel_time
        current_time = arrival_time + service_time
        deadline = due_date_dict[next_id]
        status = "Đúng Hạn!" if current_time <= deadline else "Không Kịp"

        route.append(next_id)
        unvisited.remove(next_id)
        vehicle_report.append(
            f"   - Đến điểm {next_id} lúc {arrival_time:.2f}s, rời lúc {current_time:.2f}s | Due: {deadline}s {status}"
        )
        current_id = next_id
        customers_served += 1

    route.append(depot_id)
    return route, unvisited


def a_star_multi_vehicles(coord_dict, time_dict, dataset_name="dataset", num_vehicles=25, speed=1.0,
                          max_customers_per_vehicle=6, report_dir="model/output", alpha=0.5, beta=0.5):

    # Khởi tạo từ điển thời hạn và thời gian phục vụ
    due_date_dict = {k: v[1] for k, v in time_dict.items() if k != 0}
    service_time_dict = {k: v[2] for k, v in time_dict.items() if k != 0}
    default_service_time = max(service_time_dict.values()) if service_time_dict else 90

    # Tạo thư mục và file báo cáo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"astar_report_{dataset_name}_{timestamp}.txt")

    unvisited = set(coord_dict.keys()) - {0}  # Tập các điểm chưa thăm
    vehicle_routes = []  # Danh sách lộ trình
    report_lines = []  # Nội dung báo cáo

    for vehicle_id in range(num_vehicles):
        if not unvisited:
            break

        vehicle_report = []
        # Tìm lộ trình cho một xe
        route, unvisited = a_star_single_vehicle(
            0, unvisited, coord_dict, time_dict, max_customers_per_vehicle, speed,
            alpha=alpha, beta=beta, due_date_dict=due_date_dict, service_time_dict=service_time_dict,
            default_service_time=default_service_time, vehicle_report=vehicle_report
        )
        vehicle_routes.append(route)
        report_lines.append(f"Xe {vehicle_id + 1}: {route}")
        report_lines.extend(vehicle_report)

    # Báo cáo khách hàng chưa được phục vụ
    if unvisited:
        report_lines.append("\n⚠ Vẫn còn khách chưa được phục vụ đúng hạn:")
        for cust_id in unvisited:
            x, y = coord_dict[cust_id]
            deadline = due_date_dict[cust_id]
            report_lines.append(f" - Khách {cust_id}, hạn: {deadline}s, tọa độ: ({x}, {y})")

        report_lines.append("\n Gợi ý tốc độ tối thiểu để giao các khách còn lại từ depot:")
        for cust_id in unvisited:
            distance = euclidean_distance(0, cust_id, coord_dict)
            due_time = due_date_dict[cust_id]
            service_time = service_time_dict.get(cust_id, default_service_time)
            if due_time > service_time:
                min_speed = distance / (due_time - service_time)
                report_lines.append(
                    f" - Khách {cust_id}: cần tốc độ ≥ {min_speed:.2f} m/s ({min_speed * 3.6:.2f} km/h)"
                )
            else:
                min_speed = distance / due_time
                report_lines.append(
                    f" - Khách {cust_id}: chỉ có thể giao đầu tiên với tốc độ ≥ {min_speed:.2f} m/s ({min_speed * 3.6:.2f} km/h)"
                )
    else:
        report_lines.append("\nTất cả các điểm đã được giao đúng hạn.")

    # Thống kê tổng quát
    total_customers = len(coord_dict) - 1
    delivered_customers = sum(len(route) - 2 for route in vehicle_routes)
    report_lines.append(f"\nTổng số khách cần giao: {total_customers}")
    report_lines.append(f"Tổng số khách đã giao: {delivered_customers}")
    if delivered_customers < total_customers:
        report_lines.append("⚠ Còn khách chưa được giao!")
    else:
        report_lines.append("Đã giao hết tất cả các khách!")
    report_lines.append(f"\nTổng số xe sử dụng: {len(vehicle_routes)}")
    report_lines.append(f"Đã lưu báo cáo vào: {report_path}")

    # Lưu báo cáo
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    return vehicle_routes