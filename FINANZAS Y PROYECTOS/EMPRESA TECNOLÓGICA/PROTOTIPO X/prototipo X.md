# 🏍️ Prototipo X — Copiloto Inteligente para Motociclistas

> **Visión:** Sistema integrado que elimina los puntos ciegos del motociclista y le proporciona conciencia situacional 360° en tiempo real, funcionando como un copiloto predictivo.

---

## 🎯 Problema que resuelve

| Problema | Impacto |
|---|---|
| Puntos ciegos laterales y traseros | Colisiones por cambio de carril |
| Tráfico invisible en intersecciones | Choques al girar |
| Vehículos en trayectoria de colisión | Accidentes fatales a alta velocidad |
| Fatiga visual y cognitiva | Error humano en tráfico denso |

---

## ⚙️ Arquitectura del sistema

### 1. Hardware — Sensorial

| Componente | Función |
|---|---|
| **Cámara 360° trasera + laterales** | Cobertura completa de puntos ciegos |
| **LIDAR miniatura frontal** | Detección de distancia y velocidad de vehículos adelante |
| **Sensores ultrasónicos laterales** | Vehículos en paralelo (ángulo muerto) |
| **GPS + IMU** | Posición, velocidad, inclinación, heading |
| **Módulo de comunicación V2V/V2I** | Datos de otros vehículos y semáforos |
| **Unidad de procesamiento edge** | Snapdragon / NVIDIA Jetson (procesamiento onboard) |

### 2. Software — Core Engine

```
[ Sensores ] → [ Fusión de datos ] → [ Modelo de trayectorias ] → [ Motor de riesgo ] → [ HUD / Audio ]
```

- **Fusión de datos:** Kalman filter + SLAM visual para mapear todos los objetos en un radio de 50m
- **Modelo de trayectorias:** Predicción de movimiento de cada vehículo (vector velocidad + aceleración + dirección)
- **Motor de riesgo:** Algoritmo que calcula zonas seguras vs. zonas de peligro en tiempo real
- **Mapa de calor dinámico:** Grid de seguridad alrededor de la moto con 4 colores:

### 3. Interfaz — Copiloto

| Capa | Salida |
|---|---|
| **HUD en casco** (visión aumentada) | Overlay con vehículos resaltados + flechas de trayectoria + zonas seguras |
| **Audio espacial 3D** | Alertas direccionales ("vehículo acercándose — 7 horas") |
| **Pantalla en tablero** | Mini-mapa 360° con codificación por colores |
| **Vibración háptica** | En guantes o asiento para alertas táctiles críticas |

---

## 🟢🔴 Sistema de Zonas — Código de Seguridad

| Color | Significado | Acción |
|---|---|---|
| 🟢 **Verde** | Zona despejada, segura | Tránsito normal |
| 🟡 **Amarillo** | Vehículo detectado, trayectoria predecible | Monitorear |
| 🟠 **Naranja** | Vehículo aproximándose, posible conflicto | Preparar maniobra |
| 🔴 **Rojo** | Colisión inminente (<2s) | Alerta máxima, maniobra evasiva sugerida |

---

## 🧠 Funcionalidades clave

### Detección predictiva de trayectorias
- No solo detecta vehículos — **predice dónde estarán en 2s/5s/10s**
- Diferencia entre: auto detenido, auto en movimiento, peatón, ciclista
- Calcula probabilidad de intersección con tu ruta

### Zonas seguras en tiempo real
- Mapa dinámico que se actualiza 30 veces/segundo
- Sugiere posicionamiento óptimo en el carril
- Indica ventanas seguras para cambio de carril o adelantamiento

### Modo Intersección
- Detecta vehículos ocultos por edificios/camiones
- Advierte sobre conductores en vía con prioridad
- Calcula timing seguro para cruce

### Modo Lluvia / Baja visibilidad
- Realza siluetas de vehículos con IA de mejora de imagen
- Aumenta sensibilidad de alertas
- Compensa falta de visibilidad del conductor

### Modo Estacionamiento
- Sensores ultrasónicos guían maniobras en reversa
- Detecta obstáculos bajos (alcantarillas, bordillos)

---

## 📊 MVP — Fase 1 (mínimo producto viable)

| Componente | Tecnología | Costo estimado |
|---|---|---|
| Cámara trasera 170° + display retrovisor | Cámara de reversa automotriz + pantalla OLED | $30-50 |
| Sensor ultrasónico lateral x2 + alerta audible | HC-SR04 + buzzer | $10 |
| App Android/iOS conectada vía BT | Smartphone del usuario + app | $0 (dev) |
| GPS + mapbox para tracking | API gratuita | $0 |
| **Total MVP** | | **$40-60** |

### Stack tecnológico sugerido (MVP)
- **Embedded:** ESP32-S3 (procesamiento + BT + WiFi)
- **Lenguaje:** C++ (firmware) + Python (backend)
- **App:** Flutter / React Native (MVP rápido)
- **IA:** TensorFlow Lite para detección de objetos

---

## 🔮 Visión a futuro

- Integración V2X (vehicle-to-everything)
- Actualizaciones OTA del motor de riesgo
- Modo convoy entre motos del mismo grupo
- Datos anónimos para mapear zonas peligrosas de la ciudad
- Colaboración con aseguradoras (descuentos por uso)

---

## 🏁 Next steps

- [ ] Investigar sensores disponibles (costos + specs)
- [ ] Definir plataforma hardware (ESP32 vs Raspberry Pi vs Jetson)
- [ ] Prototipar sensor ultrasónico + alerta audible (fase 1)
- [ ] Diseñar UX del HUD / app
- [ ] Probar en ruta y registrar datos de trayectorias

---

> *"Que la moto no sea solo libertad — que sea también seguridad inteligente."*
