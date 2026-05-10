# Restauración del Sync Inteligente — Obsidian Vault
# Si el servidor se reinicia o el workspace se pierde:
# 1. Clonar el repo
# 2. Instalar inotify-tools
# 3. Cargar crontab
# 4. Cargar servicio systemd

## 1. Instalar dependencia
```bash
apt-get install -y inotify-tools
```

## 2. Restaurar crontab
```bash
crontab _INFRA-crontab.txt
```

## 3. Restaurar servicio systemd
```bash
cp _INFRA-watcher.service /etc/systemd/system/obsidian-watcher.service
systemctl daemon-reload
systemctl enable --now obsidian-watcher.service
```

## 4. Verificar
```bash
crontab -l                     # Debe mostrar 2 cron jobs
systemctl status obsidian-watcher  # Debe estar active (running)
```

---

*Generado por J.A.R.V.I.S. — 2026-05-06*
