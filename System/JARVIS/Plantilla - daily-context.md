---
created: 2026-05-13
type: template-script
purpose: Generate System/JARVIS/daily-context.md
---



<%*
// ── RECOLECTOR DE CONTEXTO DIARIO ──
// Escanea todo el vault, recoge tareas del dia, estructura y modificados
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

// ── 1. Collect today's tasks ──
const pendingTasks = [];
const completedTasks = [];

for (const file of vaultFiles) {
    const content = await vault.read(file);
    const lines = content.split('\n');
    for (const line of lines) {
        const hasDate = line.includes(`📅 ${TODAY_STR}`) || line.includes(`📅${TODAY_STR}`);
        if (!hasDate) continue;
        
        if (/^\s*-\s*\[ \]/.test(line)) {
            const task = line.replace(/^\s*-\s*\[ \]\s*/, '').trim();
            pendingTasks.push(`- [ ] ${task}  — *${file.path}*`);
        } else if (/^\s*-\s*\[x\]/.test(line)) {
            const task = line.replace(/^\s*-\s*\[x\]\s*/, '').trim();
            completedTasks.push(`- [x] ${task}  — *${file.path}*`);
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
        const ds = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
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

content += `> 📊 **${vaultFiles.length}** notas — **${folderSet.size}** carpetas — **${pendingTasks.length}** pendientes hoy\n\n`;

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

// ── Directory tree ──
content += `## 📁 Estructura del vault\n\n`;
content += treeOutput + '\n';

// ── Recently modified ──
content += `## 🆕 Modificados recientemente\n`;
content += recentFiles.join('\n') + '\n\n';

content += `---\n`;
content += `*Generado: ${TODAY_SHORT} ${String(TODAY.getHours()).padStart(2,'0')}:${String(TODAY.getMinutes()).padStart(2,'0')} — Script Templater*\n`;

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
