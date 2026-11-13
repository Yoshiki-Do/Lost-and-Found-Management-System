
from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules


project_dir = Path(SPECPATH)

# Collect pywebview dependencies
webview_datas, webview_binaries, webview_hiddenimports = collect_all("webview")

# Collect dynamically imported modules
hidden_imports = (
    webview_hiddenimports
    + collect_submodules("uvicorn")
    + collect_submodules("sqlalchemy.dialects")
)

a = Analysis(
    ["desktop.py"],
    pathex=[str(project_dir)],
    binaries=webview_binaries,
    datas=[
        (str(project_dir / "app" / "templates"), "app/templates"),
        (str(project_dir / "app" / "static"), "app/static"),
    ] + webview_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="LostAndFound",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)
