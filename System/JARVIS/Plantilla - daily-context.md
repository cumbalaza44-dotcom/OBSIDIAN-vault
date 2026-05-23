---
created: 2026-05-13
modified: 2026-05-23
type: template-script
purpose: Generate System/JARVIS/daily-context.md
---



<%*
// ── RECOLECTOR DE CONTEXTO DIARIO ──
// Escanea todo el vault, recoge tareas del dia, atrasadas, malformateadas, estructura y modificados
// Escribe System/JARVIS/daily-context.md en markdown 100% plano
// Ejecutar desde paleta de comandos: Templater: Insert Template

const TODAY = new Date();
const yyyy = TODAY.getFullYear();
const mm = String(TODAY.getMonth() + 1).padStart(2, '0');
const dd = String(TODAY.getDate()).padStart(2, '0');
const TODAY_STR = `${yyyy}-${mm}-${dd}`;
const TODAY_SHORT = `${dd}/${mm}/${yyyy}`;

const vault = app.vault;
const vaultFiles = vault.getFiles()
    .filter(f => f.extension === 'md')
    .filter(f => !f.path.includes('.git/'))
    .filter(f => !f.path.includes('_VAULT-'))
    .filter(f => f.path !== 'Hoy.md')
    .filter(f => !f.path.startsWith('System/JARVIS/'))
    .sort((a, b) => a.path.localeCompare(b.path));

// ── Helpers ──
function parseTaskDate(line) {
    const m = line.match(/📅\s?(\d{4})-(\d{2})-(\d{2})/);
    if (!m) return null;
    return new Date(parseInt(m[1]), parseInt(m[2]) - 1, parseInt(m[3]));
}

function fmtDate(d) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// ── 1. Collect today's + overdue + malformed tasks ──
const pendingTasks = [];
const completedTasks = [];
const overdueTasks = [];
const malformedTasks = [];

const TODAY_MIDNIGHT = new Date(TODAY.getFullYear(), TODAY.getMonth(), TODAY.getDate());

// Standard format that Tasks plugin will recognize:
//   "descripción 📅 YYYY-MM-DD"
//   "descripción 📅 YYYY-MM-DD ⏫"
// Date must be at end (before emoji flags only), with space before 📅
// Accept: "desc 📅 YYYY-MM-DD" or "desc ⏰ HH:MM 📅 YYYY-MM-DD" (date at end)
const GOOD_DATE_RE = /(?:^|\s)(?:⏰\s*\d{1,2}:\d{2}\s+)?📅\s\d{4}-\d{2}-\d{2}(?:\s*[⏫🔽🔼✅⏰])*\s*$/;

for (const file of vaultFiles) {
    const content = await vault.read(file);
    const lines = content.split('\n');
    for (const line of lines) {
        const taskDate = parseTaskDate(line);
        if (!taskDate) continue;

        // Check format compliance for Tasks plugin
        if (!GOOD_DATE_RE.test(line.trim()) && line.trim().startsWith('- [')) {
            const hasSpaceBefore = /\s📅/.test(line) || /^\s*-\s*\[ ?\]\s*📅/.test(line);
            const hasSpaceAfter = /📅\s\d/.test(line);
            const dateAtEnd = /📅\s\d{4}-\d{2}-\d{2}\s*$/.test(line) ||
                              /📅\s\d{4}-\d{2}-\d{2}\s*[⏫🔽🔼✅⏰]/.test(line);
            if (!hasSpaceBefore || !hasSpaceAfter || !dateAtEnd) {
                malformedTasks.push(`- ${file.path}: \`${line.trim().substring(0, 80)}\``);
            }
        }

        const isToday = taskDate.getTime() === TODAY_MIDNIGHT.getTime();
        const isOverdue = taskDate.getTime() < TODAY_MIDNIGHT.getTime();
        const isChecked = /^\s*-\s*\[x\]/.test(line);

        if (isToday) {
            if (isChecked) {
                const task = line.replace(/^\s*-\s*\[x\]\s*/, '').trim();
                completedTasks.push(`- [x] ${task}  — *${file.path}*`);
            } else {
                const task = line.replace(/^\s*-\s*\[ \]\s*/, '').trim();
                pendingTasks.push(`- [ ] ${task}  — *${file.path}*`);
            }
        } else if (isOverdue && !isChecked) {
            const task = line.replace(/^\s*-\s*\[ \]\s*/, '').trim();
            overdueTasks.push(`- [ ] ${task}  — *${file.path}* *(📅 ${fmtDate(taskDate)})*`);
        }
    }
}

