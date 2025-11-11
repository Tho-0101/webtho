from ketnoidb.ketnoi_mysql import ket_noi_mysql

conn = ket_noi_mysql("localhost", "root", "", "qlankhang")

if conn:
    print("Kết nối thành công, bạn có thể thực thi truy vấn tại đây.")
    conn.close()
else:
    print("Kết nối thất bại.")
