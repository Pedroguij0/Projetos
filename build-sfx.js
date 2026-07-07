const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const sevenZipDir = path.join(process.env.TEMP, '7z');
const distDir = path.join(__dirname, 'dist');
const appDir = path.join(distDir, 'BroserAuto-win32-x64');
const sfxModule = path.join(sevenZipDir, '7z.sfx');
const archivePath = path.join(distDir, 'app.7z');
const configPath = path.join(distDir, 'app.conf');
const outputPath = path.join(distDir, 'BroserAuto.exe');

const config = `;!@Install@!UTF-8!
Title="BroserAuto"
ExtractDialogText="Extraindo BroserAuto..."
RunProgram="BroserAuto-win32-x64\\BroserAuto.exe"
;!@InstallEnd@!
`;

if (!fs.existsSync(appDir)) {
  console.error('App directory not found. Run npm run pack first.');
  process.exit(1);
}

if (!fs.existsSync(sevenZipDir) || !fs.existsSync(sfxModule)) {
  console.error('7zip not found at', sevenZipDir);
  process.exit(1);
}

console.log('Creating 7z archive...');
execSync(`"${path.join(sevenZipDir, '7z.exe')}" a -t7z -mx=9 "${archivePath}" "${appDir}"`, { stdio: 'pipe' });

console.log('Creating SFX config...');
fs.writeFileSync(configPath, config, 'utf8');

console.log('Building BroserAuto.exe...');
execSync(`cmd /c "copy /b "${sfxModule}" + "${configPath}" + "${archivePath}" "${outputPath}" > nul 2>&1"`);

const stats = fs.statSync(outputPath);
console.log(`Done! BroserAuto.exe (${(stats.size / 1024 / 1024).toFixed(0)} MB) created at dist/BroserAuto.exe`);

fs.unlinkSync(archivePath);
fs.unlinkSync(configPath);
