const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const appDir = __dirname;
const packageJsonPath = path.join(appDir, 'package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));

const appName = packageJson.name || 'BroserAuto';
const version = packageJson.version || '1.0.0';
const outDir = path.join(appDir, 'dist', `${appName}-v${version}`);

console.log(`\n  Iniciando build do ${appName} v${version}...\n`);

if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
}

/* Lista de arquivos e pastas a incluir no build */
const includes = [
    'server.js',
    'main.py',
    'package.json',
    'launcher_debug.bat',
    'launcher_script.ps1',
    'launcher_app.vbs',
    'renderer',
];

includes.forEach(item => {
    const src = path.join(appDir, item);
    const dest = path.join(outDir, item);
    if (fs.existsSync(src)) {
        if (fs.lstatSync(src).isDirectory()) {
            copyDir(src, dest);
            console.log(`  ✔ Pasta copiada: ${item}`);
        } else {
            fs.copyFileSync(src, dest);
            console.log(`  ✔ Arquivo copiado: ${item}`);
        }
    } else {
        console.log(`  ⚠ Aviso: ${item} nao encontrado`);
    }
});

/* Empacota com Electron (opcional: requer electron-builder) */
const electronPkgPath = path.join(appDir, 'node_modules', '.bin', 'electron-builder');
if (fs.existsSync(electronPkgPath + '.cmd') || fs.existsSync(electronPkgPath)) {
    console.log('\n  Empacotando com Electron...');
    try {
        execSync('npx electron-builder --win portable', {
            cwd: appDir,
            stdio: 'inherit',
        });
        console.log('  ✔ Build Electron concluido!');
    } catch (err) {
        console.log('  ⚠ Build Electron falhou (pode ignorar se quiser apenas os fontes)');
    }
} else {
    console.log('\n  ⚠ electron-builder nao encontrado. Build apenas com fontes.');
    console.log('  Para build Electron: npm install --save-dev electron-builder');
}

console.log(`\n  Build concluido em: ${outDir}\n`);

function copyDir(src, dest) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}
