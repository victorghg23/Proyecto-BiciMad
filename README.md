# _PROYECTO BICIMAD_ 🚲💨

En este proyecto tendrá la oportunidad de encontrar una aplicación que podrá tener un uso diario. Aquí podrá conocer la estación de BiciMad más cercana que se encuentra al monumento al que desea visitar y los metros de distancia que tiene de la estación al monumento.

**¡Tranquilo!** No es necesario que se acuerde del nombre completo del Monumento... Simplemente con poner alguna palabra que le recuerde a él, la aplicación sabrá exactamente a cuál se refiere de todos ellos.

---

## Estado ##

Proyecto final del Modulo 1 Ironhack Data Analytics - Python

Presentación del proyecto: 16/03/2024

### _Evolución del proyecto_ ###

Este proyecto se encontrará en constante cambio con el objetivo de sacar el mayor partido a la aplicación. 
El objetivo final será hacer una extracción de datos a tiempo real de las estaciones BiciMad y poder tratar con cualquier destino disponible.

---

## ¿Con qué herramientas se ha trabajado el proyecto?

La esencia del 'Proyecto Bicimad' es Python, dentro del cual se han usado las siguientes bibliotecas:

```
pandas
numpy
requests
json
ast
fuzzywuzzy
geopy.distance
geopy.distance
geopandas
matplotlib.pyplot
argparse
```

---

## Datos ##

* bicimad_stations.csv: Lo encontrará dentro del repositorio
* [Monumentos.json](https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=json&file=0&filename=300356-0-monumentos-ciudad-madrid&mgmtid=eb8e993ae322b610VgnVCM1000001d4a900aRCRD&preview=full)

> ⚠️ ¡ATENCIÓN! DEBE DE CAMBIAR LA RUTA DEL ARCHIVO BICIMAD_STATIONS.CSV A DONDE USTED LO HAYA GUARDADO ⚠️

---

## ¿Por qué el Proyecto BiciMad? ##

Las personas que vivimos en las principales metrópolis vamos al ritmo que la propia ciudad nos pide... No tenemos tiempo para perder el tiempo, y es por ello por lo que ha nacido este proyecto. Con simplemente introducir a dónde desea ir, 
usted podrá llegar a ese destino teniendo en cuenta múltiples factores que evite que tenga que irse a otra estación porque a la que había llegado ya estaba completamente ocupada o inactiva. 
Con ello conseguiremos no solo un ahorro de tiempo notable, sino que también tendremos la oportunidad de evitar accidentes que podían haber sido perfectamente evitables si aquella estación hubiese tenido un hueco libre o hubiese estado activa en ese momento... 
Además, por supuesto, de un ahorro interesante de dinero en caso de que utilice este servicio muy amenudo.

---

## USO ##

Al meterse en la terminal y poner en marcha este código, deberá poner:

_--estacion (numero de la estación en la que se encuentra) --monumento ('nombre del monumento')_
