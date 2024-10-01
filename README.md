# Pong en pygame

## Estructura del Juego

El juego es una implementación del clásico Pong utilizando la biblioteca `pygame` en Python. La estructura del juego incluye los siguientes componentes principales:

1. **Pantalla de Juego**: La ventana donde se desarrolla el juego.
2. **Raquetas**: Controladas por los jugadores para golpear la pelota.
3. **Pelota**: Se mueve por la pantalla y rebota en las raquetas y los bordes de la pantalla.
4. **Marcador**: Muestra la puntuación de los jugadores.

## Contenido

### Archivos Principales

- `main.py`: Contiene la lógica principal del juego.
- `resources/files/detalle-colisiones.csv`: Archivo CSV que registra las colisiones de la pelota con las raquetas y los bordes.
- `resources/files/detalle-partida-jugador.csv`: Archivo CSV que registra los detalles de las partidas jugadas por los usuarios.

### Datos de Usuarios

- **`detalle-colisiones.csv`**: Este archivo contiene registros de colisiones con las siguientes columnas:
  - `codUsuario`: Código del usuario.
  - `numPartida`: Número de la partida.
  - `fecha`: Fecha de la colisión.
  - `descripcion`: Descripción de la colisión con coordenadas.
  - `tipoColision`: Tipo de colisión (1\|2 o 2\|1).

- **`detalle-partida-jugador.csv`**: Este archivo contiene detalles de las partidas con las siguientes columnas:
  - `codUsuario`: Código del usuario.
  - `numPartida`: Número de la partida.
  - `puntajeA`: Puntuación del jugador A.
  - `puntajeB`: Puntuación del jugador B.
  - `fechaPartida`: Fecha de la partida.

## Descripcion

El juego de Pong en `pygame` permite a dos jugadores competir controlando raquetas para golpear una pelota. La pelota rebota en las raquetas y los bordes de la pantalla, y el objetivo es evitar que la pelota pase más allá de la raqueta del jugador. La puntuación se registra y se muestra en pantalla. Además, se guardan detalles de las colisiones y las partidas en archivos CSV para su posterior análisis.

Para ejecutar el juego, asegúrate de tener `pygame` instalado y ejecuta el archivo `main.py`.