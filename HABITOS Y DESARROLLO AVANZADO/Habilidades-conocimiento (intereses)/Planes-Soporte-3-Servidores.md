  # 📋 Planes de Soporte — Los 3 Servidores (GPU / CPU / Storage)

> Plantilla: Presentación SYS-122H-TN Plan de Soporte (47 slides, 14/10/2026).
> Estructura por servidor: Perfil → Subsistemas → Plan de soporte (6 frentes) → Checklist → Puntos de control.
> Troubleshooting operativo → ver Playbook-Runbook-DC.md (R/M/G).

---

## 1. SYS-422GS-NB3RT-LCC — GPU Server ×144 (4U, líquido D2C)

### Perfil
8× GPU NVIDIA HGX B300 (288GB HBM3e c/u) · 2× Xeon 6700 (350W) · 32× DDR5 RDIMM · 8× E1.S NVMe + 2× M.2 · 4× PSU 6.6kW (2+2) · 8× OSFP 800G ConnectX-8 · NVLink 5 (1.8TB/s) · 84.6 kg neto.

### Subsistemas
- **Cómputo:** GPUs SXM sobre cold plate; interconexión NVLink/NVSwitch; HBM ≠ RAM ≠ NVMe (3 memorias distintas, no se suman).
- **Memoria:** 32 DIMM (16/socket); mapa de población del manual X14DBG-LC; registrar FRU/P/N de cada DIMM.
- **Storage:** 8× E1.S hot-swap (formato NO compatible con E3.S del ASG) + 2× M.2 boot (S3808N para RAID).
- **Red:** 8× OSFP 800G (fabric InfiniBand/Ethernet de GPU → Q3400-RA) + 2× RJ45 10GbE + BMC 1GbE → OOB.
- **Energía:** 4× 6.6kW Titanium 2+2 → circuitos A/B; cambiar una en caliente sin caída.
- **Térmica:** D2C líquido en GPUs/CPU — PLANTA no es solo aire: caudal, ΔT, presión, fugas. Fans 80mm solo secundarios.

### Plan de soporte (6 frentes)
| Frente | Foco específico de este equipo |
|---|---|
| Hardware | GPU tray, PSU 6.6kW, E1.S, DIMM, fans — intercambio por procedimiento OEM con sistema de líquido |
| Térmica/DLC | Manifold, cold plates, caudal/presión del loop del rack, fugas, throttling GPU |
| Red | ConnectX-8 + OSFP 800G, FEC/enlaces fabric, ópticas |
| Energía | 2+2 A/B, balance de carga, power shelf del rack |
| Observabilidad | nvidia-smi/BMC: temp, clocks, ECC HBM, throttling; telemetría hidráulica |
| Incidentes | P1 si caída masiva de GPUs por térmica/energía; blast radius = 8 GPU/nodo, 72/rack SU |

### Checklist diario (equipo)
□ BMC sin alarmas · □ Temp GPU bajo umbral OEM sin throttling · □ Enlaces 800G sin CRC/discards · □ E1.S SMART OK · □ 4 PSU verde · □ Flujo de líquido y sin fugas

### ⚠️ Puntos de control (evitar supuestos)
- **NO asumir hot-swap de GPU/cold plate** — confirmar MOP/SOP y drenaje según modelo.
- No abrir circuito hidráulico con sistema cargado; aislamiento eléctrico + hidráulico.
- 84.6 kg → 2 personas o rail kit siempre.

### Doc OEM
supermicro.com → SYS-422GS-NB3RT-LCC (datasheet en PDF local verificado 12/10)

---

## 2. SYS-122H-TN — CPU Node ×12 (1U, aire)

### Perfil *(slides 30-47 del PPTX)*
2× Xeon 6700/6500 (LGA-4710, hasta 86C P / 144C E) · 32× DDR5 RDIMM (4TB@6400 1DPC, 8TB@6000 2DPC; MRDIMM 8000 P-core) · 3× PCIe 5.0 x16 + 1 AIOM (OCP 3.0) · 8× 2.5" hot-swap (opción 12) + 2× M.2 · PSU 1.2-2.6kW hot-plug (según SKU) · BMC 1GbE dedicado · MB X14DBM-SP · aire (fans alta presión, conductos).

### Subsistemas
- **CPU/Memoria:** simetría de población; eventos ECC corregidos/no corregidos ANTES de sustituir; QVL obligatorio.
- **Storage:** RAID 0/1/5/10 vía Intel VROC key/controlador (verificar BOM); SMART/NVMe health; seriales antes de cambiar discos.
- **Red:** NIC por AIOM o PCIe — NO incluida en supuesto base; BMC en red de gestión aislada.
- **Energía:** A/B en PDU separados; derating por SKU; alarmas PSU.
- **Térmica:** AIRE puro — inlet temp, RPM, polvo, blanking panels, presión estática. **Sin CDU.**

### Plan de soporte (6 frentes)
Hardware (CPU/DIMM/PCIe/BMC/FRU) · Red (AIOM/ópticas) · Almacenamiento (SMART/VROC) · Energía (PSU/A-B) · Térmica (airflow) · Operación (tickets/RCAs).

