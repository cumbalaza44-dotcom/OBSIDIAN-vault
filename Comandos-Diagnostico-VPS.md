# Comandos de Diagnóstico VPS — Nodo Lento

> Ejercicio 1: diagnóstico de nodo lento. 4 bloques con comando Linux, explicación y equivalente Windows.

---

## Bloque 1 — Carga, memoria y disco

| Comando Linux | Explicación | Equivalente Windows |
|---|---|---|
| `uptime` | Muestra hace cuánto está encendido el equipo y la carga promedio (1, 5, 15 min). Carga alta = CPU saturada. | `systeminfo \| find "System Boot Time"` + Administrador de tareas → Rendimiento (PowerShell: `(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime`) |
| `free -h` | Muestra RAM total, usada, libre y swap en formato legible. Detecta falta de memoria. | `systeminfo \| find "Memory"` o PowerShell: `Get-CimInstance Win32_OperatingSystem \| Select TotalVisibleMemorySize, FreePhysicalMemory` |
| `df -h` | Muestra espacio libre en cada disco/partición. Detecta disco lleno. | `Get-PSDrive C` o CMD: `wmic logicaldisk get caption,freespace,size` |

---

## Bloque 2 — Procesos que consumen recursos

| Comando Linux | Explicación | Equivalente Windows |
|---|---|---|
| `ps aux --sort=-%cpu \| head -20` | Lista los 20 procesos que más CPU consumen. Detecta el culpable del lentitud. | PowerShell: `Get-Process \| Sort-Object CPU -Descending \| Select -First 20` |
| `ps aux --sort=-%mem \| head -20` | Lista los 20 procesos que más RAM consumen. | PowerShell: `Get-Process \| Sort-Object WorkingSet -Descending \| Select -First 20` |
| `top` / `htop` | Monitor interactivo en vivo de CPU, RAM y procesos. | Administrador de tareas (`taskmgr`) o PowerShell: `Get-Process` en bucle |

---

## Bloque 3 — Logs del sistema

| Comando Linux | Explicación | Equivalente Windows |
|---|---|---|
| `journalctl -p err -b` | Muestra errores del arranque actual. Detecta fallos de servicios o hardware. | Visor de eventos (`eventvwr.msc`) → Registros de Windows → Sistema |
| `journalctl -u <servicio> --since "1 hour ago"` | Muestra logs de un servicio específico de la última hora. | PowerShell: `Get-EventLog -LogName Application -Newest 50 -Source <nombre>` o `Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=(Get-Date).AddHours(-1)}` |
| `dmesg \| tail -50` | Muestra últimos 50 mensajes del kernel (hardware, drivers, disco). | PowerShell: `Get-WinEvent -LogName System -MaxEvents 50` |

---

## Bloque 4 — Red y conectividad

| Comando Linux | Explicación | Equivalente Windows |
|---|---|---|
| `ss -tuln` | Lista puertos TCP/UDP en escucha. Verifica qué servicios están expuestos. | CMD: `netstat -ano` o PowerShell: `Get-NetTCPConnection -State Listen` |
| `ping -c 4 8.8.8.8` | Envía 4 paquetes a Google DNS. Mide latencia y pérdida de paquetes. | CMD/PowerShell: `ping -n 4 8.8.8.8` |
| `mtr --report 8.8.8.8` / `traceroute 8.8.8.8` | Traza la ruta de red salto por salto. Detecta dónde se pierde latencia. | CMD: `tracert 8.8.8.8` o PowerShell: `Test-NetConnection 8.8.8.8 -TraceRoute` |
| `curl -o /dev/null -s -w "%{time_total}s" https://ejemplo.com` | Mide tiempo de respuesta HTTP de un sitio. | PowerShell: `Measure-Command { Invoke-WebRequest https://ejemplo.com }` |

---

## Bloque 5 — Direcciones IP (local y pública)

| Comando Linux | Explicación | Equivalente Windows |
|---|---|---|
| `ip -brief addr` | Muestra interfaces con su IP local de forma compacta. | PowerShell: `Get-NetIPAddress -AddressFamily IPv4 \| Select IPAddress, InterfaceAlias` |
| `hostname -I` | Muestra solo las IPs locales del equipo. | CMD: `ipconfig` (buscar IPv4) |
| `curl -s ifconfig.me` | Muestra la IP pública del VPS. | PowerShell: `(Invoke-WebRequest ifconfig.me).Content` |

---

## Resumen rápido

| Bloque | Qué diagnostica | Comando clave Linux | Comando clave Windows |
|---|---|---|---|
| 1 | Carga / RAM / disco | `uptime`, `free -h`, `df -h` | `systeminfo`, `Get-PSDrive` |
| 2 | Procesos top | `ps aux --sort=-%cpu` | `Get-Process \| Sort CPU -Desc` |
| 3 | Errores / logs | `journalctl -p err -b` | `eventvwr` / `Get-WinEvent` |
| 4 | Red / latencia | `ss -tuln`, `ping`, `mtr` | `netstat -ano`, `ping`, `tracert` |
| 5 | IP local / pública | `ip -brief addr`, `curl ifconfig.me` | `ipconfig`, `(iwr ifconfig.me).Content` |
