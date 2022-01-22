<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">
<img  align="right" width="60" style="float: right;" src="https://www.dit.upm.es/images/dit08.gif">

<br/><br/>
# SOLUCIÓN PRACTICA CREATIVA 2
### Equipo 38: Alejandro Mariscal y Carlos Chinchilla
<br/><br/>

# Despliegue de una aplicación escalable

## PARTE 1

Para desplegar una aplicación monolítica alojada en un servidor/MV hemos usado el servicio IaaS de Google Cloud. Para esta primera parte se ha realizado un script en python que automatiza el despliegue de una aplicación que muestra información sobre libros. Para ello se ha creado una instancia en gcloud donde se ha clonado el siguiente repositorio que contiene todos los archivos necesarios de la aplicación: <https://github.com/CDPS-ETSIT/practica_creativa2.git>. Se ejecutó el siguiente comando:

```
sudo git clone https://github.com/CDPS-ETSIT/practica_creativa2.git p2
```

Una vez realizado el script que se puede encontrar [aquí](./ARCHIVOS/PARTE1/parte1.py), se ejecuta en la shell el siguiente comando para ejecutar el script que lanza la app:

```
sudo python3 parte1.py
```
Para acceder a la aplicación habrá que escribir en el navegador la dirección ip de la MV con el puerto 9080: https://ipMV:9080/productpage

## PARTE 2

Para la segunda parte de la práctica se va a hacer el despliegue de la aplicación monolítica pero en este caso usando contenedores Docker. Para esta segunda parte y para el resto de la práctica hemos usado el servicio de computacion en la nube de google cloud para desplegar las instancias necesarias. Como en la primera parte, clonamos el repositorio de git a la maquina virtual para poder utilizar los archivos necesarios para que la app funcione. 

![Diagrama aplicacion monolitica](./images/app-monolith.png)

En este caso como la aplicación se va a desplegar en un contenedor, hemos creado su correspondiente Dockerfile que pueden consultar [aquí](./ARCHIVOS/PARTE2/Dockerfile.txt). Una vez escrito el Dockerfile creamos la imagen con:
```
sudo docker build -t equipo38/product-page .
```
Posteriormente arrancamos el contenedor pasando como parámetro la variable de entorno que modifica el título del html:
```
sudo docker run -e GROUP_NAME="EQUIPO38" -dp 9080:9080 --name EQUIPO38-BOOKSTORE equipo38/product-page
```
Para modificar el título del html se ha usado un script que modifica dicho titulo y lanza la aplicación. Ese script es el que se ha usado en el comando CMD del Dockerfile. El script se puede encontrar [aquí](./ARCHIVOS/PARTE2/edithtml.py). Además como se puede observar en el comando anterior, se ha mapeado el puerto 9080 de la MV con el 9080 de contenedor. Para acceder a la aplicación: https://ipMV:9080/productpage

## PARTE 3

En esta parte se va a descomponer la aplicación en cuatro microservicios (aplicación políglota): productpage, details, reviews y ratings. Se muestra una figura que ilustra dicha descomposición.

![Diagrama de aplicacion basada en microservicios](./images/app-microservices.png)

Como se puede observar cada microservicio esta escrito en un lenguaje diferente, por lo que crearemos un Dockerfile para cada servicio, exceptuando el del servicio reviews que ya se nos proporciona. Los dockerfiles se pueden visualizar en este repositorio, por aqui abajo se proporcionan sus enlaces

- [Dockerfile](./ARCHIVOS/PARTE3/Dockerfile-Productpage.txt) de productpage (python)
- [Dockerfile](./ARCHIVOS/PARTE3/Dockerfile-Reviews.txt) de reviews (java)
- [Dockerfile](./ARCHIVOS/PARTE3/Dockerfile-Details.txt) de details (ruby)
- [Dockerfile](./ARCHIVOS/PARTE3/Dockerfile-Ratings.txt) de ratings (node)

Una vez creados los Dockerfile se crearan las imagenes con el comando:
```
sudo docker build -t equipo38/productpage .
```
Cada una con su respectivo nombre segun el microservicio.

Una vez creadas las cuatro imagenes procedemos a escribir el [docker-compose](./ARCHIVOS/PARTE3/docker-compose.yml). En dicho archivo declararemos tanto los 4 microservicios (con sus imagenes ya creadas), como las variables de entorno definidas en los Dockerfile. Aunque esta aplicación no es interactiva ni almacena datos, se han creado volumenes para cada uno de los microservicios. 

Una vez terminado el docker-compose, bastara con escribir:
```
sudo docker-compose up -d
```
