#! /usr/bin/python
from subprocess import call
import sys
import os

#Editamos el titulo del html
fin=open("bookinfo/src/productpage/templates/productpage.html", "r")
fout=open("bookinfo/src/productpage/templates/index2.html", "w")

for line in fin:
    if "Simple Bookstore App" in line:
            fout.write("{% block title %}Simple Bookstore App "+os.environ['GROUP_NAME']+"{% endblock %}")
    else:
            fout.write(line)
fin.close()
fout.close()

call(["rm bookinfo/src/productpage/templates/productpage.html"], shell=True)
call(["mv bookinfo/src/productpage/templates/index2.html p2/bookinfo/src/productpage/templates/productpage.html"], shell=True)

#Habilitamos el puerto 9080
call(["sudo gcloud compute firewall-rules create habilita9080 --allow tcp:9080"], shell=True)
#Lanzamos la aplicacion
call(["sudo python3 bookinfo/src/productpage/productpage_monolith.py 9080"], shell=True)
