import urllib
import requests
import re
from .Profs import *
from .Result import *

HUJI_URL_Bagrot = 'http://bagrut-calculator.huji.ac.il/api/bargrutCalculator/GetBagrutCalc/'
HUJI_URL_MAJORS = 'http://www.huji.ac.il/dataj/controller/getinfo/TLM-CHECKSICKUY'

#TODO left on huji: 1. deal with heseg(how?) 2. expend HUJI_HASH for all prof's 3. Build accpeted major's rejex in 'get accpeted major's func'

# Huji request object - creates a request to huji in c-tor, generate and saves bagrot_avg score, pyscho score, over all
# score and the prof's accepted in huji.
class Huji_Request:
    # bagrut_score = '' # avg bagrut score
    # pyscho_score = () # entered pyscho score , 0 - overall_Score, 1 - math , 2 - hebrew , 3- english
    # tlv_request = Request # is this the right syntax
    HUJI_HASH = {'אזרחות': '24', 'אנגלית': '16', 'הבעה עברית': '11', 'הסטוריה': '22', 'מתמטיקה': '35',
                'ספרות': '8', 'תנ"ך': '1'}

    # generate the requests and saves the results into the data variables
    # psycho - entered as a 4-way tuple ( 0 - overall_Score, 1 - math , 2 - hebrew , 3- english)
    # profs_list - entered as a list of Pros's with prof's name, units and grade for each prof
    def __init__(self, profs_list, psycho):
        self.Profs = profs_list
        self.psycho_score = psycho
        self.get_bagrut_avg()
        self.get_accepted_majors()
        # self.result = Result.Result(self)

    # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it
    def find_subject_id(self, subject_name):
        return self.HUJI_HASH[subject_name]
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

    def get_bagrut_avg(self):
        r = requests.post(HUJI_URL_Bagrot, data=self.parse_subjects(), headers={'Content-Type': 'application/json'})
        avg_score_list = re.search(r'("MarkAverage":(.*))', r.text)
        # the score is grouped 2 at the regex return value and comes with an annoying ',' , which is discraded by split
        undivded_bagrot_avg = float(avg_score_list.group(2).split(',')[0])
        self.bagrut_score = str(undivded_bagrot_avg / 10)


    def get_accepted_majors(self):
        accepted_paylod = 'stidno=00000000'
        accepted_paylod += '&psic='
        accepted_paylod += self.psycho_score[0]
        accepted_paylod += '&psicreali='
        accepted_paylod += self.psycho_score[1]
        accepted_paylod += '&psichomani='
        accepted_paylod += self.psycho_score[2]
        accepted_paylod += '&bagrut='
        accepted_paylod += self.bagrut_score
        accepted_paylod += '&heseg=3&mecjer=&toaru=&semlhug1=&faculta=&optheseg=50'  # Notice Heseg tag , it might be calced at server-side, i think it tells if your get discount for good grades
        r = requests.post(HUJI_URL_MAJORS, data=accepted_paylod,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})  # genreate TLV request here
        # print(r.text)
        accepted_list = re.findall(
            r'<tr align="right" bgcolor="FAF3DD">.*?<a.*?>(.*?)<\/a>.*?<td class="text" dir="rtl">(.*?)<\/td>.*?<\/tr>',
            r.text, re.DOTALL)
        accepted_list_profs = []
        accepted_list_reason = []
        accepted_list_cleaned = []
        for i in accepted_list:
            i_as_str = str(i)
            # print(i_as_str)
            i_as_str = i_as_str.replace("\\n\\t", "")
            # print(i_as_str)
            accepted_list_cleaned.append(i_as_str)
            # i[1]=i[1].replace('\n\t', '')
            the_reason = i[1].replace('\n\t', '')
            # print(the_reason)
            accepted_list_profs.append(i[0])
            accepted_list_reason.append(the_reason)
        # print(accepted_list_cleaned)
        self.accepted = accepted_list_cleaned
        self.accepted_str=str(self.accepted)
        print(self.accepted_str)


    def print_results(self):
        print('Huji Results: ')
        print('The bagrut score for Huji is: ' + self.bagrut_score)
        print('The accepted majors for Huji is: '+ self.accepted_str)
#
#     def generate_result(self):
#         return Result.Result(self.bagrut_score, None , None)  # third arg is list of accepted profs
# #
# a = Profs.Prof('אזרחות',5,90)
# b = Profs.Prof('אנגלית', 5, 80)
# c = Profs.Prof('הבעה עברית', 5, 80)
# d = Profs.Prof('הסטוריה', 5, 80)
# e = Profs.Prof('מתמטיקה', 5, 80)
# f = Profs.Prof('ספרות', 5, 80)
# g = Profs.Prof('תנ"ך', 5, 80)
# listp = [a,b,c,d,e,f,g]
# huji = Huji_Request(listp, ('660', '630', '600', '150'))
# print(huji.generate_result())