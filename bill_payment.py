import requests
import json
import numpy as np
import shortuuid
import pprint

pp = pprint.PrettyPrinter(indent=1)

for i in range(919676553305,919676553317):
    msisdn = i
    end_point_1 = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)
    header = {'Accept':'application/json','ERICSSON.Partition-Id':'1'}
    response_1_obj = (requests.get(end_point_1)).json()
    internal_id = response_1_obj['resources'][0]['id']
    end_point_2 = 'http://vmr-inv-0017-trf2.ete.ka.sw.ericsson.se:20080/fin/internalGui/v1/customerFinanceSummary?customerId={}'.format(internal_id)
    response_2_obj = (requests.get(end_point_2)).json()

    amount = (response_2_obj)['resources'][0]['totalOpenAmount']['currencyAmount']['amount']['number']

    value = (response_2_obj)['resources'][0]['openInvoices'][0]['externalId']

    # print(internal_id,amount,value)
    payObj_dict = ''
    with open('payment_object.json','r') as payObj_file:
        payObj_dict = json.load(payObj_file)
        pp.pprint(payObj_dict)
    with open('payment_object.json','w') as payObj_file:
        payObj_dict['resource']['customerTask']['customerId'] = internal_id
        print(payObj_dict['resource']['customerTask']['customerId'])
        payObj_dict['resource']['customerTask']['initializationTasks'][0]['initializationTaskItems'][0]['amount']['amount']['number'] = amount
        print(payObj_dict['resource']['customerTask']['initializationTasks'][0]['initializationTaskItems'][0]['amount']['amount']['number'])
        print(payObj_dict['resource']['customerTask']['initializationTasks'][0]['initializationTaskItems'][0]['declarationOfIntent']['characteristicValueSets'][0]['characteristicValues'][0]['values'][0]['value'])
        payObj_dict['resource']['customerTask']['initializationTasks'][0]['initializationTaskItems'][0]['declarationOfIntent']['characteristicValueSets'][0]['characteristicValues'][0]['values'][0]['value'] = value
        payObj_dict['resource']['id'] = shortuuid.ShortUUID().random(length=36)
        json.dump(payObj_dict,payObj_file,indent=2)
        end_point_3 = 'http://vmr-inv-0017-trf2.ete.ka.sw.ericsson.se:20080/fin/business/v1/financialTask/'
        a = requests.post(end_point_3,data = payObj_dict,headers={"Content-Type ":"application/json"})
        print(a.status_code)
        brk = input('Check\t')


# 3 requests to be done for Payment Process
##  GET-1   ->  extract 3(openAmount, value, customerId ) arguments 
##  POST-2  ->  substitute above args in post object
##  GET-3   ->  status check request