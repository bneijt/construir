Build a hackage package
-----------------------

The job creation requires a cabal installation and will download the given
hackage package and dependencies to the job directory.

./hackagejob.py module

will download module and all of it's depdencies into the job directory and use `../mkjob.py` to create a job image with the name `module.ext2`.

The job requires the `opt` installation of `haskellplatform` from the `haskellplatform` job in the `job` directory.

Make sure you have the following files before running `./hackagejob.py`:

 - `./job/debs/` containing all the haskellplatform archives required and the archives specific for the job
 - `./job/opt_haskell-platform-2012.4.0.0.tar.bz2` an archive containing the haskell-platform installation (including cabal) with the `/opt` prefix.

The `hackagejob.py` script will remove `job/pkg` and download cabal archives into there, then use `construir.template` to create `job/bin/construir` with the package name and haskell platform version injected. Currently the haskell platform version is hardcoded into `hackagejob.py`.
