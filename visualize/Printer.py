import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.graph_objs as go
from algorithms.Heuristic import euclidean_distance

import os
import matplotlib.pyplot as plt

def print_one_txt_file(file_name):
    input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "input"))
    file_path = os.path.join(input_folder, file_name)

    if not os.path.exists(file_path):
        print(f"File '{file_name}' không tồn tại trong thư mục model/input/")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    # Tìm dòng bắt đầu bảng dữ liệu
    table_start_idx = None
    for i, line in enumerate(lines):
        if 'XCOORD' in line and 'YCOORD' in line:
            table_start_idx = i + 1
            break

    if table_start_idx is None:
        print("Không tìm thấy bảng chứa tọa độ trong file.")
        return

    data_lines = lines[table_start_idx:]
    coords = []
    depot = None

    for line in data_lines:
        parts = line.strip().split()
        if len(parts) >= 3 and parts[0].isdigit():
            cust_id = int(parts[0])
            x, y = int(parts[1]), int(parts[2])
            if cust_id == 0:
                depot = (x, y)
            else:
                coords.append((cust_id, x, y))

    if depot is None:
        print("Không tìm thấy điểm gốc (CUST NO. == 0).")
        return

    # Vẽ tọa độ và lưu ảnh
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "output"))
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(15, 15))
    for cust_id, x, y in coords:
        plt.scatter(x, y, color='blue', s=25)
        plt.text(x, y, f"{cust_id}", fontsize=9)

    depot_x, depot_y = depot
    plt.scatter(depot_x, depot_y, color='red', s=12, label="Depot")
    plt.text(depot_x + 1, depot_y, "Depot (P0)", fontsize=10, fontweight='bold')

    plt.title(f"Customer Coordinates from {file_name}")
    plt.xlabel("XCOORD")
    plt.ylabel("YCOORD")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()

    image_path = os.path.join(output_folder, file_name.replace('.txt', '_coordinates.png'))
    plt.savefig(image_path)
    plt.close()

    # Chuẩn bị các dict dữ liệu
    coord_dict = {cust_id: (x, y) for cust_id, x, y in coords}
    coord_dict[0] = depot

    time_dict = {}
    demand_dict = {}
    due_date_dict = {}
    service_time_dict = {}

    for line in data_lines:
        parts = line.strip().split()
        if len(parts) >= 7 and parts[0].isdigit():
            cust_id = int(parts[0])
            demand = int(parts[3])
            ready_time = int(parts[4])
            due_date = int(parts[5])
            service_time = int(parts[6])

            demand_dict[cust_id] = demand
            due_date_dict[cust_id] = due_date
            service_time_dict[cust_id] = service_time
            time_dict[cust_id] = (ready_time, due_date, service_time)

    return coord_dict, time_dict, demand_dict, due_date_dict, service_time_dict

def plot_vehicle_routes(vehicle_routes, coord_dict, due_date_dict, file_name='c101'):
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "output"))
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(15, 15))

    for cust_id, (x, y) in coord_dict.items():
        plt.scatter(x, y, color='blue', s=20)
        label = f"{cust_id}"
        if cust_id in due_date_dict:
            label += f"\n({due_date_dict[cust_id]})"
        plt.text(x, y, label, fontsize=7)

    depot_x, depot_y = coord_dict[0]
    plt.scatter(depot_x, depot_y, color='red', s=50, label="Depot")
    plt.text(depot_x + 1, depot_y, "Depot", fontsize=9, fontweight='bold')

    colors = cm.get_cmap('tab20', len(vehicle_routes))

    for i, route in enumerate(vehicle_routes):
        x_vals = [coord_dict[point][0] for point in route]
        y_vals = [coord_dict[point][1] for point in route]
        plt.plot(x_vals, y_vals, label=f"Xe {i + 1}", color=colors(i))

    plt.title(f"Tuyến đường của {len(vehicle_routes)} xe")
    plt.xlabel("XCOORD")
    plt.ylabel("YCOORD")
    plt.axis("equal")
    plt.legend(fontsize='small')
    plt.grid(True)

    save_path = os.path.join(output_folder, f"{file_name}_routes.png")
    plt.savefig(save_path)
    plt.close()
    print(f"Biểu đồ tuyến đường đã lưu tại: {save_path}")

def plot_vehicle_routes_interactive(vehicle_routes, coord_dict, due_date_dict, file_name='c203'):
    fig = go.Figure()

    # Vẽ điểm depot
    depot_x, depot_y = coord_dict[0]
    fig.add_trace(go.Scatter(
        x=[depot_x], y=[depot_y],
        mode='markers+text',
        marker=dict(size=8, color='red'),
        text=['Depot'],
        textposition='top center',
        hovertext=[f"Depot<br>X: {depot_x}, Y: {depot_y}"],
        hoverinfo='text',
        name='Depot'
    ))

    # Vẽ điểm khách
    for cust_id, (x, y) in coord_dict.items():
        if cust_id == 0:
            continue
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=6, color='blue'),
            text=[str(cust_id)],
            textposition='top center',
            hovertext=[f"Khách {cust_id}<br>X: {x}, Y: {y}<br>Due: {due_date_dict.get(cust_id, 'N/A')}"],
            hoverinfo='text',
            showlegend=False
        ))

    # Vẽ tuyến đường các xe (ẩn ban đầu)
    for i, route in enumerate(vehicle_routes):
        x_vals = [coord_dict[p][0] for p in route]
        y_vals = [coord_dict[p][1] for p in route]
        hover_texts = [
            f"{'Depot' if p == 0 else f'Khách {p}'}<br>X: {coord_dict[p][0]}, Y: {coord_dict[p][1]}<br>Due: {due_date_dict.get(p, 'N/A')}"
            for p in route
        ]
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines+markers',
            hovertext=hover_texts,
            hoverinfo='text',
            name=f"Xe {i + 1}",
            visible='legendonly'
        ))

    fig.update_layout(
        title="Tuyến đường các xe (click để xem chi tiết)",
        xaxis_title="X",
        yaxis_title="Y",
        width=1200,
        height=1200
    )

    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "output"))
    os.makedirs(output_folder, exist_ok=True)
    save_path = os.path.join(output_folder, f"{file_name}_interactive_routes.html")
    fig.write_html(save_path)
    print(f"Đã tạo biểu đồ tương tác tại: {save_path}")


def tinh_quang_duong(vehicle_routes, coord_dict):
    tong_quang_duong_tat_ca_xe = 0
    quang_duong_tung_xe = []

    for i, route in enumerate(vehicle_routes):
        total = 0
        for j in range(len(route) - 1):
            p1, p2 = route[j], route[j + 1]
            total += euclidean_distance(p1, p2, coord_dict)
        quang_duong_tung_xe.append(total)
        tong_quang_duong_tat_ca_xe += total

    return quang_duong_tung_xe, tong_quang_duong_tat_ca_xe
