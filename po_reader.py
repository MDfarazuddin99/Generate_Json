
import json
import pprint
import pandas as pd


po_dict = dict()
a = input('Enter PO Name: ')
folder_name = 'P_'+a+'/P_'+a
with open('{}_POJSON.json'.format(folder_name),'r') as po_file:
    po_data = json.load(po_file)
    po_dict['POId'] = po_data['id']
    po_dict['POName'] = po_data['name']
    po_dict['ProductPriceId'],temp_po_prices = list(),list()
    po_dict['ProductPolicyRefId'],temp_po_refs = list(),list()
    for p_ref in po_data['versions'][0]['poPolicyRefs']:
        if 'priceId' not in p_ref.keys():
            temp_po_prices.append(p_ref['productOfferingPriceRelations'][0]['targetEntityPath'][0]['entityId'])
            temp_po_refs.append(p_ref['id'])
    po_dict['ProductPolicyRefId'].append(temp_po_refs)
    po_dict['ProductPriceId'].append(temp_po_prices)

with open('{}_PSJSON.json'.format(folder_name),'r',encoding="utf8") as po_file:
    po_data = json.load(po_file)
    po_dict['cfssId'],temp_cfss = list(),list()
    for po_cfss in po_data['versions'][0]['relationsTo']:
        temp_cfss.append(po_cfss['targetId'])
    po_dict['cfssId'].append(temp_cfss)

    with open('{}_ALLCFSSJSON.json'.format(folder_name),'r',encoding="utf8") as po_file:
        po_data = json.load(po_file)
        po_dict['rfssId'],temp_rfss = list(),list()
        for po_cfss in po_dict['cfssId'][0]:
            for po_rfss in po_data['services']:
                if po_cfss == po_rfss['id']:
                    temp_rfss.append(po_rfss['versions'][0]['relationsTo'][0]['targetId'])
        po_dict['rfssId'].append(temp_rfss)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(po_dict) 
po_df = pd.DataFrame(po_dict)
csv_file = a.lower()
po_df.to_csv('All_PO/po_{}.csv'.format(csv_file),index=False) 