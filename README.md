# Modal_PEMS

Herramienta para asesorar Planes Estratégicos de Movilidad Sostenible ([PEMS](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwiv5ZD1kOLPAhWSix4KHcbxCicQFggoMAE&url=http%3A%2F%2Fwww.metropol.gov.co%2FBlog%2FDocuments%2FIntrumento_normativo_gestion_aire_sept18_2015.docx&usg=AFQjCNF9v86CY4FrhtZarsl7-4WxB6Mhvw&sig2=7WO4KxBFMo8ioouUDSCpyg&bvm=bv.135974163,d.dmo)) en el Área Metropolitana del Valle de Aburrá. 

## Contiene:

* Encuestas para diagnóstico de patrones y potenciales tendencias de movilidad
* Herramienta para resumir y visualizar automáticamente cada encuesta que llegue, o todas las encuestas, sin necesidad de que un analista lo haga cada vez que hay un nuevo miembro.
* Herramienta para calcular de manera aproximada los impactos ambientales de la empresa por materia de transporte de sus empleados.
* Herramienta para focalizar esfuerzos de empresas/gobiernos según las situaciones y preferencias de los empleados de cada empresa.
* Compendio de datos y resultados centralizada en Google Drive (usando Google Drive API)

## Detalles:

* Creación y manejo de formularios con [Jotform](http://www.jotform.com).
* Código principal en Python. Base de datos con Pandas, gráficos con Matplotlib y Seaborn.
* Interacción con formularios a través del [Jotform API](http://api.jotform.com/docs/). Conversión de formularios en formato json a formato .csv (para compatibilidad con Excel).
* Georreferenciación, distancias y topografía gracias al [Google Maps API](https://developers.google.com/maps/).
* Manejo de archivos y compendio de resultados a través del [Google Drive API] (https://developers.google.com/drive/v2/reference/) (versiones 2 y 3).
