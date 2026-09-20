# 🛟 Guía de Recuperación OpenClaw

> Si H.E.L.E.N. deja de responder en Telegram, seguir estos pasos en orden.
> Última actualización: 2026-09-20 | Versión base: `2026.9.5` (Node 26.9.0)

---

## 1. Esperar (2 min)

El servicio tiene auto-reinicio activado (`Restart=always`, 10 seg).
La mayoría de caídas se recuperan solas. Si en 2 minutos sigue sin responder, pasar al paso 2.

## 2. Entrar al servidor

Desde cualquier terminal con SSH (en iPhone usar la app **Termius**):

```bash
ssh root@204.168.135.114
```

## 3. Diagnóstico (en orden)

```bash
# ¿Está corriendo?
systemctl status openclaw.service --no-pager | head -n 15

# Ver últimos errores
journalctl -u openclaw.service -n 50 --no-pager

# Verificar versión y salud
openclaw --version
openclaw doctor
```

## 4. Reinicio manual

```bash
sudo systemctl restart openclaw.service
# Esperar 30 seg y probar en Telegram
```

## 5. Rollback (si una actualización rompió algo)

```bash
# Volver a la versión estable actual
npm install -g openclaw@2026.9.5

# Restaurar configuración (ajustar fecha al .bak más reciente)
cp ~/.openclaw/openclaw.json.bak-20260920 ~/.openclaw/openclaw.json

# Reiniciar
sudo systemctl restart openclaw.service
```

> ⚠️ Requisito: OpenClaw 2026.9.x exige **Node ≥24.16 o ≥26.1**.
> Si el rollback falla con error de engine, primero:
> `nvm install 26 && nvm use 26 && nvm alias default 26`

## 6. Ubicación de respaldos

| Qué | Dónde |
|-----|-------|
| Config actual | `~/.openclaw/openclaw.json` |
| Backups config | `~/.openclaw/openclaw.json.bak-*` |
| Snapshot completo | `~/openclaw-backup-*.tar.gz` |
| Workspace GitHub | `COPIA-openclaw` (rama `main`) |
| Vault Obsidian | Submódulo `obsidian-vault` (repo propio) |

## 7. Último recurso

Si ni SSH responde, el problema es el VPS (Hetzner), no OpenClaw.
Entrar al panel de **Hetzner Cloud** y hacer reboot desde la consola web.

---

### Push dual del vault (recordatorio)

```bash
# STEP 1: push del submódulo
cd /root/.openclaw/workspace/obsidian-vault && git add . && git commit -m "msg" && git push
# STEP 2: push del repo principal
cd /root/.openclaw/workspace && git add obsidian-vault && git commit -m "msg" && git push
```
