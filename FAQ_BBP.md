# FAQ for BBP spack usage


<details>
  <summary>Q: How do I build and *load* a piece of software?</summary>

  We'll install `Ed(1)`, the standard editor.

  Make sure you're setup as per [this](https://github.com/BlueBrain/spack#building-software-on-bluebrain5).

  Specifically that you have the `spack` git repo on the `develop` branch, and have created and linked the files into `~/.spack/`

  ```console
  spack install ed
  ```

  This produces output, and should end with something like:
  `$SPACK_INSTALL_PREFIX/linux-rhel7-x86_64/gcc-6.4.0/ed-1.4-35jlkv`

  One can then run `ed` with
  ```
  $SPACK_INSTALL_PREFIX/linux-rhel7-x86_64/gcc-6.4.0/ed-1.4-35jlkv/ed
  ```

  More complex packages will have an environment that needs to be setup by the module system.
  To find the module that was built, issue:
  ```
  spack module tcl find --full-path ed
  ```

  At which point, you should be able to:
  ```
  module load $path_from_above
  ```
</details>

<details>
  <summary>Q: Why do I have to rebuild the entire world?</summary>

  If you are on the `BB5`, you shouldn't need to.

  As [described here](https://github.com/BlueBrain/spack#building-software-on-bluebrain5), one can use the system packages available with an appropriate `~/.spack/packages.yaml`.
</details>


<details>
  <summary>Q: Why do I see `PACK_INSTALL_PREFIX` in my install?  Things are failing!</summary>

  It is expected that the environment variable `$SPACK_INSTALL_PREFIX` is defined.
  If it isn't you, may be getting weird expansions from that.
</details>

<details>
  <summary>Q: Why are the module files not being rebuilt?</summary>

  The `spack module tcl refresh` command respects a blacklists that are in:
  * `spack/deploy/configs/applications/modules.yaml`
  * `spack/deploy/configs/serial-libraries/modules.yaml`
  * `~/.spack/modules.yaml`

  Run `spack --debug module tcl refresh` and search for the module you expect to be built.
  Modify the blacklist to have the module built.
</details>

<details>
  <summary>Q: Why is it so slow to interact with the `spack` repository if on GPFS</summary>

  Make sure the `spack` repo is checked out in a subdirectory of `$HOME`.
  The `spack` repository is quite large, and when it is checked out under a `/gpfs/bbp.cscs.ch/project/*` directory, performance can be 10x slower than on the SSD provided storage of `$HOME`.
</details>

<details>
  <summary>Q: Where is the binary cache?</summary>

  We currently don't have a binary cache - it is complicated to setup: needs to have the same based path (????[pls more details]).
  Please make sure you have setup the correct `~/.spack/packages.yaml` so that you are not rebuilding the available system packages

</details>
