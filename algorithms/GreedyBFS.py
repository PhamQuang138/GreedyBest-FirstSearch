import os
from datetime import datetime
from algorithms.Heuristic import euclidean_distance

def greedy_bfs(coord_dict, time_dict,
               dataset_name="dataset",
               num_vehicles=25,
               speed=1.0,
               max_customers_per_vehicle=6,
               report_dir="model/output"):

    due_date_dict = {k: v[1] for k, v in time_dict.items() if k != 0}
    service_time_dict = {k: v[2] for k, v in time_dict.items() if k != 0}
    default_service_time = max(service_time_dict.values()) if service_time_dict else 90

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"gbfs_report_{dataset_name}_{timestamp}.txt")

    unvisited = set(coord_dict.keys()) - {0}
    vehicle_routes = []
    report_lines = []

    for vehicle_id in range(num_vehicles):
        if not unvisited:
            break

        current_id = 0
        current_time = 0
        route = [0]
        customers_served = 0
        vehicle_report = []

        while customers_served < max_customers_per_vehicle:
            feasible = []
            for cust_id in unvisited:
                distance = euclidean_distance(current_id, cust_id, coord_dict)
                travel_time = distance / speed
                arrival_time = current_time + travel_time
                service_time = service_time_dict.get(cust_id, default_service_time)
                total_time = arrival_time + service_time

                if total_time <= due_date_dict[cust_id]:
                    priority = due_date_dict[cust_id]
                    feasible.append((cust_id, travel_time, priority, service_time))

            if not feasible:
                break

            feasible.sort(key=lambda x: (x[2], x[1]))  # (due_date, travel_time)
            next_id, travel_time, _, service_time = feasible[0]

            arrival_time = current_time + travel_time
            current_time = arrival_time + service_time
            deadline = due_date_dict[next_id]
            status = "Đúng Hạn!" if current_time <= deadline else "Không Kịp"

            route.append(next_id)
            unvisited.remove(next_id)
            vehicle_report.append(
                f"   - Đến điểm {next_id} lúc {arrival_time:.2f}s, rời lúc {current_time:.2f}s | Due: {deadline} {status}"
            )
            current_id = next_id
            customers_served += 1

        route.append(0)
        vehicle_routes.append(route)

        report_lines.append(f"Xe {vehicle_id + 1}: {route}")
        report_lines.extend(vehicle_report)

    if unvisited:
        report_lines.append("\n⚠ Vẫn còn khách chưa được phục vụ đúng hạn:")
        for cust_id in unvisited:
            x, y = coord_dict[cust_id]
            deadline = due_date_dict[cust_id]
            report_lines.append(f" - Khách {cust_id}, hạn: {deadline}s, tọa độ: ({x}, {y})")

        report_lines.append("\n Gợi ý tốc độ tối thiểu để giao các khách còn lại từ depot:")
        now = current_time
        for cust_id in unvisited:
            distance = euclidean_distance(0, cust_id, coord_dict)
            due_time = due_date_dict[cust_id]
            service_time = service_time_dict.get(cust_id, default_service_time)
            time_left = due_time - now - service_time
            if due_time > service_time:
                min_speed = distance / (due_time - service_time)
                report_lines.append(
                    f" - Khách {cust_id}: cần tốc độ ≥ {min_speed:.2f} m/s ({min_speed * 3.6:.2f} km/h)"
                )
            else:
                min_speed = distance / time_left
                report_lines.append(
                    f" - Khách {cust_id}: chỉ có thể giao đầu tiên với tốc độ ≥ {min_speed:.2f} m/s ({min_speed * 3.6:.2f} km/h)"
                )
    else:
        report_lines.append("\nTất cả các điểm đã được giao đúng hạn.")

    # Thống kê tổng khách và kiểm tra thiếu
    total_customers = len(coord_dict) - 1  # trừ depot
    delivered_customers = sum(len(route) - 2 for route in vehicle_routes)  # trừ điểm đầu và cuối

    report_lines.append(f"\nTổng số khách cần giao: {total_customers}")
    report_lines.append(f"Tổng số khách đã giao: {delivered_customers}")
    if delivered_customers < total_customers:
        report_lines.append(" Còn khách chưa được giao!")
    else:
        report_lines.append("Đã giao hết tất cả các khách!")

    report_lines.append(f"\nTổng số xe sử dụng: {len(vehicle_routes)}")
    report_lines.append(f"Đã lưu báo cáo vào: {report_path}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    return vehicle_routes
