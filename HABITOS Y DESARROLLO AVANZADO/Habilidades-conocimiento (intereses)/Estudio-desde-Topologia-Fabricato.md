# Estudio desde Topología Real — Fabricato (XIO DC)

> Fuente: export Fabricato_Topologia_XIO.html (74 racks · 637 equipos · 10.049 cables)
> Uso: ejercicios prácticos con datos reales del datacenter de IA donde trabajas.
> Mapeado al Plan-Estudio-DataCenter-Hardware.md (semanas 1-6).
> Specs verificadas vía web 12/10/2026 (fábricas: supermicro.com, nvidia.com, opengear.com, vertiv.com).

## ⚠️ Correcciones vs identificación previa
- ~~"SYS-422GS trae 4 GPU"~~ → **son 8 GPUs** (HGX B300 8-GPU, verificado en Supermicro).
- ~~"ARS-121GL = servidor general purpose"~~ → **es plataforma GB300 liquid-cooled** (familia Blackwell); confirmar rol exacto en sitio.

## Inventario real (dato base)
| Rol | Qty | Modelo |
|-----|-----|--------|
| GPU Server | 144 | Supermicro SYS-422GS-NB3RT-LCC (4U) |
| Server | 144 | ARS-121GL-NB3-LCC (1U) |
| NVLink Switch | 72 | SSE-NVL72SW-N5500 |
| Power Shelf | 64 | GB300 Power Shelf 33kW (32 left + 32 right) |
| ODF fibra | 84 | CommScope PPL-2U 144 MPO / XP-48 LC |
| OOB Leaf | 52 | NVIDIA SN2201 |
| GPU Fabric Leaf/Spine | 16 + 8 | NVIDIA Q3400-RA |
| CDU | 8 | LCS-SCDU-250LP4002 |
| CPU Node | 12 | Supermicro SYS-122H-TN (2U) |
| HPS Node | 9 | Supermicro ASG-1115S-NE316R |
| Switches red (SN5610 Core/GFE/HPS/CPDL) | 12 | NVIDIA SN5610 |
| Routers | 4 | Juniper MX204 (2) + MikroTik CCR2004 (2) |
| OOB Spine / Border Leaf | 2+2 | NVIDIA SN4700 |
| Cluster Services | 2 | NVIDIA UFM Appliance 3.5 |
| Console Server | 2 | Opengear CM8132-10G |
| Racks | 74 × 48U | GR(24) NR(36) NW(8) MMR(6) |

## 📋 Fichas técnicas verificadas (búsqueda web)

### 🟢 SYS-422GS-NB3RT-LCC — GPU Server (144×)
- **4U, refrigeración líquida**; dual Intel Xeon 6700 (hasta 350W TDP c/u)
- **GPU: NVIDIA HGX B300 8-GPU** · hasta 2.3TB HBM3e
- Interconnect: 5.ª gen NVLink/NVSwitch (1.8TB/s) · 8× ConnectX-8 SuperNIC (800Gb/s)
- RAM: 32× DIMM DDR5 (8TB @5200MT/s) · Almacenamiento: 8× E1.S NVMe hot-swap + 2× M.2
- **Power: 4× PSU 6.6kW Titanium redundantes (2+2)** ← FRU clave
- 4× PCIe Gen5 x16
- 📚 Ejercicio FRUs: PSU 6.6kW, ventiladores, DIMM E1.S, NVMe, GPU tray

### 🟢 ARS-121GL-NB3-LCC (144×)
- 1U liquid-cooled, power delivery por busbar, familia GB300/Blackwell (Grace+Blackwell)
- E1.S PCIe 5.0 hot-swap · NVLink C2C
- ⚠️ Confirmar en sitio: rol exacto (¿compute tray del NVL72?) — modelo exacto NB3-LCC sin ficha pública

### 🔵 Q3400-RA — GPU Fabric Spine/Leaf (24×)
- **4U InfiniBand Quantum-3, 144 puertos XDR** en 72 cages OSFP
- **115.2 Tb/s** · 400 o 800 Gb/s por puerto · radix 144
- 8 PSU removibles · 200-240 VAC · NVOS + UFM · topología fat-tree de 2 niveles
- 📚 Para Semana 3 (red) y Semana 6 (incidentes): cuántos leaf caben por spine

### 🔵 SN2201 — OOB Leaf (52×)
- **1G management switch: 48× 1GbE RJ45** + 4× QSFP28 uplinks (100GbE)
- 448 Gb/s · 667 Mpps · puerto de gestión dedicado + consola serie
- Conecta puertos **BMC/OOB de servidores, DPUs, SuperNICs** ← es LA red por donde haces SSH/iDRAC
- 📚 Ejercicio SSH (guía Sáb 3): conectarte vía esta red

### 🔵 SN5610 (12×) vs SN4700 (4×) — espectro Ethernet
| | SN5610 (Core/GFE/HPS/CPDL) | SN4700 (OOB Spine/Border) |
|---|---|---|
| Serie | Spectrum-4 | Spectrum-3 |
| Formato | 2U | 1U |
| Puertos | 64× OSFP | 32× QSFP-DD |
| Velocidad | **800GbE** | 400GbE |
| Capacidad | 51.2 Tb/s | 12.8 Tb/s |

