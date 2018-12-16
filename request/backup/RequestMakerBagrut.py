import urllib
import requests
import re
import Profs
TLV_URL = "http://www.ims.tau.ac.il/md/ut/Bagrut_T.aspx"
HUJI_URL = 'http://bagrut-calculator.huji.ac.il/api/bargrutCalculator/GetBagrutCalc/'
BAR_ILAN_URL = 'https://dory.os.biu.ac.il/EnrollmentChances/pages/CalcBagrutResultsAction.do'
URL_TECHNION = 'https://admissions.technion.ac.il/wp-content/plugins/technion-calculators/technion-calculators-sum.php'
URL_BEER_SHEVA = 'https://bgu4u.bgu.ac.il/pls/rgwp/!rg.CalcBagrutResults'
URL_ARIEL ='http://www.ariel.ac.il/projects/Tzmm/Mark/CalcMark.asp'
TLV_SECHEM_URL='http://www.ims.tau.ac.il/md/ut/Tziunim.aspx'
sechem_tlv='__VIEWSTATE=%2FwEPDwULLTEwOTIyNjIwNjQPFg4eB21lY2hpbmFkHgVzaGFuYWUeBWFfaGF0Zh4Fa19oYXRmHgVhX2JhZ2YeBWtfYmFnZh4FdF9iYWdmFgICCQ9kFgICAQ8WAh4EVGV4dAV2Jm5ic3A7Jm5ic3A716DXkCDXnNeR15fXldeoINeQ16og16HXldeSINeU16bXmdeV158g15TXnteR15XXp9epLCDXldec15TXlteZ158g15DXqiDXoNeq15XXoNeZINeU15fXmdep15XXkSZuYnNwOyZuYnNwO2QYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgYFBnJkU3VnMQUGcmRTdWcxBQZyZFN1ZzIFBnJkU3VnMgUGcmRTdWczBQZyZFN1ZzPlDcGQ3FBF1a1IAUuSOuVDIL4GiILj3He9NhWHcdmHXg%3D%3D&__VIEWSTATEGENERATOR=A8657CD6&__EVENTVALIDATION=%2FwEdAAjTXnnCX0PYjgrV2%2BRyFrC4UcvNScKIMFGMoyyyWalOCPowOZKnFntRi6dZY8u7LnAAkVInIdXr7THKVORwc9NBdI0nddCh%2FXXQn6%2FowDm6Zr9J%2Fm18W80U3ZlPMYxXm%2FeAl4n0PtIC8mpwwElKA7V4zUBpfBxkIWhFcfWFBDt26kl82nSDk4yokl133CYz2m2WKKvhTPwz6mlLICRk4D6Q&sug=1&txtHatama=&txtBagrut=111&txtPsicho=666&btncalc.x=18&btncalc.y=3&mechina='
TLV_SIKUIM_URL='http://www.ims.tau.ac.il/md/ut/Sikuim_T.aspx'