// ── 2. Build directory tree ──
function buildTree(files) {
    const tree = {};

    for (const f of files) {
        const parts = f.path.replace(/\.md$/, '').split('/');
        let current = tree;
        for (let i = 0; i < parts.length - 1; i++) {
            if (!current[parts[i]]) current[parts[i]] = { _files: [] };
            current = current[parts[i]];
        }
        const lastName = parts[parts.length - 1];
        if (!current._files) current._files = [];
        current._files.push(lastName);
    }
    return tree;
}

function renderTree(node, indent) {
    let output = '';
    const keys = Object.keys(node).filter(k => k !== '_files').sort();
    const files = (node._files || []).sort();
    const total = files.length + keys.length;
    let idx = 0;

    for (const k of keys) {
        idx++;
        const isLast = idx === total;
        const prefix = isLast ? '└──' : '├──';
        output += `${indent}${prefix} 📁 ${k}/\n`;
        const deeper = indent + (isLast ? '    ' : '│   ');
        output += renderTree(node[k], deeper);
    }

    for (let i = 0; i < files.length; i++) {
        idx++;
        const isLast = idx === total;
        const prefix = isLast ? '└──' : '├──';
        output += `${indent}${prefix} ${files[i]}.md\n`;
    }

    return output;
}

const tree = buildTree(vaultFiles);
const treeOutput = renderTree(tree, '');

// ── 3. Recently modified (top 5) ──
const recentFiles = vaultFiles
    .sort((a, b) => b.stat.mtime - a.stat.mtime)
    .slice(0, 5)
    .map(f => {
        const d = new Date(f.stat.mtime);
        const ds = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        return `- ${f.path} — *${ds}*`;
    });

// ── 4. Build content ──
let content = '';
content += `# 📋 Contexto Diario — ${TODAY_SHORT}\n\n`;

const folderSet = new Set();
for (const f of vaultFiles) {
    const dir = f.parent?.path || '';
    if (dir) folderSet.add(dir);
}

content += `> 📊 **${vaultFiles.length}** notas — **${folderSet.size}** carpetas — **${pendingTasks.length}** pendientes hoy — **${overdueTasks.length}** atrasadas`;
if (malformedTasks.length > 0) content += ` — ⚠️ **${malformedTasks.length}** con formato incorrecto`;
content += `\n\n`;

// ── Today's tasks ──
content += `## 🏋️ Tareas de hoy\n\n`;
if (pendingTasks.length === 0 && completedTasks.length === 0) {
    content += `*Sin tareas programadas para hoy.* 🎯\n\n`;
} else {
    if (pendingTasks.length > 0) {
        content += `### ⏳ Pendientes\n`;
        content += pendingTasks.join('\n') + '\n\n';
    }
    if (completedTasks.length > 0) {
        content += `### ✅ Completadas\n`;
        content += completedTasks.join('\n') + '\n\n';
    }
}

// ── Overdue tasks ──
if (overdueTasks.length > 0) {
    content += `## ⚠️ Tareas atrasadas\n\n`;
    overdueTasks.sort();
    content += overdueTasks.join('\n') + '\n\n';
}

// ── Malformed tasks ──
if (malformedTasks.length > 0) {
    content += `## ❌ Tareas con formato de fecha incorrecto\n\n`;
    content += `Estas tareas tienen \`📅\` pero el formato no es compatible con el plugin Tasks. `;
    content += `Edítalas para que la fecha esté al final: \`descripción 📅 YYYY-MM-DD\`\n\n`;
    malformedTasks.sort();
    content += malformedTasks.join('\n') + '\n\n';
}

// ── Directory tree ──
content += `## 📁 Estructura del vault\n\n`;
content += treeOutput + '\n';

// ── Recently modified ──
content += `## 🆕 Modificados recientemente\n`;
content += recentFiles.join('\n') + '\n\n';

content += `---\n`;
content += `*Generado: ${TODAY_SHORT} ${String(TODAY.getHours()).padStart(2, '0')}:${String(TODAY.getMinutes()).padStart(2, '0')} — Script Templater*\n`;

// ── 5. Write to file ──
const targetPath = 'System/JARVIS/daily-context.md';
const existingFile = vault.getAbstractFileByPath(targetPath);

if (existingFile) {
    await vault.modify(existingFile, content);
} else {
    const dirPath = 'System/JARVIS/';
    const existingDir = vault.getAbstractFileByPath(dirPath);
    if (!existingDir) {
        await vault.createFolder(dirPath);
    }
    const f = vault.getFileByPath(targetPath);
    if (f) {
        await vault.modify(f, content);
    } else {
        await vault.create(targetPath, content);
    }
}

// ── Notify user ──
new Notice('✅ daily-context.md generado — ' + TODAY_SHORT);
%>