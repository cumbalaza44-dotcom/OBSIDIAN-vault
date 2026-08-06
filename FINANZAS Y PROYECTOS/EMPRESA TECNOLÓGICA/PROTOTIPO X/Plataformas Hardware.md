# ⚙️ Plataformas Hardware — Prototipo X

> **Objetivo:** Definir la unidad de procesamiento que correrá el stack completo (YOLO + ByteTrack + Kalman) en la moto.
> **Fecha de definición:** 5 Ago 2026

---

## 📋 Requisitos del entorno moto

| Requisito | Valor mínimo | Ideal |
|---|---|---|
| FPS (inference) | 15-20 | 30+ |
| Consumo | < 15W | < 10W |
| Tamaño | Compatible con estribo/manillar | Compacto (< 10cm) |
| Temperatura | 0-50°C outdoor | Con disipación pasiva |
| Vibración | Resistente a motocicleta | Funda amortiguadora |
| Alimentación | 12V moto → USB 5V | Batería interna + paso USB |

---

## 🏆 Plataformas evaluadas

### Opción A: NVIDIA Jetson Orin Nano (8GB) — FASE 2

| Especificación | Detalle |
|---|---|
| **Precio** | ~$249 USD (Developer Kit) |
| **GPU** | 1024 cores CUDA (Ampere) |
| **CPU** | 6-core ARM Cortex-A78AE |
| **NPU** | 40 TOPS AI performance |
| **RAM** | 8 GB LPDDR5 |
| **YOLO11n (TensorRT)** | ~40-60 FPS |
| **YOLO11s (TensorRT)** | ~25-35 FPS |
| **Consumo** | 7-15W (configurable) |
| **Tamaño** | ~100mm × 70mm (carrier board) |
| **SDK** | JetPack (TensorRT, CUDA, cuDNN incluidos) |
| **Cámaras soportadas** | CSI (MIPI), USB, GMSL |
| **Temperatura** | 0-70°C |

**Ventajas:**
- Mejor rendimiento por watt en la categoría
- TensorRT optimiza automáticamente los modelos ONNX → trt
- SDK completo:DeepStream para pipeline de video, VPI para Kalman/visual odometry
- Comunidad NVIDIA activa, documentación excelente
- Soporte nativo para YOLO (Ultralytics tiene export directo a TensorRT)
- 40 TOPS permiten correr YOLO11s/m, no solo nano

**Desventajas:**
- Precio: ~$1M COP (Developer Kit)
- Consumo más alto que Pi5 + Coral
- Necesita refrigeración activa (ventilador incluido en dev kit)
- Más grande que Pi5

**Cuándo usar:** Cuando el prototipo esté validado y se necesite rendimiento máximo para modelo más pesado o múltiples cámaras simultáneas.

---

### Opción B: Raspberry Pi 5 (8GB) + Google Coral USB TPU — FASE 1

| Especificación | Detalle |
|---|---|
| **Precio Pi 5** | ~$80 USD |
| **Precio Coral USB** | ~$60 USD |
| **Total** | ~$140 USD (~$560K COP) |
| **CPU Pi 5** | Quad-core Cortex-A76 @ 2.4GHz |
| **RAM Pi 5** | 8 GB LPDDR4X |
| **Coral TPU** | 4 TOPS (Integer) |
| **YOLO11n (Coral/Edge TPU)** | ~25-35 FPS |
| **Consumo total** | ~8-12W |
| **Tamaño** | Pi: 85mm × 56mm + Coral: 65mm × 30mm |
| **Cámaras** | CSI (MIPI), USB |
| **OS** | Raspberry Pi OS (Debian-based) |

**Ventajas:**
- Precio: la mitad del Jetson
- Comunidad gigantesca — miles de tutoriales YOLO + Coral
- Coral descarga la inferencia del CPU → Pi maneja ByteTrack + Kalman sin estrés
- Fácil de montar: funda 3D + cable GPIO para sensores ultrasónicos
- USB Coral es plug-and-play con PyCoral/TFLite
- Reparable: si algo falla, cualquier Pi shop lo tiene

**Desventajas:**
- Dos placas separadas = más volumen (conector USB entre ellas)
- Coral USB tiene 4 TOPS vs 40 TOPS del Orin — modelo limitado a YOLO11n
- No tiene TensorRT — usa TFLite/Edge TPU compiler
- Sin SDK de DeepStream (pipeline de video manual)
- Sin soporte CUDA nativo

**Cuándo usar:** Para prototipo rápido, bajo costo, alta documentación. La primera iteración funcional.

---

### Opción C: NVIDIA Jetson Nano (4GB) — DESCARTADA

| Especificación | Detalle |
|---|---|
| **Precio** | ~$99 USD (descontinuado, usado) |
| **GPU** | 128 cores CUDA (Maxwell) |
| **RAM** | 4 GB LPDDR4 |
| **YOLO11n** | ~12-15 FPS |
| **Consumo** | 5-10W |

**Veredicto:** Tecnología de 2019. Insuficiente para YOLO11 a FPS aceptables. Descartado.

---

### Opción D: Orange Pi 5 Plus (RK3588) — DESCARTADA

| Especificación | Detalle |
|---|---|
| **Precio** | ~$100-130 USD |
| **NPU** | 6 TOPS (Rockchip RK3588) |
| **RAM** | 8/16 GB LPDDR5 |

**Veredicto:** NPU interesante pero documentación pobre. Conversión PyTorch → RKNN con bugs conocidos. Comunidad pequeña. Risk/reward no favorable para prototipo. Descartado.

---

## 🗺️ Roadmap de hardware

```
FASE 1 (Prototipo)          FASE 2 (Validación)         FASE 3 (Producto)
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ Pi 5 + Coral USB    │────▶│ Jetson Orin Nano    │────▶│ Custom carrier PCB  │
│ ~$140 USD           │     │ ~$249 USD           │     │ ~$150-200 USD       │
│ YOLO11n @ 25-35 FPS │     │ YOLO11s @ 25-35 FPS │     │ YOLO11m @ 20-30 FPS │
│ 1 cámara            │     │ 2-3 cámaras         │     │ 3-4 cámaras + radar │
│ Prototipo funcional │     │ Demo completa       │     │ Producto final      │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

---

## 📊 Comparativa final

| Criterio | Pi 5 + Coral | Jetson Orin Nano |
|---|---|---|
| **Costo total** | ~$140 USD ✅ | ~$249 USD |
| **FPS YOLO11n** | 25-35 | 40-60 ✅ |
| **FPS YOLO11s** | No viable | 25-35 ✅ |
| **Múltiples cámaras** | 1-2 max | 3-4 ✅ |
| **Comunidad/docs** | Excelente ✅ | Buena |
| **Facilidad de prototipo** | Alta ✅ | Media |
| **Consumo** | 8-12W ✅ | 7-15W |
| **Tamaño** | Dos placas | Una placa ✅ |
| **SDK integrado** | No | Sí (DeepStream, VPI) ✅ |
| **Escalabilidad** | Limitada | Alta ✅ |

---

## 🔑 Decisión

| Fase | Plataforma | Razón |
|---|---|---|
| **Fase 1 — Prototipo** | **Raspberry Pi 5 + Coral USB** | Bajo costo, alta documentación, funciona para validación |
| **Fase 2 — Validación** | **Jetson Orin Nano** | Más FPS, más cámaras, SDK completo, camino a producto |
| **Fase 3 — Producto** | **Custom PCB con Orin Nano module** | Integrado, optimizado, miniaturizado |

---

> *"Empezar barato, escalar con datos. El Pi5 valida la idea, el Orin la ejecuta."*
