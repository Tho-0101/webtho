import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
import sys
import os

# --- Import các hàm CSDL của bạn ---

# Chúng ta sẽ dùng các lệnh import tuyệt đối (absolute imports)
# Điều này yêu cầu bạn phải cấu hình PyCharm đúng cách
try:
    from ketnoidb.ketnoi_mysql import ket_noi_mysql
    from common.getdanhmuc import get_danh_sach_danhmuc  # Sửa: laydanhmuc -> getdanhmuc
    from common.insertdanhmuc import insert_danh_muc  # Sửa: themdanhmuc -> insertdanhmuc
    from common.xoadanhmuc import delete_danh_muc  # Giữ nguyên
    from common.suadanhmuc import update_danh_muc  # Sửa: capnhatdanhmuc -> suadanhmuc
except ImportError as e:
    # Lỗi này 99% xảy ra vì PyCharm không biết thư mục gốc (PythonProject) ở đâu
    print(f"--- LỖI IMPORT: {e} ---")
    messagebox.showerror("Lỗi Import",
                         f"Không tìm thấy mô-đun: {e}\n\n"
                         "BẠN CẦN LÀM:\n\n"
                         "1. Trong PyCharm, nhìn cây thư mục bên trái.\n"
                         "2. Chuột phải vào thư mục cha (PythonProject).\n"
                         "3. Chọn 'Mark Directory as' -> 'Sources Root'.\n"
                         "4. Chạy lại chương trình.")
    sys.exit()  # Thoát nếu không import được

# --- Biến toàn cục cho kết nối CSDL ---
connection = None


# --- CÁC HÀM XỬ LÝ SỰ KIỆN ---

def load_data_to_treeview():
    """
    Lấy dữ liệu từ CSDL và hiển thị lên TreeView
    """
    for item in tree.get_children():
        tree.delete(item)

    danh_sach = get_danh_sach_danhmuc(connection)

    if danh_sach:
        for dm in danh_sach:
            tree.insert("", tk.END, values=dm)
    print("Cập nhật dữ liệu TreeView thành công.")


def on_tree_select(event):
    """
    Khi người dùng nhấp vào một hàng trong TreeView,
    dữ liệu sẽ được điền vào các ô Entry.
    """
    selected_item = tree.focus()
    if not selected_item:
        return

    values = tree.item(selected_item, 'values')

    clear_entries()

    entry_id.config(state='normal')
    entry_id.insert(0, values[0])
    entry_id.config(state='readonly')

    entry_ten.insert(0, values[1])
    entry_mota.insert(0, values[2])


def clear_entries():
    """
    Xóa sạch nội dung trong các ô Entry
    """
    entry_id.config(state='normal')
    entry_id.delete(0, tk.END)
    entry_id.config(state='readonly')

    entry_ten.delete(0, tk.END)
    entry_mota.delete(0, tk.END)
    print("Đã làm mới các ô nhập liệu.")
    if tree.focus():
        tree.selection_remove(tree.focus())


def add_category():
    """
    Xử lý sự kiện nút "Thêm"
    """
    ten = entry_ten.get()
    mota = entry_mota.get()

    if not ten:
        messagebox.showwarning("Thiếu thông tin", "Tên danh mục không được để trống.")
        return

    try:
        # Gọi hàm insert từ file common/insertdanhmuc.py
        insert_danh_muc(connection, ten, mota)
        messagebox.showinfo("Thành công", "Đã thêm danh mục mới thành công!")
        clear_entries()
        load_data_to_treeview()
    except Error as e:
        messagebox.showerror("Lỗi CSDL", f"Lỗi khi thêm danh mục: {e}")


def delete_category():
    """
    Xử lý sự kiện nút "Xóa"
    """
    id_dm = entry_id.get()

    if not id_dm:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một danh mục từ danh sách để xóa.")
        return

    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa danh mục có ID {id_dm} không?"):
        try:
            # Gọi hàm delete từ file common/xoadanhmuc.py
            delete_danh_muc(connection, int(id_dm))
            messagebox.showinfo("Thành công", f"Đã xóa danh mục ID {id_dm} thành công!")
            clear_entries()
            load_data_to_treeview()
        except ValueError:
            messagebox.showerror("Lỗi", "ID danh mục không hợp lệ.")
        except Error as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa danh mục: {e}")


