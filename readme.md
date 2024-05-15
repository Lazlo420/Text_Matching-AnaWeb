# Proyecto de Analitica - [Nombre en progreso]

La idea es extraer noticias de 2017 y 2018 de diferentes medios de comunicacion. Cuando los tengamos, toca vectorizar texto para interpretarlo. O quiza, realizar grafos (?) para realizar una red de noticias. No tiene punto esto ultimo, aunque depende de como podamos aplicarlo al objetivo general.

### Medios tomados en cuenta:
- Comercio
- Gestion - Por similitud a comercio, no creo que haya cruce en noticias | El comercio 2, mas comercio que nunca
- [Peru21](https://peru21.pe/archivo/todas/2017-01-01/) | Semejante al comercio
- [Correo](https://diariocorreo.pe/archivo/todas/2017-01-01/) 
- [Ojo](https://ojo.pe/archivo/todas/2017-01-01/)
- Trome - https://trome.com/archivo/todas/2017-01-01/ | Hay que interactuar con la pagina. (ya no hace falta)

## Progreso
[19/04] Se creo el codigo que extraera los links de las paginas que se vean como la del comercio. Falta la parte en la que consulta cada pagina y extrae informacion. De momento podemos tener los links de todas las noticias como un primer entregable basico.

[26/04] Extraccion del contenido de periodicos del comercio. 73,000 links recopilados. 36,984 noticias extraidas. Existe una fuga que vamos a ignorar o investigar. De momento lo marcamos como un mini exito. El tiempo de ejecucion fue 70 minutos. Franz quiere extraer las imagenes tambien. Nuevos periodicos a tomar en cuenta

[28/04] Tratando de replicar todo lo del comercio pero para Peru 21. No es tan a lo bruto, hace falta meterse a la pagina con selenium y llegar hasta abajo en la pagina. 