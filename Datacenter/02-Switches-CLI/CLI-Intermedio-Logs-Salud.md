---
created: 2026-11-24
tags: [datacenter, CLI, logs, diagnostico, switches, servidores, BMC]
---

# 🖥️ CLI Intermedio — Logs + Salud de Hardware

> **Nivel:** Ya dominas lo básico (status, version, logs simples). Esto es el siguiente nivel: leer salud del hardware por consola sin tocar fierros.
> **Principio:** Todo lo que puedas saber por CLI, no lo adivines en campo.

---

## 1. Switches — Diagnóstico profundo

### Salud del sistema

```bash
show environment          # Temp, voltaje, fans, PSU — todo en uno
show environment fan      # Detalle fans (RPM por unidad)
show environment power    # Detalle PSU (input/output watts, estado)
show environment thermal  # Sensores temperatura por zona
show system               # Uptime, memoria, CPU del switch
show processes cpu        # Si CPU alta → qué proceso la consume
```

### Logs e historial

```bash
show logs                 # Buffer general (últimos eventos)
show logs | grep -i "error\|fail\|down\|crc"   # Solo problemas
show interfaces counters errors                # CRC + drops por puerto
show interfaces <puerto> counters               # Detalle un puerto
clear counters <puerto>                         # Resetear para medir desde cero
# ...esperar 5 min...
show interfaces <puerto> counters               # ¿siguen creciendo?
```

### Vecinos y topología

```bash
show lldp neighbors       # Qué hay conectado en cada puerto
show lldp neighbors detail # + modelo, firmware, IP del vecino
show mac-address-table    # Qué MACs ve por puerto (útil si DCIM miente)
show vlan brief           # VLANs configuradas
show port-channel summary # LAGs y su estado
```

### Cuándo preocuparse (umbrales)

| Métrica | Normal | Alerta | Crítico |
|---------|--------|--------|---------|
| Temp switch | <45°C | 45-60°C | >60°C |
| CPU switch | <30% | 30-70% | >70% sostenido |
| CRC errores | 0 | Creciendo lento | Creciendo rápido |
| Flaps (24h) | 0 | 1-3 | >3 |
| Fan RPM | Nominal ±10% | Una fan en 0 | 2+ fans en 0 |
| PSU | Todas OK | 1 en alerta | 1 caída (sin redundancia) |

---

## 2. Servidores — Salud por BMC/iDRAC

### IPMI (genérico, cualquier BMC)

```bash
ipmitool sdr                    # Todos los sensores (temp, volt, fan)
ipmitool sdr type Temperature    # Solo temperaturas
ipmitool sdr type Fan            # Solo fans
ipmitool sel list                # System Event Log (errores hardware)
ipmitool sel list last 20        # Últimos 20 eventos
ipmitool mc info                 # Firmware BMC + versión
ipmitool chassis status          # Estado power + último evento
ipmitool sensor thresh <id>      # Umbrales de un sensor
```

### Linux (dentro del servidor)

```bash
# Hardware general
dmidecode -s system-serial-number  # Serial (para validar DCIM)
dmidecode -t memory                 # DIMMs instalados por slot
lscpu                              # CPU modelo + cores
lsblk                              # Discos visibles
nvme list                          # NVMe específicos
lspci | grep -i "nvidia\|mellanox"  # GPUs + NICs

# Salud
dmesg | grep -i "error\|fail\|warn" | tail -30   # Errores kernel
journalctl -p err -b                             # Errores desde boot
nvidia-smi                                       # GPUs: temp, power, uso, throttling
nvidia-smi -q -d TEMPERATURE,POWER                # Detalle temp/power
ethtool <iface>                                  # Link, velocidad, duplex
ethtool -S <iface> | grep -i "err\|crc\|drop"    # Errores NIC
sensors                                          # Temp CPU/board (si lm-sensors)
uptime                                           # Uptime + load average
```

### Umbrales servidor

| Métrica | Normal | Alerta | Crítico |
|---------|--------|--------|---------|
| CPU temp | <70°C | 70-85°C | >85°C |
| GPU temp | <75°C | 75-87°C | >87°C (throttling) |
| DIMM errores | 0 | ECC corregibles | ECC no corregibles |
| NVMe temp | <60°C | 60-70°C | >70°C |
| Load average | < cores | = cores × 1.5 | > cores × 2 |
| Disk errors (dmesg) | 0 | I/O warnings | Read-only remount |

---

## 3. Rutina CLI por turno (10 min)

```bash
# 1. Switch principal del área (2 min)
show environment | grep -i "alarm\|fail\|critical"
show interfaces counters errors | grep -v " 0 "

# 2. Un servidor del rack del día (3 min)
ipmitool sel list last 10
ipmitool sdr type Temperature

# 3. Validación cruzada (5 min)
# Comparar lo que dice Zabbix vs lo que dice el CLI
# Si difieren → hallazgo (Zabbix ciego)
```

---

## 4. Comandos que NO debes correr sin autorización

| Comando | Por qué es peligroso |
|---------|---------------------|
| `reload` / `reboot` | Reinicia el switch — tumba todo |
| `clear logs` | Borra evidencia |
| `write erase` | Borra configuración |
| `firmware upgrade` | Sin ventana = suicidio |
| `shutdown <puerto>` | Tumba link en producción |
| `ipmitool chassis power off` | Apaga servidor remoto |
| `dd`, `mkfs`, `fdisk` | Destruyen datos |

---

<div align="center">

`🦾 CLI intermedio: lee la salud sin tocar fierros.`

</div>
