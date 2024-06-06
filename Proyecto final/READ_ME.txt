READ ME:

El siguiente archivo contiene la descripción de cada archivo necesario para la implementación de un seguidor de linea basado en inteligencia artificial.

cope.py: Codigo de la camara y la oled donde imprime entre 0 y 1 lo que ve la camara, se envia la informaciona al oled.
seguidor.py: En este codigo se plantea la base del entrenamiento basado en el numero de unos que se recibe de la camara.
entrenador perceptron.py :Este archivo implementa la clase Matriz y  guarda el entrenamiento basado en pesos y sesgos para cada salida, junto con el numero de datos de entrada y numero de salidas en la primera fila de un txt.
perceptron_training.txt: entrenamiento guardado.
seguidor con perceptron.py: Este archivo implementa la clase Matriz y hace uso del txt de entrenamiento para predecir la dirección.
seguidor con aprendizaje con refuerzo.py: Este archivo utiliza los dos perceptrones y el entrenamiento para seguir la linea mejorando consecutivamente. 

Video de explicación:
https://youtu.be/Try4CjK5-8c?si=rf2iuKJCq7WEjK5d


Presentado por:
Elvis Salazar Mendez
20202005022
Julian Santiago Moreno Cucaita
20201005114
Cristian David Barragan
20211005074


