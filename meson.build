project(
    'gsas_ii',
    'c', 'cython', 'fortran',
    version: '2.0.0',
    license: 'BSD',
    meson_version: '>= 1.1.0',
    default_options : {
      'optimization': '2',
    },
)

# Seek the backend
if meson.backend() != 'ninja'
  error('Ninja backend required')
endif

# define some compilers
cc = meson.get_compiler('c')
cy = meson.get_compiler('cython')


m_dep = cc.find_library('m', required : false)
if m_dep.found()
  add_project_link_arguments('-lm', language : 'c')
endif

fc = meson.get_compiler('fortran')
if fc.get_id() == 'gcc'
  # add_global_arguments('-fcheck=bounds', language : 'fortran')
  add_global_arguments('-fno-range-check', language : 'fortran')
  add_global_arguments('-w', language : 'fortran')
endif


py = import('python').find_installation(pure: false)
py_dep = py.dependency()

# This is adopted from scipy's meson.build
#

# Uses the `numpy-config` executable (or a user's numpy.pc pkg-config file).
# Will work for numpy>=2.0, hence not required (it'll be a while until 2.0 is
# our minimum supported version). Using this now to be able to detect the
# version easily for >=2.0.
numpy_dep = dependency('numpy')
f2py_freethreading_arg = []
if numpy_dep.found()
  if numpy_dep.version().version_compare('>=2.1.0')
    f2py_freethreading_arg = ['--free-threading']
  endif
endif

# NumPy include directory - needed in all submodules
# The chdir is needed because within numpy there's an `import signal`
# statement, and we don't want that to pick up scipy's signal module rather
# than the stdlib module. The try-except is needed because when things are
# For cross-compilation it is often not possible to run the Python interpreter
# in order to retrieve numpy's include directory. It can be specified in the
# cross file instead:
#   [properties]
#   numpy-include-dir = /abspath/to/host-pythons/site-packages/numpy/core/include
#
# This uses the path as is, and avoids running the interpreter.
#
# We deliberately use an *absolute* numpy include path here (rather than the
# relative one that upstream scipy computes with os.path.relpath).  On Windows,
# a relative include path can become very long when the project is built in a
# deeply-nested location -- for example when GSAS-II is built as a pixi-build
# git dependency, where the source lives in the rattler git cache while numpy
# lives in the build's host prefix.  In that situation the relative `-I` path
# walks all the way up to a common ancestor and back down again, and the
# resulting path for deeply-included headers (e.g. numpy/_public_dtype_api_table.h,
# which is included from numpy/__multiarray_api.h) overflows the 260-character
# Windows MAX_PATH limit.  gcc then reports a spurious "No such file or
# directory" for a header that is actually present.  An absolute path keeps
# every include comfortably under MAX_PATH.
#
# `include_directories()` rejects absolute paths, so the numpy/f2py include
# directories are passed to the compiler directly as `-I` arguments below.
incdir_numpy = meson.get_external_property('numpy-include-dir', 'not-given')
if incdir_numpy == 'not-given'
  incdir_numpy = run_command(py,
    ['-c', 'import numpy; print(numpy.get_include())'],
    check: true
  ).stdout().strip()
endif

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'

# Don't use the deprecated NumPy C API. Define this to a fixed version instead of
# NPY_API_VERSION in order not to break compilation for released SciPy versions
# when NumPy introduces a new deprecation.
numpy_nodepr_api = ['-DNPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION']

# Absolute numpy/f2py include dirs, fed to the compiler as `-I` args to avoid
# the Windows MAX_PATH overflow described above.
numpy_inc_args = ['-I' + incdir_numpy, '-I' + incdir_f2py]

np_dep = declare_dependency(compile_args: numpy_nodepr_api + ['-I' + incdir_numpy])

fortranobject_c = incdir_f2py / 'fortranobject.c'


# Share this object across multiple modules.
fortranobject_lib = static_library('_fortranobject',
  fortranobject_c,
  c_args: numpy_nodepr_api + numpy_inc_args,
  dependencies: py_dep,
  gnu_symbol_visibility: 'hidden',
)
fortranobject_dep = declare_dependency(
  link_with: fortranobject_lib,
  compile_args: numpy_inc_args,
)




subdir('GSASII')
subdir('sources')
subdir('backcompat')
