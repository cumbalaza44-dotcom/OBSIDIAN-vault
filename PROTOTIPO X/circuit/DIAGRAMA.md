# 🔌 Diagrama de Cableado — Prototipo X v1.0

## Componentes y Conexiones

### ESP32-S3 DevKit → HLK-LD2410 (Radar Izquierdo)

```
ESP32-S3          HLK-LD2410 (L)
────────          ──────────────
GPIO16 (RX2)  ←── TX (salida datos)
GPIO17 (TX2)  ──→ RX (entrada config)
GND           ──→ GND
5V            ──→ VCC (3.3-5V)
```

### ESP32-S3 DevKit → HLK-LD2410 (Radar Derecho)

```
ESP32-S3          HLK-LD2410 (R)
────────          ──────────────
GPIO18 (RX1)  ←── TX (salida datos)
GPIO19 (TX1)  ──→ RX (entrada config)
GND           ──→ GND
5V            ──→ VCC
```

### ESP32-S3 DevKit → LED Strip WS2812B

```
ESP32-S3          LED Strip
────────          ─────────
GPIO8       ──→ DIN (entrada datos)
5V          ──→ VCC (5V)
GND         ──→ GND
```

### ESP32-S3 DevKit → Vibradores + Buzzer

```
ESP32-S3          Vibrador Izquierdo
────────          ──────────────────
GPIO4 (PWM)  ──→ Signal (a través de MOSFET N-channel)
5V           ──→ VCC del MOSFET
GND          ──→ GND

ESP32-S3          Vibrador Derecho
────────          ──────────────────
GPIO5 (PWM)  ──→ Signal (MOSFET)
5V           ──→ VCC del MOSFET
GND          ──→ GND

ESP32-S3          Buzzer
────────          ──────
GPIO6       ──→ Signal (+ del buzzer)
GND         ──→ Signal (- del buzzer)
```

### ESP32-S3 DevKit → OLED 128x64

```
ESP32-S3          OLED SSD1306
────────          ────────────
GPIO21 (SDA) ──→ SDA
GPIO22 (SCL) ──→ SCL
3.3V         ──→ VCC
GND          ──→ GND
```

### Alimentación

```
BATERÍA MOTO 12V ──→ FUSE 2A ──→ BUCK CONVERTER 12V→5V ──→ RAIL 5V
                                                                    │
                                              ┌─────────────────────┤
                                              │                     │
                                        ESP32-S3               LED Strip
                                        Radar L                Vibradores
                                        Radar R                Buzzer
                                        OLED
```

### MOSFET para Vibradores (x2)

```
        VCC (5V)
         │
         │
    ┌────┴────┐
    │ Vibrador │
    │  ERM     │
    └────┬────┘
         │
         │
    ┌────┴────┐
    │ MOSFET  │
    │ 2N7000  │
    │ (N-ch)  │
    └─┬───┬───┘
      │   │
      D   G──── 1kΩ ──→ GPIO4/5
      │   │
    S ──── GND
```

## Notas de Montaje

1. **Separación de radares:** Los dos HLK-LD2410 deben estar separados mínimo 20cm para evitar interferencia cruzada.

2. **Orientación de radares:** Montar en ángulo de 45° hacia atrás, apuntando a los ángulos muertos laterales.

3. **LED Strip:** Puede ir en el manillar (visible por el conductor) o en la parte trasera (visible por otros vehículos).

4. **Vibradores:** Uno en cada grip del manillar, dentro de la empuñadura o pegados con cinta doble cara.

5. **Buzzer:** Bajo el asiento, protegido de lluvia.

6. **Protección:**
   - Todos los cables con termorretráctil
   - Conectores JST waterproof donde sea posible
   - Case impresa 3D con IP65 mínimo

## Fuse y Protección

```
Bateria 12V ──→ FUSE 2A ──→ Buck Converter
                                │
                            FUSE 1A ──→ 5V Rail (ESP32 + sensores)
                                │
                            FUSE 2A ──→ 5V Rail (LED strip + vibradores)
```

## Cómo probar sin la moto

Si quiere probar en el banco antes de montar en la moto:

```
USB 5V ──→ ESP32 (por USB)
         ──→ Radares (por 5V pin)
         ──→ OLED (por 3.3V)
         ──→ LED strip (por 5V)

Para simular tráfico: mueva la mano frente al radar
```
