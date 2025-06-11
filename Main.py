from visualize.Printer import print_one_txt_file
from visualize.Printer import plot_vehicle_routes, plot_vehicle_routes_interactive, tinh_quang_duong
from algorithms.GreedyBFS import greedy_bfs
from algorithms.A_star import a_star_multi_vehicles
from algorithms.Heuristic import euclidean_distance


# Đọc dữ liệu từ file
coord_dict, time_dict, demand_dict, due_date_dict = print_one_txt_file("r101.txt")

# Tạo due_date_dict từ time_dict (do Greedy cần để kiểm tra hạn)
due_date_dict = {k: v[1] for k, v in time_dict.items() if k != 0}

# Chạy thuật toán Greedy BFS (có xét due date)
GBFS = greedy_bfs(coord_dict, due_date_dict=due_date_dict, num_vehicles=25, max_customers_per_vehicle=4, speed=2)
#
# # Chạy thuật toán A*
# A_star = a_star_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)

# In kết quả GBFS
print("Test GBFS: \n")
speed =2
for i, r in enumerate(GBFS):
    print(f"Xe {i + 1}: {r}")
    current_time = 0
    for j in range(1, len(r)):
        from_node = r[j - 1]
        to_node = r[j]
        distance = euclidean_distance(from_node, to_node, coord_dict)
        current_time += distance / speed
        due = due_date_dict.get(to_node, None)
        if to_node != 0:
            print(f"   - Đến điểm {to_node} lúc {current_time:.2f}s | Due: {due} {'Đúng Hạn!' if current_time <= due else 'Không kịp'}")


# # In kết quả A*
# print("Test A*: \n")
# for i, r in enumerate(A_star):
#     print(f"Xe {i + 1}: {r}")

# plot_vehicle_routes(A_star, coord_dict, due_date_dict, file_name="A203")
# plot_vehicle_routes_interactive(A_star, coord_dict, due_date_dict, file_name="A203")
# qd_xe1, qd_tong1 = tinh_quang_duong(A_star, coord_dict)
plot_vehicle_routes(GBFS, coord_dict, due_date_dict, file_name="r101")
plot_vehicle_routes_interactive(GBFS, coord_dict, due_date_dict, file_name="r101")
qd_xe, qd_tong = tinh_quang_duong(GBFS, coord_dict)
# In quãng đường GBFS
print("Chi tiết quãng đường GBFS: \n")
for i, d in enumerate(qd_xe):
    print(f"Quãng đường Xe {i + 1}: {d:.2f}")
print(f"Tổng quãng đường của tất cả 25 xe (GBFS): {qd_tong:.2f}\n")

# # In quãng đường A*
# print("Chi tiết quãng đường A*: \n")
# for i, d in enumerate(qd_xe1):
#     print(f"Quãng đường Xe {i + 1}: {d:.2f}")
# print(f"Tổng quãng đường của tất cả 25 xe (A*): {qd_tong1:.2f}")


# Lưu Ý:
# Tốc độ thấp → Thời gian di chuyển giữa các điểm tăng lên:
# arrival_time = current_time + distance / speed
# Nếu arrival_time > due_date thì điểm đó bị loại khỏi các lựa chọn trong bước Greedy.
# Do đó, nếu tất cả các điểm không thể đến đúng hạn → thuật toán sẽ không chọn điểm nào thêm vào route
# → kết thúc sớm với route [0, 0].
# ⚠ Greedy Best First Search chọn điểm kế tiếp theo tiêu chí đánh giá
# (ví dụ gần nhất, tốt nhất theo heuristic) nhưng vẫn phải đảm bảo ràng buộc thời gian.
# Nếu không còn điểm nào thỏa mãn, nó sẽ dừng.