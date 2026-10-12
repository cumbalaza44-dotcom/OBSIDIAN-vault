# Estudio desde Topología Real — Fabricato (XIO DC)

> Fuente: export Fabricato_Topologia_XIO.html (74 racks · 637 equipos · 10.049 cables)
> Uso: ejercicios prácticos con datos reales del datacenter de IA donde trabajas.
> Mapeado al Plan-Estudio-DataCenter-Hardware.md (semanas 1-6).

## Inventario real (dato base)
| Rol | Cantidad | Modelo |
|-----|----------|--------|
| GPU Server | 144 | Supermicro SYS-422GS-NB3RT-LCC (4U) |
| Server | 144 | ARS-121GL-NB3-LCC-R1 (1U) |
| NVLink Switch | 72 | SSE-NVL72SW-N5500 |
| Power Shelf | 64 | GB300 Power Shelf 33kW (32 left + 32 right) |
| ODF fibra | 84 | CommScope PPL-2U 144 MPO / XP-48 LC |
| OOB Leaf | 52 | NVIDIA SN2201 |
| GPU Fabric Leaf/Spine | 16 + 8 | Spine: NVIDIA Q3400-RA (400G) |
| CDU | 8 | refrigeración líquida |
| CPU Node | 12 | Supermicro SYS-122H-TN (2U) |
| Racks | 74 × 48U | GR(24) NR(36) NW(8) MMR(6) |

## Ejercicios por tema (Semana 1-6)

### 1. Inventario / DCIM (S5)
- Hallazgo real: racks se llaman GR-A1… pero equipment.rack dice "GPU-RACK-01" (rack_id correcto, nombre inconsistente). Cables sin length_m ni color.
- [ ] Ejercicio: auditar 5 racks y proponer regla de nombrado única (TIA-606).
- [ ] Ejercicio: qué campos faltan completar en cables para cumplir documentación.

### 2. Energía (S1) — el más jugoso
- [ ] 64 power shelves × 33 kW = 2.112 kW solo en shelves. ¿Cuántos racks de alimentación necesitas? ¿Cuántos breakers?
- [ ] Regla 80%: si un PDU maneja 22 kW, ¿cuántos GB300 power shelf caben?
- [ ] Diferencia UPS vs PDU en un diseño con 33 kW por shelf.

### 3. FRUs y potencia GPU (S2-S3)
- [ ] 144 GPU servers 4U: ¿cuántos GPUs hay si cada SYS-422GS trae 4? ¿coincide con NVL72 × N?
- [ ] Power shelf left/right: ¿por qué 32+32 y no 64 iguales? (redundancia/fases)
- [ ] Lista FRU típica de un SYS-422GS: PSU, fans, DIMM, NVMe, NIC, GPU tray.

### 4. Cooling líquido — CDU (S1, tema nuevo)
- [ ] 8 CDU para 74 racks: ¿qué es un CDU y qué reparte? (agua vs aire, bucle cerrado)
- [ ] Busca: "CDU coolant distribution unit liquid cooling datacenter"

### 5. Fibra y ODF (S5)
- [ ] 84 ODF: ¿qué es un ODF y cuántos puertos MPO aguanta cada uno? (144 MPO cada PPL-2U)
- [ ] Cálculo: 10.049 cables ÷ 84 ODF ≈ ¿cuántos cables por ODF en promedio?

### 6. Red: NVLink + fabric GPU + OOB (S3-S6)
- [ ] 72 NVLink Switch para 144 GPU servers: ¿qué conecta NVLink (intra-rack/sistema) vs el GPU Fabric Leaf/Spine (inter-rack)?
- [ ] OOB: 52 leaf + 2 spine = red de gestión fuera de banda. ¿Por qué separada? (esto es lo que tocas con SSH/iDRAC)

### 7. Etiquetado real (S1)
- [ ] Cables con label OOB-001…OOB-nnn: ¿siguen TIA-606? Propón esquema completo: EQUIPO-PUERTO-RACK.

## Progreso
- [ ] Semana 1: ejercicios 2, 4, 7
- [ ] Semana 2-3: ejercicio 3, 6
- [ ] Semana 5: ejercicio 1, 5
- [ ] Semana 6: simulacro integrador con datos reales

## Notas
- Archivo fuente: Fabricato_Topologia_XIO.zip (en inbound, temporal)
- Preguntar en sitio: refrigeración líquida (CDU), potencia real por rack, cuántas GPUs totales.
