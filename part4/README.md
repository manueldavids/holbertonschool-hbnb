# HBnB Frontend (Part 4)

Este es el frontend de la aplicación HBnB que se conecta con el backend API (Part 3).

## 🚀 Ejecución Rápida

### Opción 1: Script Automático (Recomendado)
```bash
# Desde la raíz del proyecto
./start_app.sh
```

### Opción 2: Manual (Dos Terminales)
```bash
# Terminal 1: Backend API (Part 3)
cd part3
python3 run.py

# Terminal 2: Frontend (Part 4)
cd part4
python3 -m http.server 8000
```

## 🌐 URLs de Acceso

Una vez ejecutada, podrás acceder a:

- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000
- **Documentación API**: http://localhost:5000/api/v1/swagger

## 📋 Funcionalidades

### Para Usuarios No Autenticados
- Ver lugares de demostración
- Filtrar lugares por precio
- Navegar por la interfaz
- **Registrar nueva cuenta**

### Para Usuarios Autenticados
- Iniciar sesión con email y contraseña
- Ver lugares reales desde la API
- Ver detalles de lugares
- Agregar reseñas (funcionalidad en desarrollo)

## 🔧 Configuración

### Requisitos Previos
1. **Backend API (Part 3)**: Debe estar ejecutándose en puerto 5000
2. **Base de Datos**: El backend debe tener la base de datos configurada
3. **CORS**: Configurado para permitir peticiones desde localhost:8000

### Estructura de Archivos
```
part4/
├── index.html          # Página principal
├── login.html          # Página de login
├── register.html       # Página de registro (NUEVA)
├── place.html          # Página de detalles de lugar
├── add_review.html     # Página para agregar reseñas
├── config.js           # Configuración de URLs (NUEVO)
├── scripts.js          # Lógica JavaScript principal
├── styles/
│   └── styles.css      # Estilos CSS
└── images/             # Imágenes del sitio
```

## 🔌 Conexión con el Backend

El frontend se conecta con el backend a través de:

### Endpoints Utilizados
- `POST /api/v1/auth/login` - Autenticación
- `POST /api/v1/users/register` - Registro de usuarios (NUEVO)
- `GET /api/v1/places/` - Obtener lugares
- `GET /api/v1/places/<id>` - Obtener detalles de lugar
- `POST /api/v1/reviews/` - Crear reseñas

### Configuración CORS
El backend está configurado para aceptar peticiones desde:
- http://localhost:8000
- http://localhost:8001
- http://127.0.0.1:8000
- http://127.0.0.1:8001

## 🐛 Solución de Problemas

### Error: "WebSocket connection failed"
- **Causa**: Estás usando Live Server en lugar del servidor HTTP simple
- **Solución**: Usa `python3 -m http.server 8000` en lugar de Live Server

### Error: "Failed to load places"
- Verifica que el backend esté ejecutándose en puerto 5000
- Revisa la consola del navegador para errores de CORS
- Asegúrate de que la base de datos esté inicializada

### Error: "Login failed"
- Verifica que el usuario exista en la base de datos
- Revisa que el backend esté funcionando correctamente
- Comprueba los logs del backend para errores

### Error: "Network error"
- Verifica que ambos servicios estén ejecutándose
- Comprueba que los puertos no estén ocupados
- Revisa la configuración de CORS en el backend

## 📝 Desarrollo

### Agregar Nuevas Funcionalidades
1. Modifica los archivos HTML según sea necesario
2. Actualiza `scripts.js` para la lógica JavaScript
3. Actualiza `styles.css` para los estilos
4. Prueba la integración con el backend

### Personalización
- **Colores**: Modifica las variables CSS en `styles.css`
- **Layout**: Edita los archivos HTML
- **Funcionalidad**: Modifica `scripts.js`
- **URLs**: Modifica `config.js`

## 🔒 Seguridad

- Las peticiones autenticadas usan JWT tokens
- Los tokens se almacenan en cookies del navegador
- Las peticiones incluyen headers de autorización
- CORS está configurado para prevenir ataques CSRF

## 📊 Estado del Proyecto

- ✅ Página principal funcional
- ✅ Sistema de login
- ✅ **Sistema de registro (NUEVO)**
- ✅ Visualización de lugares
- ✅ Filtros de precio
- 🔄 Sistema de reseñas (en desarrollo)
- 🔄 Gestión de usuarios (en desarrollo)

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz tus cambios
4. Prueba la integración con el backend
5. Envía un pull request

## 📄 Licencia

Este proyecto es parte del currículo de Holberton School. 