Proyecto: Descrito en el pdf adjunto

El proyecto sera resuelto en 4 Micro Retos:
1. Micro Reto 1: Módulo de Entrada (El Oído)
Objetivo: Capturar la información "sucia" o informal del cliente.
Qué hacer: Crear una API que escuche dos canales:
Correo (Gmail API): Leer el cuerpo del correo.
WhatsApp (Webhook): Recibir mensajes de texto.
Salida clave: Convertir ese texto informal en un JSON estructurado (ej. { "nombre_empresa": "Taller Juan", "giro": "Mecánico", "datos": "Uso aceite reciclado..." }) y pasarlo al Reto 2.

2. Micro Reto 2: Agente Inteligente y Generación (El Cerebro)
Objetivo: Usar IA Generativa para "pensar" como un consultor ambiental.
Qué debes hacer:
Tomar el JSON del Reto 1.
Construir un Prompt para una IA (como GPT-4 o Gemini) que diga: "Actúa como experto ASG, analiza estos datos del Taller Juan y genera un texto persuasivo y una calificación de sostenibilidad".
Salida clave: Un nuevo JSON enriquecido con el análisis, los "numeritos" (calificación) y textos de marketing listos para el diseño.

3. Micro Reto 3: Diseño y Branding (El Artista)
Objetivo: Maquetar el reporte para que se vea profesional y tenga publicidad (el modelo de negocio).
Qué debes hacer:
Usar una API de diseño (sugieren Canva API, pero si es complejo en 48h, podrías usar librerías de generación de PDF como ReportLab o WeasyPrint en Python diseñando con HTML/CSS).
Importante: Debe tener una Portada (Certificado con datos de la empresa) y una Contraportada (Espacio lleno de logos de patrocinadores locales, ej. "Pollo Feliz").
Salida clave: Un archivo PDF de alta calidad.

4. Micro Reto 4: Infraestructura (El Esqueleto)
Objetivo: Que el sistema sea robusto y portátil.
Qué debes hacer:
Docker: Todo debe correr en contenedores. Un contenedor para el API, otro para la lógica, etc.
CI/CD: Tener un archivo (ej. GitHub Actions) que demuestre que si subes código, se hacen pruebas automáticas.
Persistencia: Guardar los reportes generados en una base de datos.

1.Micro Reto 1: Módulo de Entrada (El Oído)
¿Cómo ejecutarlo?
Enciende LM Studio:
Carga un modelo ligero (ej. Mistral o Llama 3 8B).
Ve a la pestaña de "Server" (doble flecha) -> Start Server.
Asegúrate de que corra en el puerto 1234.

Levanta el Docker:
Abre tu terminal en la carpeta micro_reto_1 y ejecuta:
docker compose up --build