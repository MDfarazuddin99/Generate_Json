import os
import shortuuid
import random as rd
import pprint
import xml.etree.ElementTree as ET




def change_initial_final_xml(date):
    '''
        function to change initial.xml and final.xml
    '''
    base_path = '/root/INV/3.7.7/traffic/data/gy/1mscc/'
    initial_xml_tree,final_xml_tree = ET.parse(os.path.join(base_path,'initial.xml')),ET.parse(os.path.join(base_path,'final.xml'))    
    initial_xml_root,final_xml_root = initial_xml_tree.getroot(),final_xml_tree.getroot()
    element_initial1,element_final = initial_xml_root.find('AVP[@code="55"]'),final_xml_root.find('AVP[@code="55"]')
    # print(element_initial1.attrib,element_final.attrib)
    year = date['year']
    month = date['month']
    day = date['day']
    hour = date['hour']
    minute = date['minute']
    second = date['second']
    element_initial1.set('value','CEST: {}-{}-{} {}:{}:{}'.format(year,month,day,hour,minute,second))
    element_initial2 = initial_xml_root.find('AVP[@code="263"]')
    element_initial2.set('value',"${0}.set(${1}-vari1_{2}-${3})".format('{Local.session}','{Global.sessionID}',shortuuid.uuid(),'{Global.step}'))
    element_final.set('value','CEST: {}-{}-{} {}:{}:{}'.format(year,month,day,hour,minute,second))
    initial_xml_tree.write(os.path.join(base_path,'initial.xml'),encoding='UTF-8',xml_declaration=True)
    final_xml_tree.write(os.path.join(base_path,'final.xml'),encoding='UTF-8',xml_declaration=True) 
# /root/INV/3.7.7/traffic/data/gy/1mscc/


def change_gy_xml(msisdn):
    '''
        function to change GyData1msccInitTerm.xml
    '''
    base_path = '/root/INV/3.7.7/traffic/data/gy/'
    gydata_xml_tree = ET.parse(os.path.join(base_path,'GyData1msccInitTerm.xml'))
    gydata_xml_root = gydata_xml_tree.getroot()
    element_gydata1,element_gydata2 = gydata_xml_root.find('Repository/Global/Variable[@name="MSISDNstartValue"]'),gydata_xml_root.find('Repository/Global/Variable[@name="MSISDNstopValue"]')
    # print(element_gydata1.attrib,element_gydata2.attrib)
    element_gydata1.set('value',msisdn)
    element_gydata2.set('value',msisdn)
    gydata_xml_tree.write(os.path.join(base_path,'GyData1msccInitTerm.xml'))
# /root/INV/3.7.7/traffic/data/gy/

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    msisdn = str(8455953410)
    date = {'year':'2020','month':'01','day':'01','hour':'08','minute':'01','second':'01'}
    # hour = input('Enter hour: ')
    # minute = input('Enter minute: ')
    change_gy_xml(msisdn)
    change_initial_final_xml(date)
    pp.pprint(date)
    # os.system("./ffs.sh")
    #   config dict for msisdn ranges.    
    numberOfEvents = rd.randint(50,100)

    for i in range(1,31):
        lessthan10 = lambda a : str(a) if (a >= 10) else '0' + str(a)
        date['day'] = lessthan10(i)
        perDay =  lambda x : x//30
        eventsPerDay = perDay(numberOfEvents)
        remainingEvents = numberOfEvents - eventsPerDay * 30
        print("TotalNumberOfEvents = {}, Day = {}".format(numberOfEvents,i))
        for j in range(1,eventsPerDay+1):
            date['minute'] = lessthan10(j)            
            # pp.pprint(date)
            print('{}-{}-{} {}:{}:{}'.format(date['year'],date['month'],date['day'],date['hour'],date['minute'],date['second']))
            change_initial_final_xml(date)
            # os.system('./ffs.sh')

        if i <= remainingEvents:    
            date['day'] = lessthan10(i)
            date['minute'] = lessthan10(eventsPerDay+1)
            print('->{}-{}-{} {}:{}:{}'.format(date['year'],date['month'],date['day'],date['hour'],date['minute'],date['second']))
            change_initial_final_xml(date)
            # os.system('./ffs.sh')