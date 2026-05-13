Desarrolla un software profesional en Python para el análisis y predicción del precio del oro mediante modelos de series temporales e inteligencia artificial. El sistema debe estar diseñado con una interfaz moderna, intuitiva, dinámica e interactiva, aplicando principios de UI/UX para brindar una experiencia visual clara, profesional y fácil de usar incluso para usuarios no técnicos.

El sistema debe usar los datos que se está proporcionando en esta misma carpeta. por lo tanto, hacer las estimaciones con dichos datos, las cuales incluyen información del precio del oro, Bitcoin, VIX, GLD u otras variables relacionadas. Debe validar automáticamente los datos, detectar formatos de fechas, limpiar valores inconsistentes y organizar toda la información en una sola estructura temporal lista para análisis.

La aplicación debe incluir:

Pantalla principal tipo dashboard.
Diseño moderno con tarjetas informativas, gráficos interactivos e indicadores visuales.
Menú lateral de navegación.
Botones dinámicos y responsivos.
Íconos representativos para cada módulo.
Barras de progreso durante el entrenamiento de modelos.
Indicadores estadísticos y métricas visuales.
Interfaz clara, elegante y minimalista.

El sistema debe tener los siguientes módulos:

Carga de datos:
para poder tener los datos, usar los archivos proporcionados en esta misma carpeta.
Mostrar vista previa de los datos.
Mostrar cantidad de registros, fechas disponibles y variables detectadas.
Limpieza y preprocesamiento:
Conversión automática de fechas.
Eliminación o corrección de valores nulos.
Normalización y escalamiento de datos.
Integración automática de datasets.
Análisis exploratorio:
Gráficos históricos del precio del oro.
Correlación entre variables.
Indicadores estadísticos:
media
desviación estándar
volatilidad
retornos
Barras y tarjetas con estadísticas resumidas.
Ingeniería de características:
Generación automática de:
medias móviles
lags
retornos
volatilidad
Permitir activar o desactivar variables desde la interfaz.
Modelos predictivos:
Implementar:
ARIMA
SARIMA
Redes neuronales LSTM
Modelos multivariables

El usuario debe poder:

seleccionar el modelo,
configurar parámetros básicos,
elegir variables de entrada,
definir horizonte de predicción:
1 año
5 años
10 años
Entrenamiento y evaluación:
Mostrar:
RMSE
MAE
Accuracy estimada
Comparación visual entre modelos
Tiempo de entrenamiento

Incluir:

barras de progreso,
indicadores visuales,
alertas inteligentes,
mensajes descriptivos fáciles de entender.
Predicción futura:
Mostrar gráficas de predicción.
Comparar valores históricos vs predichos.
Generar intervalos de confianza.
Mostrar tendencias alcistas o bajistas mediante indicadores visuales.
Visualización:
Usar gráficos modernos e interactivos:
líneas
velas financieras
histogramas
heatmaps
comparativos dinámicos

Todos los gráficos deben ser:

interactivos,
responsivos,
visualmente modernos,
fáciles de interpretar.
Exportación:
Permitir exportar:
reportes PDF,
Excel,
imágenes de gráficas,
resultados de predicción.
Tecnologías recomendadas:
Backend:
Python

Frontend/UI:

Streamlit o PyQt6

Librerías:

pandas
numpy
matplotlib
plotly
seaborn
statsmodels
scikit-learn
tensorflow / keras

Diseño UI/UX:

interfaz elegante,
colores modernos,
tarjetas visuales,
animaciones suaves,
distribución limpia,
navegación intuitiva.

El sistema debe sentirse como una plataforma profesional de análisis financiero y predicción inteligente, priorizando:

claridad visual,
facilidad de uso,
rendimiento,
modularidad,
escalabilidad,
mantenibilidad del código.

El código debe organizarse en módulos separados y bien estructurados, siguiendo buenas prácticas de desarrollo de software, arquitectura limpia y comentarios claros para facilitar futuras mejoras.