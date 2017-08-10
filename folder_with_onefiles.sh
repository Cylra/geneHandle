#!/bin/bash
#指定文件夹,文件夹下的多个文件夹中只保留最大的文件,其余删除

export LANG=C

if [ "$#" -lt 1 ]
then
    echo "usage: $0 sortDir"
    exit 1
fi

cd $1
for i in `ls`
do
    if [ -d "$i" ]
    then
        #open dir
        cd $i     
        for file in `ls -lS | grep -v "^d" | tail -n +3 | awk '{print $9}'`
        do
            rm -rf  ${file}
        done
        #return dir
        cd ..
        #echo "----------------------"
    fi
done
