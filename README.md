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
4. Make sure the format of the version is correct under [BeSLighthouse/issues](https://github.com/Be-Secure/BeSLighthouse/issues).
5. Please provide the name of the project exactly as is given in their repository.
   
    ` Note:- Make sure you give the complete path to the directories`

## Usage
1. Open terminal
2. Using the below command, run [main.sh](scripts/main.sh) file.
    
    `$ ./main.sh`
