# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/).

## [2.0.0] - 2026-10-26

### 🔧 Mantenimiento

- **Arquitectura:** `dashboard-streamlit/dashboard_app.py` (838 líneas) dividido en el paquete `proyecto/dashboard/` (`config`, `engines`, `analysis`, `charts`, `views`). Ahora se ejecuta con `streamlit run dashboard-streamlit/dashboard_app.py`.
- **SOLID:** el dashboard depende del protocolo `AnalysisEngine`; los motores XLM-R y de reglas son estrategias intercambiables. Las páginas se registran en un diccionario y las acciones sugeridas por intención están en configuración (abierto/cerrado).
- **Funcional sin internet:** antes el dashboard no arrancaba porque buscaba `src/` en una carpeta equivocada y requería descargar los modelos. Ahora usa el motor de reglas por defecto y permite elegir XLM-R desde la barra lateral; si XLM-R no está disponible, cae al motor offline con un aviso.
- **Diseño moderno:** tema oscuro, encabezado destacado, tarjetas de métricas y paleta común en todos los gráficos.
- `requirements-dashboard.txt` con dependencias livianas para el dashboard.
- 8 pruebas nuevas del dashboard y del motor offline (12 en total); CI instala `pandas`.

## [1.1.0] - 2026-10-26

### 🔧 Mantenimiento

- Pruebas automatizadas del score de churn y del pipeline offline: se ejecutan sin modelos ni GPU (4 pruebas).
- Flujo de CI que corre las pruebas en cada cambio.
- README con insignias de CI y versión, y sección de pruebas.
- `.gitignore` ampliado.
