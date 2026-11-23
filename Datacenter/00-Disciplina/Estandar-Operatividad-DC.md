---
created: 2026-11-16
updated: 2026-11-23
version: v2.2
estado: plantilla viva — mejorar con cada turno
tags: [datacenter, operatividad, RMA, commissioning, disciplina]
---

# 🧩 Estándar Mínimo de Operatividad — Técnico DC

> Plantilla viva. Cada turno que aprendas algo, se agrega aquí.
> Si está aquí, está priorizado.
> v2.0 (23/11): Disciplina Operativa integrada como sección 0.
> v2.2 (23/11): Objetivos permanentes + formato entrega general de turno.

## 0.1 Objetivos permanentes — el norte de cada turno

> Estos 4 objetivos aplican SIEMPRE, incluso en el turno más tranquilo. Son lo que convierte "estar de turno" en "hacerse cargo del DC".

**1. Trazabilidad — si no está escrito, no pasó**
- Todo lo que toques, veas o decidas deja rastro: ticket, DCIM, foto, entrega.
- Nada vive solo en tu cabeza o en tu celular. El siguiente turno debe poder reconstruir tu noche sin llamarte.
- Regla: al cerrar, cualquiera que lea tu entrega sabe qué hiciste, qué viste, qué dejaste pendiente y qué hay que vigilar.

**2. Validación cruzada — desconfía del monitor**
- Ningún dato de Zabbix/DCIM se da por cierto hasta validarlo en campo (CLI + LED + serial físico).
- Cada turno: al menos 1 validación. ¿Dice UP? Míralo. ¿Dice tal serial en tal U? Confírmalo.
- Cada discrepancia encontrada = un punto ciego menos. Se registra como hallazgo, no como queja.
- Origen: lección 15/11 (Zabbix ciego) + INC-002 (umbral 2.26 dB real vs reportado).

**3. Proactividad — el turno tranquilo produce**
- Turno sin incidentes NO es turno vacío. Es turno de levantar línea base.
- Mínimo por noche tranquila: 1 rack documentado + 1 validación cruzada + ronda con foto.
- En 15 turnos el DC queda mapeado. Nadie más lo está haciendo. Ese es tu diferencial.
- Lo que hoy documentas es lo que mañana te hace rápido diagnosticando.

**4. Dinamismo en equipo — resuelve el dolor ajeno**
- Cómputo, facility y fibra son tus aliados, no tus vecinos. Pregunta qué les duele.
- Cómputo: ¿qué racks les fallan más? ¿qué info les falta? Te vuelves su fuente.
- Facility: energía y clima mandan. Avisar antes + registrar después = respaldo.
- Fibra: tu aliado técnico. Lo que te enseñe se documenta y se devuelve en formato útil.
- Regla: cada hallazgo que sirva a otro equipo se comparte en la entrega general. Así nace la autoridad: siendo útil, no pidiendo permiso.

## 0.2 Disciplina operativa — toda maniobra

> Caso base: MPO NIC → leaf 15/11 + hallazgo 17/11. La falla técnica se resolvió bien (peinado MPO, fracturas fuera, radios corregidos). Lo que falló fue el orden. Esta sección existe para que el orden nunca falle.

### 7 pasos obligatorios — desglose operativo

**1. Autorización — nadie toca sin papel**
- Qué pedir: # ticket, quién autoriza (nombre + rol), ventana con hora inicio-fin exacta.
- Verbal no vale. Si el líder dice "hágale" de palabra → pedir que lo escriba en el ticket o chat del turno.
- Sin ventana fija no hay maniobra. "Cuando se pueda" no es ventana.
- Caso real: 15/11 se operó con autorización verbal → apagado desde PDU sin shutdown confirmado, encendido desde PDU. Eso no vuelve a pasar.

**2. Impacto — pensar antes de tocar**
- Preguntas obligatorias: ¿qué servicio cuelga de este fierro? ¿qué pasa si lo tumbo 5 min? ¿a quién le duele?
- Avisar a: NetOps (dueños del enlace), cómputo (si hay GPUs/entrenamiento), DC Ops (dueños de ventana).
- Si el impacto toca entrenamiento distribuido (NICs XE2 o similar) → prioridad alta, MOP formal obligatorio.
- Regla INC-002: 4 cables en riesgo = mazo completo. El impacto no es 1 cable, es todo lo que pasa por ese punto físico.

