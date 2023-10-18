while read p; do
  echo -n $p
  echo -n " "
  timeout 10 xrdfs $p:8443 query config version
  echo " "
done <hosts.txt
