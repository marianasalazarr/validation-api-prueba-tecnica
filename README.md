# validation-api-prueba-tecnica
Prueba técnica para Becario XDEVELOP: API de validaciones documentales con Django + DRF, JWT y extracción de RFC desde PDF

# Prueba Técnica - API de Validaciones Documentales (Becario XDEVELOP)

API backend desarrollada con **Django + Django REST Framework** para autenticar usuarios con JWT, crear solicitudes de validación, subir PDFs y extraer automáticamente el RFC.

## Decisiones técnicas clave

- **Framework elegido**: Django + DRF (por su robustez en APIs REST, serializadores, permisos personalizados y documentación automática con drf-spectacular)
- **Arquitectura**:
  - Apps por dominio: `core` (autenticación, excepciones, permisos) y `validations` (modelo, vistas, serializadores, servicio de extracción)
  - Separación clara: lógica de extracción en servicio independiente (`services/extractor.py`)
  - Ownership: permiso personalizado `IsOwner` para que solo el creador vea/modifique sus validaciones
  - Errores uniformes: handler centralizado + excepciones propias (`FileInvalid`, `ExtractionFailed`)
- **Extracción**: solo PDF (pdfplumber + regex para RFC mexicano). XLSX dejado como mejora futura
- **Limitaciones actuales**:
  - Solo PDF (≤ 5 MB)
  - Solo extracción de RFC
  - Base de datos SQLite
  - Sin registro de usuarios ni refresh tokens
- **Posibles mejoras**:
  - Soporte XLSX (openpyxl/pandas)
  - Extracción de más campos (NSS, CURP, nombre)
  - Procesamiento asíncrono (Celery)
  - Tests unitarios más amplios
  - PostgreSQL en producción

## Instalación y ejecución local

1. Clonar el repositorio
   ```bash
   git clone https://github.com/marianasalazarr/validation-api-prueba-tecnica.git
   cd validation-api-prueba-tecnica
