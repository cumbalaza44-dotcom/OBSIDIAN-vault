# 📸 Periféricos y Cámaras — Prototipo X

> **Objetivo:** Documentar los métodos de entrada de datos (cámaras, sensores, GPS/IMU) necesarios para el copiloto inteligente.
> **Compatibilidad:** Ambas plataformas (Pi 5 + Coral / Jetson Orin Nano)
> **Fecha:** 5 Ago 2026

---

## 📋 Requisitos del sistema de entrada

| Parámetro | Mínimo MVP | Ideal producto final |
|---|---|---|
| Cámaras | 1 (trasera/lateral) | 3-4 (360° cobertura) |
| Resolución | 720p @ 30fps | 1080p @ 30fps |
| Ángulo de visión | ≥ 120° (wide angle) | ≥ 170° (ultra wide) |
| Tipo de shutter | Global (para moto en movimiento) | Global |
| Sensores ultrasónicos | 2 (laterales) | 4 (laterales + frontal + trasero) |
| GPS | 1 módulo | 1 módulo GNSS multibanda |
| IMU | 1 (acelerómetro + giroscopio) | 1 IMU de 6 ejes |
| Distancia sensor-cámara | - | Co-temporal (mismo timestamp) |

---

## 📷 Cámaras — Evaluación

### Tipo 1: Cámara CSI (MIPI) — RECOMENDADA

| Modelo | Sensor | Resolución | FOV | Shutter | Precio | Compatible Pi 5 | Compatible Orin |
|---|---|---|---|---|---|---|---|
| **Raspberry Pi Camera Module 3** | IMX708 | 12MP / 1080p30 | 76° | Rolling | ~$25 | ✅ nativo CSI | ❌ (formato Pi) |
| **Raspberry Pi Camera Module 3 Wide** | IMX708 | 12MP / 1080p30 | 120° | Rolling | ~$30 | ✅ nativo CSI | ❌ (formato Pi) |
| **Arducam 16MP IMX296** | IMX296 | 1.6MP / 720p60 | 75° | **Global** | ~$35 | ✅ | ❌ directo |
| **Arducam 8MP OV8856** | OV8856 | 8MP / 1080p30 | 120° | Rolling | ~$20 | ✅ | ❌ directo |
| **NVIDIA IMX219 (Jetson)** | IMX219 | 8MP / 1080p30 | 77° | Rolling | ~$15 | ❌ | ✅ nativo CSI |
| **NVIDIA IMX477 (Jetson)** | IMX477 | 12.3MP / 4K30 | 75° | Rolling | ~$50 | ❌ | ✅ nativo CSI |
| **Leopard Imaging IMX290** | IMX290 | 2MP / 1080p60 | 130° | **Global** | ~$60 | ⚠️ adapter | ✅ (GMSL/CSI) |

**Criterio crítico para moto:** Global shutter > Rolling shutter. En movimiento, las cámaras con rolling shutter producen "jello effect" que degrada la detección de YOLO.

### Tipo 2: Cámara USB — Alternativa cross-platform

| Modelo | Resolución | FOV | Shutter | Precio | Pi 5 | Orin |
|---|---|---|---|---|---|---|
| **Logitech C920/C922** | 1080p30 | 78° | Rolling | ~$60 | ✅ | ✅ |
| **Elgato Facecam** | 1080p60 | 82° | Rolling | ~$150 | ✅ | ✅ |
| **Arducam USB3 IMX290** | 1080p60 | 130° | **Global** | ~$80 | ✅ | ✅ |
| **E-Con Systems See3CAM** | 1080p60 | 120° | **Global** | ~$100 | ✅ | ✅ |

**Ventaja USB:** Funciona en ambas plataformas sin adaptadores. Ideal para Fase 1 donde la cámara se comparte entre Pi5 y Orin.

### Tipo 3: Cámara IP (RTSP) — Para cobertura máxima

| Modelo | Resolución | FOV | Precio | Notas |
|---|---|---|---|---|
| **Reolink Argus 3** | 1080p30 | 122° | ~$50 | WiFi, batería |
| **Hikvision DS-2CD1043** | 4MP | 106° | ~$60 | PoE, outdoor |

**Uso:** Cámara adicional para grabación cíclica (caja negra) o cobertura trasera remota.

---

## 🔧 Configuración recomendada por fase

### Fase 1 — Prototipo (Pi 5 + Coral)

