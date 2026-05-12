---
created: 2026-05-12
tags: [hoy, dashboard, tareas, dinamico]
---

# 📋 Hoy

> **🔄 Actualización automática** — Tasks + Dataview integrados.  
> Abre esta nota en Obsidian y los datos se refrescan solos.

---

## ⏳ Pendientes

```tasks
due today
not done
group by filename
sort by priority
```

---

## ✅ Completadas hoy

```tasks
done today
group by filename
sort by done
```

---

## 📊 Resumen rápido

```dataview
TABLE 
  length(rows) AS "Cantidad"
FROM ""
WHERE !contains(file.path, ".git/") AND !contains(file.path, "_VAULT-")
FLATTEN file.tasks AS t
WHERE t.due = date(today) AND !t.completed
GROUP BY "Pendientes hoy"
```

---

*Dinámico vía Tasks + Dataview — Sin sincronización externa.*
