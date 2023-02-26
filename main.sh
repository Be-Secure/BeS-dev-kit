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
	while read -r user_configs; do
		if echo $user_configs | grep -q "^#"
			then
				continue
		fi
		echo $user_configs > tmp.txt
		local user_config_param=$(cut -d "=" -f 1 tmp.txt)
		local user_config_values=$(cut -d "=" -f 2 tmp.txt)
		unset $user_config_param
		export $user_config_param=$user_config_values
	done < acc-config.cfg
    [[ -f tmp.txt ]] && rm tmp.txt 

}

function __acc_run
{
    __acc_set_conf
    read -p "Enter TAVOSS-TR id:" id
    read -p "Enter project name:" name
    __acc_generate_ossp_data $id $name
    __acc_generate_version_data $id $name
    __acc_get_version_hash $id $name

}

__acc_run