import json
import datetime
import shortuuid
import pandas as pd
import copy 
import pprint
import re 
import os
import names
import numpy as np
pp = pprint.PrettyPrinter(indent=4)

product_price_object = {
                        "tmpId": "tmp_productPrice1",
                        "validFor": {
                            "start": "${startDate}"
                        },
                        "productOfferingPriceId": "${poproductPriseId}"
                    }


product_policy_ref_object = {
                                "tmpId": "tmp_productPolicyRef1",
                                "poPolicyRefId": "${poPolicyId}",
                                "validFor": {
                                    "start": "${startDate}"
                                }
                        }

service_object = {
            "tmpId": "${cfss_reference_id}"
}

cfss_object = {
        "serviceType": "CF",
                "validFor": {
                    "start": "${startDate}"
                },
                "tmpId": "${cfss_reference_id}",

                "serviceSpecification": {
                    "serviceSpecificationId": "${cfss_id}"
                },
                "statuses": [
                        {
                            "validFor": {
                                "start": "${startDate}"
                            },
                            "status": "ServiceActive"
                        }
                ],
                "rfServices": [
                        
                ]
    }

rfss_object = {

            "serviceType": "RF",

            "resourceReferences": [

                            {

                                            "tmpId": "b9a75f1916de4713af4ed349e75add84"

                            }

            ],

            "validFor": {

                            "start": "${startDate}"

            },

            "tmpId": "${rfss_reference_id}",

            "serviceSpecification": {
                            "serviceSpecificationId": "${rfss_id}"
            },
            
            "statuses": [
                            {
                                "validFor": {
                                                "start": "${startDate}"
                                },
                                "status": "ServiceActive"
                            }
            ]

    }

product_object = {
                        "productOffering": {
                            "productOfferingId": "${po_id}"
                        },

                        "validFor": {
                            "start": "${startDate}"
                        },

                        "name": "${po_name}",

                        "billAccAssignmentRules": [
                                        {

                                                        "tmpId": "tmp_billAccAssignmentRule",

                                                        "validFor": {

                                                                        "start": "${startDate}"

                                                        }

                                        }
                        ],

                        "tmpId": "2afd63ea745a4115bd07c5c5e7abf123",

                        "statuses": [
                                    {

                                                    "validFor": {

                                                                    "start": "${startDate}"

                                                    },

                                                    "status": "ProductActive"

                                    }

                        ],

                        "productPrices": [

                        ],

                        "productPolicyRefs": [

                        ],

                        "services": [

                        ]

                }



def make_po_price_objects(product_price_object,po_df):
    product_price_object_list = list()
    for price in re.findall("'([^']*)'",po_df['ProductPriceId'][0]):
        temp_product_price_object = copy.deepcopy(product_price_object)
        temp_product_price_object['productOfferingPriceId'] = price
        temp_product_price_object['tmpId'] = str(shortuuid.uuid())
        product_price_object_list.append(temp_product_price_object)
    return product_price_object_list

def make_po_ref_objects(product_policy_ref_object,po_df):
    po_ref_object_list = list()
    for ref in re.findall("'([^']*)'",po_df['ProductPolicyRefId'][0]):
        temp_product_policy_ref_object = copy.deepcopy(product_policy_ref_object)
        temp_product_policy_ref_object['tmpId'] = str(shortuuid.uuid())
        temp_product_policy_ref_object['poPolicyRefId'] = ref
        po_ref_object_list.append(temp_product_policy_ref_object)
    return po_ref_object_list

def make_service_objects(service_object,po_df,all_cfss_ids):
    service_objects_list = list()
    for cfss_id in re.findall("'([^']*)'",po_df['cfssId'][0]):
        temp_service_object = copy.deepcopy(service_object)
        temp_service_object['tmpId'] = all_cfss_ids[cfss_id]
        service_objects_list.append(temp_service_object)
    return service_objects_list

def make_cfss_objects(cfss_object,all_cfss_ids,all_rfss_ids,all_cfss_rfss_ids):
    cfss_object_list = list()
    for cfssid,tmpid in all_cfss_ids.items():
        temp_cfss_object = copy.deepcopy(cfss_object)
        temp_cfss_object['serviceSpecification']['serviceSpecificationId'] = cfssid
        temp_cfss_object['tmpId'] = tmpid 
        cfss_object_list.append(temp_cfss_object)        
    for so in cfss_object_list:
        cfssid = so['serviceSpecification']['serviceSpecificationId']
        # print(cfssid  ,'--',all_cfss_rfss_ids[cfssid],'--',all_rfss_ids[all_cfss_rfss_ids[cfssid]])
        so['rfServices'].append({"tmpId":all_rfss_ids[all_cfss_rfss_ids[cfssid]]})
    return cfss_object_list

def make_rfss_objects(rfss_object,all_cfss_rfss_ids,all_rfss_ids):
    rfss_object_list = list()
    for rfssid,tmpid in all_rfss_ids.items():
        temp_rfss_object = copy.deepcopy(rfss_object)
        temp_rfss_object['tmpId'] = tmpid
        temp_rfss_object['serviceSpecification']['serviceSpecificationId'] = rfssid
        rfss_object_list.append(temp_rfss_object)
    return rfss_object_list

def make_product_object(product_object,po_df,all_cfss_ids):
    temp_product_object = copy.deepcopy(product_object) 
    temp_product_object['productOffering']['productOfferingId'] = po_df['POId'][0]
    temp_product_object['name'] = po_df['POName'][0]
    po_price_objects_list = make_po_price_objects(product_price_object,po_df)
    temp_product_object['productPrices'] = po_price_objects_list
    po_ref_object_list = make_po_ref_objects(product_policy_ref_object,po_df)
    temp_product_object['productPolicyRefs'] = po_ref_object_list
    service_object_list = make_service_objects(service_object,po_df,all_cfss_ids)
    temp_product_object['services'] = service_object_list
    return temp_product_object

 
