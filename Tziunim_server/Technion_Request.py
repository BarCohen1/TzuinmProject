import requests
import re
from .Profs import *
from .Result import *

BAGROUT_URL = 'https://admissions.technion.ac.il/wp-content/plugins/technion-calculators/technion-calculators-sum.php'

#TODO 1. fill up the Bagrot_HASH table with all profs 2. add handasa and camoti sechem options 3. get all accepted majors list
class Technion_Request:
    profs_HASH = {'אזרחות': 'ezrahut', 'אנגלית': 'english', 'הבעה עברית': 'habaa', 'הסטוריה': 'history', 'מתמטיקה': 'mathematic',
                'ספרות': 'hebrew_lit', 'תנ"ך': 'bible', 'כימיה': '' , 'ביוטכנולוגיה' : ''}
    units_HASH = {'אזרחות': 'yEzrahut', 'אנגלית': 'yEnglish', 'הבעה עברית': 'yHabaa', 'הסטוריה': 'yHistory', 'מתמטיקה': 'yMathematic',
                'ספרות': 'yHebrew_lit', 'תנ"ך': 'yBible', 'כימיה': '' , 'ביוטכנולוגיה' : ''}
    sifi_cabla = {'אדריכלות נוף': '80', 'ארכיטקטורה': '80', 'ביוכימיה מולקולרית': '83',
                  'ביולוגיה (עדיפות שנייה 90)': '83',
                  'הנדסת אווירונוטיקה וחלל': '84', 'הנדסה אזרחית': '85', 'הנדסת ביוטכנולוגיה ומזון': '84',
                  'הנדסה ביוכימית': '84',
                  'הנדסה ביו-רפואית': '87', 'הנדסה ביו-רפואית ופיזיקה': '88', 'הנדסת הסביבה': '83',
                  'הנדסת חומרים': '85',
                  'הנדסת חומרים וביולוגיה': '86', 'הנדסת חומרים וכימיה': '86', 'הנדסת חומרים ופיזיקה': '86',
                  'הנדסת חשמל*': '88.3',
                  'הנדסת חשמל ופיזיקה': '91', 'הנדסה כימית': '83', 'הנדסת מיפוי וגיאו-אינפורמציה': '83',
                  'הנדסת מכונות': '85',
                  'הנדסת מערכות מידע*': '89', 'הנדסת נתונים ומידע': '88.5', 'הנדסת תעשייה וניהול*': '83.5',
                  'חינוך למדע וטכנולוגיה*': '83',
                  'כימיה': '83', 'מדעי המחשב*': '89', 'מדעי המחשב ומתמטיקה*': '90', 'מדעי המחשב ופיזיקה': '90',
                  'מתמטיקה*': '84',
                  'מתמטיקה עם מדעי המחשב*': '84', 'מתמטיקה עם סטטיסטיקה*': '84', 'מתמטיקה-פיזיקה*': '86',
                  'פיזיקה': '84', 'רפואה': '93-94',
                  'הנדסה ביו-רפואית ורפואה ': '94-93'}

    # generate the requests and saves the results into the data variables
    # psycho - entered as a 4-way tuple ( 0 - overall_Score, 1 - math , 2 - hebrew , 3- english)
    # profs_list - entered as a list of Pros's with prof's name, units and grade for each prof
    def __init__(self, profs_list, psycho):
        self.Profs = profs_list
        self.psycho_score = psycho # entered pyscho score , 0 - overall_Score, 1 - math , 2 - hebrew , 3- english
        self.get_bagrut_avg()  # avg bagrut score
        # self.get_overall_score()
        self.get_accepted_majors()
        # self.print_results()

    # in charge of turning Prof values into fitting Huji form data request
        # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it

    def get_bagrut_avg(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(BAGROUT_URL , data=self.parse_subjects() , headers= header)
        bagrot_regex = re.search(r"(ממוצע ציוני הבגרות ללא בונוסים: (\d+\.\d+|\d+))", r.text)
        print(bagrot_regex)
        regex_ = bagrot_regex.group(2)
        print(regex_)
        self.bagrot_score = str(regex_)
        optimal_bagrot_regex = re.search(r"(ממוצע בגרות מיטבי: (\d+\.\d+|\d+))", r.text)
        self.optimal_bagrot_regex = str(optimal_bagrot_regex.group(2))
        sechem_regex =  re.search(r"(הסכם לדיוני הקבלה הוא:(\d+\.\d+|\d+))", r.text)
        self.sechem_score = str(sechem_regex.group(2))

    def parse_subjects(self):
        #TODO id of matkzoot beheria (profs you choose) are in HEBREW , we must find them all and decode them before adding them to payload
        payload = ''
        payload += 'bagrot=true&'
        for prof in self.Profs:
            print(prof)
            print(prof.name)
            payload += self.find_subject_unit_id(prof.name) + '=' + prof.units + '&'
            payload += self.find_subject_grade_id(prof.name) + '=' + prof.grade + '&'
        pscho_score_str=str(self.psycho_score[0])
        print(type(pscho_score_str))
        payload += 'psychometry=' + pscho_score_str + '&'
        payload += '&memuca=sehem'
        # print(payload)
        return payload

    def get_accepted_majors(self):
        accepted = []
        for major in self.sifi_cabla.keys():
            if self.sifi_cabla[major] <= self.sechem_score:
                accepted.append(major)
        self.accepted_majors = accepted

    def find_subject_grade_id(self, subject_name):
        return self.profs_HASH[subject_name]

    def find_subject_unit_id(self, subject_name):
        return self.units_HASH[subject_name]

    # def generate_result(self):
    #     return Result.Result(self.bagrut_score, self.sechem, str(self.accepted)) #third arg is list of accepted profs

    def print_results(self):
        print('Technion Results: ')
        print('The bagrut score without bonuses is: ' +self.bagrot_score)
        print('The optimal bagrut score with bonuses is: ' + self.optimal_bagrot_regex)
        print('The sechem score is: ' + self.sechem_score)
        print('The accpeted majors in Technion are:' + str(self.accepted_majors))


# a = Profs.Prof('אזרחות',5,90)
# b = Profs.Prof('אנגלית', 5, 80)
# c = Profs.Prof('הבעה עברית', 5, 80)
# d = Profs.Prof('הסטוריה', 5, 80)
# e = Profs.Prof('מתמטיקה', 5, 80)
# f = Profs.Prof('ספרות', 5, 80)
# g = Profs.Prof('תנ"ך', 5, 94)
# listp = [a,b,c,d,e,f,g]
# a = Technion_Request(listp, ('660', '630', '600', '150'))