**3. Pre-check — foto del antes**
- LEDs del puerto/equipo (color + estado) + foto.
- Link: `show interfaces status` en switch / `ethtool <iface>` en servidor → captura.
- Errores base: `show interfaces counters errors` / `ethtool -S <iface> | grep -i "err\|crc\|drop"` → anotar valores. Sin baseline no hay forma de probar que la maniobra no empeoró nada.
- Monitoreo: captura Zabbix del puerto/equipo (valor + timestamp). Si Zabbix dice algo distinto al CLI → desconfiar de Zabbix (lección 15/11: Zabbix ciego).
- Etiquetas: leer ambos extremos del cable. Si no hay etiqueta → anotarlo como hallazgo, no improvisar.

**4. Maniobra — un cambio a la vez**
- Solo lo autorizado. Si en campo ves algo más roto → lo anotas, no lo tocas. Otro ticket, otra ventana.
- Un cambio a la vez: si reemplazas 4 cables (caso INC-002), es uno por uno con validación entre cada uno. Nunca los 4 a la vez.
- Paso a paso escrito ANTES de empezar, no durante. Si no lo escribiste, no lo tienes claro.
- Fibra: no halar del cable, usar seguro del conector. Respetar radio curvatura (OM3/OM4 ≈ 3 cm mínimo). Velcro, no bridas plásticas apretadas.
- Energía: shutdown controlado confirmado ANTES de tocar PDU. Encendido desde botón/interruptor del equipo, no desde PDU.

**5. Verificación — probar que quedó bien**
- Link UP + velocidad negociada correcta (comparar con pre-check).
- CRC/flaps en 0 o no creciendo durante 5 min mínimo.
- Lado remoto confirma: el vecino (servidor/switch) ve el link UP también. Un solo lado no es verificación.
- Monitoreo valida dato real: Zabbix/DCIM muestra el estado correcto DESPUÉS de la maniobra. Si sigue mostrando lo viejo → actualizar, no ignorar.
- Regla de oro: todo cambio físico de puerto exige validación lógica + monitoreo/DCIM el mismo día. Sin excepción.

**6. Registro — si no está escrito, no pasó**
- Ticket: qué se hizo, serial/PN viejo + nuevo, hora inicio-fin real, responsable.
- DCIM: ubicación, estado, serial actualizados el mismo día.
- Fotos antes/después cargadas (no en el celular, en el ticket o repo).
- Repuestos retirados → a bodega con acta, no al piso ni encima del rack. Cable dañado de evidencia → embolsado y etiquetado, no a la basura hasta cierre del caso.
- Etiquetado TIA-606 en ambos extremos del cable nuevo: `ORIGEN-RACK/U/PTO → DESTINO-RACK/U/PTO + fecha`.

**7. Lección — qué falló en el orden**
- Pregunta obligatoria al cerrar: ¿qué parte de los pasos 1-6 se saltó o se hizo a medias?
- No es "el cable estaba malo". Es "no validamos Zabbix antes" o "no pedimos ventana escrita".
- Cada lección alimenta este estándar (sección Mejoras pendientes) o un SOP específico.
- Métrica personal: si repites la misma lección 2 veces → el paso correspondiente necesita checklist propio.

### 5 prohibidos — por qué existen

1. **Apagar desde PDU sin shutdown controlado confirmado** — *Por qué:* corrompe filesystem, mata RAID en escritura, deja GPUs en estado inconsistente. *Caso:* 15/11 apagado total desde PDU. *Correcto:* shutdown por OS/iDRAC → confirmar apagado → recién ahí tocar PDU si es necesario.
2. **Mezclar UTP en organizadores de potencia** — *Por qué:* inducción electromagnética degrada señal, riesgo de calentamiento, imposible hacer tracing limpio. *Caso:* 15/11 UTP en potencia. *Correcto:* potencia por un lado, datos por otro. Siempre.
3. **Dejar repuestos tirados** — *Por qué:* se pierden seriales, se dañan conectores, nadie sabe si sirve o es basura. *Caso:* 15/11 repuestos sin gestión. *Correcto:* a bodega con acta el mismo turno, o embolsado + etiquetado como evidencia.
4. **Basura/comida en rack** — *Por qué:* atrae plagas, obstruye flujo de aire, riesgo de corto. *Caso:* servilletas dentro del rack 15/11. *Correcto:* nada que no sea fierro/cable dentro del rack. Punto.
5. **Cerrar turno sin entrega escrita** — *Por qué:* el siguiente turno opera a ciegas, repite diagnósticos, puede revertir tu fix. *Correcto:* hecho / pendiente / qué monitorear. Siempre, aunque "no pasó nada" (la ronda + entrega cuentan como evidencia).

