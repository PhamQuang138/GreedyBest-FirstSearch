import os

def print_one_txt_file(file_name):
    # Xác định thư mục chứa các file
    input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "input"))
    file_path = os.path.join(input_folder, file_name)

    if not os.path.exists(file_path):
        print(f"❌ File '{file_name}' không tồn tại trong thư mục model/input/")
        return

    print(f"==================== 📄 File: {file_name} ====================")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content.strip())
