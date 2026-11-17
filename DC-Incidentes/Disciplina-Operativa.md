# Disciplina Operativa — DC Hardware
Fecha: 2026-11-17 | Caso base: MPO NIC → leaf 15/11 + hallazgo 17/11

## 7 pasos obligatorios (toda maniobra)
1. Autorización — ticket / quién autoriza / ventana hora inicio-fin
2. Impacto — qué se afecta si sale mal, quién debe saber (NetOps, cómputo)
3. Pre-check — LEDs, link, errores, foto + captura monitoreo real
4. Maniobra — solo lo autorizado, un cambio a la vez, paso a paso escrito
5. Verificación — link UP, velocidad, CRC/flaps 5 min, lado remoto confirma + monitoreo valida dato real
6. Registro — ticket, DCIM, fotos antes/después, seriales/PNs, repuestos a bodega con acta
7. Lección — qué falló en el orden, no solo en el fierro

## 5 prohibidos
1. Apagar desde PDU sin shutdown controlado confirmado
2. Mezclar UTP en organizadores de potencia
3. Dejar repuestos tirados
4. Basura/comida en rack
5. Cerrar turno sin entrega escrita

## Mínimo medible por turno
- Inicio 15 min: leer entrega anterior + tickets + ronda visual (LEDs, ruido, temp, basura, cables) — foto si hay hallazgo
- Durante: 7 pasos siempre. Sin autorización escrita no se toca
- Cierre 15 min: tickets + DCIM al día, repuestos a bodega, fotos cargadas, entrega escrita (hecho / pendiente / monitorear)
- Métrica: turno perfecto = 0 prohibidos + 100% maniobras con 7 pasos + entrega escrita

## Lección 15/11 → 17/11 (MPO leaf)
Reportados puertos 5 y 7 caídos → falsos, estaban OK. Real: puertos 3-17 movidos antes sin gestión en switch → Zabbix ciego. Fierro quedó bien (peinado MPO, fracturas fuera, radios corregidos). Falló orden: PDU sin shutdown confirmado, sin ventana fija, repuestos tirados, UTP en potencia, sin paso a paso, entrega sin detalle, servilletas en rack.
Regla: todo cambio físico de puerto exige validación lógica + monitoreo/DCIM el mismo día.

## Links
- SOP detalle fierro: `sop-datacenter/SOP-01-cables.md` (fuera del vault, pendiente migrar)