# In charge of sending making the request given a dict of values of them from 'subject': 'numOfBagrutunits' , 'grade'
class RequestMakerBagrut:
    TLV_HASH = {'אזרחות': '063', 'אנגלית': '010', 'הבעה עברית': '05', 'היסטוריה/תע"י': '020', 'מתמטיקה': '014',
                'ספרות': '04', 'תנ"ך': '01', 'מחשבת ישראל': '021', 'ערביתמ': '094', 'אלקטרוניקה': '050', 'אמנות': '027',
                'ביולוגיה': '017', 'גיאוגרפיה': '041', 'חקלאות': '019', 'חשמל': '055', 'כימיה': '016',
                'מדעי החברה': '022', 'מדעי המחשב': '042', 'מוסיקה': '028', 'מכשור ובקרה': '053', 'מכניקה הנדסית': '054',
                'ערבית': '012', 'פיזיקה': '015', 'פסיכולוגיה': '073', 'צרפתית': '011', 'שפה זרה אחרת': '013',
                'תורה שבע"פ': '03', 'תלמוד': '02', 'אחר עם בונוס': '096', 'אחר עם בונוס': '097', 'אחר עם בונוס': '00',
                'אחר ללא בונוס': '080', 'אחר ללא בונוס': '098'}

    # generate the requests and saves the results into the data variables
    # psycho - entered as a 4-way tuple ( 0 - overall_Score, 1 - math , 2 - hebrew , 3- english)
    # profs_list - entered as a list of Pros's with prof's name, units and grade for each prof
    def __init__(self, profs_list, psycho):
        self.Profs = profs_list
        self.bagrut_score = ''
        self.psycho_score = psycho
        self.get_bagrut_avg()
        self.get_overall_tlv_score()


    # in charge of turning Prof values into fitting tlv form data request
    def tlv_parse_subjects(self):
        tlv_dict = {}
        for val in self.Profs:
            id = self.find_subject_id(val.name)
            tlv_dict['tziun' + id] = val.grade
            tlv_dict['yl' + id] = val.units
        return tlv_dict

    # generate the over all sechem score.
    # This is done by using a get request (to get session validation), generates fitting payload, sending a Post
    # Requst with payload and finding via regex the over_all score
    def get_overall_tlv_score(self):
        get = requests.get(TLV_SECHEM_URL)
        TLV_REGEX = re.findall(r'(id="__.*" value="(.*)")', get.text)
        enc_8_regex = '__VIEWSTATE='
        enc_8_regex += urllib.parse.quote(TLV_REGEX[0][1], safe='')
        enc_8_regex += '&__VIEWSTATEGENERATOR='
        enc_8_regex += urllib.parse.quote(TLV_REGEX[1][1], safe='')
        enc_8_regex += '&__EVENTVALIDATION='
        enc_8_regex += urllib.parse.quote(TLV_REGEX[2][1], safe='')
        enc_8_regex += '&sug=1&txtHatama=&txtBagrut='+self.bagrut_score+'&txtPsicho='+self.psycho_score+'&btncalc.x=14&btncalc.y=16&mechina='
        r = requests.post(TLV_SECHEM_URL, data=enc_8_regex,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def get_bagrut_avg(self):
        r = requests.post(TLV_URL, data=self.tlv_parse_subjects())  # genreate TLV request here
        avg_score = re.search(r'(<b>&nbsp;(.*?)&nbsp;</b>.*?</table>)', r.text)
        avg_score = avg_score[2]
        print(avg_score)
        self.bagrut_score = avg_score

    def get_accepted_majors(self):
        accepted_paylod = 'txtBagrut='
        accepted_paylod += self.bagrut_score
        accepted_paylod += '&txtPsicho='
        accepted_paylod += self.psycho_score
        accepted_paylod += '&allfacs=1&facs=11&facs=06&facs=01&facs=12&facs=07&facs=03&facs=14&facs=08&facs=04&facs=15&facs=10&facs=05&facs=18&facs=09&Enter.x=31&Enter.y=8'
        print(accepted_paylod)
        r = requests.post(TLV_SIKUIM_URL, data=accepted_paylod,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})  # genreate TLV request here
        print(r.text)

    # send a Post request to Huji with huji payload, finds avg_bagrut ret with regex and saves it
    def get_bagrut_avg(self):
        r = requests.post(TLV_URL, data =self.tlv_parse_subjects()) # genreate TLV request here
        self.bagrut_score = str(re.search(r'(<b>&nbsp;(.*?)&nbsp;</b>.*?</table>)', r.text))

    #Prof's name is entered as the key for the TLV_HASH tables that hold that Prof's unique id
    def find_subject_id(self, subject_name):
        return self.TLV_HASH[subject_name]


a = Profs.Prof('אזרחות',5,90)
c = Profs.Prof('אנגלית', 5, 80)
b = [c,a]
request = RequestMakerBagrut(b, '666')
print(request.bagrut_score)

