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
    version('1.1.1', sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')
    version('1.0.4', sha256='bbc5c88a4acfecd3b059a01680926c693b82cf3b41733719c384fb0b371ca581')

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
    depends_on("python@2.7:2.8")

    # Run-time dependencies:

    depends_on("openblas")
    depends_on("lapack")

    depends_on("pcre2")
    depends_on("gmp")
    depends_on("mpfr")

    depends_on("libgit2")
    depends_on("curl")


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
    depends_on("hdf5", when="+hdf5", type="run")
    depends_on("mpi", when="+mpi", type="run")
    depends_on("py-matplotlib", when="+plot", type="run")

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
            "USE_SYSTEM_BLAS=1",
            "USE_SYSTEM_LAPACK=1",
            "USE_SYSTEM_PCRE=1",
            "USE_SYSTEM_GMP=1",
            "USE_SYSTEM_MPFR=1",
            "USE_SYSTEM_LIBGIT2=1",
            "USE_SYSTEM_CURL=1",
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

        # Configure Julia
        with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                  "a") as juliarc:
            if not spec.satisfies("@1:") and \
                    ("@master" in spec or "@release-0.5" in spec or "@0.5:" in spec):
                # This is required for versions @0.5:
                juliarc.write(
                    '# Point package manager to working certificates\n')
                juliarc.write('LibGit2.set_ssl_cert_locations("%s")\n' %
                              cacert_file)
                juliarc.write('\n')
            juliarc.write('# Put compiler cache into a private directory\n')
            juliarc.write('empty!(Base.LOAD_CACHE_PATH)\n')
            juliarc.write('unshift!(Base.LOAD_CACHE_PATH, "%s")\n' % cachedir)
            juliarc.write('\n')
            juliarc.write('# Put Julia packages into a private directory\n')
            if spec.satisfies("@1:"):
                juliarc.write('ENV["JULIA_DEPOT_PATH"] = "{0}"\n'.format(pkgdir) )
            else:
                juliarc.write('ENV["JULIA_PKGDIR"] = "%s"\n' % pkgdir)
            juliarc.write('\n')

        # Install some commonly used packages
        julia = spec['julia'].command
        if spec.satisfies('@1:'):
            julia("-e", 'using Pkg; Pkg.update()')
        else:
            julia("-e", 'Pkg.init(); Pkg.update()')

        def pkg_add(name):
            if spec.satisfies('@1:'):
                julia("-e",
                      'using Pkg; Pkg.add("{0}"); using {0}'.format(name))
            else:
                julia("-e", 'Pkg.add("{0}"); using {0}'.format(name))

        def pkg_build(name):
            if spec.satisfies('@1:'):
                julia("-e",
                      'using Pkg; Pkg.build("{0}"); using {0}'.format(name))
            else:
                julia("-e", 'Pkg.build("{0}"); using {0}'.format(name))

        # Install HDF5
        if "+hdf5" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# HDF5\n')
                juliarc.write('push!(Libdl.DL_LOAD_PATH, "%s")\n' %
                              spec["hdf5"].prefix.lib)
                juliarc.write('\n')
            pkg_add("HDF5")
            pkg_add("JLD")

        # Install MPI
        if "+mpi" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# MPI\n')
                juliarc.write('ENV["JULIA_MPI_C_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpicc"))
                juliarc.write('ENV["JULIA_MPI_Fortran_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpifort"))
                juliarc.write('\n')
            pkg_add("MPI")

        # Install Python
        if "+python" in spec or "+plot" in spec:
            with open(join_path(prefix, "etc", "julia", "juliarc.jl"),
                      "a") as juliarc:
                juliarc.write('# Python\n')
                juliarc.write('ENV["PYTHON"] = "%s"\n' % spec["python"].home)
                juliarc.write('\n')
            # Python's OpenSSL package installer complains:
            # Error: PREFIX too long: 166 characters, but only 128 allowed
            # Error: post-link failed for: openssl-1.0.2g-0
            pkg_build("PyCall")

        if "+plot" in spec:
            pkg_add("PyPlot")
            pkg_add("Colors")
            # These require maybe gtk and image-magick
            pkg_add("Plots")
            pkg_add("PlotRecipes")
            pkg_add("UnicodePlots")
            julia("-e", """\
using Plots
using UnicodePlots
unicodeplots()
plot(x->sin(x)*cos(x), linspace(0, 2pi))
""")

        # Install SIMD
        if "+simd" in spec:
            pkg_add("SIMD")

        julia("-e", 'Pkg.status()')
