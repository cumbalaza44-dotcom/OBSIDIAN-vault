# 🏍️ Prototipo X — Copiloto Inteligente para Motociclistas

> **Visión:** Sistema integrado que da al motociclista conciencia situacional 360° en tiempo real, funcionando como un copiloto predictivo que **ve** lo que los conductores no ven.

---

## 🧠 Filosofía del Problema

### El sesgo cognitivo del conductor de auto

El conductor de auto vive en una **burbuja de confort**: metal alrededor, aire acondicionado, música, cero exposición física. Su cerebro entra en modo automático — busca otros autos, no motos. **No es maldad, es sesgo cognitivo.**

### Datos clave (Hurt Report — 900+ accidentes analizados)

| Hallazgo | Dato |
|---|---|
| Choques donde el auto **no vio** a la moto | **67%** (2 de cada 3) |
| Configuración más frecuente | Auto gira a la izquierda frente a moto que va derecho |
| Lugar más peligroso | **Intersecciones** |
| Visión obstruida por brillo/u otros vehículos | **~50%** de choques múltiples |
| Velocidad pre-impacto mediana | 29.8 mph (~48 km/h) |
| Accidentes sin clima adverso | **98%** |
| Errores del rider (frenado excesivo, curva) | **67%** de accidentes individuales |

### Dualidad estratégica

| Dirección | Enfoque | Dependencia | Limitación |
|---|---|---|---|
| **A — Ser visible** | Ropa alta visibilidad, luces, reflectividad | Depende de que el conductor **quiera** mirar | impacto limitado |
| **B — Ver más** | Sensores 360°, IA, predicción de trayectorias | **No depende de nadie** | Requiere hardware/software |

> **Prototipo X elige la Dirección B:** No cambiar al conductor (imposible), sino compensar su ceguera con datos.

### Paradigma: Conciencia activa

**La solución no es:** "Mira, soy una moto" (pasivo, depende del sesgado)
**La solución es:** "Yo ya te vi a ti, y sé lo que vas a hacer" (poder del rider)

```
CICLO DE CONCIENCIA ACTIVA:

PERCIBIR → PROCESAR → DECIDIR → ENTREGAR
   │           │          │          │
   │           │          │          └─ Alertar al rider (HUD/audio/háptico)
   │           │          └─ Calcular: ¿hay riesgo? ¿en cuántos segundos?
   │           └─ Fusión de datos: ¿qué es cada objeto? ¿hacia dónde va?
   └─ Cámaras, sensores, LIDAR: capturar TODO el entorno 360°
```

La moto se convierte en un sistema que percibe el entorno con capacidad sobrehumana — 360°, sin puntos ciegos, predicción de trayectorias — y entrega esa información al rider para que **él** decida.

---

## 📏 QUÉ MEDIR EN LA PRÁCTICA (Especificaciones MVP)

### Métrica #1 — TTC (Time to Collision)

**La más crítica.** Tiempo restante antes de colisión si mantienen trayectoria y velocidad.

| TTC | Nivel | Acción |
|---|---|---|
| > 5s | 🟢 Seguro | Monitoreo normal |
| 3-5s | 🟡 Precaución | Alerta visual suave |
| 2-3s | 🟠 Urgente | Alerta audio + visual |
| < 2s | 🔴 Crítico | Alerta máxima + vibración |

### Métrica #2 — Distancia a objetos

| Sensor | Rango | Precisión | Costo |
|---|---|---|---|
| Ultrasónico (HC-SR04) | 0.02-4m | ±3mm | $1-3 |
| Radar mmWave | 0.5-50m | ±0.1m | $15-30 |
| Cámara + IA | 1-100m | Variable | $5-15 |
| LIDAR mini | 0.1-100m | ±2cm | $50-100 |

**MVP:** Ultrasónico (cercanos) + Cámara (mediana distancia).

### Métrica #3 — Velocidad relativa

- Velocidad propia: GPS + IMU
- Velocidad del otro: Cámaras + IA
- Velocidad de cierre: (Velocidad otro) - (Velocidad propia)

### Métrica #4 — Trayectoria predicha

El sistema predice dónde ESTARÁ el otro, no solo dónde ESTÁ.

Datos necesarios: posición (x,y), velocidad (mag + dir), aceleración, ángulo de dirección.

### Métrica #5 — Zona de conflicto