def update_category():
    """
    Xử lý sự kiện nút "Sửa"
    """
    id_dm = entry_id.get()
    ten_moi = entry_ten.get()
    mota_moi = entry_mota.get()

    if not id_dm:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một danh mục từ danh sách để sửa.")
        return

    if not ten_moi:
        messagebox.showwarning("Thiếu thông tin", "Tên danh mục không được để trống.")
        return

    try:
        # Gọi hàm update từ file common/suadanhmuc.py
        update_danh_muc(connection, int(id_dm), ten_moi, mota_moi)
        messagebox.showinfo("Thành công", f"Đã cập nhật danh mục ID {id_dm} thành công!")
        clear_entries()
        load_data_to_treeview()
    except ValueError:
        messagebox.showerror("Lỗi", "ID danh mục không hợp lệ.")
    except Error as e:
        messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật danh mục: {e}")


def on_closing():
    """
    Xử lý sự kiện khi đóng cửa sổ
    """
    global connection
    if connection and connection.is_connected():
        connection.close()
        print("Đã đóng kết nối CSDL.")
    window.destroy()


# --- KHỞI TẠO KẾT NỐI CSDL ---
try:
    # (Hãy thay đổi thông tin kết nối của bạn ở đây nếu cần)
    connection = ket_noi_mysql("localhost", "root", "", "qlankhang")
    if connection is None or not connection.is_connected():
        messagebox.showerror("Lỗi Kết Nối", "Không thể kết nối đến CSDL. Vui lòng kiểm tra lại.")
        sys.exit()
except Error as e:
    messagebox.showerror("Lỗi Kết Nối", f"Lỗi khi kết nối CSDL: {e}")
    sys.exit()

# --- THIẾT KẾ GIAO DIỆN (GUI) ---

# 1. Cửa sổ chính
window = tk.Tk()
window.title("Quản lý Danh mục Sản phẩm")
window.geometry("800x500")

# 2. Khung Form nhập liệu (bên trái)
frame_form = tk.Frame(window, padx=10, pady=10)
frame_form.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_form, text="THÔNG TIN DANH MỤC", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

# ID
tk.Label(frame_form, text="ID Danh mục:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
entry_id = tk.Entry(frame_form, font=("Arial", 11), state='readonly')
entry_id.grid(row=1, column=1, pady=5, padx=5)

# Tên danh mục
tk.Label(frame_form, text="Tên danh mục:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
entry_ten = tk.Entry(frame_form, font=("Arial", 11), width=30)
entry_ten.grid(row=2, column=1, pady=5, padx=5)

# Mô tả
tk.Label(frame_form, text="Mô tả:", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
entry_mota = tk.Entry(frame_form, font=("Arial", 11), width=30)
entry_mota.grid(row=3, column=1, pady=5, padx=5)

# 3. Khung các nút chức năng (dưới form)
frame_buttons = tk.Frame(frame_form)
frame_buttons.grid(row=4, column=0, columnspan=2, pady=20)

btn_them = tk.Button(frame_buttons, text="Thêm", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=8,
                     command=add_category)
btn_them.grid(row=0, column=0, padx=5)

btn_xoa = tk.Button(frame_buttons, text="Xóa", font=("Arial", 11, "bold"), bg="#f44336", fg="white", width=8,
                    command=delete_category)
btn_xoa.grid(row=0, column=1, padx=5)

btn_sua = tk.Button(frame_buttons, text="Sửa", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", width=8,
                    command=update_category)
btn_sua.grid(row=0, column=2, padx=5)

btn_lam_moi = tk.Button(frame_form, text="Làm mới Form", font=("Arial", 11), command=clear_entries)
btn_lam_moi.grid(row=5, column=0, columnspan=2, pady=10)

# 4. Khung Hiển thị Danh sách (bên phải)
frame_list = tk.Frame(window, padx=10, pady=10)
frame_list.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(frame_list, text="DANH SÁCH HIỆN CÓ", font=("Arial", 14, "bold")).pack(pady=10)

# Cột cho TreeView
columns = ('id', 'ten', 'mo_ta')
tree = ttk.Treeview(frame_list, columns=columns, show='headings')

tree.heading('id', text='ID')
tree.heading('ten', text='Tên Danh mục')
tree.heading('mo_ta', text='Mô tả')

tree.column('id', width=50, anchor=tk.CENTER)
tree.column('ten', width=150)
tree.column('mo_ta', width=250)

scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

tree.bind('<<TreeviewSelect>>', on_tree_select)

# --- CHẠY ỨNG DỤNG ---

load_data_to_treeview()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()