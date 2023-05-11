import os

from spack.package import *
from spack.pkg.builtin.hpctoolkit import Hpctoolkit as BuiltinHpctoolkit


class Hpctoolkit(BuiltinHpctoolkit):
    __doc__ = BuiltinHpctoolkit.__doc__

    version("2023.03.stable", branch="release/2023.03")
    version("2023.03.01", commit="9e0daf2ad169f6c7f6c60408475b3c2f71baebbf")

    variant(
        "python", default=False, description="Support unwinding Python source.", when="@2023.03:"
    )

    depends_on("elfutils~nls", type="link")
    depends_on("libmonitor@2023.02.13:", when="@2023.01:")
    depends_on("xz+pic libs=static", type="link")
    depends_on("yaml-cpp@0.7.0: +shared", when="@2022.10:")

    depends_on("python@3.10:", type=("build", "run"), when="+python")

    conflicts("xz@5.2.7:5.2.8", msg="avoid xz 5.2.7:5.2.8 (broken symbol versions)")
    conflicts("+mpi", when="@2022.10.01", msg="hpcprof-mpi is not available in 2022.10.01")

    conflicts(
        "^hip@5.3:", when="@:2022.12", msg="rocm 5.3 requires hpctoolkit 2023.03.01 or later"
    )

    # Fix a bug where make would mistakenly overwrite hpcrun-fmt.h.
    # https://gitlab.com/hpctoolkit/hpctoolkit/-/merge_requests/751
    def patch(self):
        with working_dir(join_path("src", "lib", "prof-lean")):
            if os.access("hpcrun-fmt.txt", os.F_OK):
                os.rename("hpcrun-fmt.txt", "hpcrun-fmt.readme")

    # Note: Replace 'configure_args' to prevent conflicts with definition of MPICXX ENV variable
    def configure_args(self):
        spec = self.spec

        args = [
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-bzip=%s" % spec["bzip2"].prefix,
            "--with-dyninst=%s" % spec["dyninst"].prefix,
            "--with-elfutils=%s" % spec["elfutils"].prefix,
            "--with-tbb=%s" % spec["intel-tbb"].prefix,
            "--with-libmonitor=%s" % spec["libmonitor"].prefix,
            "--with-libunwind=%s" % spec["libunwind"].prefix,
            "--with-xerces=%s" % spec["xerces-c"].prefix,
            "--with-lzma=%s" % spec["xz"].prefix,
            "--with-zlib=%s" % spec["zlib"].prefix,
        ]

        if spec.satisfies("@2022.10:"):
            args.append("--with-libiberty=%s" % spec["libiberty"].prefix)
        else:
            args.append("--with-binutils=%s" % spec["binutils"].prefix)
            args.append("--with-libdwarf=%s" % spec["libdwarf"].prefix)

        if spec.satisfies("@:2020.09"):
            args.append("--with-gotcha=%s" % spec["gotcha"].prefix)

        if spec.target.family == "x86_64":
            args.append("--with-xed=%s" % spec["intel-xed"].prefix)

        if spec.satisfies("@:2022.03"):
            args.append("--with-mbedtls=%s" % spec["mbedtls"].prefix)

        if spec.satisfies("@2021.05.01:"):
            args.append("--with-memkind=%s" % spec["memkind"].prefix)

        if spec.satisfies("+papi"):
            args.append("--with-papi=%s" % spec["papi"].prefix)
        else:
            args.append("--with-perfmon=%s" % spec["libpfm4"].prefix)

        if spec.satisfies("@2022.10:"):
            args.append("--with-yaml-cpp=%s" % spec["yaml-cpp"].prefix)

        if "+cuda" in spec:
            args.append("--with-cuda=%s" % spec["cuda"].prefix)

        if "+level_zero" in spec:
            args.append("--with-level0=%s" % spec["oneapi-level-zero"].prefix)

            # gtpin requires level_zero
            if "+gtpin" in spec:
                args.append("--with-gtpin=%s" % spec["intel-gtpin"].prefix)
                args.append("--with-igc=%s" % spec["oneapi-igc"].prefix)

        if "+opencl" in spec:
            args.append("--with-opencl=%s" % spec["opencl-c-headers"].prefix)

        if spec.satisfies("+rocm"):
            args.extend(
                [
                    "--with-rocm-hip=%s" % spec["hip"].prefix,
                    "--with-rocm-hsa=%s" % spec["hsa-rocr-dev"].prefix,
                    "--with-rocm-tracer=%s" % spec["roctracer-dev"].prefix,
                    "--with-rocm-profiler=%s" % spec["rocprofiler-dev"].prefix,
                ]
            )

        if spec.satisfies("+python"):
            p3config = join_path(spec["python"].prefix, "bin", "python3-config")
            args.append("--with-python=%s" % p3config)

        # MPI options for hpcprof-mpi. +cray supersedes +mpi.
        if spec.satisfies("+cray"):
            args.append("--enable-mpi-search=cray")
            if spec.satisfies("@:2022.09 +cray-static"):
                args.append("--enable-all-static")
            else:
                args.append("HPCPROFMPI_LT_LDFLAGS=-dynamic")

        elif spec.satisfies("+mpi"):
            args.append("MPICXX=%s" % spec["mpi"].mpicxx)

        # Make sure MPICXX is not picked up through the environment.
        else:
            args.append("MPICXX=")

        if spec.satisfies("+debug"):
            args.append("--enable-develop")

        return args
