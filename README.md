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

Una vez terminado el docker-compose, bastará con escribir:
```
sudo docker-compose up -d
```

## PARTE 4
En esta parte de la práctica, hemos utilizado la herramienta de despliegue de Kubernetes GKE (Google Kubernetes Engine). Previamente, hemos cargado las imágenes creadas en el apartado anterior al repositorio de imágenes de Docker ***Docker Hub*** de forma que podrán ser utilizadas por los deployments durante el desarrollo de esta parte. El enlace al repositorio donde se encuentran las imágenes es : https://hub.docker.com/u/alexmariscalr

Para poder utilizarlas, las llamamos en el fichero yaml de cada microservicio:

```
image: alexmariscalr/productpage:v1
image: alexmariscalr/details:v1
image: alexmariscalr/ratings:v1
image: alexmariscalr/reviews:v1
image: alexmariscalr/reviews:v2
image: alexmariscalr/reviews:v3
```

Estos son los ficheros yaml con los deployments y los servicios para los 4 microservicios:

- [productpage.yaml](./ARCHIVOS/PARTE4/productpage.yaml) de Product Page
- [details.yaml](./ARCHIVOS/PARTE4/details.yaml) de Details
- [ratings.yaml](./ARCHIVOS/PARTE4/ratings.yaml) de Ratings
- [reviews-svc.yaml](./ARCHIVOS/PARTE4/reviews-svc.yaml) del servicio de Reviews
- [review-v1.yaml](./ARCHIVOS/PARTE4/productpage.yaml) con el deployment de la versión 1 de Reviews
- [review-v2.yaml](./ARCHIVOS/PARTE4/review-v2.yaml) con el deployment de la versión 2 de Reviews
- [review-v3.yaml](./ARCHIVOS/PARTE4/review-v3.yaml) con el deployment de la versión 3 de Reviews

Una vez creados, arrancamos el cluster de Kubernetes con 5 nodos. Desde GKE:

Establecemos la zona y región donde se va a desplegar el cluster:
```
gcloud config set compute/zone us-central1-a 
```

Creamos el clúster llamado ***cluster-parte4*** con 5 nodos:
```
gcloud container clusters create cluster-parte4 --num-nodes=5 --zone=us-central1-a
```

Subimos todos los ficheros al proyecto de google cloud en ***~/parte4/***
Accedemos a ese directorio : 
```
cd parte4
```
Finalmente creamos los objetos a partir de los ficheros yaml: 
```
kubectl apply –f productpage.yaml
kubectl apply –f details.yaml
kubectl apply –f ratings.yaml
kubectl apply –f reviews-svc.yaml
```
Y, dependiendo de la versión que quiera mostrarse:
```
kubectl apply –f review-v1.yaml     kubectl apply –f review-v2.yaml     kubectl apply –f review-v3.yaml
```

Para comprobar el estado de los podsy de los servicios que están corriendo:
  - Listar servicios : ```kubectl get svc```
  - Listar deployments : ```kubectl get deploy```
  - Listar pods : ```kubectl get po```

Podemos observar que se han creado 2 pods para el microservicio Rating y 3 pods para el servicio de Details, ya que así ha sido especificado en los deployments de cada uno de los servicios      
  
Podemos acceder al servicio de productpage a través de la dirección IP externa que se muestra al listar los servicios, con el siguiente formato de URL:
```<dirección_IP_externa>:9080/productpage```



## PARTE OPCIONAL

En esta parte, hemos desplegado los microservicios de Kubernetes utilizando [Helm Chart](https://helm.sh/).

Con los siguientes comandos, crearemos y generaremos las plantillas renderizadas. Cada una de ellas contendrá los correspondientes ficheros yaml con sus respectivos servicios y deployments. Se han creado 3 plantillas, una para cada versión:

```
helm install --debug --dry-run parte5-v1 ~/parte5/helm
```
```
helm install --debug --dry-run parte5-v2 ~/parte5/helm
```
```
helm install --debug --dry-run parte5-v3 ~/parte5/helm
```

Ahora, simplemente, para poder inicializar los deployments y los pods con **solo un comando** tendremos que ejecutar:

```
helm install parte5-v1 ~/parte5/helm
```
```
helm install parte5-v2 ~/parte5/helm
```
```
helm install parte5-v3 ~/parte5/helm
```

Solamente tendremos que ejecutar el comando para la versión que queremos instalar. Para cambiar de versión, habrá que eliminar previamente tanto los deployments como los pods con:

```
kubectl delete --all services
```
```
kubectl delete --all deployments
```
```
kubectl delete --all pods
```

## CONCLUSIÓN

Analizando estas cuatro maneras de implementar el despliegue de esta aplicación, hemos valorado los pros y los contras de cada una, en términos de fiabilidad y escalabilidad.

En las dos primeras partes, se ha desplegado una aplicación monolítica que agrupa todas las funciones en un solo código. Las otras dos partes, segmentan esta aplicación en cuatro microservicios que son desplegados en diferentes contenedores o clusters.

En el ámbito de la escalabilidad y la flexibilidad, está claro que una aplicación monolítica muestra mucha más rigidez y es más dificil de escalar. Aplicaciones como Kubernetes permiten realizar réplcas de un pod con las mismas caracteristicas que utilizan el mismo servicio.

En términos de eficiencia, si no fuera por las altas velocidades en cuanto a las arquitecturas de cloud y a internet, se podría decir que son más eficientes las aplicaciones monolíticas, ya que presentan un solo código. Pero dadas las mejoras durante estos últimos años y la expansión de aplicaciones como Kubernetes y Docker-Compose, podemos decir que en efectividad ambos métodos se consideran iguales.

Errores: en un microservicio, si surge algún fallo o problema, este afectará a dicho microservicio únicamente. A diferencia de las plicaciones monolíticas en las que un error puede hacer que todo el monolito falle. 

Las DevOps están extremadamente ligadas a los microservicios en los que el cambio es constante. Con ellos, la productividad aumenta de manera proporcional al aumento de la aplicación.