| Tipo | Ejemplo | Peligrosidad |
|---|---|---|
| Cruce frontal | Auto gira izq frente a moto | 🔴 CRÍTICO |
| Adelantamiento | Auto adelanta por derecha | 🟠 ALTA |
| Cambio carril | Auto cambia sin ver moto | 🟠 ALTA |
| Frenado brusco | Auto de adelante frena | 🟡 MEDIA |
| Aprox. trasera | Auto se acerca por detrás | 🟡 MEDIA |

---

## 📊 FLUJO DE DATOS (20 Hz)

```
1. CAPTURAR → Cámaras + Ultrasónicos + GPS/IMU
2. PROCESAR → IA (objetos) + Fusión + TTC + Predicción
3. DECIDIR → ¿Riesgo? ¿Nivel? ¿Dirección?
4. ENTREGAR → Sonido + LED + Vibración
```

### Valores clave MVP

| Parámetro | Valor | Fuente |
|---|---|---|
| Vel. pre-impacto mediana | 48 km/h | Hurt Report |
| Dist. frenado a 50 km/h | ~15m | Física |
| Tiempo reacción humano | 1.5s | Promedio |
| TTC mínimo seguro | 3s | Estándar ADAS |
| Frecuencia muestreo | 20 Hz | Balance costo/rendimiento |
| Cobertura | 360° | Puntos ciegos |

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

## 🗄️ Caja Negra — Registro Fo Negra — Registro Forense

> Como la caja negra de un avión: datos críticos almacenados de forma segura para esclarecer incidentes.

### 📥 Qué registra

| Dato | Propósito |
|---|---|
| 📍 **GPS + altitud + heading** | Posición exacta en cada momento |
| ⏱️ **Timestamp** (UTC + local) | Línea de tiempo precisa |
| 🚗 **Trayectorias de vehículos cercanos** | Quién estaba dónde y hacia dónde iba |
| 📐 **Inclinación / ángulo de la moto** | Maniobras, derrapes, caídas |
| 📹 **Video cíclico 360°** (últimos 15 min) | Grabación continua que se sobrescribe |
| 🔊 **Audio ambiental** (micrófono) | Bocinas, frenazos, colisiones |
| 📊 **Estado del sistema** (sensores, alertas, batería) | Fallos o mal funcionamiento pre-incidente |
| 📈 **Velocidad + aceleración + frenado** | Patrón de conducción pre-incidente |

### 🔒 Almacenamiento

| Característica | Especificación |
|---|---|
| **Medio** | MicroSD de alta resistencia (128GB+, clase 10) |
| **Cifrado** | AES-256 (solo accesible con clave del dueño) |
| **Protección física** | Módulo sellado, resistente a impacto y fuego (IP67) |
| **Autonomía** | Batería interna que mantiene 5 min de grabación post-corte |
| **Ubicación** | Bajo el asiento / dentro del chasis — oculto y anclado |

### 🚨 Eventos que activan bloqueo (guardado permanente)

El sistema **no sobrescribe** cuando ocurre:

- 🔴 **Colisión detectada** (acelerómetro + sensor de impacto)
- 🔴 **Caída** (inclinación > 60° en < 0.5s + vibración)
- 🔴 **Frenado brusco** (desaceleración > 8 m/s²)
- 🟡 **Alerta máxima** (zona roja activa por > 3s)
- 🟡 **Apagado forzado** (pérdida de energía súbita)
- 🖐️ **Activación manual** (botón de pánico en el manillar)

### 📤 Post-evento

| Paso | Acción |
|---|---|
| 1 | Caja negra bloquea el segmento actual en SD (no sobrescribible) |
| 2 | Sube automáticamente a la nube (si hay WiFi/conexión móvil) |
| 3 | Envía alerta al contacto de emergencia con coordenadas |
| 4 | Bitácora local encriptada queda disponible para autoridades/seguros |

### ⚖️ Valor legal y asegurador

- **Evidencia objetiva** para accidentes de tránsito
- **Respaldo** ante reclamaciones de seguros (quién tuvo la culpa)
- **Reducción de prima** (aseguradoras premian conducción monitoreada)
- **Paz mental** para familiares en caso de incidente grave

---

## 📊 MVP — Fase 1"}] (mínimo producto viable)

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

## 🏆 ANÁLISIS DE COMPETENCIA E INNOVACIÓN

### Tecnologías existentes en AUTOS (mercado maduro)

