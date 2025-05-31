from algorithms.Heuristic import euclidean_distance

def greedy_bfs_multi_vehicles(coord_dict, num_vehicles=25, max_customers_per_vehicle=4):
    unvisited = set(coord_dict.keys()) - {0}
    vehicle_routes = []

    for _ in range(num_vehicles):
        current_id = 0
        route = [0]

        for _ in range(max_customers_per_vehicle):
            if not unvisited:
                break
            # Chọn khách hàng gần nhất chưa phục vụ
            next_id = min(unvisited, key=lambda p: euclidean_distance(current_id, p, coord_dict))
            route.append(next_id)
            unvisited.remove(next_id)
            current_id = next_id

        route.append(0)  # quay lại depot
        vehicle_routes.append(route)

    return vehicle_routes
