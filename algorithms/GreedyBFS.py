from algorithms.Heuristic import euclidean_distance

def greedy_bfs(coord_dict, due_date_dict,
               num_vehicles=25, max_customers_per_vehicle=4, speed=1.0):
    unvisited = set(coord_dict.keys()) - {0}
    vehicle_routes = []

    for _ in range(num_vehicles):
        current_id = 0
        current_time = 0
        route = [0]

        for _ in range(max_customers_per_vehicle):
            feasible = []

            for cust_id in unvisited:
                travel_time = euclidean_distance(current_id, cust_id, coord_dict) / speed
                arrival_time = current_time + travel_time

                if arrival_time <= due_date_dict[cust_id]:
                    feasible.append((cust_id, travel_time))

            if not feasible:
                break

            # Chọn khách gần nhất trong số khả thi
            next_id, travel_time = min(feasible, key=lambda x: x[1])
            current_time += travel_time
            route.append(next_id)
            unvisited.remove(next_id)
            current_id = next_id

        route.append(0)  # quay lại depot
        vehicle_routes.append(route)

        if not unvisited:
            break  # đã thăm hết khách hàng

    return vehicle_routes