### Mínimo medible por turno
- Inicio 15 min: leer entrega anterior + tickets + ronda visual (LEDs, ruido, temp, basura, cables) — foto si hay hallazgo
- Durante: 7 pasos siempre. Sin autorización escrita no se toca
- Cierre 15 min: tickets + DCIM al día, repuestos a bodega, fotos cargadas, entrega escrita (hecho / pendiente / monitorear)
- Métrica: turno perfecto = 0 prohibidos + 100% maniobras con 7 pasos + entrega escrita

## 1. Gestión (80% del cargo)

- [ ] Tickets al día: abiertos, en curso y cerrados con evidencia
- [ ] DCIM / inventario actualizado (serial, ubicación, estado)
- [ ] SOP/MOP leído y entendido ANTES de tocar fierros
- [ ] Ventana de mantenimiento validada antes de intervenir

## 2. Fierros (20% del cargo)

- [ ] Reemplazo FRU: disco, fuente, DIMM, ventilador
- [ ] Diagnóstico básico: POST, LEDs, SEL iDRAC/iLO, dmesg
- [ ] Validación post-cambio (ver checklist abajo)

## 3. RMA — flujo cuando toque

1. Apertura: serial, falla, logs, fotos → caso con fabricante
2. Tracking: # caso, SLA, estado
3. Recepción retorno: verificar serial/modelo/físico
4. Validación en cuarentena (NO directo a producción):
   - Encendido + POST limpio
   - iDRAC/iLO accesible + firmware estándar site
   - Discos/CPU/RAM visibles
   - Red link up
   - Sensores temp/voltaje en rango
   - Burn-in 2-4h + revisar logs (SEL, dmesg)
5. Si falla → reabrir caso con evidencia. Si pasa → programar ventana + commissioning

## 4. CLI mínimo

- [ ] SSH + PuTTY, IPMI/iDRAC/iLO
- [ ] Logs: `journalctl`, `dmesg`, SEL iDRAC
- [ ] Estado servicios + salud hardware por consola
- [ ] Red: ping, puertos switch, VLAN

## 5. Cierre obligatorio

Todo cambio deja: ticket + inventario + monitoreo actualizado.

---

# ✅ Checklist Commissioning Post-Mantenimiento

Usar cada vez que un equipo vuelve de RMA o se interviene.

## Físico
- [ ] Rack + rieles firmes
- [ ] Cableado potencia (doble fuente, PDU balanceada)
- [ ] Cableado datos (puertos correctos)
- [ ] Etiquetado TIA-606

## Energía
- [ ] Doble fuente activa
- [ ] Consumo esperado

## Gestión
- [ ] IPMI / iDRAC / iLO responde
- [ ] Credenciales estándar
- [ ] NTP + DNS OK
- [ ] Firmware en versión estándar del site

## Red
- [ ] Puertos en switch correcto (S4048/Z9664)
- [ ] VLAN correcta
- [ ] Ping + SSH OK

## Sistema
- [ ] SO / firmware versión estándar
- [ ] RAID sano
- [ ] Sin errores en logs (SEL, dmesg, journalctl)

## Monitoreo
- [ ] Aparece en DCIM
- [ ] Aparece en monitoreo + alertas configuradas

## Documentación y entrega
- [ ] Ticket cerrado: qué se hizo, serial, hora, responsable
- [ ] Inventario marcado como OPERATIVO
- [ ] Evidencia guardada (fotos/logs si aplica)

---

## 📌 Anexo: Lección 15/11 → 17/11 (MPO leaf)

Reportados puertos 5 y 7 caídos → falsos, estaban OK. Real: puertos 3-17 movidos antes sin gestión en switch → Zabbix ciego. Fierro quedó bien (peinado MPO, fracturas fuera, radios corregidos). Falló orden: PDU sin shutdown confirmado, sin ventana fija, repuestos tirados, UTP en potencia, sin paso a paso, entrega sin detalle, servilletas en rack.
Regla: todo cambio físico de puerto exige validación lógica + monitoreo/DCIM el mismo día.
Caso base de la disciplina operativa (origen 17/11, integrada 23/11).

---

## 📝 Mejoras pendientes (agregar con la práctica)
- [ ] Versiones firmware estándar del site (anotar cuando las tengas)
- [ ] Contactos / portal RMA por fabricante (Dell, HPE, etc.)
- [ ] Rack de cuarentena disponible (ubicación)
- [ ] Comandos exactos que uses en turno
