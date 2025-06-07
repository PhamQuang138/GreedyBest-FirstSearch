from visualize.Printer import print_one_txt_file
from algorithms.GreedyBFS import greedy_bfs_multi_vehicles
from visualize.Printer import plot_vehicle_routes, plot_vehicle_routes_interactive, tinh_quang_duong
from algorithms.A_star import a_star_single_vehicle, a_star_multi_vehicles

if __name__ == "__main__":
    coord_dict, time_dict, demand_dict = print_one_txt_file("c203.txt")

    GBFS = greedy_bfs_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)
    A_star = a_star_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4)
    for i, r in enumerate(GBFS):
        print(f"Xe {i + 1}: {r}")
    for i, r in enumerate(A_star):
        print(f"Xe {i + 1}: {r}")

    plot_vehicle_routes(GBFS, coord_dict, file_name="c203")
    plot_vehicle_routes_interactive(GBFS, coord_dict, file_name="c203")
    qd_xe, qd_tong = tinh_quang_duong(GBFS, coord_dict)

    plot_vehicle_routes(A_star, coord_dict, file_name="A203")
    plot_vehicle_routes_interactive(A_star, coord_dict, file_name="A203")
    qd_xe1, qd_tong1 = tinh_quang_duong(A_star, coord_dict)
    print("Test GBFS: \n")
    for i, d in enumerate(qd_xe):
        print(f"Quãng đường Xe {i+1}: {d:.2f}")
    print(f"Tổng quãng đường của tất cả 25 xe: {qd_tong:.2f}")
    print("\n")
    print("Test A*: \n")
    for i, d in enumerate(qd_xe1):
        print(f"Quãng đường Xe {i+1}: {d:.2f}")
    print(f"Tổng quãng đường của tất cả 25 xe: {qd_tong1:.2f}")
