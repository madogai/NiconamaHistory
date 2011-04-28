from distutils.core import setup
import py2exe

py2exe_options = {
  'compressed': 1,
  'optimize': 2,
  'bundle_files': 2,
  'dist_dir': '../dist',
}

config_files = ('', [
    'niconama_history.conf',
    'logging.conf'
])

setup(
  options={'py2exe': py2exe_options},
  console=[{'script' : 'niconama_history.py'}],
  data_files=[config_files],
  zipfile=None
)
