# Busca Recetas

**Autor:** Tymur Kulivar Shymanskyi  
**Clase:** Diseño de interfaces

## Descripción

Aplicación de escritorio en Python para buscar recetas mediante una interfaz gráfica intuitiva conectada a una API.

## Características

- **Interfaz gráfica:** Utiliza `tkinter` para la creación de la interfaz gráfica.
- **Búsqueda avanzada:** Permite buscar recetas por nombre, tiempo de preparación, dificultad, calorías y tipo de receta.
- **Visualización de recetas:** Muestra las recetas obtenidas de la API en un formato fácil de leer.
- **Desplazamiento:** Soporte para desplazamiento en la lista de recetas.


## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/Timasostima/BuscaRecetas.git
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd BuscaRecetas
    ```
3. Instala las dependencias necesarias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la API en un proceso separado:
    ```sh
    python app/main.py
    ```
2. La interfaz gráfica se abrirá automáticamente y podrás comenzar a buscar recetas.

## Estructura del Proyecto


- [`app/`](app): Contiene la aplicación de escritorio.
  - [`main.py`](app/main.py): Punto de entrada de la aplicación. Ejecuta la API y la interfaz gráfica.
  - [`gui.py`](app/gui.py): Contiene la clase `GUI` que define la interfaz gráfica principal.
  - [`sidebar.py`](app/sidebar.py): Contiene la clase `Sidebar` que define la barra lateral de la interfaz gráfica.
  - [`slider.py`](app/slider.py): Define la clase `Slider` utilizada en la interfaz gráfica.
  - [`utils.py`](app/utils.py): Funciones utilitarias para la aplicación.
  - [`Recipe.py`](app/Recipe.py): Define la clase `Recipe` que representa una receta.
- [`api/`](api): Contiene la API que proporciona las recetas.
  - [`api.py`](api/api.py): Contiene la lógica de la API que proporciona las recetas.

## Licencia

Este proyecto está licenciado bajo la Licencia Pública General de GNU. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.