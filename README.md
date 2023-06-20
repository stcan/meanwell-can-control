# meanwell-can-control
Tool to control Power Supplys from Mean Well via CAN Bus

Tested with the 24V Version BIC-2200-24-CAN and NPB-abc0 Series Charger

Please note:  this tool is not yet complete and also not fully tested. Do not use without monitoring the devices. There is no error handling yet !!!

What is missing:
- variables plausibility check
- some functions

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
       typeread             -- read power supply type
       statusread           -- read power supply status
       faultread            -- read power supply fault status

       can_up               -- start can bus
       can_down             -- shut can bus down

       <value> = amps oder volts * 100 --> 25,66V = 2566 
        
# example_charge_control.py        
Example code to control battery charging and discharging depending on the electricity meter. 
Do not use without adaptation to local conditions and only under supervision! 

- All scripts are without any warranty. Use at your own risk
