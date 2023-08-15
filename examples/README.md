        
# example_charge_control.py        
Example code to control battery charging and discharging depending on the electricity meter. 

New feature : Control the max and min values for charge/discharge voltages and currents using the file: examples/charge_control.conf

Please rename example_charge_control.py to charge_control.py to get it working with the check_process.sh

Do not use without adaptation to local conditions and under supervision! 

# check_process.sh

Runs everery 2 seconds to check if the charge_control.py script is working.

-- crontab 
*/2 * * * * /home/pi/bin/check_process.sh > /dev/null 2>&1


All scripts are without any warranty. Use at your own risk
