# bic2200-can-control
Tool to control Mean Well BIC-2200-CAN  Bidirectional Power Supplys

Tested with the 24V Version BIC-2200-CAN-24

Please note:  this tool to control the BIC-2200 is not yet complete and also not fully tested. Do not use without monitoring the BIC-2200. There is no error handling yet !!!

What is missing:
- status queries
- error handling
- variables plausibility check
- programming missing functions

       Usage: ./bic2200.py parameter value
       
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
        
# example_charge_control.py        
Example code to control battery charging and discharging depending on the electricity meter. 
Do not use without adaptation to local conditions and only under supervision! 
