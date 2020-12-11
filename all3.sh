#!/bin/bash
EventStartDate="Jan 01 2020"
NumberOfDays=378
firstmsisdn=8455953469
lastmsisdn=8455953469
SlotTime=1
StepSize=1200

export EventStartDate
export NumberOfDays
export firstmsisdn
export lastmsisdn
export SlotTime
export StepSize

#sh -x cssms3.sh
sh -x csvoice3.sh
#sh -x pssms3.sh
    
