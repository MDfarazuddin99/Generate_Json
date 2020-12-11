import requests
import json
import numpy as np
li = []
# for i in range(8455953410,8455953469):
msisdn = '8455953410'
end_point_internal_id = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)
header = {'Accept':'application/json','ERICSSON.Partition-Id':'1'}
response_1_obj = (requests.get(end_point_internal_id)).json()
internal_id = response_1_obj['resources'][0]['id']
end_point_balance_enquiry = 'http://vmr-inv-0008-trf2.ete.ka.sw.ericsson.se:13180/cha/balanceEnquiry/v1/customer/{}/?expand=/:recursive'.format(internal_id)
response_2_obj = (requests.get(end_point_balance_enquiry,headers=header)).json()
remaining_balance = response_2_obj['billingAccounts'][0]['billingAccountBuckets'][0]['value']['number']
    # li.append(int(remaining_balance)/1000000)
print('ExternalId: {}\nInternalId: {}\nRemaining balance: {}'.format(msisdn,internal_id,int(remaining_balance)/1000000))


# print(li)

# lii = [99141.0, 99427.0, 99351.0, 99301.0, 99282.0, 99368.0, 99232.0, 99395.0, 99177.0, 99374.0, 99453.0, 99025.0, 98960.0, 99357.0, 99071.0, 99000.0, 98959.0, 99599.0, 99475.0, 99148.0, 99486.0, 99476.0, 99518.0, 99362.0, 99187.0, 99103.0, 99567.0, 99250.0, 99406.0, 99073.0, 99156.0, 99274.0, 99270.0, 99161.0, 99786.0, 99811.0, 99797.0, 99826.0, 99795.0, 99808.0, 99775.0, 99806.0, 99815.0, 99788.0, 99808.0, 99784.0, 99800.0, 99820.0, 99816.0, 99830.0, 99830.0, 99816.0, 99828.0, 99788.0, 99825.0, 99819.0, 99829.0, 99781.0, 99777.0]
# lii = np.array(lii)
# li = np.array(li)

# print(lii - li)

# print(np.where(np.any(lii != li,axis=0)))