        
# example_charge_control.py        
Example code to control battery charging and discharging depending on the electricity meter. 

New feature : Control the max and min values for charge/discharge voltages and currents using the file: examples/charge_control.conf

Please rename example_charge_control.py to charge_control.py to get it working with the check_process.sh

Do not use without adaptation to local conditions and under supervision! 

# check_process.sh

cron job is running everery 2 seconds to check if the charge_control.py script is working. If not, the script is restarted and the restart is logged.

*/2 * * * * /home/pi/bin/check_process.sh > /dev/null 2>&1

To stop the charge_control script the crontab entry has to be deactivated and the script has to be stopped.

All scripts are without any warranty. Use at your own risk
