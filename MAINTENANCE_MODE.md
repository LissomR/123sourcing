# Modo de Mantenimiento - Control de Costos

## ¿Qué es esto?

Se ha agregado un modo de mantenimiento que permite pausar el sistema sin eliminarlo. Cuando está activado, **todas las solicitudes retornarán error 503 inmediatamente** sin procesar nada, lo que reduce drásticamente el consumo de recursos y costos.

## ¿Cómo Activarlo en Railway?

### Opción 1: Desde el Dashboard de Railway

1. Ve a tu proyecto en Railway
2. Selecciona tu servicio
3. Ve a la pestaña **"Variables"**
4. Agrega una nueva variable:
   - **Nombre**: `MAINTENANCE_MODE`
   - **Valor**: `true`
5. Guarda los cambios
6. El servicio se reiniciará automáticamente y empezará a rechazar todas las solicitudes

### Opción 2: Desde Railway CLI

```bash
railway variables --set MAINTENANCE_MODE=true
```

## ¿Cómo Desactivarlo?

Cuando quieras volver a usar el sistema:

### Desde el Dashboard:
1. Ve a Variables
2. Elimina la variable `MAINTENANCE_MODE` o cambia su valor a `false`
3. Guarda los cambios

### Desde CLI:
```bash
railway variables --set MAINTENANCE_MODE=false
```

O eliminarla completamente:
```bash
railway variables --unset MAINTENANCE_MODE
```

## Respuesta que Recibirán las Solicitudes

Cuando el modo mantenimiento está activo, todas las solicitudes HTTP recibirán:

```json
{
  "errorCode": 503,
  "errorMessage": "Sistema en mantenimiento. Servicio temporalmente no disponible para reducir costos durante fase de pruebas.",
  "status": "maintenance"
}
```

Con código HTTP: **503 Service Unavailable**

## Beneficios

- ✅ **Reducción inmediata de costos**: El servidor consume recursos mínimos
- ✅ **No pierdes la configuración**: Todo permanece intacto
- ✅ **Fácil de activar/desactivar**: Solo una variable de entorno
- ✅ **Respuesta rápida**: No procesa nada pesado, solo retorna el error
- ✅ **Útil para pruebas**: Activa cuando no estés probando

## Recomendaciones

1. **Activa el modo mantenimiento cuando no estés trabajando activamente en el proyecto**
2. Desactívalo solo cuando necesites hacer pruebas
3. Considera también reducir los recursos (RAM/CPU) del servicio en Railway si es posible
4. Monitorea tus costos desde el dashboard de Railway

## Notas Técnicas

- El middleware intercepta **todas** las solicitudes antes de que lleguen a Django
- No consume recursos de Base de Datos
- No carga modelos de ML
- No procesa imágenes ni OCR
- Respuesta inmediata en microsegundos
