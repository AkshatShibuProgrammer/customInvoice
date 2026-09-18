import os
import re

def enhance_dashboard(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for folder-path-strip
    pattern_strip = re.compile(
        r'<div class="folder-path-strip">.*?<div class="folder-path-text" id="dispFolderPath">.*?</div>.*?<a id="btnOpenFolder".*?</a>\s*</div>',
        re.DOTALL
    )

    new_strip = '''<div class="folder-path-strip">
          <div style="flex: 1; min-width: 220px;">
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--text-dim);">Directory Location:</div>
            <div class="folder-path-text" id="dispFolderPath">Dates/10Aug/</div>
          </div>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center;">
            <button id="btnCopyPath" type="button" class="btn" onclick="copyFolderPath()" title="Copy folder path to clipboard">
              📋 Copy Path
            </button>
            <button id="btnOpenExplorer" type="button" class="btn btn-primary" onclick="launchExplorerBat()" title="Open this folder directly in Windows File Explorer">
              ⚡ Open in File Explorer
            </button>
            <a id="btnOpenFolder" href="Dates/10Aug/" target="_blank" class="btn" title="Open directory in browser tab">
              📂 View in Browser
            </a>
          </div>
        </div>'''

    content, n = pattern_strip.subn(new_strip, content)
    print(f"{os.path.basename(file_path)}: replaced strip = {n}")

    # Inject helper scripts before </script>
    if 'function launchExplorerBat()' not in content:
        helper_code = '''
let currentActiveDate = '10Aug';

function copyFolderPath() {
  const relPath = document.getElementById('dispFolderPath').textContent.trim();
  let fullPath = decodeURIComponent(window.location.pathname);
  if (fullPath.startsWith('/') && fullPath.charAt(2) === ':') fullPath = fullPath.substring(1);
  const lastSlash = Math.max(fullPath.lastIndexOf('/'), fullPath.lastIndexOf('\\\\'));
  const baseDir = lastSlash !== -1 ? fullPath.substring(0, lastSlash + 1) : '';
  const resolved = (baseDir + relPath).replace(/\\//g, '\\\\');
  
  navigator.clipboard.writeText(resolved).then(() => {
    const btn = document.getElementById('btnCopyPath');
    const orig = btn.innerHTML;
    btn.innerHTML = '✓ Copied!';
    setTimeout(() => { btn.innerHTML = orig; }, 1800);
  }).catch(() => {
    prompt('Copy folder path to clipboard:', resolved);
  });
}

function launchExplorerBat() {
  const relPath = document.getElementById('dispFolderPath').textContent.trim();
  let fullPath = decodeURIComponent(window.location.pathname);
  if (fullPath.startsWith('/') && fullPath.charAt(2) === ':') fullPath = fullPath.substring(1);
  const lastSlash = Math.max(fullPath.lastIndexOf('/'), fullPath.lastIndexOf('\\\\'));
  const baseDir = lastSlash !== -1 ? fullPath.substring(0, lastSlash + 1) : '';
  const resolved = (baseDir + relPath).replace(/\\//g, '\\\\');
  
  // Creates a lightweight launcher that opens Windows File Explorer directly to this date's folder
  const batText = `@echo off\\r\\nstart "" explorer.exe "${resolved}"\\r\\nexit\\r\\n`;
  const blob = new Blob([batText], { type: 'application/x-bat' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `open_${currentActiveDate}_folder.bat`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
'''
        # Hook tracking into selectDate
        content = content.replace("function selectDate(dateKey) {", "function selectDate(dateKey) {\n  currentActiveDate = dateKey;")
        content = content.replace("</script>", helper_code + "\n</script>")
        print(f"{os.path.basename(file_path)}: injected helper script")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    enhance_dashboard(r'f:\Code by Akshat\testgemini\customizable-invoice-generator-webpage (2)\akshat-reimbursement.html')
    enhance_dashboard(r'f:\Code by Akshat\testgemini\customizable-invoice-generator-webpage (2)\mayank-reimbursement.html')
