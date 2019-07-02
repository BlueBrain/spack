# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    version('master', branch='master')
    version('1.2.0-stable', branch='release-1.2')
    version('1.2.0-rc1', sha256='e301421b869c6ecea8c3ae06bfdddf67843d16e694973b4958924914249afa46')
    version('1.1.1', sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')

    # TODO: Split these out into jl-hdf5, jl-mpi packages etc.
    variant("cxx", default=False, description="Prepare for Julia Cxx package")
    variant("hdf5", default=False, description="Install Julia HDF5 package")
    variant("mpi", default=True, description="Install Julia MPI package")
    variant("plot", default=False,
            description="Install Julia plotting packages")
    variant("python", default=False,
            description="Install Julia Python package")
    variant("simd", default=False, description="Install Julia SIMD package")

    variant('binutils', default=sys.platform != 'darwin',
            description="Build via binutils")

    # Build-time dependencies:
    depends_on("m4", type="build")
    depends_on("pkgconfig")

    # Combined build-time and run-time dependencies:
    # (Yes, these are run-time dependencies used by Julia's package manager.)
    depends_on("binutils", when='+binutils')
    depends_on("cmake @2.8:")
    depends_on("git")
    depends_on("openssl")
    depends_on("python")

    depends_on("llvm+link_dylib@7:")

    # Run-time dependencies:

    # depends_on("blas")
    # depends_on("lapack")

    depends_on("pcre2")
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("suite-sparse")

    # depends_on("libuv")
    depends_on("curl")
    depends_on("libgit2")
    # depends_on("libm")
    # depends_on("libxml2")
    # # depends_on("lzma")
    # depends_on("ncurses")
    # depends_on("zlib")


    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    # Run-time dependencies for Julia packages:
    depends_on("hdf5", when="+hdf5", type=("build", "run"))
    depends_on("mpi", when="+mpi", type=("build", "run"))
    depends_on("py-matplotlib", when="+plot", type=("build", "run"))

    # def setup_environment(self, spack_env, run_env):
    #     import pdb
    #     pdb.set_trace()

    def install(self, spec, prefix):
        # Julia needs git tags
        if os.path.isfile(".git/shallow"):
            git = which("git")
            git("fetch", "--unshallow")
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly.
        options = [
            "USE_BINARYBUILDER=0",
            "USE_SYSTEM_LLVM=1",
            "USE_SYSTEM_PCRE=1",
            "USE_SYSTEM_LIBM=1",
            # "USE_SYSTEM_BLAS=1",
            # "USE_SYSTEM_LAPACK=1",
            "USE_SYSTEM_GMP=1",
            "USE_SYSTEM_MPFR=1",
            "USE_SYSTEM_SUITESPARSE=1",
            # "USE_SYSTEM_LIBUV=1",
            "USE_SYSTEM_CURL=1",
            "USE_SYSTEM_LIBGIT2=1",
            # "# LIBBLAS={0}".format(spec["blas"].libs),
            # "LIBBLASNAME={0}".format(spec["blas"].name),
            # "# LIBLAPACK={0}".format(spec["lapack"].libs),
            # "LIBLAPACKNAME={0}".format(spec["lapack"].name),
            "prefix={0}".format(prefix)
        ]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        make()
        make("install")

        # Julia's package manager needs a certificate
        cacert_dir = join_path(prefix, "etc", "curl")
        mkdirp(cacert_dir)
        cacert_file = join_path(cacert_dir, "cacert.pem")
        curl = which("curl")
        curl("--create-dirs",
             "--output", cacert_file,
             "https://curl.haxx.se/ca/cacert.pem")

        # Put Julia's compiler cache into a private directory
        cachedir = join_path(prefix, "var", "julia", "cache")
        mkdirp(cachedir)

        # Store Julia packages in a private directory
        pkgdir = join_path(prefix, "var", "julia", "pkg")
        mkdirp(pkgdir)

        juliarc = join_path(prefix, "etc", "julia", "startup.jl")

        # Configure Julia
        with open(juliarc, "a") as fd:
            if not spec.satisfies("@1:") and \
                    ("@master" in spec or "@release-0.5" in spec or "@0.5:" in spec):
                # This is required for versions @0.5:
                fd.write('# Point package manager to working certificates\n')
                fd.write('LibGit2.set_ssl_cert_locations("%s")\n' % cacert_file)
                fd.write('\n')
            # fd.write('# Put compiler cache into a private directory\n')
            # fd.write('empty!(Base.LOAD_CACHE_PATH)\n')
            # fd.write('unshift!(Base.LOAD_CACHE_PATH, "%s")\n' % cachedir)
            # fd.write('\n')
            fd.write('# Put Julia packages into a private directory\n')
            fd.write('empty!(DEPOT_PATH)\n')
            fd.write('push!(DEPOT_PATH, "{0}")\n'.format(pkgdir))
            fd.write('\n')

        # Install some commonly used packages
        julia = spec['julia'].command
        julia("-e", 'using Pkg; Pkg.update()')

        def pkg_add(name):
            julia("-e", 'using Pkg; Pkg.add("{0}"); using {0}'.format(name))

        # Install HDF5
        if "+hdf5" in spec:
            with open(juliarc, "a") as fd:
                fd.write('# HDF5\n')
                fd.write('push!(Libdl.DL_LOAD_PATH, "%s")\n' % spec["hdf5"].prefix.lib)
                fd.write('\n')
            pkg_add("HDF5")
            pkg_add("JLD")

        # Install MPI
        if "+mpi" in spec:
            with open(juliarc, "a") as fd:
                fd.write('# MPI\n')
                fd.write('ENV["JULIA_MPI_C_COMPILER"] = "%s"\n' %
                         join_path(spec["mpi"].prefix.bin, "mpicc"))
                fd.write('ENV["JULIA_MPI_Fortran_COMPILER"] = "%s"\n' %
                         join_path(spec["mpi"].prefix.bin, "mpifort"))
                fd.write('\n')
            pkg_add("MPI")

        # Install Python
        if "+python" in spec or "+plot" in spec:
            with open(juliarc, "a") as fd:
                fd.write('# Python\n')
                fd.write('ENV["PYTHON"] = "%s"\n' % spec["python"].command.path)
                fd.write('\n')
            # Python's OpenSSL package installer complains:
            # Error: PREFIX too long: 166 characters, but only 128 allowed
            # Error: post-link failed for: openssl-1.0.2g-0
            pkg_add("PyCall")

        if "+plot" in spec:
            pkg_add("PyPlot")
            pkg_add("Colors")
            # These require maybe gtk and image-magick
            pkg_add("Plots")
            pkg_add("RecipesBase")
            pkg_add("GraphRecipes")
            pkg_add("StatsPlots")
            pkg_add("UnicodePlots")
            julia("-e", """\
using Plots
using UnicodePlots
unicodeplots()
plot(x->sin(x)*cos(x), range(0, stop=2*pi, length=20))
""")

        # Install SIMD
        if "+simd" in spec:
            pkg_add("SIMD")

        julia("-e", 'using Pkg; Pkg.status()')

        # We're done installing, prepend user-writable depot path!
        with open(juliarc, "a") as fd:
            fd.write('prepend!(DEPOT_PATH, [expanduser("~/.julia")])')
