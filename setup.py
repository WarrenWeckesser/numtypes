from os.path import join


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('numtypes')
    config.add_subpackage('tests', 'numtypes')
    config.add_extension('numtypes._nint',
                         extra_compile_args=['-std=c99'],
                         sources=[join('src', '_nint.c.src')])

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(name='numtypes',
          version='0.0.1',
          configuration=configuration)
