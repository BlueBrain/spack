# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepysnap(PythonPackage):
    """Blue Brain SNAP is a Python library for accessing BlueBrain circuit models
    represented in SONATA format."""

    homepage = "https://github.com/BlueBrain/snap"
    pypi = "bluepysnap/bluepysnap-0.12.0.tar.gz"

    version("3.0.1", sha256="733bf35f90d11a70284793f0f0974fea628f70a47f16c4a200872ef75f36b597")

    patch(
        "https://github.com/BlueBrain/snap/commit/7ec05a6843b24ca1ad1f2e897369b631d7891331.patch?full_index=1",
        sha256="271cbad0d51c71b8843d2fb13c2c52752eea19a056974506135b1f971fec1211",
        when="@3.0.1",
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm@:7", type="build")

    depends_on("py-cached-property@1.0:", type=("build", "run"))
    depends_on("py-h5py@3.0.1:3", type=("build", "run"))
    depends_on("py-importlib-resources@5:", when="@2:", type=("build", "run"))
    depends_on("py-jsonschema@4", type=("build", "run"))

    depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    depends_on("py-libsonata@0.1.24:", when="@2:2", type=("build", "run"))
    depends_on("py-libsonata@0.1.26:", when="@3:3", type=("build", "run"))

    depends_on("py-morphio@3", type=("build", "run"))
    depends_on("py-morph-tool@2.4.3:2", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-more-itertools@8.2.0:", type=("build", "run"))
    depends_on("py-brain-indexer@3.0.0:", type=("build", "run"))
