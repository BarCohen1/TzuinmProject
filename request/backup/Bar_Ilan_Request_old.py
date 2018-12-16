import urllib
import requests
import re
import Profs
import Result
Bar_Ilan_Get_Cookie = 'https://dory.os.biu.ac.il/EnrollmentChances/pages/index.jsp'
Bar_Ilan_GET_Bagrot_URL = 'https://dory.os.biu.ac.il/EnrollmentChances/pages/input_bagrut.jsp'
Bar_Ilan_URL_Bagrot = 'https://dory.os.biu.ac.il/EnrollmentChances/pages/CalcBagrutResultsAction.do'
Bar_Ilan_add_prof_url = 'https://dory.os.biu.ac.il/EnrollmentChances/pages/AddNewSubjectAction.do'
# HUJI_URL_MAJORS = 'http://www.huji.ac.il/dataj/controller/getinfo/TLM-CHECKSICKUY'
#TODO - how to auto get cookie into header-bar-ilan post request
#TODO - Hash tabel for Bar ilan added prof's , optinal and mandator
#TODO - sechem
#TODO - get accepted majors

# Huji request object - creates a request to huji in c-tor, generate and saves bagrot_avg score, pyscho score, over all
# score and the prof's accepted in huji.
class Bar_Ilan_Request:
    bagrut_score = '' # avg bagrut score
    pyscho_score = () # entered pyscho score , 0 - overall_Score, 1 - math , 2 - hebrew , 3- english
    over_all_score = ''
    profs_accepted = []
    cookie = ''
    # tlv_request = Request # is this the right syntax
    NORMAL_HASH = {'אזרחות': '24', 'אנגלית': '16', 'הבעה עברית': '11', 'הסטוריה': '22', 'מתמטיקה': '35',
                'ספרות': '8', 'תנ"ך': '1'}

    Bar_Ilan_ADDED_PROFS_HASH = { 'פילוסופיה': '17' }
    # generate the requests and saves the results into the data variables
    # psycho - entered as a 4-way tuple ( 0 - overall_Score, 1 - math , 2 - hebrew , 3- english)
    # profs_list - entered as a list of Pros's with prof's name, units and grade for each prof
    def __init__(self, profs_list, psycho):
        self.Profs = profs_list
        self.psycho_score = psycho
        # self.get_referer()
        # self.get_added_prof(Profs.Prof('אזרחות',5,90))
        self.get_bagrut_avg()
        # self.get_overall_score()
        # self.get_accepted_majors()

    def get_referer(self):
        r = requests.get(Bar_Ilan_Get_Cookie)
        # print(r.headers.get('Set-Cookie'))
        cookie = str(r.headers.get('Set-Cookie').split(';')[0])
        print('This is the orginal parsed cookie from the dori domain: ')
        # cookie_dict = ({'Cookie': 'JSESSIONID=0000BsBPEPNGTkNY6OYEYtpOHtG:-1'})
        # cookie_dict = ({'Cookie': cookie})
        # print(cookie_dict)
        a='"'+cookie+'"'
        print("a is:" + cookie)
        temp = {'Cookie': cookie}
        r = requests.get(Bar_Ilan_GET_Bagrot_URL)
        print(r.text)
        print('This is the headers the request got after the request for the dori GET bagrut websiter:')
        # print(r.text)
        print(r.request.headers)
        # print(cookie)

    # in charge of turning Prof values into fitting Huji form data request
    def parse_subjects(self):
        huji_list = []
        for val in self.Profs:
            cur_prof = {}
            if val not in self.NORMAL_HASH:
                self.get_added_prof(val)
            else:
                id = self.find_subject_id(val.name)

                cur_prof["SubjectID"] = int(id)
                cur_prof["ISProject"] = 'false'
                cur_prof["Points"] = str(val.units)
                cur_prof["Grade"] = str(val.grade)
                huji_list.append(cur_prof)
            payload = {"Year" : 2018 , "SectorID": 1, "Subjects": huji_list} # Year update needed each year
        return str(payload)


    def get_added_prof(self, val):
        # id = self.Bar_Ilan_ADDED_PROFS_HASH[val.name]
        # payload = 'score='+val.grade+'&units='+ val.units+'&bagrutId='+id+'&actionType=optional'
        a ='score=55&units=5&bagrutId=17&actionType=optional'
        # print(payload)
        print(self.cookie)
        r = requests.post(Bar_Ilan_add_prof_url , data=a, headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie' :'JSESSIONID=00002Ik5OkGYxWk1O4ofNEn-n1k:-1'})
        print(r.request.headers)
        print(r.text)

    def get_accepted_majors(self):
        pass

    def get_overall_score(self):
        pass

    # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it
    def get_bagrut_avg(self):
        # print(self.cookie)
        print("hey")
        with requests.Session() as s:
            r = s.get(Bar_Ilan_Get_Cookie)
            # print(r.headers.get('Set-Cookie'))

            cookie = str(r.headers.get('Set-Cookie').split(';')[0])
            # a = '"' + cookie + '"'

            header_bar_ilan = {'Content-Type': 'application/x-www-form-urlencoded' , 'Cookie': 'JSESSIONID=00005Z1SkddS4O9hDTalztHLFtr:-'}

            # r = s.post(URL2, data="username and password data payload")
            r = s.post(Bar_Ilan_URL_Bagrot, data='inputBagrutExamForm.mandatoryBagrutExamBeans%5B0%5D.units=5&inputBagrutExamForm.mandatoryBagrutExamBeans%5B0%5D.score=77&inputBagrutExamForm.mandatoryBagrutExamBeans%5B1%5D.units=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B1%5D.score=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B2%5D.units=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B2%5D.score=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B3%5D.units=5&inputBagrutExamForm.mandatoryBagrutExamBeans%5B3%5D.score=77&inputBagrutExamForm.mandatoryBagrutExamBeans%5B4%5D.units=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B4%5D.score=&inputBagrutExamForm.mandatoryBagrutExamBeans%5B5%5D.units=5&inputBagrutExamForm.mandatoryBagrutExamBeans%5B5%5D.score=99&inputBagrutExamForm.mandatoryBagrutExamBeans%5B6%5D.units=5&inputBagrutExamForm.mandatoryBagrutExamBeans%5B6%5D.score=77&inputBagrutExamForm.mandatoryBagrutExamBeans%5B7%5D.units=5&inputBagrutExamForm.mandatoryBagrutExamBeans%5B7%5D.score=77&inputBagrutExamForm.optionalBagrutExamBeans%5B0%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B0%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B1%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B1%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B2%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B2%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B3%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B3%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B4%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B4%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B5%5D.units=5&inputBagrutExamForm.optionalBagrutExamBeans%5B5%5D.score=77&inputBagrutExamForm.optionalBagrutExamBeans%5B6%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B6%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B7%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B7%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B8%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B8%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B9%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B9%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B10%5D.units=&inputBagrutExamForm.optionalBagrutExamBeans%5B10%5D.score=&inputBagrutExamForm.optionalBagrutExamBeans%5B11%5D.units=5&inputBagrutExamForm.optionalBagrutExamBeans%5B11%5D.score=99', headers = header_bar_ilan, cookies = '')
        # )
        print(r.text)
        print(r.request.headers)
        print(cookie)

        # self.parse_subjects()
        # r = requests.post(Bar_Ilan_URL_Bagrot, data =self.parse_subjects() , headers = {'Content-Type': 'application/json'})
        # avg_score_list = re.search(r'("MarkAverage":(.*))', r.text)


    def find_subject_id(self, subject_name):
        return self.NORMAL_HASH[subject_name]

# a = Profs.Prof('אזרחות',5,90)
# b = Profs.Prof('אנגלית', 5, 80)
# c = Profs.Prof('הבעה עברית', 5, 80)
# d = Profs.Prof('הסטוריה', 5, 80)
# e = Profs.Prof('מתמטיקה', 5, 80)
# f = Profs.Prof('ספרות', 5, 80)
# g = Profs.Prof('תנ"ך', 5, 80)
g = Profs.Prof('פילוסופיה', 5, 80)
listp = [g]
request = Bar_Ilan_Request(listp, 660)
