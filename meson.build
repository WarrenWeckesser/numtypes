project(
  'numtypes',
  'c',
  meson_version: '>= 1.1.0',
  default_options: [
    'c_std=c99',
  ]
)

py_mod = import('python')
py = py_mod.find_installation(pure: false)

message('Python is at ' + py.full_path())

cc = meson.get_compiler('c')

# Generate _version.py by reading the version from pyproject.toml.
custom_target(input : 'pyproject.toml',
              output : '_version.py',
              command : [
                py, '../_build_utils/make_version_file.py',
                '@INPUT@', '@OUTPUT@'
              ],
              install : true,
              install_dir : py.get_install_dir() / 'numtypes')

#----------------------------------------------------------------------
# Get the numpy include directory, and find the npymath library.
#----------------------------------------------------------------------

incdir_numpy = run_command(py,
  [
    '-c',
    'import numpy; print(numpy.get_include())'
  ],
  check: true
).stdout().strip()

message('NumPy include directory is ' + incdir_numpy)

includes = include_directories(
  [
    incdir_numpy,
  ],
)

npymath_path = incdir_numpy / '..' / 'lib'
npymath_lib = cc.find_library('npymath', dirs: npymath_path)


#----------------------------------------------------------------------
# Python source code to be installed.
#----------------------------------------------------------------------

py.install_sources(
  [
    'numtypes/__init__.py',
  ],
  subdir : 'numtypes',
)

py.install_sources(
  [
    'numtypes/tests/__init__.py',
    'numtypes/tests/test_logtypes.py',
    'numtypes/tests/test_nint32.py',
    'numtypes/tests/test_polarcomplex.py',
    'numtypes/tests/test_python_logfloat.py',
  ],
  subdir : 'numtypes/tests',
)

subdir('src')
