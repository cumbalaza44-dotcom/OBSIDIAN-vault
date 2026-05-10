---
created: 2026-05-05
tags: [indice, vault, dashboard]
updated: 2026-05-05 09:40
---

# 📚 VAULT INDEX — Dinámico

> **🔄 Actualización automática** — Dataview + Tasks integrados.  
> Cada que abras esta nota en Obsidian, los datos se refrescan solos.

---

```dataviewjs
// === ESTADÍSTICAS GENERALES ===
let all = dv.pages('').where(p => p.file.path != '_VAULT-INDEX.md' && !p.file.path.includes('.git/'));
let total = all.length;
let folders = new Set(all.map(p => p.file.folder));
let empty = all.where(p => dv.array(p.file.lines).length === 0);
let withTasks = all.where(p => dv.array(p.file.tasks).length > 0);
let completed = all.where(p => dv.array(p.file.tasks).where(t => t.completed).length > 0);

dv.paragraph(`📊 **${total}** notas · **${folders.size}** carpetas · **${empty.length}** vacías · **${withTasks.length}** con tareas`);
```

---

## 📂 Notas por carpeta

```dataview
TABLE 
  length(file.lines) AS "Líneas",
  file.etags AS "Tags",
  date(file.mtime) AS "Modificado"
FROM ""
WHERE file.name != "_VAULT-INDEX" AND !contains(file.path, ".git/")
SORT file.folder ASC, file.name ASC
```

---

## 🆕 Agregadas recientemente

```dataview
TABLE 
  file.folder AS "Carpeta",
  date(file.ctime) AS "Creada"
FROM ""
WHERE file.name != "_VAULT-INDEX" AND !contains(file.path, ".git/")
SORT file.ctime DESC
LIMIT 5
```

---

## 📝 Pendientes globales (Tasks)

```dataview
TASK FROM "" WHERE !completed
SORT created ASC
```

---

## 📄 Notas vacías (por rellenar)

```dataview
TABLE 
  file.folder AS "Carpeta",
  date(file.ctime) AS "Creada"
FROM ""
WHERE 
  file.name != "_VAULT-INDEX" AND 
  !contains(file.path, ".git/") AND
  length(file.lines) = 0
SORT file.folder ASC
```

---

## 🔗 Notas sin enlaces

```dataview
TABLE 
  file.folder AS "Carpeta",
  length(file.inlinks) AS "Entrantes",
  length(file.outlinks) AS "Salientes"
FROM ""
WHERE 
  file.name != "_VAULT-INDEX" AND 
  !contains(file.path, ".git/") AND
  length(file.outlinks) = 0 AND
  length(file.lines) > 0
SORT file.folder ASC
```

---

## 🏷️ Tags usados

```dataview
TABLE 
  rows.file.link AS "Notas"
FROM ""
WHERE !contains(file.path, ".git/")
FLATTEN file.tags AS tag
GROUP BY tag
SORT tag ASC
```

---

## 🗂️ Resumen por carpeta

```dataviewjs
let all = dv.pages('').where(p => p.file.path != '_VAULT-INDEX.md' && !p.file.path.includes('.git/'));
let groups = all.groupBy(p => p.file.folder);

dv.table(
  ["Carpeta", "Notas", "Líneas totales", "Vacías", "Con tareas"],
  groups.sort(g => g.key).map(g => {
    let notes = g.rows;
    let total_lines = notes.values.reduce((acc, n) => acc + (n.file.lines ? n.file.lines.length : 0), 0);
    let empty_count = notes.where(n => dv.array(n.file.lines).length === 0).length;
    let with_tasks = notes.where(n => dv.array(n.file.tasks).length > 0).length;
    return [g.key, notes.length, total_lines, empty_count, with_tasks];
  })
);
```

---

*Mantenido por J.A.R.V.I.S. — Se actualiza automáticamente al visualizar la nota en Obsidian con Dataview.*
