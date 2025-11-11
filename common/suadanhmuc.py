import mysql.connector
from mysql.connector import Error


def update_danh_muc(connection, id_danhmuc, ten_danhmuc_moi, mo_ta_moi):
    """
    Hàm cập nhật thông tin một danh mục trong bảng 'danhmuc' dựa vào id_danhmuc
    - connection: đối tượng kết nối MySQL
    - id_danhmuc: ID của danh mục cần cập nhật (khóa chính)
    - ten_danhmuc_moi: Tên danh mục mới
    - mo_ta_moi: Mô tả mới
    """
    cursor = None
    try:
        cursor = connection.cursor()

        # Câu lệnh SQL UPDATE
        sql = "UPDATE danhmuc SET ten_danhmuc = %s, mo_ta = %s WHERE id_danhmuc = %s"

        # Giá trị truyền vào (lưu ý thứ tự phải khớp với câu SQL)
        # (ten_danhmuc_moi, mo_ta_moi, id_danhmuc)
        val = (ten_danhmuc_moi, mo_ta_moi, id_danhmuc)

        cursor.execute(sql, val)
        connection.commit()

        # Kiểm tra xem có hàng nào thực sự bị ảnh hưởng không
        if cursor.rowcount > 0:
            print(f"✅ Cập nhật danh mục có ID {id_danhmuc} thành công!")
        else:
            print(f"⚠️ Không tìm thấy danh mục nào có ID {id_danhmuc} để cập nhật.")

    except Error as e:
        print(f"❌ Lỗi khi cập nhật danh mục: {e}")
        # Nếu lỗi thì rollback
        try:
            connection.rollback()
            print("🔄 Đã rollback thay đổi.")
        except Error as re:
            print(f"❌ Lỗi khi rollback: {re}")
    finally:
        # Đóng cursor
        if cursor:
            cursor.close()