# cronicahealth
CronicaHealth es un sistema innovador diseñado para optimizar el registro, monitoreo y seguimiento de pacientes con enfermedades crónicas, ofreciendo una solución integral que combina precisión médica, accesibilidad tecnológica y seguridad de datos.

## Capacidades avanzadas

- **Soporte de modelos dataclass**: Permite definir modelos de datos usando Python dataclasses, con soporte para tipos anidados, listas, fechas y serialización/deserialización automática (incluyendo listas de modelos hijos).
- **CRUD automático**: Inserción, actualización, eliminación y consulta de datos basada en los modelos definidos, con manejo transparente de listas y fechas.
- **Diseñadores automáticos**:
  - **Formularios de detalle**: Generación automática de formularios para edición y visualización de cualquier modelo, con validación de campos y controles personalizados según el tipo de dato.
  - **Buscadores automáticos**: Generación de interfaces de búsqueda para cualquier modelo, permitiendo filtrar y consultar registros de forma flexible.
- **Soporte de metadatos**: Los modelos pueden incluir metadatos para personalizar controles, validaciones, visibilidad en tablas, y más.
- **Serialización avanzada**: Listas de modelos hijos se almacenan como JSON y se reconstruyen automáticamente como instancias de sus modelos al leer desde la base de datos.

## Ejemplo de uso

```python
from database.models import Paciente, Consulta
from ui.designer import FormDetailDesigner, FormSearcherDesigner

# Crear formulario de detalle para un paciente
FormDetailDesigner(Paciente(), "Detalle Paciente").show()

# Crear buscador para consultas
FormSearcherDesigner(Consulta(), "Buscar Consultas").show()
```

CronicaHealth acelera el desarrollo de aplicaciones médicas robustas, seguras y adaptables, minimizando el código manual y maximizando la flexibilidad.
