import json
a  = ''
with open('temp.json','r') as po:
    a = json.load(po)

print(a)
with open('temp.json','w') as po:
    json.dump(a,po,indent=4)