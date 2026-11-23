# M5 — Energía busbar DC 50V + CDU

> Dónde: Power Shelf 33kW ×64 (32 left + 32 right, 6× PSU 5.5kW c/u) + CDU 250kW ×8.
> 64 × 33kW = 2.112 kW carga DC. 8 × 250kW = 2.000 kW frío (¡coincide!).

## Pre-check
- ¿Qué riel? Left / Right / ambos. Medir, no adivinar.
- PSUs presentes y LED por módulo (6 por shelf)
- CDU: temp ida/retorno, flujo, presión, bombas redundantes, SNMP/web
- Avisar a facility ANTES de tocar energía (dueños del sistema)

## Maniobra
- PSU shelf: hot-swap 1 módulo a la vez, verificar redundancia N antes
- Nunca mezclar UTP en organizadores de potencia (prohibido #2)
- Busbar DC: sin intervención sin MOP formal + facility presente

## Verificación
- [ ] Tensión 50V DC por riel + corriente balanceada L/R
- [ ] Todos los módulos PSU verdes
- [ ] CDU: temp/flujo/presión en rango, sin alarmas
- [ ] Ticket + aviso a facility con valores medidos
