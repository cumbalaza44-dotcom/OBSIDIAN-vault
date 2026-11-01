# 🏍️ Prototipo X — Copiloto Moto: Arquitectura v1.0

## Problema a resolver
Mientras conduce moto, el motociclista tiene **puntos ciegos** que no cubren los espejos:
- Vehículos acercándose por detrás en ángulos muertos
- Autos adelantando por la derecha
- Vehículos en intersecciones que no se ven hasta el último momento
- Bicicletas/motos que se acercan rápido y silenciosamente

## Solución: Sistema de Detección de Tráfico por Radar + Alertas

### Componentes principales

| # | Componente | Función | Costo aprox (USD) |
|---|-----------|---------|-------------------|
| 1 | **ESP32-S3 DevKit** | MCU principal — procesa datos de radar | ~$8 |
| 2 | **HLK-LD2410** (x2) | Radar mmWave 24GHz — detecta movimiento y distancia | ~$12 c/u |
| 3 | **WS2812B LED Strip** (1m) | Alerta visual por colores (verde/amarillo/rojo) | ~$5 |
| 4 | **Vibrador ERM** (x2) | Alerta háptica en manillar (izq/der) | ~$2 c/u |
| 5 | **OLED 0.96" I2C** | Display de estado y distancia | ~$4 |
| 6 | **Buzzer activo** | Alerta sonora en emergencia | ~$1 |
| 7 | **Fuente 12V → 5V Buck** | Alimentación desde batería de moto | ~$3 |
| 8 | **Protoboard + cables** | Conexiones | ~$3 |
| **TOTAL** | | | **~$50 USD** |

### Ubicación en la moto

```
         [OLED Display]
              │
    ┌─────────┴─────────┐
    │      HANDLEBAR     │
    │  [Vib L]    [Vib R]│
    └─────────┬─────────┘
              │
         ┌────┴────┐
         │  ESP32  │
         │  S3     │
         └────┬────┘
              │
    ┌─────────┴─────────┐
    │   REAR SUBFRAME    │
    │                    │
  [Radar I]         [Radar D]
  (izquierda)      (derecha)
    ↙ ángulo          ↘ ángulo
   120°                120°
```

### Ángulos de cobertura del radar

```
        REAR
         │
    ╲    │    ╱
     ╲   │   ╱
  R-izq  │  R-der
  120°   │  120°
     ╱   │   ╲
    ╱    │    ╲
         │
        MOTO →
```

Cada radar HLK-LD2410 cubre 120° horizontal, montado en ángulo hacia atrás:
- **Radar izquierdo:** cubre ángulo muerto izquierdo + carril izquierdo
- **Radar derecho:** cubre ángulo muerto derecho + carril derecho + adelantamientos

### Lógica de alertas

| Distancia | Nivel | LED | Vibración | Buzzer |
|-----------|-------|-----|-----------|--------|
| > 5m | 🟢 Seguro | Verde fijo | Off | Off |
| 2-5m | 🟡 Precaución | Amarillo parpadeo lento | Off | Off |
| 1-2m | 🟠 Alerta | Rojo parpadeo | Vibración suave | Off |
| < 1m | 🔴 Peligro | Rojo sólido + flash | Vibración fuerte | Bip rápido |
| Se acelera hacia ti | ⚠️ Inminente | Rojo strobe | Vibración continua | Bip continuo |

### Detectando "se acelera hacia ti"
El radar LD2410 reporta **distancia + velocidad** (Doppler). Si la distancia disminuye a > 0.5 m/s, el vehículo se está acercando → escalar alerta aunque esté a 3-4 metros.

### Alimentación
- Batería de moto: 12V
- Buck converter: 12V → 5V (ESP32 + sensores)
- Consumo estimado: ~500mA a 5V (2.5W total)
- Fuse de protección: 2A

### Firmware
- Arduino/PlatformIO con ESP-IDF
- Dual-core: Core 0 = lectura radar, Core 1 = alertas + display
- WiFi: modo STA para debugging (web server en 192.168.4.1)
- OTA updates para iterar sin cables

### Fase 1 (Primer prototipo funcional)
- [x] Diseño de arquitectura
- [ ] Código firmware ESP32
- [ ] Simulador de datos de radar para testing en PC
- [ ] Diagrama de cableado
- [ ] BOM final con links de compra
- [ ] Instrucciones de montaje

### Fase 2 (Post-primer prototipo)
- [ ] Cámara frontal para detección de semáforos/obstáculos
- [ ] Conexión Bluetooth al teléfono para logging
- [ ] GPS para mapeo de zonas peligrosas
- [ ] App companion (iOS/Android)

### Fase 3 (Producción)
- [ ] PCB personalizada
- [ ] Case 3D print resistente al agua (IP65)
- [ ] Integración con ECU de la moto (CAN bus)
- [ ] Certificación CE/FCC
