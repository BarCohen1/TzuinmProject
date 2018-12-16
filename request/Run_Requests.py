import Technion_Request as Technion
import Huji_Request as Huji
import Tlv_Request as Tlv
import Beer_Sheva_Request as Beer
import Profs as Profs



a = Profs.Prof('אזרחות',5,50)
b = Profs.Prof('אנגלית', 5, 90)
c = Profs.Prof('הבעה עברית', 5, 90)
d = Profs.Prof('הסטוריה', 5, 80)
e = Profs.Prof('מתמטיקה', 5, 90)
f = Profs.Prof('ספרות', 5, 90)
g = Profs.Prof('תנ"ך', 5, 90)
listp = [a,b,c,d,e,f,g]


def main(profs_list, psycho):
    Technion.Technion_Request(profs_list, psycho).print_results()
    Huji.Huji_Request(profs_list, psycho).print_results()
    Tlv.Tlv_Request(profs_list,psycho).print_results()
    Beer.Beer_Sheva_Request(profs_list,psycho).print_results()


if __name__ == "__main__":
    main(listp, ('770', '770', '700', '150'))

