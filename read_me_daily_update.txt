
Configuring the Auto Update Shell Script:


The project directory contains a file called:
     Daily_update_check.sh

This file is a bash script that will be executed with a Cron job every 24 hours.

The script will send a curl request to the designated url, and will listen for a response with a parameter of:
    Update_required = True

If the parameter is found, then the script will move on to initiate a GIT PULL request to update the project directory.

If there is an error, it will error out and log the error. If the parameter is not set to True, then the script will just exit.

—--------------------------------------------
Once you've named your script, don't forget to make it executable using the chmod command:

    chmod +x daily_update_check.sh

After that, you can run the script like this (but you do not need to at this time):

    ./daily_update_check.sh

Afterwards, to make the script run every 24 hours, you can use a cron job. Open the cron tab file using the following command:

    crontab -e
Then, add the following line at the end of the file (replace /path/to/update_script.sh with the actual path to your script):

    0 0 * * * /path/to/update_script.sh >> /path/to/log.txt
This cron job will run the script every day at midnight. The output of the script (including any errors) will be logged to log.txt.
