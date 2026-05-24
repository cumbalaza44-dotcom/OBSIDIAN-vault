---
created: 2026-05-12
modified: 2026-05-23
tags:
  - hoy
  - dashboard
  - tareas
  - dinamico
---

# 📋 Panóptico de Tareas

> **🔄 Actualización automática** — Tasks + Dataview integrados.  
> Abre esta nota en Obsidian y los datos se refrescan solos.

---

## ⚠️ Atrasadas (vencieron antes de hoy)

```tasks
due before today
not done
group by filename
sort by due reverse
```

---

## ⏳ Hoy

```tasks
due today
not done
group by filename
sort by priority
```

## 🔮 Próximas (vencen en los próximos 7 días)

```tasks
due after today
due before in 7 days
not done
group by filename
sort by due
```

---

## ✅ Completadas hoy

```tasks
done today
group by filename
sort by done
```

---

## 📦 Sin fecha

```tasks
no due date
not done
group by filename
```

---

## 📊 Resumen

```dataviewjs
const pending = dv.pages("").file.tasks
  .where(t => !t.completed && t.due);

const today = new Date();
today.setHours(0, 0, 0, 0);

const overdue = pending.where(t => t.due?.ts && t.due.ts < today);
const todayTasks = pending.where(t => t.due?.ts && t.due.ts === today);
const upcoming = pending.where(t => t.due?.ts && t.due.ts > today && t.due.ts <= (today + 7*86400000));

dv.paragraph(`> 🗂️ **${dv.pages("").length}** notas — ${overdue.length} atrasadas — ${todayTasks.length} hoy — ${upcoming.length} próximas — ${pending.where(t => !t.due).length} sin fecha`);
```

---

*Panel dinámico vía Tasks + Dataview.*

