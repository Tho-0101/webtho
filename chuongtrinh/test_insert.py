from common.insertdanhmuc import insert_danh_muc
from ketnoidb.ketnoi_mysql import ket_noi_mysql
connection = ket_noi_mysql("localhost", "root", "", "qlankhang")

while True:

        ten=input("nhập tên dm")
        mo_ta=input("nhập vào mô ta")
        insert_danh_muc(connection,ten,mo_ta)
        con=input("tt y;thoat nhan bat ki")
        if con=="y":
            break
