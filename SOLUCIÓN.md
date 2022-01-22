<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">
<img  align="right" width="60" style="float: right;" src="https://www.dit.upm.es/images/dit08.gif">

<br/><br/>

# Equipo 38: Alejandro Mariscal y Carlos Chinchilla
# Despliegue de una aplicación escalable

## PARTE 1

Para desplegar una aplicación monolítica alojada en un servidor/MV hemos usado el servicio IaaS de Google Cloud. Para esta primera parte se ha realizado un script en python que automatiza el despliegue de una aplicación que muestra información sobre libros. Para ello se ha creado una instancia en gcloud donde se ha clonado el siguiente repositorio que contiene todos los archivos necesarios de la aplicación: <https://github.com/CDPS-ETSIT/practica_creativa2.git>. Se ejecutó el siguiente comando:

```
sudo git clone https://github.com/CDPS-ETSIT/practica_creativa2.git p2
```

Una vez realizado el script que se puede encontrar en [a relative link](./ARCHIVOS/PARTE1/parte1.py) se ejecuta en la shell el siguiente comando para ejecutar el script que lanza la app.

```
sudo python3 parte1.py
```