| Tecnología | Función | Estado |
|---|---|---|
| ADAS (Advanced Driver-Assistance) | Cámaras + radar + lidar para asistencia | Estándar en autos nuevos |
| AEB (Automated Emergency Braking) | Frenado automático de emergencia | Obligatorio UE desde 2024 |
| Blind Spot Monitoring (BSM) | Detección de puntos ciegos con radar | Común en autos medianos |
| FCW (Forward Collision Warning) | Alerta de colisión frontal | Estándar |
| Lane Departure Warning (LDW) | Alerta al salirse de carril | Estándar |
| V2X (Vehicle-to-Everything) | Comunicación auto-auto-infraestructura | En implementación |

### Competidores en MOTOS (mercado emergente — NUESTRA OPORTUNIDAD)

| Producto | Tipo | Qué hace | Limitación |
|---|---|---|---|
| **BMW K1600GT** | OEM | Detección de puntos ciegos (radar) | Solo OEM, costoso |
| **Ducati Multistrada** | OEM | V2X (Ducati Connect) | Solo Ducati, ecosistema cerrado |
| **Honda Gold Wing** | OEM | Algunos features ADAS | Caro, no modular |
| **Sena/Cardo** | Aftermarket | Comunicación bluetooth | Sin sensores de seguridad |
| **Cámaras reversa** | Aftermarket | Retrovisor digital | Sin IA, sin alertas |
| **Radar detectors** | Aftermarket | Detectan radar policial | NO previenen colisiones |

### 🔴 GAPS DEL MERCADO (nuestra oportunidad)

| Lo que NO existe | Lo que nosotros podemos ofrecer |
|---|---|
| Sistema integrado 360° para motos | Cámaras + sensores + IA en un paquete |
| Predicción de trayectorias para motos | Algoritmo TTC específico para motos |
| Caja negra forense para motos | Registro + bloqueo automático en accidente |
| Solución aftermarket accesible | $40-60 MVP vs. miles en OEM |
| IA de detección de objetos para motos | TFLite en edge, no solo radar |
| Alerta direccional (audio espacial) | "Vehículo a las 7 horas" |

### 🎯 NUESTRA INNOVACIÓN — MERCADO NUEVO O CREACIÓN DE MERCADO

> **No estamos entrando a un mercado existente. Estamos CREANDO el mercado ADAS aftermarket para motociclistas.**

```
EXISTE EN AUTOS:          EXISTE EN MOTOS:         NOSOTROS OFRECEMOS:
ADAS completo    →       Pocos features OEM   →   ADAS aftermarket accesible
AEB obligatorio   →       Nada comparable      →   Predicción + alerta (no frenado)
V2X en desarrollo →       Ducati Connect       →   V2X abierto + sensores propios
Cámaras + IA      →       Retrovisor digital   →   IA completa 360°
Caja negra        →       Nada                 →   Caja negra forense
```

**¿Por qué es CREACIÓN de mercado?**

| Argumento | Evidencia |
|---|---|
| No hay producto equivalente | No existe ADAS aftermarket completo para motos |
| Los OEM no lo ofrecen | BMW/Ducati tienen features aislados, no sistema integrado |
| El precio OEM es prohibitivo | $500+ vs. nuestro $40-60 |
| No hay categoría definida | No existe "ADAS para motos" como categoría de producto |
| Demanda no articulada | Los motociclistas no piden esto porque no saben que es posible |
| Mercado gigante sin cubrir | ~200M motos en el mundo, casi sin tecnología de seguridad aftermarket |

**Esto es Blue Ocean Strategy:** Crear un mercado nuevo donde no hay competencia directa.

### 💡 IDEAS QUE PODEMOS IMPORTAR

| De autos a motos | Cómo adaptarla |
|---|---|
| Blind Spot Monitoring | Sensores ultrasónicos laterales + alerta |
| Forward Collision Warning | Cámara frontal + TTC calculation |
| AEB (frenado automático) | **NO aplicable** — la moto no puede frenar sola sin riesgo de caída |
| V2X | Módulo WiFi/BT para comunicación moto-moto |
| Caja negra (flight recorder) | MicroSD + GPS + acelerómetro |
| Audio espacial 3D | Bocinas direccionales en casco |

### 🚀 DÓNDE INNOVAMOS NOSOTROS

1. **Precio:** OEM cuesta $500+. Nosotros $40-60.
2. **Modular:** Empezar con sensores básicos, escalar.
3. **Moto-específico:** No adaptar tecnología de auto, diseñar para moto.
4. **Caja negra + Legal:** Evidencia forense + reducción de prima de seguro.
5. **Conciencia activa:** No solo alertar — predecir.
6. **Open ecosystem:** No cerrado como BMW/Ducati.

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
