import os
import random as rd
import pprint

def edit_sh_file(base_code,changes_dict):
    '''
        base_code -> string, without parameters to be changed for sms or voice calls generation.
        changes_dict -> dictionary, contains parameter related for sms or voice calls generation.
    '''
    edited_code = list()
    edited_code.append(base_code.split('\n')[0])
    for key,val in changes_dict.items():
        if key == 'EventStartDate':
            tmp_str = '{}=\"{}\"'.format(key,val)
            edited_code.append(tmp_str)
        else:
            tmp_str ='{}={}'.format(key,val)
            edited_code.append(tmp_str)
    edited_code += base_code.split('\n')[1:]
    edited_code_str = ''
    for line in edited_code:
        edited_code_str = edited_code_str + line + '\n'
    return edited_code_str


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent = 3)
#   Base code in string for all3.sh for generating only sms calls. 
    base_code_sms = '''#!/bin/bash

export EventStartDate
export NumberOfDays
export firstmsisdn
export lastmsisdn
export SlotTime
export StepSize

sh -x cssms3.sh
#sh -x csvoice3.sh
#sh -x pssms3.sh
    '''

#   Base code in string for all3.sh for generating only voice calls. 
    base_code_voice = '''#!/bin/bash

export EventStartDate
export NumberOfDays
export firstmsisdn
export lastmsisdn
export SlotTime
export StepSize

#sh -x cssms3.sh
sh -x csvoice3.sh
#sh -x pssms3.sh
    '''


#   Parameters dictionary for sms or voice. 
    changes_dict = {
        'EventStartDate':'Jan 01 2020',
        'NumberOfDays':2,
        'firstmsisdn':8455953410,
        'lastmsisdn':8455953424,
        'SlotTime':1,
        'StepSize':1200,
    }
#   config dict for msisdn ranges.    
    msisdn_ranges_dict = {"C1":(8455953410,8455953424),"C2":(8455953425,8455953444),"C3":(8455953445,8455953469)}
#   config dict for sms random ranges.
    sms_event_ranges_dict = {"C1":(0,50),"C2":(0,30),"C3":(0,60),"C4":(0,10),"C5":(0,5)}
#   config dict for voice random ranges.
    voice_event_ranges_dict = {"C1":(50,500),"C2":(250,1000),"C3":(100,400),"C4":(400,1200),"C5":(500,1500)}
    
    print('msisdn ranges dict')
    pp.pprint(msisdn_ranges_dict)
    print('sms event ranges dict')
    pp.pprint(sms_event_ranges_dict)
    print('voice event ranges dict')
    pp.pprint(voice_event_ranges_dict)

    for key,val in msisdn_ranges_dict.items():
        # print("Customer type = {}\nCustomer Range = ({} - {})".format(key,val[0],val[1]))
        initial_msisdn = val[0]
        final_msisdn = val[1]

#       sms generation loop         
        for i in range(initial_msisdn,final_msisdn+1):
            # print('Customer type = {}\tCustomer msisdn = {}'.format(key,i))
            pp.pprint(changes_dict)
            changes_dict['firstmsisdn'] = i
            changes_dict['lastmsisdn'] = i
            changes_dict['NumberOfDays'] = rd.randint(sms_event_ranges_dict[key][0],sms_event_ranges_dict[key][1])
            edited_code = edit_sh_file(base_code_sms,changes_dict)
            with open('all3.sh','w') as shell_file:
                shell_file.write(edited_code)
            os.system('./all3.sh')
            with open('all3.sh','r') as shell_file:
                print(shell_file.read())

#       voice-call generation loop         	
        for i in range(initial_msisdn,final_msisdn+1):
            # print('Customer type = {}\tCustomer msisdn = {}'.format(key,i))
            pp.pprint(changes_dict)
            changes_dict['firstmsisdn'] = i
            changes_dict['lastmsisdn'] = i
            changes_dict['NumberOfDays'] = rd.randint(voice_event_ranges_dict[key][0],voice_event_ranges_dict[key][1])
            edited_code = edit_sh_file(base_code_voice,changes_dict)
            with open('all3.sh','w') as shell_file:
                shell_file.write(edited_code)
            # os.system('./all3.sh')
            with open('all3.sh','r') as shell_file:
                print(shell_file.read())

