import json
import requests
import pprint
import shortuuid

pp = pprint.PrettyPrinter(indent=3)
for msisdn in range(917989139684,917989139702):

    endpoint_1 = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)

    end_point_internal_id = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/readCustomerExtId/extId/customer/{}'.format(msisdn)
    header = {'Accept':'application/json','ERICSSON.Partition-Id':'1'}
    response_1_obj = (requests.get(end_point_internal_id)).json()

    internal_id = response_1_obj['resources'][0]['id']
    print("Internal-Id = ",internal_id)
    billingAccountId = response_1_obj['resources'][0]['billAccAssignmentRules'][0]['accountId']
    print("Billing Account Id = ",billingAccountId)

    endpoint_2 = 'http://vmr-inv-0014-trf2.ete.ka.sw.ericsson.se:13180/inv/offCycleBillManagement/v1/onDemandBillRun'

    on_demand_body = {
        "resource": {
            "customerId":internal_id,
            "billingAccountId":billingAccountId,
            "paymentDueOffset": "3",
            "reason": "AC04"
        }
    } 

    on_demand_header = {
        'Content-Type':'application/json',
        'ERICSSON.Partition-Id':'1',
        'ERICSSON.GlobaL-Unique-Request-Id':shortuuid.ShortUUID().random(length=12)
    }

    pp.pprint(on_demand_header)

    pp.pprint(on_demand_body)
    response_2_obj = requests.post(endpoint_2,json=on_demand_body,headers=on_demand_header)

    print(response_2_obj.status_code)