if __name__ == "__main__":
    start_date = "2020-01-01T00:00:00.000Z" 
    # input_ = input('Enter Customer Type: ')       
    input_dict = {'C1':['Basic','Data'],'C2':['Basic','Voice','Data'],'C3':['Basic','Data','Data_Roaming'],'C4':['Basic','Voice','Voice_Roaming','Data'],'C5':['Unlimited']}
    menu_dict = {'C1':20,'C2':20,'C3':20,'C4':0,'C5':0}
    msisdn = 919676553302
    customer_count = 1
    for key in menu_dict:
        for i in range(1,menu_dict[key]+1):
            print(key,i,customer_count)
            customer_count += 1
            input_pos = input_dict[key]
            msisdn += 1
            all_po_files_csv = list()
            for po in input_pos:
                # print('P_{}'.format(po))
                all_po_files_csv.append(os.path.join('All_PO','po_' + po.lower() + '.csv'))  

            all_cfss_ids = dict()
            all_rfss_ids = dict()
            all_cfss_rfss_ids = dict()
            for csv_file in all_po_files_csv:
                po_df = pd.read_csv(csv_file)
                cfss_id_list = re.findall("'([^']*)'",po_df['cfssId'][0])
                for cfss_id in cfss_id_list:
                    if cfss_id not in all_cfss_ids.keys():
                        all_cfss_ids[cfss_id] = shortuuid.uuid()
                rfss_id_list = re.findall("'([^']*)'",po_df['rfssId'][0])
                for rfss_id,cfss_id in zip(rfss_id_list,cfss_id_list):
                    if rfss_id not in all_rfss_ids.keys():
                        all_rfss_ids[rfss_id] = shortuuid.uuid()  
                    if rfss_id not in all_cfss_ids.keys():
                        all_cfss_rfss_ids[cfss_id] = rfss_id 

            cfss_object_list = make_cfss_objects(cfss_object,all_cfss_ids,all_rfss_ids,all_cfss_rfss_ids)
            rfss_object_list = make_rfss_objects(rfss_object,all_cfss_rfss_ids,all_rfss_ids)

            # print('all_cfss_ids')
            # pp.pprint(all_cfss_ids)
            # print('all_rfss_ids')
            # pp.pprint(all_rfss_ids)
            # print('all_cfss_rfss_ids')
            # pp.pprint(all_cfss_rfss_ids)

            with open('base.json','r') as base_file:
                config_dict = json.load(base_file)
                for csv_file in all_po_files_csv:
                    # print(csv_file)        
                    po_df = pd.read_csv(csv_file)
                    po = make_product_object(product_object,po_df,all_cfss_ids)
                    config_dict['resource']['agreements'][0]['contract']['products'].append(po)
                names_dict = pd.read_csv('names.csv')
                print(names_dict.loc[customer_count]['first_name'],customer_count)
                config_dict['resource']['agreements'][0]['contract']['services'] = cfss_object_list + rfss_object_list 
                config_dict['resource']['billingAccounts'][0]['customerBillSpecifications'][0]['billSpec']['billSpecId'] = 'd8dc0644-5d07-4ae4-9ae6-8acdc8c4fa3c'
                config_dict['resource']['billingAccounts'][0]['customerBillSpecifications'][0]['customerDocSpecs'][0]['docSpecId'] = '0db86207-0ef7-42d7-9c9e-5116b4e3697e'
                config_dict['resource']['billingAccounts'][0]['customerBillSpecifications'][0]['customerDocSpecs'][0]['customerDocFormatSpecs'][0]['docFormatSpecId'] = 'b5bf739e-e63b-4296-87a7-e8eeb068f2d1'
                config_dict['resource']['billingAccounts'][0]['customerBillSpecifications'][0]['customerBillingCycleSpecifications'][0]['billingCycleSpec']['billingCycleSpecId'] = '55acd7c0-01eb-42fe-896c-8603e74a5e35'
                config_dict['resource']['billingAccounts'][0]['characteristicValues'][0]['characteristic']['characteristicId'] = 'c9364181776f84540aa8d73b0561229d' 
                config_dict['resource']['billingAccounts'][0]['characteristicValues'][0]['values'][0]['value'] = 'Teacher'
                config_dict['resource']['billingAccounts'][0]['characteristicValues'][1]['characteristic']['characteristicId'] = 'ba7443fb5574a491b964ed57e2e62fc3'
                config_dict['resource']['billingAccounts'][0]['characteristicValues'][1]['values'][0]['value'] = 'HAR'
                config_dict['resource']['billingAccounts'][0]['buckets'][0]['bucketSpec']['bucketSpecId'] = '38181097-e4ea-4ddd-901d-2f8d0795059b'
                config_dict['resource']['relatedParty']['partyNames'][0]['givenNames'] = names_dict.loc[customer_count]['first_name']
                config_dict['resource']['relatedParty']['partyNames'][0]['familyNames'] = names_dict.loc[customer_count]['last_name']
                config_dict['resource']['billingAccounts'][0]['billingAccountSpec']['billingAccountSpecId'] = 'ad9d5dcf-8470-4e03-981b-f9f568d730bd'
                str_json = json.dumps(config_dict)
                str_json = str_json.replace('${msisdn}',str(msisdn))
                str_json = str_json.replace('${startDate}',start_date)
                config_dict = json.loads(str_json)
                with open('All_Customers/{}/custom_{}_{}_{}.json'.format(key,key,i,customer_count),'w+') as custom_file:
                    json.dump(config_dict,custom_file,indent=6)


