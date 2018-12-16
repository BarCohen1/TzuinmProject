import requests
import re
import Profs

BAGROUT_URL = 'https://bgu4u.bgu.ac.il/pls/rgwp/!rg.CalcBagrutResults'
SECHEM_URL = 'https://bgu4u.bgu.ac.il/pls/rgwp/!rg.CalcSekemResults'

#TODO 1. fill up the Bagrot_HASH table with all profs 2. add handasa and camoti sechem options 3. get all accepted majors list
class Beer_Sheva_Request:
    bagrut_score = '' # avg bagrut score
    pyscho_score = () # entered pyscho score , 0 - overall_Score, 1 - math , 2 - hebrew , 3- english
    over_all_score = ''
    profs_accepted = []
    # tlv_request = Request # is this the right syntax
    BeerSheva_HASH = {'אזרחות': '46', 'אנגלית': '11', 'הבעה עברית': '84', 'הסטוריה': '27', 'מתמטיקה': '17',
                'ספרות': '14', 'תנ"ך': '15', 'כימיה': '17' , 'ביוטכנולוגיה' : '19'}

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
        # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it

    def get_bagrut_avg(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = 'on_grade11=&on_learning_units11=&subjects11=&subjects11Val=&on_grade12=&on_learning_units12=&subjects12=&subjects12Val=&on_grade13=&on_learning_units13=&subjects13=&subjects13Val=&on_grade14=&on_learning_units14=&subjects14=&subjects14Val=&on_grade15=&on_learning_units15=&subjects15=&subjects15Val=&on_grade16=&on_learning_units16=&subjects16=&subjects16Val=&on_grade17=&on_learning_units17=&subjects17=&subjects17Val=&on_grade18=&on_learning_units18=&subjects18=&subjects18Val=&on_grade19=&on_learning_units19=&subjects19=&subjects19Val=&on_grade20=&on_learning_units20=&subjects20=&subjects20Val=&on_grade1=88&on_learning_units1=5&subjects1=%E0%F0%E2%EC%E9%FA&subjects1Val=11&on_grade2=90&on_learning_units2=5&subjects2=%EE%FA%EE%E8%E9%F7%E4&subjects2Val=17&on_grade3=99&on_learning_units3=4&subjects3=%EB%E9%EE%E9%E4&subjects3Val=19&on_grade4=87&on_learning_units4=5&subjects4=%E1%E9%E5%E8%EB%F0%E5%EC%E5%E2%E9%E4&subjects4Val=169&on_grade5=84&on_learning_units5=4&subjects5=%FA%F0%22%EA&subjects5Val=15&on_grade6=77&on_learning_units6=2&subjects6=&subjects6Val=417&on_grade7=95&on_learning_units7=4&subjects7=%E4%E9%F1%E8%E5%F8%E9%E4&subjects7Val=27&on_grade8=&on_learning_units8=&subjects8=&subjects8Val=&on_grade9=&on_learning_units9=&subjects9=&subjects9Val=&on_grade10=&on_learning_units10=&subjects10=&subjects10Val=&on_optimal_avg=&rc_where_to_go=&on_avg_grade='
        r = requests.post(BAGROUT_URL , data=self.parse_subjects() , headers= header)
        bagrot_regex = re.search(r"(BagrutCalcResultsValues\((.*),(.*)\))", r.text)
        self.bagrot_score = str(bagrot_regex.group(3))
        print('The optimal bagrut score is: ' +self.bagrot_score)

    def parse_subjects(self):
        payload = ''
        counter = 1
        for prof in self.Profs:
            payload += 'on_grade' + str(counter) + '=' + prof.grade + '&'
            payload += 'on_learning_units' + str(counter) + '=' + prof.units + '&'
            payload += 'subjects' + str(counter) + '=' + '&'
            payload += 'subjects' + str(counter) + 'Val' + '=' + self.find_subject_id(prof.name) + '&'
            counter +=1
        payload += 'on_optimal_avg=&rc_where_to_go=&on_avg_grade='
        return payload

    def get_accepted_majors(self):
        pass

    def get_overall_score(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        sechem_payload = 'rn_year=2018&on_final_sekem=&on_mitsraf=&on_psychometry=' + str(self.psycho_score[0]) + '&on_bagrut_average=' + self.bagrot_score + '&on_psychometry_prep=&on_preparatory_average=&on_grade_eng=&on_learning_units_eng=&on_grade_math=&on_learning_units_math=&on_grade_lang=&on_learning_units_lang=&on_third_lang=0&rn_include_mitsraf=0'
        r = requests.post(SECHEM_URL, data=sechem_payload, headers=header)
        sechem_regex = re.search(r"(on_final_sekem.value = (.*);)", r.text)
        self.scheme_score = str(sechem_regex.group(2))

    def print_results(self):
        print('Beer sheva Results: ')
        print('The bagrut score without bonuses is: ' + self.bagrot_score)
        print('The sechem score is: ' + self.scheme_score)


    def find_subject_id(self, subject_name):
        return self.BeerSheva_HASH[subject_name]
    
#
# a = Profs.Prof('אזרחות',5,90)
# b = Profs.Prof('אנגלית', 5, 80)
# c = Profs.Prof('הבעה עברית', 5, 80)
# d = Profs.Prof('הסטוריה', 5, 80)
# e = Profs.Prof('מתמטיקה', 5, 86)
# f = Profs.Prof('ספרות', 5, 80)
# g = Profs.Prof('תנ"ך', 5, 94)
# listp = [a,b,c,d,e,f,g]
# a = Beer_Sheva_Request(listp, ('660', '630', '600', '150'))