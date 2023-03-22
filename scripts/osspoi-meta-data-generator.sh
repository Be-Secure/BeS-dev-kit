#!/bin/bash

function __acc_generate_ossp_data {

    local id=$1
    local name=$2
    
    python3 $ACC_ROOT_DIR/python/generate-ossp-master-data.py $id $name
    [[ $? -ne 0 ]] && echo "Could not generate data" && return 1

}

function __acc_generate_version_data
{
    local id name

    id=$1
    name=$2

    python3 $ACC_ROOT_DIR/python/generate-version-data.py $id $name
}

function __acc_get_version_hash
{
    local id=$1
    local name=$2
    local version=$(cat $ACC_ROOT_DIR/tmp_file)

    git clone -q https://github.com/$GITHUB_ORG/$name $ACC_ROOT_DIR/repo/$name

    cd $ACC_ROOT_DIR/repo/$name
    local tag_hash=$(git show-ref --tags | grep -w "$version" | cut -d " " -f 1)
    [[ -z $tag_hash ]] && echo "Could not find version $version under repo $name" && return 1 
    cd $ACC_ROOT_DIR/scripts
    
    python3 $ACC_ROOT_DIR/python/update-version-data.py $id $name $tag_hash
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
        value=$(echo $configs | cut -d "=" -f 2)
        [[ -z $value ]] && echo "Please set the value for $param before running the script" && return 1
		export $param=$value
	done < $HOME/besecure-developer-toolkit/acc-config.cfg
}

function __acc_check_dir_exist
{
    local dirs=("$BES_OSSPOI_DIR" "$ACC_ROOT_DIR" "$DATASTORE_DIR")
    local flag=0
    for dir in "${dirs[@]}"
    do
        if [[ ! -d $dir ]]; then

            flag=1
            echo "Could not find $dir in the path"
        fi
    done

    if [[ $flag == 1 ]]; then
        return 1
    else
        return 0
    fi

}

function __acc_get_scorecard
{
    local id=$1
    local name=$2
    
    python3 $ACC_ROOT_DIR/python/get-scorecard-data.py $id $name
    [[ $? -eq 0 ]] && return 0
}

function __acc_get_criticality_score
{
    local id=$1
    local name=$2
    
    [[ -z $GITHUB_AUTH_TOKEN ]] && echo "

Criticality score needs your Github Personal Access Token(classic)

Run the below command 

$ export GITHUB_AUTH_TOKEN=<your access token>

You can also update the same in $ACC_ROOT_DIR/acc-config.cfg file.
" && return 1
    
    criticality_score --repo github.com/$GITHUB_ORG/$name --format json >> $ACC_ROOT_DIR/criticality_score.json

    python3 $ACC_ROOT_DIR/python/get-criticality_score-data.py $id $name
    [[ $? -eq 0 ]] && return 0

}



function __acc_cleanup
{

    [[ -f $ACC_ROOT_DIR/tmp_file ]] && rm $ACC_ROOT_DIR/tmp_file
    [[ -d $ACC_ROOT_DIR/repo ]] && rm -rf $ACC_ROOT_DIR/repo
    [[ -f $ACC_ROOT_DIR/criticality_score.json ]] && rm $ACC_ROOT_DIR/criticality_score.json


}
function __acc_run
{
    __acc_set_conf ||  return 1
    __acc_check_dir_exist || return 1
    read -p "Enter TAVOSS-TR id:" id
    read -p "Enter project name:" name
    echo ""
    echo "Generating data for ossp-master..."
    echo ""    

    __acc_generate_ossp_data $id $name 

    echo ""
    echo "Generating version data"
    __acc_generate_version_data $id $name

    __acc_get_version_hash $id $name || return 1
    echo ""
    echo "Version details are placed under $BES_OSSPOI_DIR/version_details/$id-$name-Versiondetails.json"
    echo ""
    local version=$(cat $ACC_ROOT_DIR/tmp_file)
    echo "Trying to fetching scorecard results..."
    __acc_get_scorecard $id $name
    [[ $? == 0 ]] && echo "Scorecard results are placed under $DATASTORE_DIR/$name/$version/scorecard/$name-$version-scorecard-report.json"
    echo ""
    echo "Trying to fetching criticality score results..."
    __acc_get_criticality_score $id $name 
    [[ $? == 0 ]] && echo "Criticality score results are placed under $DATASTORE_DIR/$name/$version/criticality_score/$name-$version-criticality_score-report.json"
    __acc_cleanup

}

__acc_run