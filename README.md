# meanwell-can-control
Tool to control Meanwell CAN Bidirectional Power Supplys and Charger via CAN Bus

Tested with the Version BIC-2200-CAN-24 and NPB-1200-24 PSU/Charger

Please note:  this tool to control read and write settings to the CAN device 
It is not yet complete and also not fully tested. 
Do not use without monitoring the device. 
There is no error handling yet !!!
Use at your own risk !

What is missing:
- variables plausibility check
	   
	   Use ./ChargeScript for automatic charge / discharge
	   See config paramter inside the script
	   
	   Usage: ./mwcancmd.py parameter value
       To use a standalone cmd to the mw device
	   
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

       <value> = amps oder volts * 100 --> 25,66V = 2566 
        
# example_charge_control.py        
Example code to control battery charging and discharging depending on the electricity meter. 
Do not use without adaptation to local conditions and only under supervision! 

- All scripts are without any warranty. Use at your own risk
