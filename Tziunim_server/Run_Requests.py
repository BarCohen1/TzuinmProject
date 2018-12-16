from .Technion_Request import *
from .Huji_Request import *
from .Tlv_Request import *
from .Beer_Sheva_Request import *
from .Profs import *


a = Prof('אזרחות',5,90)
b = Prof('אנגלית', 5, 80)
c = Prof('הבעה עברית', 5, 80)
d = Prof('הסטוריה', 5, 80)
e = Prof('מתמטיקה', 5, 80)
f = Prof('ספרות', 5, 80)
g = Prof('תנ"ך', 5, 94)
listp = [a,b,c,d,e,f,g]

class Generate:

    def __init__(self, profs_list, psycho):
        self.profs = profs_list
        self.psycho = psycho

def main(profs_list,psycho):
    technion_results=Technion_Request(profs_list, psycho)
    huji_results=Huji_Request(profs_list, psycho)
    tlv_results=Tlv_Request(profs_list,psycho)
    bgu_results=Beer_Sheva_Request(profs_list,psycho)
    all_results=[technion_results,huji_results,tlv_results,bgu_results]

    return(all_results)

def parse_modle_1_request(user_input:dict):
    proof_list = []
    for key in user_input:
        proof_list.append(Prof(key, user_input[key][0], user_input[key][1]))
    return proof_list



