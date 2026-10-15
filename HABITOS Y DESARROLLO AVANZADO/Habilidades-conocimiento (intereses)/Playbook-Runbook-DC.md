# 🛠️ PLAYBOOK / RUNBOOK — Técnico Especialista DC Hardware

> Formato: por equipo → **Issue → Causa raíz → Solución (pasos) → Qué NO hacer**.
> Fuente: Troubleshooting_plan_APN.xlsx + fichas verificadas. Se construye al revisar cada equipo.
> Estado: 3/16 equipos ✅ | Próximos: switches (Mié 14)

---

## ✅ SYS-122H-TN (CPU Node ×12) — revisado 13/10/2026

### R1. Antes de encender (checklist pre-flight)
- **Causa:** instalación nueva o después de mantenimiento mayor.
- **Solución:** 1) Verificar cortocircuito placa-base↔chasis. 2) Desconectar cables de panel (teclado/mouse). 3) Quitar tarjetas adicionales. 4) Instalar CPU bien asentada + conectar panel frontal.
- **NO hacer:** encender sin verificar BMC_HB parpadeando ni cortocircuitos.

### R2. Sin energía / No enciende
- **Causa:** cortocircuito, CMOS, jumper mal puesto.
- **Solución:** 1) Revisar cortocircuito placa↔chasis. 2) Verificar puentes/jumpers en default. 3) Switch 115/230V de la PSU correcto. 4) Batería CMOS: medir ~3 VCC, si no → cambiar.
- **NO hacer:** dar por muerta la placa sin probar CMOS clear.

### R3. Sin vídeo (encendido OK)
- **Causa:** cable VGA / DIMM mal asentado.
- **Solución:** 1) Cable VGA + monitor ON. 2) Quitar todos los DIMM, encender (alarma = problema en memoria). 3) Recolocar DIMM hasta el click. 4) Si persiste: tarjeta de diagnóstico POST.
- **NO hacer:** empezar por cambiar CPU cuando hay alarma de memoria.

### R4. Fallo al arrancar (sin POST)
- **Causa:** memoria / config heredada.
- **Solución:** 1) Boot mínimo: solo CPU + 1 DIMM + PSU. 2) Verificar LED power + LED latido BMC y que fans giren. 3) Clear CMOS (desenchufar y tocar contactos JBT1). 4) Tarjeta POST si no hay señal.
- **NO hacer:** apagar en bucle sin esperar el POST completo.

### R5. Errores de memoria
- **Causa:** DIMM mal asentado, incompatible, ranura defectuosa.
- **Solución:** 1) DIMM bien instalados (click). 2) Mismo tipo y velocidad en todo el sistema. 3) Swap entre ranuras para aislar ranura vs módulo. 4) Memtest si hay duda.
- **NO hacer:** mezclar velocidades/marcas sin verificar compatibilidad QVL.

### R6. No conserva configuración del setup
- **Causa:** PSU de baja calidad o batería CMOS agotada.
- **Solución:** 1) PSU con calidad suficiente. 2) Batería: verificar voltaje, reemplazar si < 3 VCC.
- **NO hacer:** reconfigurar cada vez sin cambiar la batería — es síntoma, no solución.

### R7. Sistema inestable (durante/después de SO)
- **Causa:** CPU/BIOS incompatible, memoria incompatible, calor.
- **Solución:** 1) Soporte CPU en BIOS actualizada. 2) Probar módulos de memoria compatibles. 3) Revisar temperatura/ventilación.
- **NO hacer:** instalar SO en hardware sin pasar POST limpio primero.

---

## ✅ ASG-1115S-NE316R (HPS/storage ×9) — revisado 13/10/2026

### M1. Antes de encender
- **Solución:** LED **BMC_HB parpadeando** antes de power-on + LED **PWROK encendido** + conector de PSU conectado + sin cortocircuitos placa↔chasis + desconectar todo cable de placa.
- **NO hacer:** encender si BMC_HB no parpadea (placa base sin standby).

### M2. Sin energía / No enciende
- **Solución:** 1) Cortocircuitos placa↔chasis. 2) Jumpers en default. 3) **Interruptor 115V/230V de la fuente bien puesto**. 4) Power cycle. 5) Batería CMOS (3 VCC).
- **NO hacer:** olvidar el switch de voltaje (error clásico con PSU internacional).

### M3. Sin vídeo
- **Solución:** 1) Cable VGA + monitor. 2) Población DIMM según manual (24 slots, 2DPC). 3) Recolocar DIMM.
- **NO hacer:** asumir GPU — este equipo no tiene, sale por VGA onboard.

