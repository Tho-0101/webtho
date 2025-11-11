

from common.xoadanhmuc import delete_danh_muc
from ketnoidb.ketnoi_mysql import ket_noi_mysql
connection = ket_noi_mysql("localhost", "root", "", "qlankhang")

ma=input("nhap ma")
delete_danh_muc(connection,ma)