| Componente | Modelo | Cantidad | Precio | Propósito |
|---|---|---|---|---|
| **Cámara principal** | Arducam USB3 IMX290 | 1 | ~$80 | Detección vehículos (130° FOV, global shutter) |
| **Cámara trasera** | Logitech C922 | 1 | ~$60 | Retrovisor digital + caja negra |
| **Sensor ultrasónico** | HC-SR04 | 2 | ~$6 | Detección lateral cercana (<4m) |
| **GPS** | BN-880 (GPS+IMU) | 1 | ~$15 | Posición + velocidad + heading |
| **IMU externo** | MPU6050 (I2C) | 1 | ~$3 | Aceleración + inclinación (backup del BN-880) |
| **MicroSD** | Samsung EVO 128GB A2 | 1 | ~$15 | Almacenamiento caja negra |
| **Total Fase 1** | | | **~$179** | |

**Conexión Pi 5:**
```
Cámara USB (IMX290) → USB 3.0 Pi 5
Cámara USB (C922) → USB 3.0 Pi 5 (o hub USB alimentado)
HC-SR04 x2 → GPIO (Trigger/Echo pins)
BN-880 GPS → UART (GPIO 14/15)
MPU6050 → I2C (GPIO 2/3)
Coral USB → USB 3.0
```

### Fase 2 — Validación (Jetson Orin Nano)

| Componente | Modelo | Cantidad | Precio | Propósito |
|---|---|---|---|---|
| **Cámara principal** | Leopard IMX290 (GMSL) | 1 | ~$80 | 130° FOV, global shutter, bajo latencia |
| **Cámara lateral izq** | NVIDIA IMX219 | 1 | ~$15 | Punto ciego lateral izquierdo |
| **Cámara lateral der** | NVIDIA IMX219 | 1 | ~$15 | Punto ciego lateral derecho |
| **Cámara trasera** | NVIDIA IMX477 | 1 | ~$50 | Retrovisor + caja negra |
| **Radar mmWave** | TI AWR1642 | 1 | ~$30 | Velocidad relativa + distancia precisa |
| **Sensor ultrasónico** | HC-SR04 | 4 | ~$12 | Cobertura 360° cercana |
| **GPS** | u-blox NEO-M8N | 1 | ~$25 | GNSS multibanda |
| **IMU** | BNO055 | 1 | ~$20 | Fusión 9 ejes (acelerómetro + giroscopio + magnetómetro) |
| **MicroSD** | Samsung Pro Plus 256GB | 1 | ~$20 | Almacenamiento caja negra |
| **Total Fase 2** | | | **~$267** | |

**Conexión Orin Nano:**
```
IMX290 (GMSL) → GMSL/CSI port (via GMSL adapter board)
IMX219 x2 → CSI port (MIPI, requiere adapter FPC)
IMX477 → CSI port (MIPI)
AWR1642 → UART/USB (datos de radar)
HC-SR04 x4 → GPIO (o expansor I2C)
NEO-M8N → UART
BNO055 → I2C
```

---

## 🎯 Cámaras: Decisión por criterio

| Criterio | Pi 5 + Coral (Fase 1) | Jetson Orin (Fase 2) |
|---|---|---|
| **Interfaz** | USB (cross-platform) | CSI/GMSL (baja latencia) |
| **Shutter** | Global (IMX290) | Global (IMX290) |
| **FOV** | 130° (una cámara cubre) | 130° + 77° laterales |
| **Resolución** | 2MP/1080p60 | 2MP principal + 8MP laterales |
| **Cantidad** | 2 (principal + trasera) | 4 (360° completo) |
| **Precio** | ~$140 (cámaras) | ~$160 (cámaras) |

---

## 🛰️ GPS + IMU — Detalles

### Por qué ambos importan

| Sensor | Mide | Para qué sirve |
|---|---|---|
| **GPS** | Posición global (lat/lon), velocidad, heading | Ruta, velocidad absoluta, geolocalización |
| **IMU** | Aceleración lineal, velocidad angular, inclinación | Movimiento entre updates GPS, detección de caída |

### GPS + IMU integrados vs separados

| Opción | Modelo | Precio | Ventaja | Desventaja |
|---|---|---|---|---|
| **Integrado** | BN-880 (GPS+IMU) | ~$15 | Todo en uno, I2C+UART | IMU mediocre (MPU6050 interno) |
| **Separado** | u-blox NEO-M8N + BNO055 | ~$45 total | IMU de alta calidad, fusión nativa | Más caro, más cables |

**Recomendación Fase 1:** BN-880 (integrado, barato, suficiente para prototipo)
**Recomendación Fase 2:** NEO-M8N + BNO055 (separado, mejor precisión)

### Precisión GPS esperada

