import mysql.connector
from mysql.connector import Error


def get_danh_sach_danhmuc(connection):
    """
    Hàm lấy tất cả danh mục từ bảng 'danhmuc'
    - connection: đối tượng kết nối MySQL
    - Trả về: Một danh sách (list) các tuples, mỗi tuple là một hàng (danh mục).
             Trả về None nếu có lỗi.
    """
    cursor = None
    try:
        cursor = connection.cursor()

        # Câu lệnh SQL SELECT
        sql = "SELECT * FROM danhmuc"

        cursor.execute(sql)

        # Lấy tất cả kết quả
        results = cursor.fetchall()

        print(f"✅ Lấy danh sách thành công! Tìm thấy {cursor.rowcount} danh mục.")
        return results

    except Error as e:
        print(f"❌ Lỗi khi lấy danh sách danh mục: {e}")
        return None  # Trả về None nếu có lỗi
    finally:
        # Đóng cursor
        if cursor:
            cursor.close()