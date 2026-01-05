CONALITEG Book Downloader

📚🚀Este script de Python permite descargar libros de texto del catálogo histórico de la CONALITEG (Comisión Nacional de Libros de Texto Gratuitos) de México, convirtiéndolos automáticamente en un archivo PDF de alta calidad.

🌟 **Características**
Extracción Automática: Obtiene el código del libro directamente desde la URL proporcionada.  
Descarga Eficiente: Descarga las imágenes de las páginas de forma secuencial.  
Conversión a PDF: Compila todas las imágenes descargadas en un único archivo PDF con formato A4.  
Barras de Progreso: Visualiza en tiempo real el avance de la descarga y la conversión gracias a tqdm.  
Manejo de Errores: Detecta automáticamente el final del libro (error 404) y detiene la descarga de forma limpia.  

**🛠️ Requisitos Previos**
Antes de ejecutar el script, asegúrate de tener instalado Python 3.x y las siguientes bibliotecas:  
requests: Para realizar las peticiones de descarga.  
Pillow (PIL): Para el procesamiento de imágenes y obtención de dimensiones.  
fpdf: Para la generación del documento PDF.  
tqdm: Para las barras de progreso en la terminal.  
Puedes instalarlas todas ejecutando:
```Bash
    pip install requests Pillow fpdf tqdm
```
**🚀 Modo de Uso**
Clona este repositorio o descarga el archivo .py.
Busca el libro: Ve al sitio de la CONALITEG Histórico y selecciona el libro que deseas.  
Copia la URL: Asegúrate de copiar la URL de la página de visualización (ejemplo: https://historico.conaliteg.gob.mx/H1972P6MA094.htm).
Ejecuta el script:
```Bash
  python nombre_del_archivo.py
```
Pega la URL cuando el script lo solicite y presiona Enter.

El script creará una carpeta temporal para las imágenes y, al finalizar, generará el PDF en la raíz del proyecto.

**📂 Estructura de Salida**
Al procesar un libro, el script generará:  
conaliteg_images_[CODIGO]/: Una carpeta con todas las páginas en formato .jpg.  
conaliteg_book_[CODIGO].pdf: El archivo final listo para leer o imprimir.  

**⚠️ Aviso Legal**
Este proyecto ha sido creado con fines exclusivamente educativos y de uso personal. El contenido de los libros es propiedad de la Secretaría de Educación Pública (SEP) de México. Se recomienda respetar los derechos de autor y utilizar esta herramienta de manera responsable.

**🤝 Contribuciones**
¡Las contribuciones son bienvenidas! Si tienes alguna idea para mejorar el script (como añadir soporte multihilo o una interfaz gráfica), no dudes en abrir un Pull Request o reportar un Issue.