### Checklist diario (equipo)
□ BMC accesible sin alarmas · □ PSU y RPM normales · □ Sin ECC no corregibles nuevos · □ RAID/VROC sano · □ Enlaces NIC sin errores · □ Cambios documentados

### ⚠️ Puntos de control (del PPTX, slide 45)
- **NO es nodo 8×GPU** — admite máx. 1 GPU doble o 3 simples; no confundir con el 422GS.
- **Refrigeración por aire** — no asumir líquido ni CDU en este equipo.
- **Red no incluida** — depende de AIOM/tarjetas instaladas.
- Validar BOM: CPU, mem, PSU, discos, backplane, controladora varían por SKU.

### Doc OEM
supermicro.com/en/products/system/hyper/1u/sys-122h-tn · downloadcenter (manual, QRG)

---

## 3. ASG-1115S-NE316R — HPS/Storage ×9 (1U, aire, all-flash)

### Perfil
1× AMD EPYC 9004/9005 (SP5, hasta 300W) · 24× DDR5 RDIMM (9TB@384GB 2DPC) · **16× E3.S NVMe hot-swap frontales** · 2× PCIe 5.0 x16 + 2× AIOM · 2× PSU 1.6kW Titanium (1+1) · M.2 boot.

### Subsistemas
- **Storage (el rol principal):** 16 bahías E3.S — formato ≠ E1.S; RAID 0/1/5/10 con controladora add-on; índice 1-16 crítico para RMA/rebuild.
- **CPU/Memoria:** single socket — 24 DIMM en 1 CPU (2DPC); simetría obligatoria.
- **Red:** 2× AIOM — dedicar a fabric de storage (NVMe-oF/IB/RoCE según diseño).
- **Energía:** 1+1 Titanium; A/B; hot-swap.
- **Térmica:** aire, 1U — sensible a obstrucciones; E3.S genera calor denso en el frontal.

### Plan de soporte (6 frentes)
Hardware (EPYC/DIMM/E3.S/PSU) · **Almacenamiento (protagonista: SMART, wear, RAID, latencia, capacity)** · Red (AIOM) · Energía (1+1) · Térmica (airflow frontal) · Operación.

### Checklist diario (equipo)
□ BMC OK · □ LED bahías sin ámbar sólido · □ RAID sin rebuild activo · □ SMART/wear OK · □ PSU 1+1 verde · □ RPM y inlet normales

### ⚠️ Puntos de control
- **Ámbar sólido = disco fallido** (índice → log → procedimiento) · **parpadeante = rebuild (hasta 48h, NO tocar)**.
- Nunca 2 discos fuera en RAID 5; nunca apagar en rebuild.
- RAID rebuild = ventana de riesgo — monitoreo reforzado hasta cierre.

### Doc OEM
supermicro.com → ASG-1115S-NE316R (datasheet PDF local verificado 12/10)

---

## 4. Comparativo rápido (los 3 en una tabla)

| | SYS-422GS (GPU) | SYS-122H (CPU) | ASG-1115S (Storage) |
|---|---|---|---|
| Qty | 144 | 12 | 9 |
| Formato | 4U | 1U | 1U |
| CPU | 2× Xeon 6700 | 2× Xeon 6700/6500 | 1× AMD EPYC |
| Memoria | 32 DIMM | 32 DIMM | 24 DIMM |
| Disco clave | 8× E1.S | 8× 2.5" (opc 12) | 16× E3.S |
| PSU | 4× 6.6kW (2+2) | 1.2-2.6kW (varía) | 2× 1.6kW (1+1) |
| Red | 8× OSFP 800G | AIOM opcional | 2× AIOM |
| Frío | **Líquido D2C** | Aire | Aire |
| FRU estrella | GPU tray / PSU 6.6kW | DIMM / PSU | **E3.S / RAID** |
| Riesgo nº1 | Térmica líquida | ECC/BOM | Índice de disco |

## Calendario de mantenimiento (común, ajustar a SLA/OEM)
- **24×7:** alertas GPU/PSU/fans/ECC/disco/enlaces/temperaturas
- **Diario:** alarmas críticas, logs, capacidad, cambios del turno
- **Semanal:** tendencias térmicas, errores de red, ECC, utilización, advisories
- **Mensual:** inventario, firmware, cableado, redundancias, registros
- **Trimestral:** RCA, capacidad térmica/eléctrica, procedimientos
- **Anual:** pruebas de contingencia, UPS/generador, auditoría

## Flujo de cada intervención (todos los equipos)
1. Revisar (ticket/impacto/alarma) → 2. Diagnosticar (correlacionar BMC/red/potencia/térmica) → 3. Autorizar (ventana/rollback/respaldo) → 4. Intervenir (MOP/SOP + ESD) → 5. Validar (POST/enlaces/temp/caudal) → 6. Documentar (RCA/seriales/tiempos)

## Severidad (repaso rápido)
- **P1:** servicio caído, fuga activa, pérdida de redundancia crítica → inmediato
- **P2:** nodo degradado, GPU/NIC fallando, fuera de baseline → escalar especialista
- **P3:** componente redundante defectuoso → ventana aprobada
- **P4:** consulta/mejora → backlog
