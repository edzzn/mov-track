# Procesamiento de Video de un Partido de Fútbol
## Object Tracking 
*Vision por Computadora*
### Autores: 
- [Abad Freddy](https://github.com/FreddieAbad), [Reinozo Edisson](https://github.com/edzzn)

#### Descripcion detallada: [Informe](https://github.com/edzzn/mov-track/blob/master/Informe%20GPC%20-%20Abad%20y%20Reinozo.pdf)

### Funcionalidad 
El mundo actual requiere cada vez más tener ambientes controlados. Estos ambientes
controlados permiten a un gobierno garantizar la seguridad, por ejemplo, de sectores estratégicos (hospitales, escuelas, supermercados). El campo de la visión por computadora provee una solución sencilla mediante el Object tracking o rastreo de movimiento. Esta técnica de procesamiento de video se implementa en distintas fases: segmentación de la imagen, identificación de contornos, aproximación de objetos, rastreo a través de los cuadros de video y el dibujo de las secciones en movimiento. Cada fase, contiene diversos problemas que este informe pretende explorar y proponer varias metodologías que aborden estos problemas. Sin duda el campo de la visión por computadora, presenta muchas ventajas antes diversas
situaciones en las cuales explorar y explotar. El uso de este recurso, abre una multitud de posibilidades, entre ellas, por ejemplo, el reconocimiento de personas en movimiento en un video, la identificación de armas en sectores sensibles, el uso de implementos de seguridad por el personal, entre otros. Todos estos problemas y conceptos, se puede abordar utilizado varias opciones provistas por la API OpenCV para Python en 2D.
- Rastrear objetos geométricos (Object Track) en un video.
- Utilizar metodologías la segmentación de imágenes y reconocimiento de contornos
apropiados para un entorno supervisado por capturas de video ya sea con una calidad alta o baja.
- Identificar figuras geométricas estáticas y en movimiento mediante funciones provistas por a API de OpenCV 2D para Python.
- Grabar los resultados de reconocimiento de figuras en un video nuevo, basado en el video original, agregando el contorneado y etiquetas.
- Optimizar el código fuente, utilizando prácticas de programación que faciliten el mantenimiento en el tiempo de este.
- Medir la eficacia del algoritmo de rastreo ante uno o varios videos de prueba.
### Fases
- Tratamiento y Segmentación de Imágenes
  - Frame original <br>
![1 frame original](https://user-images.githubusercontent.com/38579765/87864170-a0b13980-c92a-11ea-884a-f2f70e1cac7b.jpg)

  - Filtro Gaussiano <br>
![2 filtro gaussiano](https://user-images.githubusercontent.com/38579765/87864171-a149d000-c92a-11ea-8115-c51b930dc447.png)

  - Metodo Canny <br>
![3 metodo canny](https://user-images.githubusercontent.com/38579765/87864174-a4dd5700-c92a-11ea-9a34-b2a287c070d3.png)

- Aproximación de Objetos <br>
![4 aprox](https://user-images.githubusercontent.com/38579765/87864176-a4dd5700-c92a-11ea-9149-fb49a482cea4.png)
- Rastreo de objetos a través del cuadro de video <br>
![5 rastreo](https://user-images.githubusercontent.com/38579765/87864177-a9097480-c92a-11ea-977f-ecf371a80deb.png)
- Dibujo de las áreas estáticas y en movimiento. <br>
![6 - dibujo](https://user-images.githubusercontent.com/38579765/87864178-adce2880-c92a-11ea-888b-4493d67eb25c.png)
- Grabación de Video

### Resultado
[Video](https://youtu.be/ztVkKfbCRrA)
