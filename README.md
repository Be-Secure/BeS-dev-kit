# besecure-developer-toolkit

The toolkit helps you to quickly generate meta data for BeSLighthouse visualisation. 

It can generate the following data - 
- ossp-master
- version details
- scorecard
- criticality score

## Pre-requisites

1. Python 3.x
2. GitHub personal access token (classic).
3. Set all the variables under [config](acc-config.cfg) file.

## Keep in mind

1. Make sure the format of the version is correct under [Be-Secure/issues](https://github.com/Be-Secure/Be-Secure/issues).
2. Name of the project is case-sensitive. Please provide the name of the project exactly as is given in their repository.
   
    ` Note:- Make sure you give the complete path to the directories`

## Usage
1. Open terminal
2. Using the below command, run [osspoi-meta-data-generator.sh](scripts/osspoi-meta-data-generator.sh) file.
    
    `$ ./osspoi-meta-data-generator.sh`
