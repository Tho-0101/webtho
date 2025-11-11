from common.getdanhmuc import get_danh_sach_danhmuc
from ketnoidb.ketnoi_mysql import ket_noi_mysql
connection = ket_noi_mysql("localhost", "root", "", "qlankhang")


get_danh_sach_danhmuc(connection)
danh_sach = get_danh_sach_danhmuc(connection)
if danh_sach:
    print("\n--- DANH SÁCH CÁC DANH MỤC ---")
    for dm in danh_sach:
        # dm[0] là id, dm[1] là tên, dm[2] là mô tả
        print(f"ID: {dm[0]} - Tên: {dm[1]}")
        # Hoặc in đầy đủ:
        # print(f"ID: {dm[0]}, Tên: {dm[1]}, Mô tả: {dm[2]}")
else:
    print("Không có danh mục nào hoặc đã xảy ra lỗi.")

# Đóng kết nối
if connection.is_connected():
    connection.close()