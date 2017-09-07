# -*- mode: python -*-

block_cipher = None


a = Analysis(['WindowsHelper.py'],
             pathex=['E:\\Workspace\\1.自动化工具开发\\1.开发\\16.BTK4CMCC\\new'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WindowsHelper',
          debug=False,
          strip=False,
          upx=True,
          console=True )
