from visualize.Printer import print_one_txt_file
from algorithms.GreedyBFS import greedy_bfs_multi_vehicles
from visualize.Printer import plot_vehicle_routes, plot_vehicle_routes_interactive, tinh_quang_duong
from algorithms.A_star import a_star_single_vehicle, a_star_multi_vehicles

if __name__ == "__main__":
    coord_dict, time_dict, demand_dict = print_one_txt_file("c203.txt")

    vehicle_routes = greedy_bfs_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)
    vehicle_routes1 = a_star_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)
    for i, r in enumerate(vehicle_routes):
        print(f"Xe {i + 1}: {r}")

    plot_vehicle_routes(vehicle_routes, coord_dict, file_name="r109")
    plot_vehicle_routes_interactive(vehicle_routes, coord_dict, file_name="r109")

    qd_xe, qd_tong = tinh_quang_duong(vehicle_routes, coord_dict)
    plot_vehicle_routes(vehicle_routes1, coord_dict, file_name="xr109")
    plot_vehicle_routes_interactive(vehicle_routes1, coord_dict, file_name="xr109")

    qd_xe, qd_tong = tinh_quang_duong(vehicle_routes1, coord_dict)

    for i, d in enumerate(qd_xe):
        print(f"Quãng đường Xe {i+1}: {d:.2f}")

    print(f"Tổng quãng đường của tất cả 25 xe: {qd_tong:.2f}")
