# M8 — Rack línea base (proactivo)

> 74 racks: GR 24, NR 36, NW 8, MMR 6. Meta: 1 rack/turno tranquilo → DC mapeado en ~15 turnos.
> Usa: `Datacenter/05-Turnos/Ficha-Rack-Template.md`.

## Procedimiento
1. Elegir rack (priorizar: GPU + fabric + power shelf juntos = mayor criticidad)
2. Llenar ficha: equipos por U, seriales, LEDs, energía A/B, datos origen→destino, etiquetas
3. Validación cruzada incluida: DCIM dice vs campo dice, Zabbix dice vs CLI dice
4. Fotos: panorámica + hallazgos + etiquetas
5. Hallazgos útiles → Entrega General §5 (cómputo/facility/fibra)

## Progreso acumulado
- Racks documentados: ___/74
- Faltantes críticos (GPU+fabric+shelf): ___

## Regla
Turno sin incidentes = turno M8 + M7 + ronda con foto. Nunca turno vacío.
