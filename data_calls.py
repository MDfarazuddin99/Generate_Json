import shortuuid
import random as rd
import pprint
import xml.etree.ElementTree as ET




def change_initial_final_xml(date):
    '''
        function to change initial.xml and final.xml
    '''
    initial_xml_tree,final_xml_tree = ET.parse('initial.xml'),ET.parse('final.xml')    
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
    element_final.set('value','CEST: 2020-{}-{} 09:{}:00'.format(month,date,minute))
    initial_xml_tree.write('initial.xml',encoding='UTF-8',xml_declaration=True)
    final_xml_tree.write('final.xml',encoding='UTF-8',xml_declaration=True) 



def change_gy_xml(msisdn):
    '''
        function to change GyData1msccInitTerm.xml
    '''
    gydata_xml_tree = ET.parse('GyDatalmsccInitTerm.xml')
    gydata_xml_root = gydata_xml_tree.getroot()
    element_gydata1,element_gydata2 = gydata_xml_root.find('Repository/Global/Variable[@name="MSISDNstartValue"]'),gydata_xml_root.find('Repository/Global/Variable[@name="MSISDNstopValue"]')
    # print(element_gydata1.attrib,element_gydata2.attrib)
    element_gydata1.set('value',msisdn)
    element_gydata2.set('value',msisdn)
    gydata_xml_tree.write('GyDatalmsccInitTerm.xml')


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
#   config dict for msisdn ranges.    
    msisdn_ranges_dict = {"C1":(8455953410,8455953424),"C2":(8455953425,8455953444),"C3":(8455953445,8455953469)}
#   config dict for data call ranges.
    data_event_ranges_dict = {"C1":(50,100),"C2":(30,90),"C3":(75,150),"C4":(45,90),"C5":(100,150)}

    date = {'year':'2020','month':'01','day':'01','hour':'08','minute':'00','second':'00'}
    numberOfEvents = rd.randint(50,100)
    msisdn = str(8455953410)
    change_gy_xml(msisdn)
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
        if i <= remainingEvents:
            date['day'] = lessthan10(i)
            date['minute'] = lessthan10(eventsPerDay+1)
            print('->{}-{}-{} {}:{}:{}'.format(date['year'],date['month'],date['day'],date['hour'],date['minute'],date['second']))
            change_initial_final_xml(date)


        