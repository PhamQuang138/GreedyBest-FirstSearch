from visualize.Printer import print_one_txt_file
from algorithms.GreedyBFS import greedy_bfs_multi_vehicles
from visualize.Printer import plot_vehicle_routes, plot_vehicle_routes_interactive, tinh_quang_duong

if __name__ == "__main__":
    coord_dict, time_dict, demand_dict = print_one_txt_file("c203.txt")

    # THAY ĐỔI: mỗi xe chọn 4 khách gần nhất, không trùng
    vehicle_routes = greedy_bfs_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)

    for i, r in enumerate(vehicle_routes):
        print(f"🚚 Xe {i + 1}: {r}")

    plot_vehicle_routes(vehicle_routes, coord_dict, file_name="c203")
    plot_vehicle_routes_interactive(vehicle_routes, coord_dict, file_name="c203")

    qd_xe, qd_tong = tinh_quang_duong(vehicle_routes, coord_dict)

    for i, d in enumerate(qd_xe):
        print(f"🚚 Quãng đường Xe {i+1}: {d:.2f}")

    print(f"📦 Tổng quãng đường của tất cả 25 xe: {qd_tong:.2f}")
