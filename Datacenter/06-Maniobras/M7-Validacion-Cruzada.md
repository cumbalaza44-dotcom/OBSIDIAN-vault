# M7 — Validación cruzada monitor vs campo

> Origen: lección 15/11 (Zabbix ciego) + INC-002 (2.26 dB real vs reportado).
> Meta: mínimo 1 por turno. Cada discrepancia = 1 punto ciego menos.

## Procedimiento (5 min)
1. Elegir 1 dato: un puerto, un serial, un estado, una temp — lo que sea
2. Anotar lo que dice Zabbix/DCIM (valor + timestamp)
3. Ir al campo: CLI + LED + serial físico
4. ¿Coincide? Sí → registro rápido. No → hallazgo formal

## Registro
- Entrega General §4: dato monitor vs dato campo + foto si hay discrepancia
- Si es recurrente → proponer corrección de monitoreo o DCIM (dinamismo en equipo)

## Ejemplos
- Zabbix dice UP, CLI dice DOWN → hallazgo
- DCIM dice serial X en U10, campo dice serial Y → hallazgo + actualizar DCIM
- Zabbix dice temp normal, LED ámbar → hallazgo + escalar a facility
