import mysql.connector
from mysql.connector import Error

def insert_danh_muc(connection, ten_danhmuc, mo_ta):
    """
    Hàm thêm mới một danh mục vào bảng 'danhmuc'
    - connection: đối tượng kết nối MySQL (đã được tạo từ ket_noi_mysql)
    - ten_danhmuc: tên danh mục cần thêm
    - mota: mô tả danh mục
    """
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO danhmuc (ten_danhmuc, mo_ta) VALUES (%s, %s)"
        val = (ten_danhmuc, mo_ta)
        cursor.execute(sql, val)
        connection.commit()
        print("✅ Thêm danh mục thành công!")
    except Error as e:
        print(f"❌ Lỗi khi thêm danh mục: {e}")
    finally:
        cursor.close()
