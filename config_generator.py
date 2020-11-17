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



