# bic2200-can-control
Tool for controlling Mean Well BIC-2200-CAN  Bidirectional Power Supply Series

Tested only with the 24V Version BIC-2200-CAN-24
Please note:  this software to control the BIC-2200 is not yet complete and also not fully tested. The BIC-2200 should not be operated unattended. There is no error handling yet !!!

What is missing:
- status queries
- error handling
- variables plausibility check
- programming missing functions

       Usage: ./bic22.py parameter value
       
       on                   -- output on
       off                  -- output off

       cvread               -- read charge voltage setting
       cvset <value>        -- set charge voltage
       ccread               -- read charge current setting
       ccset <value>        -- set charge current

       dvread               -- read discharge voltage setting
       dvset <value>        -- set discharge voltage
       dcread               -- read discharge current setting
       dcset <value>        -- set discharge current

       vread                -- read DC voltage
       cread                -- read DC current
       acvread              -- read AC voltage

       charge               -- set direction charge battery
       discharge            -- set direction discharge battery

       tempread             -- read power supply temperature
       can_up               -- start can bus
       can_down             -- shut can bus down

       <value> = amps oder volts * 100 --> 25,66V = 2566 
        
# charge_control.py        
Tool to control battery charging and discharging depending on the electricity meter. 

Do not use without adaptation to local conditions and only under supervision! 