| Tipo | Precisión | Update rate | Precio |
|---|---|---|---|
| BN-880 | 2.5m CEP | 10 Hz | ~$15 |
| NEO-M8N | 2.0m CEP | 10 Hz | ~$25 |
| NEO-M9N | 1.5m CEP | 25 Hz | ~$60 |

Para cálculo de TTC, 10 Hz es suficiente (el bottleneck es la cámara a 30 FPS, no el GPS).

---

## 📏 Sensores ultrasónicos — HC-SR04

| Parámetro | Valor |
|---|---|
| Rango | 2cm – 4m |
| Precisión | ±3mm |
| Ángulo de haz | ~15° |
| Frecuencia | 40 kHz |
| Update rate | ~20 Hz (máx) |
| Precio | ~$2-3 c/u |
| Alimentación | 5V |
| Interface | 2 pines GPIO (Trigger + Echo) |

**Limitaciones:**
- Solo corta distancia (máx 4m)
- Ángulo estrecho (15°) — necesita múltiples sensores para cobertura
- Sensible a temperatura y viento
- No mide velocidad relativa directamente

**Por qué son válidos para MVP:**
- Extremadamente baratos
- Funcionan en lluvia, niebla, oscuridad (no dependen de luz)
- Para distancias <4m, más precisos que la cámara
- Complemento perfecto: cámara para lejos, ultrasónico para cerca

---

## 🔊 Salidas — Alertas al rider

| Tipo | Hardware | Fase | Descripción |
|---|---|---|---|
| **Audio** | Bocina bluetooth (Sena/Cardo) | 1 | Por smartphone del rider |
| **Audio espacial** | 2 bocinas direccionales | 2 | "Vehículo a las 7 horas" |
| **Visual** | LED strip en manillar | 1 | Verde/Amarillo/Rojo |
| **Háptica** | Vibrador en guantes/asiento | 2 | Alerta táctil sin desviar vista |
| **HUD** | Display OLED 1.3" en manillar | 2 | Mini mapa + zonas de riesgo |

---

## 📦 BOM (Bill of Materials) — Fase 1 completo

| # | Componente | Modelo | Cant. | Precio/unit | Total | Fuente |
|---|---|---|---|---|---|---|
| 1 | Computador | Raspberry Pi 5 8GB | 1 | $80 | $80 | Pi shop |
| 2 | TPU | Google Coral USB | 1 | $60 | $60 | Amazon/eBay |
| 3 | Cámara principal | Arducam IMX290 USB | 1 | $80 | $80 | Amazon |
| 4 | Cámara trasera | Logitech C922 | 1 | $60 | $60 | Amazon |
| 5 | Sensor ultrasónico | HC-SR04 | 2 | $3 | $6 | AliExpress |
| 6 | GPS+IMU | BN-880 | 1 | $15 | $15 | AliExpress |
| 7 | MicroSD 128GB | Samsung EVO A2 | 1 | $15 | $15 | Local |
| 8 | Fuente USB-C | RPi 5V/5A 27W | 1 | $15 | $15 | Local |
| 9 | Disipador | Argon ONE (pasivo) | 1 | $15 | $15 | Amazon |
| 10 | Casing 3D | Impresión PETG | 1 | $5 | $5 | Impresión local |
| 11 | Cable HDMI mini | 30cm | 1 | $3 | $3 | Local |
| 12 | Funda impermeable | IP65 Electronics Box | 1 | $8 | $8 | AliExpress |
| | | | | **TOTAL** | **~$362** | |

**En COP:** ~$1.448.000 (a ~$4.000/USD)

---

## 🔄 Compatibilidad cross-platform

| Componente | Pi 5 (Fase 1) | Orin Nano (Fase 2) | Notas |
|---|---|---|---|
| Coral USB TPU | ✅ directo | ✅ con adaptador | Se reutiliza |
| Arducam IMX290 USB | ✅ directo | ✅ directo | Se reutiliza |
| Logitech C922 USB | ✅ directo | ✅ directo | Se reutiliza |
| HC-SR04 | ✅ GPIO | ✅ GPIO | Mismo código |
| BN-880 GPS | ✅ UART | ✅ UART | Mismo código |
| MPU6050 IMU | ✅ I2C | ✅ I2C | Mismo código |
| MicroSD | ✅ | ✅ | Se reutiliza |

**Conclusión:** El 70% de los periféricos de Fase 1 se reutilizan en Fase 2. La inversión no se pierde.

---

> *"La cámara es el ojo. El GPS es el sentido de ubicación. La IMU es el oído interno. Sin los tres, el cerebro (YOLO+ByteTrack+Kalman) opera a ciegas."*