### ⚡ GB300 Power Shelf 33kW (64×)
- **1U, 6× PSU hot-swap de 5.5kW → 33kW a 50 VDC** (~660-700A)
- Input: 180-305 VAC delta / 311-528 VAC wye (según proveedor: Vertiv/Flex/APC)
- PSUs en configuración N-redundante · busbar DC en rack (no C13/C19)
- 📚 Ejercicio energía: 64 × 33kW = **2.112 kW** de carga DC. ¿Cuántos breakers/fases?

### ❄️ CDU LCS-SCDU-250 (8×) — refrigeración líquida
- Clase **in-rack liquid-to-liquid 250kW** (tipo Supermicro/Delta/Accelsius MR250)
- Bombas redundantes (2N/N+1) · monitoreo SNMP/web · agua de planta → bucle cerrado GPU
- 📚 Tema nuevo Semana 1: qué reparte un CDU, temp de ida/vuelta, 250kW ≈ 3 racks GB300

### ⚫ Opengear CM8132-10G — Console Server (2×)
- **1U, 32× puertos serie RS-232 RJ45** + 2× 1GbE + 2× 10GbE SFP+
- 2GB DDR4 · dual PSU · TPM 2.0 · Smart OOB · Docker/Python
- Acceso serial a switches/BMC si se cae la red ← escenario de incidente P1
- 📚 Semana 6: recuperación cuando la red de gestión no responde

## Ejercicios por tema (Semana 1-6)

### 1. Inventario / DCIM (S5)
- Hallazgo real: racks GR-A1… pero equipment.rack dice "GPU-RACK-01" (rack_id correcto, nombre inconsistente). Cables sin length_m ni color.
- [ ] Ejercicio: auditar 5 racks y proponer regla de nombrado única (TIA-606).
- [ ] Ejercicio: qué campos faltan completar en cables para cumplir documentación.

### 2. Energía (S1) — el más jugoso
- [ ] 64 power shelves × 33 kW = 2.112 kW solo en shelves. ¿Cuántos racks de alimentación necesitas? ¿Cuántos breakers?
- [ ] Regla 80%: si un PDU maneja 22 kW, ¿cuántos GB300 power shelf caben? (33kW > 22kW → directo a busbar)
- [ ] Diferencia UPS vs PDU en un diseño con busbar DC de 50V.

### 3. FRUs y potencia GPU (S2-S3)
- [ ] 144 × 8 GPUs HGX B300 = **1.152 GPUs** — ¿cuántos sistemas NVL72 equivalen? (1.152 ÷ 72 = 16)
- [ ] PSU 2+2 del SYS-422GS: ¿qué pasa si cae una? ¿y dos del mismo lado?
- [ ] Power shelf left/right: ¿por qué 32+32 y no 64 iguales? (redundancia/fases/busbar dual)
- [ ] Lista FRU típica: PSU 6.6kW, fans, DIMM, E1.S NVMe, ConnectX-8, GPU tray.

### 4. Cooling líquido — CDU (S1, tema nuevo)
- [ ] 8 CDU × 250kW = 2.000kW de capacidad ≈ cubre la carga de 2.112kW en shelves (¡coincide!)
- [ ] Busca: "CDU coolant distribution unit liquid cooling datacenter"

### 5. Fibra y ODF (S5)
- [ ] 84 ODF: PPL-2U = 144 MPO cada uno. 10.049 cables ÷ 84 ≈ 120 cables/ODF (promedio).
- [ ] ¿Cuántas fibras vive en 144 puertos MPO? (12 fibras por MPO → capacidad vs uso)

### 6. Red: NVLink + fabric GPU + OOB (S3-S6)
- [ ] 72 NVLink Switch (SSE-NVL72SW) para 144 GPU servers: ¿1 switch por rack GB300? NVLink = intra-sistema.
- [ ] GPU Fabric: 16 leaf + 8 spine Q3400 (fat-tree 2 niveles): ¿cuántos racks por leaf?
- [ ] OOB: 52 SN2201 leaf + 2 SN4700 spine. Esta es la red de SSH/BMC — mapea puertos por rack.

### 7. Etiquetado real (S1)
- [ ] Cables con label OOB-001…OOB-nnn: ¿siguen TIA-606? Propón esquema: EQUIPO-PUERTO-RACK.

## Progreso
- [ ] Semana 1: ejercicios 2, 4, 7
- [ ] Semana 2-3: ejercicios 3, 6
- [ ] Semana 5: ejercicios 1, 5
- [ ] Semana 6: simulacro integrador con datos reales

## Notas
- Archivo fuente: Fabricato_Topologia_XIO.zip (en inbound, temporal)
- Preguntar en sitio: modelo CDU exacto, rol ARS-121GL, potencia real por rack, cuántas GPUs totales.