### M4. Fallo al arrancar (no POST)
- **Solución:** 1) Clear CMOS (JBT1). 2) Quitar todo componente, boot mínimo CPU+1 DIMM+PSU. 3) POST card.
- **NO hacer:** conectar los 16 discos antes de tener POST limpio.

### M5. Errores de memoria
- **Solución:** 1) Misma memoria (tipo+velocidad) en los 24 slots. 2) Swap módulo↔ranura para aislar. 3) Revisar QVL del EPYC.
- **NO hacer:** dejar solo 1 módulo conectado en ranura equivocada (A1 vs A2 boots).

### M6. Setup no se conserva / Inestable
- **Solución:** PSU de calidad + batería CMOS; para inestabilidad: BIOS actual, memoria compatible, temperatura OK.
- **NO hacer:** ignorar la causa raíz (casi siempre batería o PSU barata).

### ⭐ M7. RAID: LED disco ámbar (CASO ESPECIAL — 16 bahías E3.S)
- **Sólido = disco fallido:** 1) Identificar **índice físico 1-16**. 2) Leer event log. 3) Esperar confirmación del procedimiento. 4) Reemplazar → rebuild automático.
- **Parpadeante = rebuild en curso (hasta 48h):** NO TOCAR.
- **NO hacer:** ❌ sacar sin verificar índice ❌ 2 discos a la vez en RAID 5 ❌ apagar durante rebuild.
- **Regla:** el dedo equivocado = pérdida de datos. Índice > LED.

---

## ✅ SYS-422GS-NB3RT-LCC (GPU Server ×144) — revisado 13/10/2026

### G1. Antes de encender / Sin vídeo / No POST / Memoria / Inestable
- **Mismos pasos que SYS-122H (R1-R7)** — misma familia Supermicro, mismos LEDs.
- **NO hacer:** tocar líquido (D2C) con equipo encendido.

### G2. Temp alta en GPUs con PSU y fans OK
- **Causa:** sistema de refrigeración líquida (no eléctrico ni aire).
- **Solución:** revisar CDU: flujo de bomba, temperatura de ida/vuelta, quick-disconnects, nivel de fluido. Escalar a Datacenter Ops si el CDU está fuera de rango.
- **NO hacer:** cambiar GPUs por temp alta sin descartar primero el loop de líquido.

### G3. PSU 2+2 (4× 6.6kW)
- **Estado:** 2 por lado de alimentación. Pérdida de 1 por lado = sigue vivo (cambio en caliente OK).
- **NO hacer:** dejar el equipo con 3 PSU tras un cambio (reparar la fallida el mismo día).

### G4. Carga FRU (orden de desmontaje)
- **En caliente:** discos E1.S, PSU 2+2. **Apagado+ESD:** fans (4× 80mm), DIMM (32), PCIe, GPU tray (al final, 2 manos, 84.6 kg el equipo).
- **NO hacer:** operar GPU tray solo — requiere 2 personas o rail kit.

---

## ⏳ Cola — equipos por revisar (hojas XLSX pendientes)

- [x] **Switches (15/10 → Planes-Soporte-Red-UFM-otros.md):** MSN5610-WS2RC · MSN2201-CB2RC · MSN4700-WS2RC · SSE-MQM3400-RA — patrón: LED sistema parpadea >5min → SO caído → consola · LED ámbar/rojo → CPU/firmware/temp · LED fan/PSU → FRU swap
- [x] **NICs/DPUs (15/10):** BlueField-3 · ConnectX-7 · AOC-623106AN — no detecta → reseat PCIe + drivers + BIOS · LED off → cable/puerto · LED on sin tráfico → velocidad+dúplex
- [x] **UFM MUA9702H (15/10):** LED rojo → escalar NVIDIA · SSD ámbar sólido → swap · parpadeante = rebuild 48h · power cycle 5 min antes de escalar
- [x] **XE9680 (15/10):** matriz de 5 indicadores (disco/temp/eléctrico/memoria/PCIe) — fuera de topología, verificar origen en sitio
- [ ] **Faltan equipos sin hoja:** ARS-121GL, SSE-NVL72SW, Power Shelf, CDU, SN5610 datasheet, Juniper MX204, Opengear

