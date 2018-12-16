from django.shortcuts import render
from .Run_Requests import *
from .Profs import *


# Create your views here.
def parse_modle_1_request(user_input:dict):
    proof_list = []
    for key in user_input:
        print(user_input[key])
        proof_list.append(Prof(key, user_input[key][0], user_input[key][1]))
    return proof_list

keyslist=[]
valueslist=[]
profslist=[]


def get_scores(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
            #print('request is POST')
            #print(type(request.POST)) 
            #print(type(request.POST.lists()))
            #print(request.POST.lists())
            #print(parse_modle_1_request(request.POST.dict()) 
            for key, value in request.POST.lists():
                print(key)
                print(value)
                
                if key == 'psyhco':
                    #continue
                    psycho = (value[0], value[1], value[2], value[3])
                
                else:
                    keyslist.append(key)
                    valueslist.append(value)
                
            #print(keyslist)
            #print(valueslist)
            for i in valueslist:
                i.insert(0, keyslist[valueslist.index(i)])
            #print(valueslist)
            for i in valueslist:
                print(i)
                this_prof=Prof(i[0],i[1],i[2])
                profslist.append(this_prof)
            print(profslist)
            print(psycho)
            all_results=main(profslist,psycho)
            
            
            return render(request, 'module_3.html', {
'Tech_avg_bagrut_score': all_results[0].bagrot_score,
'Tech_optimal_bagrut_score':all_results[0].optimal_bagrot_regex,
'Tech_sechem_score':all_results[0].sechem_score,
'Tech_accepted_majors':all_results[0].accepted_majors,
'huji_avg_bagrut_score':all_results[1].bagrut_score,
'huji_accepted_majors':all_results[1].accepted_str,
'TLV_average_bagrut_score':all_results[2].bagrut_score,
'TLV_sechem_score':all_results[2].sechem,
'TLV_accepted_majors':all_results[2].accepted_str,
'BGU_bagrut_score':all_results[3].bagrot_score,
'BGU_scheme_score':all_results[3].scheme_score,
#'':,
})