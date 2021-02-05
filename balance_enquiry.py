import requests
import json
import numpy as np

for i in range(919676553305,919676553305+1):
    msisdn = i
    end_point_internal_id = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)
    header = {'Accept':'application/json','ERICSSON.Partition-Id':'1'}
    response_1_obj = (requests.get(end_point_internal_id)).json()
    internal_id = response_1_obj['resources'][0]['id']
    end_point_balance_enquiry = 'http://vmr-inv-0008-trf2.ete.ka.sw.ericsson.se:13180/cha/balanceEnquiry/v1/customer/{}/?expand=/:recursive'.format(internal_id)
    response_2_obj = (requests.get(end_point_balance_enquiry,headers=header)).json()
    remaining_balance = response_2_obj['billingAccounts'][0]['billingAccountBuckets'][0]['value']['number']
    print('ExternalId: {}\tInternalId: {}\tRemaining balance: {}'.format(msisdn,internal_id,int(remaining_balance)/1000000))


