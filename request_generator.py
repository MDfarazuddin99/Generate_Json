import requests
import json

end_point = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/createCustomerOnboarding/customer/'
with open('custom.json','r') as json_file:
    data = json.load(json_file)
    resp = requests.post(end_point,json=data)
    print((resp))
    if resp:
        print('sucess')




