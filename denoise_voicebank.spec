# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define the added_files list
added_files = [
    ('sillaypilled.mp3', '.'),  # Include the music file in the same folder as the executable
    ('icon.ico', '.'),          # Include the icon file in the same folder as the executable
]

a = Analysis(
    ['denoise_voicebank.py'],
    pathex=['C:\\Users\\chope\\Desktop\\sillay_denoiser_portable'],
    binaries=[],
    datas=added_files,  # Use the added_files list directly (no square brackets)
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='denoise_voicebank',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Set the icon for the executable
)