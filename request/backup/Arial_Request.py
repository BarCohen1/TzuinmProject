import urllib
import requests
import re
import Profs
import Result
url_ariel='http://www.ariel.ac.il/projects/Tzmm/Mark/CalcMark.asp'
payload_arial='selDefaultMik=1&txtNumberMikc1=3&txtMust1=*&txtNameMikc1=%E0%F0%E2%EC%E9%FA&txtNumberUnits1=5&txtNumberMark1=90&txtNumberMikc2=2&txtMust2=*&txtNameMikc2=%E4%E1%F2%E4+%F2%E1%F8%E9%FA&txtNumberUnits2=5&txtNumberMark2=90&txtNumberMikc3=20&txtMust3=*&txtNameMikc3=%EE%FA%EE%E8%E9%F7%E4&txtNumberUnits3=5&txtNumberMark3=90&txtNumberMikc4=45&txtMust4=*&txtNameMikc4=%E0%E6%F8%E7%E5%FA&txtNumberUnits4=5&txtNumberMark4=90&txtNumberMikc5=7&txtMust5=*&txtNameMikc5=%E4%F1%E8%E5%F8%E9%E4+%2F+%FA%F2%27%27%E9%2F+%E9%E3%F2+%E4%F2%ED+%E5%E4%EE%E3%E9%F0%E4&txtNumberUnits5=&txtNumberMark5=&txtNumberMikc6=4&txtMust6=*&txtNameMikc6=%F1%F4%F8%E5%FA%2F%EE%E7%F9%E1%FA+%E9%F9%F8%E0%EC&txtNumberUnits6=&txtNumberMark6=&txtNumberMikc7=1&txtMust7=*&txtNameMikc7=%FA%F0%27%27%EA&txtNumberUnits7=&txtNumberMark7=&txtNameMikc8=0&txtNumberMikc8=0&txtMust8=&txtNumberUnits8=&txtNumberMark8=&txtNameMikc9=0&txtNumberMikc9=0&txtMust9=&txtNumberUnits9=&txtNumberMark9=&txtNameMikc10=0&txtNumberMikc10=0&txtMust10=&txtNumberUnits10=&txtNumberMark10=&txtNameMikc11=0&txtNumberMikc11=0&txtMust11=&txtNumberUnits11=&txtNumberMark11=&txtNameMikc12=0&txtNumberMikc12=0&txtMust12=&txtNumberUnits12=&txtNumberMark12=&txtNameMikc13=0&txtNumberMikc13=0&txtMust13=&txtNumberUnits13=&txtNumberMark13=&txtNameMikc14=0&txtNumberMikc14=0&txtMust14=&txtNumberUnits14=&txtNumberMark14=&txtNumberPsico=0&txtNumberQuantitative=0&txtTatTciyn=0&txtDiscription=&txtAllMikc=14&txtShowOnScreen=0&txtStudentID=204037600&txtFirstN=%E9%F9%F8%E0%EC&txtLastN=%E9%F9%F8%E0%EC%E9&txtCellPhone=0501234567&txtEmail=israel%40gmail.com&txtMaxlaka=%2F'
header_arial = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

# Huji request object - creates a request to huji in c-tor, generate and saves bagrot_avg score, pyscho score, over all
# score and the prof's accepted in huji.
class Arial_Request:
    bagrut_score = '' # avg bagrut score
    pyscho_score = () # entered pyscho score , 0 - overall_Score, 1 - math , 2 - hebrew , 3- english
    over_all_score = ''
    profs_accepted = []
    # tlv_request = Request # is this the right syntax
    ARIAL_HASH = {'אזרחות': '24', 'אנגלית': '16', 'הבעה עברית': '11', 'הסטוריה': '22', 'מתמטיקה': '35',
                'ספרות': '8', 'תנ"ך': '1'}

    # generate the requests and saves the results into the data variables
    # psycho - entered as a 4-way tuple ( 0 - overall_Score, 1 - math , 2 - hebrew , 3- english)
    # profs_list - entered as a list of Pros's with prof's name, units and grade for each prof
    def __init__(self, profs_list, psycho):
        self.Profs = profs_list
        self.psycho_score = psycho
        self.get_bagrut_avg()
        self.get_overall_score()
        self.get_accepted_majors()


    # in charge of turning Prof values into fitting Huji form data request
    def parse_subjects(self):
        huji_list = []
        for val in self.Profs:
            cur_prof = {}
            id = self.find_subject_id(val.name)
            cur_prof["SubjectID"] = int(id)
            cur_prof["ISProject"] = 'false'
            cur_prof["Points"] = str(val.units)
            cur_prof["Grade"] = str(val.grade)
            huji_list.append(cur_prof)
        payload = {"Year" : 2018 , "SectorID": 1, "Subjects": huji_list} # Year update needed each year
        return str(payload)

    def get_accepted_majors(self):
        # r = requests.post(HUJI_URL_MAJORS, data=accepted_paylod , headers={'Content-Type': 'application/x-www-form-urlencoded'})  # genreate TLV request here
       pass
    def get_overall_score(self):
        pass

    # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it
    def get_bagrut_avg(self):
        r = requests.post(url_ariel, data =self.parse_subjects() , headers = header_arial)
        # avg_score_list = re.search(r'("MarkAverage":(.*))', r.text)
        # the score is grouped 2 at the regex return value and comes with an annoying ',' , which is discraded by split
        # undivded_bagrot_avg = float(avg_score_list[2].split(',')[0])
        # self.bagrut_score = str(undivded_bagrot_avg / 10)

    def find_subject_id(self, subject_name):
        return self.HUJI_HASH[subject_name]

a = Profs.Prof('אזרחות',5,90)
b = Profs.Prof('אנגלית', 5, 80)
c = Profs.Prof('הבעה עברית', 5, 80)
d = Profs.Prof('הסטוריה', 5, 80)
e = Profs.Prof('מתמטיקה', 5, 80)
f = Profs.Prof('ספרות', 5, 80)
g = Profs.Prof('תנ"ך', 5, 80)
listp = [a,b,c,d,e,f,g]
request = Arial_Request(listp, ('660', '630', '600', '150'))