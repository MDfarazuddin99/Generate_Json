import requests
import json
import numpy as np
import shortuuid
import pprint

pp = pprint.PrettyPrinter(indent=1)
# Replace Initial and Final Msisdn for Bill Payment 
for i in range(919676553361,919676553362+1):
    msisdn = i
    end_point_1 = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)
    header = {'Accept':'application/json','ERICSSON.Partition-Id':'1'}
    response_1_obj = (requests.get(end_point_1)).json()
    internal_id = response_1_obj['resources'][0]['id']
    end_point_2 = 'http://vmr-inv-0017-trf2.ete.ka.sw.ericsson.se:20080/fin/internalGui/v1/customerFinanceSummary?customerId={}'.format(internal_id)
    response_2_obj = (requests.get(end_point_2)).json()

    amount = (response_2_obj)['resources'][0]['totalOpenAmount']['currencyAmount']['amount']['number']
    print("msisdn: {}\tinternalId: {}\tOverdue : {}".format(i,internal_id,amount))

    payObj_dict = ''
    with open('payment_object.json','r') as payObj_file:
        payObj_dict = json.load(payObj_file)
    # with open('payment_object.json','w') as payObj_file:
    payObj_dict['resource']['id'] = "f504d7fb-8cba-444e-a5e0-712019f80"+ str(np.random.randint(100,1000))
    payObj_dict['resource']['customerTask']['customerId'] = internal_id
    payObj_dict['resource']['customerTask']['initializationTasks'][0]['externalId'] = shortuuid.ShortUUID().random(length=17)
    payObj_dict['resource']['customerTask']['initializationTasks'][0]['initializationTaskItems'][0]['amount']['amount']['number'] = amount#//np.random.randint(2,4)
    # pp.pprint(payObj_dict)
    with open('payment_object.json','w') as payObj_file: 
        json.dump(payObj_dict,payObj_file,indent=3)

    end_point_3 = 'http://vmr-inv-0017-trf2.ete.ka.sw.ericsson.se:20080/fin/business/v1/financialTask/'

    headers = {
        "Accept" : 'application/json;profile="http://ericsson.com/bss.financeBusiness.FinancialTask.executeResponse.2.json#"',
        "Content-Type" : 'application/json;profile="http://ericsson.com/bss.financeBusiness.FinancialTask.executeRequest.2.json#"'
    }
    resp = requests.post(end_point_3,json=payObj_dict,headers=headers)
    print((resp))
    if resp:
        print('sucess')



# 3 requests to be done for Payment Process
##  GET-1   ->  extract 3(openAmount, value, customerId ) arguments 
##  POST-2  ->  substitute above args in post object
##  GET-3   ->  status check request