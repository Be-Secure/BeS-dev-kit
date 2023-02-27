#!/bin/bash

function __acc_generate_ossp_data {

    local id=$1
    local name=$2
    
    python3 generate-ossp-master-data.py $id $name

}

function __acc_generate_version_data
{
    local id name

    id=$1
    name=$2

    python3 generate-version-data.py $id $name
}

function __acc_get_version_hash
{
    local id=$1
    local name=$2
    local version=$(cat tmp_file)

    git clone -q https://github.com/Be-Secure/$name

    cd $name

    local tag_hash=$(git show-ref --tags | grep -w "$version" | cut -d " " -f 1)
    cd ..
    
    python3 update-version-data.py $id $name $tag_hash
    [[ -d $name ]] && rm -rf $name
    [[ -f tmp_file ]] && rm tmp_file
}

function __acc_set_conf
{
    local param values
	while read -r configs; do
		if echo $configs | grep -q "^#"
			then
				continue
		fi
        param=$(echo $configs | cut -d "=" -f 1)
        values=$(echo $configs | cut -d "=" -f 2)
		export $param=$values
	done < acc-config.cfg
    [[ -f tmp.txt ]] && rm tmp.txt 

}

function __acc_get_scorecard
{
    local id=$1
    local name=$2
    
    python3 get-scorecard-data.py $id $name
}

function __acc_get_criticality_score
{
    local id=$1
    local name=$2
    
    [[ -z $GITHUB_AUTH_TOKEN ]] && echo "
    Run the below command 
    
    $ export GITHUB_AUTH_TOKEN=<your access token>
    
    You can also update the same in acc-config.cfg file.
    " && return 1
    
    criticality_score --repo github.com/Be-Secure/$name --format json >> criticality_score.json

    python3 get-criticality_score-data.py $id $name

    [[ -f criticality_score.json ]] && rm criticality_score.json
}

function __acc_run
{
    __acc_set_conf
    read -p "Enter TAVOSS-TR id:" id
    read -p "Enter project name:" name
    __acc_generate_ossp_data $id $name
    __acc_generate_version_data $id $name
    __acc_get_version_hash $id $name
    __acc_get_scorecard $id $name
    __acc_get_criticality_score $id $name || return 1

}

__acc_run