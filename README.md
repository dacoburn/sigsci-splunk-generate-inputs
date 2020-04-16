# Auto Generate Splunk SigSci App Inputs

## Purpose of this script

This script is written to be used on the system where the SigSci Splunk App is running (https://splunkbase.splunk.com/app/3495 ). It will use the credentials provided to it in order to generate the `inputs.conf` automatically with any inputs not already found in the configuration file. 

## How to use

The script should be pretty simple to use and can be automated with a cronjob if desired. It does use the python `requests` library. If you are using the Splunk Python then you will either need to install `requests` for Python2 or use `python3` to execute the script. Splunk's Python3 seems to have the requests librarby installed natively.

**executing the script**

The `settings.json` should be in the same directory as where you are executing the script.

`python3 sync_splunk_inputs.py`


**Settings Options**

| Setting | Default Value | Description |
|---------|---------------|-------------|
| corp | None | This should be the api name for your corp. Same as what you use in the Splunk App |
| api_user | None | This should be your e-mail that is associated with the API Token you will be using |
| api_token | None | This should be the api_token associated with your API User |
| inputs_file | None | This should be the path to you `local/inputs.conf` I.E. `$SPLUNK_HOME/etc/apps/sigsci_TA_for_splunk/local/inputs.conf`
| input_delta | 5 | Delta in minutes to pull data |
|inputs_index | default | What Splunk Index to save events in |
| input_interval | 300 | Value in seconds. Should be the same as Delta, I.e. 300 seconds = 5 minutes. I recommend leaving both at 5 minutes |
| input_disabled | 0 | Whether the input is disabled or enabled |
| requestEnabled | true | Whether to create Request Inputs |
| eventEnabled | true | Whether to create Event Inputs |
| activityEnabled | true | Whether to create the Corp Activity Input |