from visualize.Printer import print_one_txt_file
from visualize.Printer import plot_vehicle_routes, plot_vehicle_routes_interactive, tinh_quang_duong
from algorithms.GreedyBFS import greedy_bfs
from algorithms.Heuristic import euclidean_distance

# Thông số
dataset_name = "r110"
speed = 0.8

# Đọc dữ liệu từ file
coord_dict, time_dict, demand_dict, due_date_dict, service_time_dict = print_one_txt_file(f"{dataset_name}.txt")

# Tạo dict hạn giao và thời gian phục vụ từ time_dict
due_date_dict = {k: v[1] for k, v in time_dict.items() if k != 0}
service_time_dict = {k: v[2] for k, v in time_dict.items() if k != 0}

# Chạy thuật toán Greedy BFS
GBFS = greedy_bfs(coord_dict,
                  time_dict=time_dict,
                  dataset_name="r110",
                  num_vehicles=25,
                  speed=0.8,
                  max_customers_per_vehicle=6)


# === In kết quả tuyến ===
print("Test GBFS:\n")
for i, route in enumerate(GBFS):
    print(f"Xe {i + 1}: {route}")
    current_time = 0
    for j in range(1, len(route)):
        from_node = route[j - 1]
        to_node = route[j]
        distance = euclidean_distance(from_node, to_node, coord_dict)
        travel_time = distance / speed
        current_time += travel_time
        if to_node != 0:
            current_time += service_time_dict.get(to_node, 0)
            due = due_date_dict.get(to_node, None)
            status = "Đúng Hạn!" if current_time <= due else "Không kịp"
            print(f"   - Đến điểm {to_node} lúc {current_time:.2f}s | Due: {due} {status}")

# Vẽ tuyến đường
plot_vehicle_routes(GBFS, coord_dict, due_date_dict, file_name=dataset_name)
plot_vehicle_routes_interactive(GBFS, coord_dict, due_date_dict, file_name=dataset_name)

# Tính quãng đường
qd_xe, qd_tong = tinh_quang_duong(GBFS, coord_dict)
print("\nChi tiết quãng đường GBFS:")
for i, d in enumerate(qd_xe):
    if d > 0.0:
        print(f"Quãng đường Xe {i + 1}: {d:.2f}")
print(f"Tổng quãng đường của tất cả xe (GBFS): {qd_tong:.2f} m\n")
