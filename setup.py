from Cython.Distutils import build_ext
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup

import os
import sys


install_requires = [
    'cffi',
    'chainer >=1.23, !=2.0.0a1, !=2.0.0b1',
    'cython',
    'mpi4py',
]

ext_include_dirs = []
ext_library_dirs = []
if 'CUDA_HOME' in os.environ:
    ext_include_dirs.append(os.path.join(os.environ['CUDA_HOME'], 'include'))
    ext_library_dirs.append(os.path.join(os.environ['CUDA_HOME'], 'lib64'))

if 'NCCL_ROOT' in os.environ:
    ext_include_dirs.append(os.path.join(os.environ['NCCL_ROOT'], 'build/include'))
    ext_library_dirs.append(os.path.join(os.environ['NCCL_ROOT'], 'build/lib'))


ext_modules = [
    Extension(
        name='chainermn.nccl.nccl',
        sources=['chainermn/nccl/nccl.pyx'],
        libraries=['nccl'],
        include_dirs=ext_include_dirs,
        library_dirs=ext_library_dirs)
]

if '--no-nccl' in sys.argv:
    sys.argv.remove('--no-nccl')
    ext_modules = []
elif os.environ.get('READTHEDOCS', None) == 'True':
    ext_modules = []
    install_requires.remove('mpi4py')  # mpi4py cannot be installed without MPI

setup(
    name='chainermn',
    version='1.0.0b2',
    description='ChainerMN: Multi-node distributed training with Chainer',
    author='Takuya Akiba',
    author_email='akiba@preferred.jp',
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    install_requires=install_requires
)
