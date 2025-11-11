import mysql.connector
from mysql.connector import Error

def ket_noi_mysql(host_name, user_name, user_password, db_name):
    """
    Hàm kết nối tới cơ sở dữ liệu MySQL
    Trả về đối tượng connection nếu thành công, None nếu lỗi
    """
    try:
        connection = mysql.connector.connect(
            host=host_name,       # ✅ dùng biến, không dùng chuỗi
            user=user_name,
            password=user_password,
            database='qlankhang'
        )
        if connection.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return connection
    except Error as e:
        print(f"❌ Lỗi khi kết nối MySQL: {e}")
        return None

