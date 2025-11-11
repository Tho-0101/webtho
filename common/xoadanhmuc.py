import mysql.connector
from mysql.connector import Error


def delete_danh_muc(connection, id_danhmuc):
    """
    Hàm xóa một danh mục khỏi bảng 'danhmuc' dựa vào id_danhmuc
    - connection: đối tượng kết nối MySQL
    - id_danhmuc: id của danh mục cần xóa (khóa chính)
    """
    cursor = None
    try:
        cursor = connection.cursor()

        # Sửa tên cột thành 'id_danhmuc' cho khớp với CSDL của bạn
        sql = "DELETE FROM danhmuc WHERE id_danhmuc = %s"

        val = (id_danhmuc,)

        cursor.execute(sql, val)
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Xóa danh mục có ID {id_danhmuc} thành công!")
        else:
            print(f"⚠️ Không tìm thấy danh mục nào có ID {id_danhmuc} để xóa.")

    except Error as e:
        print(f"❌ Lỗi khi xóa danh mục: {e}")
        try:
            connection.rollback()
            print("🔄 Đã rollback thay đổi.")
        except Error as re:
            print(f"❌ Lỗi khi rollback: {re}")
    finally:
        if cursor:
            cursor.close()