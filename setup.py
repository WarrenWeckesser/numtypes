from os.path import join


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_info

    compile_args = ['-std=c99', '-Werror']
    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('numtypes')
    config.add_subpackage('numtypes/tests')
    config.add_extension('numtypes._nint',
                         extra_compile_args=['-std=c99'],
                         sources=[join('src', '_nint.c.src')],
                         **get_info("npymath"))
    config.add_extension('numtypes._complex_int',
                         extra_compile_args=['-std=c99'],
                         sources=[join('src', '_complex_int.c.src')],
                         **get_info("npymath"))
    config.add_extension('numtypes._polarcomplex',
                         extra_compile_args=['-std=c99'],
                         sources=[join('src', '_polarcomplex.c.src')])
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(name='numtypes',
          version='0.0.2.dev0',
          configuration=configuration)
