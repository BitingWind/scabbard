#!/usr/bin/env bash


summary_file=${WORKSPACE}/API_Automation_Test/${PROJECT}/summary_file


function parameter_pre_check(){

    if [ -z ${param} ];then
    	echo "${param} 为空。。。stop"
        exit 1
    fi

}
function auto_test_run(){
  cd ${WORKSPACE}/API_Automation_Test/${PROJECT}
  pwd

  working_dir=`pwd`
  export PYTHONPATH=$PYTHONPATH:$working_dir

  export PYTHONIOENCODING=UTF-8

  python ./test_runner/${automation_main_file} --group_id ${LARK_GROUP_ID}
}

function main(){
  parameter_pre_check
  auto_test_run
}


main