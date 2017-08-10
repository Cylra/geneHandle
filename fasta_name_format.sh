#! /bin/bash
#替换fasta文件中的名称，只保留NC号等,并添加>，只能执行一次
if [ $# -lt 1 ]
then
   echo "usage: $0 dir"
   exit 1
fi

cd $1
for file in `ls`
do
    kk=`sed -n '1p' ${file} | cut -d '|' -f 4 | awk -F '.' '{print $1}'`
    kk=\>${kk}
    sed -i "1c$kk" ${file}
done
