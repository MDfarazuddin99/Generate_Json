import requests
import json
import os

def make_post_request(json_file):
    end_point = 'http://vmr-inv-0006.ete.ka.sw.ericsson.se:13080/cpm/business/v1/createCustomerOnboarding/customer/'
    with open(json_file,'r') as json_file:
        data = json.load(json_file)
        resp = requests.post(end_point,json=data)
        print((resp))
        if resp:
            print('sucess')

if __name__ == "__main__":
    base_path = 'All_Customers'
    print(os.listdir(base_path))
    for folder in os.listdir(base_path):
        print(folder)
        folder_path = os.path.join(base_path,folder)
        for file_ in os.listdir(folder_path):
            print(file_)
            make_post_request(os.path.join(folder_path,file_))

    




