
from common.suadanhmuc import update_danh_muc
from ketnoidb.ketnoi_mysql import ket_noi_mysql
connection = ket_noi_mysql("localhost", "root", "", "qlankhang")

while True:
        ma=input("nhapma")
        ten=input("nhập tên dm")
        mo_ta=input("nhập vào mô ta")

        update_danh_muc(connection, ma, ten, mo_ta)
        if con!="y":
            break
