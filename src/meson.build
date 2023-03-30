
#----------------------------------------------------------------------
# nint build configuration
#----------------------------------------------------------------------

nint_c = custom_target(
    input : ['../tools/conv_template.py',
             '../src/_nint.c.src'],
    output : '_nint.c',
    command : [py, '@INPUT0@', '@INPUT1@', './src']
)

py.extension_module(
  '_nint',
  nint_c,
  install : true,
  subdir : 'numtypes',
  include_directories : includes,
  dependencies : [npymath_lib]
)

#----------------------------------------------------------------------
# polarcomplex extension module configuration
#----------------------------------------------------------------------

polarcomplex_c = custom_target(
    input : ['../tools/conv_template.py',
             '../src/_polarcomplex.c.src',],
    output : ['_polarcomplex.c'],
    command : [py, '@INPUT0@', '@INPUT1@', './src']
)

py.extension_module(
  '_polarcomplex',
  [polarcomplex_c, 'npy_2_complexcompat.h'],
  install : true,
  subdir : 'numtypes',
  include_directories : includes,
)

#----------------------------------------------------------------------
# logtypes extension module configuration
#----------------------------------------------------------------------

logtypes_c = custom_target(
    input : ['../tools/conv_template.py',
             'logtypes/_logtypes.c.src'],
    output : ['_logtypes.c'],
    command : [py, '@INPUT0@', '@INPUT1@', './src']
)

py.extension_module(
  '_logtypes',
  logtypes_c,
  install : true,
  subdir : 'numtypes',
  include_directories: includes,
)

#----------------------------------------------------------------------
# python_logtypes extension module configuration
#----------------------------------------------------------------------

python_logtypes_srcs = [
  'logtypes/_python_logtypes.c'
]

py.extension_module(
  '_python_logtypes',
  python_logtypes_srcs,
  install : true,
  subdir : 'numtypes',
  include_directories : includes,
)