## 📦 RMA con fabricantes (runbook)
1. **Verificar:** modelo, P/N exacto, serial, garantía — diagnosticar tú primero (los fabricantes piden pruebas previas).
2. **Abrir caso:** evidencias = logs/BMC, foto del LED, índice del componente (serial, U, rack).
3. **Obtener RMA#** + dirección + P/N de reemplazo autorizado.
4. **Extraer** el FRU con ESD · empaque antiestático · etiqueta con RMA#.
5. **Registrar:** activo en estado "en RMA" con guía de envío en DCIM.
6. **Recibir:** validar P/N vs autorizado, seriales, condición física — NO instalar sin validar.
7. **Instalar + validar:** POST, enlaces, sensores, burn-in mínimo.
8. **Cerrar:** actualizar DCIM (alta del repuesto, baja del viejo), ticket con evidencias.

## ✅ Commissioning / validación post-mantenimiento
Checklist antes de dar por cerrada CUALQUIER intervención:
- [ ] POST completo + BMC accesible
- [ ] Enlaces: velocidad negociada = diseño, sin CRC/discards nuevos
- [ ] Sensores en rango (temp, fans, PSU, caudal si líquido)
- [ ] Versión firmware vs baseline
- [ ] Prueba funcional del componente tocado (disco→SMART, DIMM→sin ECC nuevos, PSU→carga OK)
- [ ] Bitácora: qué, cuándo, quién, resultado
- [ ] DCIM actualizado: P/N, estado, fecha
- [ ] Ticket cerrado con evidencia (foto + logs)

## 🤝 Matriz de escalamiento (coordinación de tu cargo)
| Tú (Hardware) | Network Ops | Physical Connectivity | Datacenter Ops |
|---|---|---|---|
| FRU, BIOS/BMC, POST, RAID, swap de componentes | Config switch/fabric, rutas, VLANs, UFM | Cableado, patch, fibra MPO/LC, etiquetado, ODF | Energía PDU/UPS, CDU, clima, ambiente, acceso |

- **Escalas a NetOps:** enlace caído no resuelto con óptica/cable, config, fabric.
- **Escalas a PhysConn:** cable/fibra dañada, troncales, etiquetado, patch.
- **Escalas a DCOps:** energía, temperatura de sala, fugas, permisos de rack.
- **P1:** todos los equipos — tú lideras el hardware; comunicación con severidad y ventana desde el minuto 1.

## 📇 Rutina DCIM / inventario
Campos vivos por activo: serial · P/N · rack/U exacto · estado (operativo/en RMA/baja) · fecha último mantenimiento · garantía · responsable.
**Regla: cambio físico = actualización en DCIM en el mismo turno.**

---

## 🧭 Orden canónico de diagnóstico (bisect)

Cortar el problema a la mitad en cada paso — barato→caro Y remoto→local→invasivo:

1. **Ticket → etiqueta:** verificar activo (rack, U, serial) antes que nada.
2. **Blast radius:** ¿otros equipos del rack con el mismo síntoma? → Sí = aguas arriba (PDU/switch OOB). No = este nodo.
3. **Remoto primero:** ¿link del puerto OOB en el switch? UP → BMC vivo → problema en red/monitoreo (IP/ARP/agente). DOWN → lado servidor → bajas al rack.
4. **Visual no invasivo:** power LED, BMC_HB, PSU LEDs, **velocidad de fans** (máxima = failsafe con BMC muerto; normal = otro escenario).
5. **Dos pistas en paralelo, sin mezclar:** gestión (BMC) y cómputo (POST/video). BMC muerto no lo explican CPU/RAM (el BMC vive de standby).
6. **Escalada de acción:** power cycle (60s) → reset standalone BMC → recuperación firmware → escalar/RMA. Un eslabón por vez.
7. **Validar + documentar** en DCIM/playbook.

---

## 📋 Reglas transversales (aplican a TODOS)
1. **Orden de diagnóstico:** lo más barato → lo más caro (cable → FRU → procedimiento fabricante → procedimiento DC).
2. **Flujo:** síntoma → LED/log → causa → swap mínimo → validar → documentar en DCIM.
3. **ESD siempre** antes de tocar componentes internos.
4. **Un solo cambio a la vez** — si cambias dos cosas, no sabes cuál lo arregló.
5. **Documentar después de cada intervención:** serial, hora, técnico, resultado.

---

## 📝 Registro de casos simulados

**CASO 1 (13/10) — SYS-122H, rack NR-A4, BMC sin heartbeat:** ✅ cerrado.
- Aciertos: verificar activo, separar dominios (potencia ≠ gestión), blast radius, no tocar nada (remoto→local), sospecha #1 BMC correcta, CPU/RAM descartada con buena lógica (BMC vive de standby).
- Brecha identificada: el ORDEN de ejecución — de ahí nació el marco "Orden canónico (bisect)" de arriba.
