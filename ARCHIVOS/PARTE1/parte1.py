#! /usr/bin/python
from subprocess import call
import sys
import os

#Creamos un directorio de trabajo y clonamos el repositorio git
call(["git clone https://github.com/CDPS-ETSIT/practica_creativa2 p2 "], shell=True)

#Instalamos el gestor de paquetes PIP
call(["sudo apt-get -y update "], shell=True)
call(["sudo apt-get -y install python3-pip "], shell=True)


#Instalamos la lista de dependencias 
call(["sudo pip3 install -r p2/bookinfo/src/productpage/requirements.txt"], shell=True)

#Modificamos el titulo del html
fin=open("p2/bookinfo/src/productpage/templates/productpage.html", "r")
fout=open("p2/bookinfo/src/productpage/templates/index2.html", "w")

for line in fin:
    if "Simple Bookstore App" in line:
            fout.write("{% block title %}Simple Bookstore App "+os.environ['GROUP_NAME']+"{% endblock %}")
    else:
            fout.write(line)
fin.close()
fout.close()

call(["rm p2/bookinfo/src/productpage/templates/productpage.html"], shell=True)
call(["mv p2/bookinfo/src/productpage/templates/index2.html p2/bookinfo/src/productpage/templates/productpage.html"], shell=True)


#Habilitamos el puerto 9080
call(["sudo gcloud compute firewall-rules create habilita9080 --allow tcp:9080"], shell=True)
#Lanzamos la aplicacion
call(["sudo python3 p2/bookinfo/src/productpage/productpage_monolith.py 9080"], shell=True)



