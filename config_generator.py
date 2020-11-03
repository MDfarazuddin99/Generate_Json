import json
import datetime
import shortuuid
import pandas as pd
import copy 
import pprint
import re 

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
                "validFo444r": {
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

def make_service_objects(service_object,n=0):
    service_objects_list = list()
    for i in range(n):
        temp = copy.deepcopy(service_object)
        temp['tmpId'] = str(shortuuid.uuid())
        service_objects_list.append(temp)
    return service_objects_list


def make_cfss_objects(cfss_object,service_object_list,po_df):
    cfss_object_list = list()
    for so in service_object_list:
        temp_cfss_object = copy.deepcopy(cfss_object)
        temp_cfss_object["tmpId"] = so["tmpId"]
        cfss_object_list.append(temp_cfss_object)
    for so,cfssid in zip(cfss_object_list,re.findall("'([^']*)'",po_df['cfssId'][0])):
        so['serviceSpecification']['serviceSpecificationId'] = cfssid
        so['rfServices'].append({"tmpId":str(shortuuid.uuid())}) 
    return cfss_object_list

def make_rfss_objects(rfss_object,cfss_object_list,po_df):
    rfss_object_list = list()
    for so in cfss_object_list:
        temp_rfss_object = copy.deepcopy(rfss_object)
        temp_rfss_object["tmpId"] = so["rfServices"][0]['tmpId']
        rfss_object_list.append(temp_rfss_object)
    for so,rfssid in zip(rfss_object_list,re.findall("'([^']*)'",po_df['rfssId'][0])):
        so['serviceSpecification']['serviceSpecificationId'] = rfssid
    return rfss_object_list


def make_product_object(product_object,po_df):
    temp_product_object = copy.deepcopy(product_object) 
    temp_product_object['productOffering']['productOfferingId'] = po_df['POId'][0]
    temp_product_object['name'] = po_df['POName'][0]
    po_price_objects_list = make_po_price_objects(product_price_object,po_df)
    temp_product_object['productPrices'] = po_price_objects_list
    po_ref_object_list = make_po_ref_objects(product_policy_ref_object,po_df)
    temp_product_object['productPolicyRefs'] = po_ref_object_list
    service_object_list = make_service_objects(service_object,len(re.findall("'([^']*)'",po_df['cfssId'][0])))
    temp_product_object['services'] = service_object_list
    return temp_product_object


start_date = "2020-01-01T00:00:00.000Z" 
po_df = pd.read_csv('p_basic.csv')

po = make_product_object(product_object,po_df)
cfss_object_list = make_cfss_objects(cfss_object,po['services'],po_df)
rfss_object_list = make_rfss_objects(rfss_object,cfss_object_list,po_df)


po_df_ = pd.read_csv('po_data.csv')

po_ = make_product_object(product_object,po_df_)
cfss_object_list_ = make_cfss_objects(cfss_object,po_['services'],po_df_)
rfss_object_list_ = make_rfss_objects(rfss_object,cfss_object_list_,po_df_)


with open('base.json','r') as base_file:
    config_dict = json.load(base_file)
    config_dict['resource']['agreements'][0]['contract']['products'].append(po) 
    config_dict['resource']['agreements'][0]['contract']['products'].append(po_) 
    config_dict['resource']['agreements'][0]['contract']['services'] = cfss_object_list + rfss_object_list + cfss_object_list_ + rfss_object_list_
    str_json = json.dumps(config_dict)
    str_json = str_json.replace('${startDate}',start_date)
    config_dict = json.loads(str_json)
    with open('custom.json','r+') as custom_file:
        json.dump(config_dict,custom_file,indent=6)

print(len(cfss_object_list),len(rfss_object_list),len(cfss_object_list_),len(rfss_object_list_))