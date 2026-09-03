from PyInstaller.utils.hooks import collect_submodules


a = Analysis(
    ["main.py"],
    pathex=["."],
    hiddenimports=collect_submodules("requests"),
    datas=[],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, name="formulaforge-backend", console=False)
