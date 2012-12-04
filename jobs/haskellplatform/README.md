Create a tar file in the output directory containing
the Haskell platform installation in /opt

Requires the `opt_ghc.tar` from the ghc job.
And a lot of debian packages, including:
    job/debs/
    job/debs/mesa-common-dev_7.7.1-5_amd64.deb
    job/debs/libgmp3-dev_2%3a4.3.2+dfsg-1_amd64.deb
    job/debs/libsm-dev_2%3a1.1.1-1_amd64.deb
    job/debs/libxfixes3_1%3a4.0.5-1_amd64.deb
    job/debs/x11proto-kb-dev_1.0.4-1_all.deb
    job/debs/libglu1-mesa-dev_7.7.1-5_amd64.deb
    job/debs/libxi6_2%3a1.3-7_amd64.deb
    job/debs/libgl1-mesa-dri_7.7.1-5_amd64.deb
    job/debs/libice6_2%3a1.0.6-2_amd64.deb
    job/debs/libsm6_2%3a1.1.1-1_amd64.deb
    job/debs/libice-dev_2%3a1.0.6-2_amd64.deb
    job/debs/libxdmcp-dev_1%3a1.0.3-2_amd64.deb
    job/debs/libgmpxx4ldbl_2%3a4.3.2+dfsg-1_amd64.deb
    job/debs/libxdamage1_1%3a1.1.3-1_amd64.deb
    job/debs/libdrm-intel1_2.4.21-1~squeeze3_amd64.deb
    job/debs/x11proto-core-dev_7.0.16-1_all.deb
    job/debs/libxt-dev_1%3a1.0.7-1_amd64.deb
    job/debs/libx11-dev_2%3a1.3.3-4_amd64.deb
    job/debs/xtrans-dev_1.2.5-1_all.deb
    job/debs/libdrm2_2.4.21-1~squeeze3_amd64.deb
    job/debs/x11proto-input-dev_2.0-2_all.deb
    job/debs/libglu1-mesa_7.7.1-5_amd64.deb
    job/debs/x11-common_1%3a7.5+8+squeeze1_all.deb
    job/debs/libxau-dev_1%3a1.0.6-1_amd64.deb
    job/debs/freeglut3_2.6.0-1_amd64.deb
    job/debs/libpthread-stubs0_0.3-2_amd64.deb
    job/debs/zlib1g-dev_1%3a1.2.3.4.dfsg-3_amd64.deb
    job/debs/libxcb1-dev_1.6-1_amd64.deb
    job/debs/libpthread-stubs0-dev_0.3-2_amd64.deb
    job/debs/libxext-dev_2%3a1.1.2-1_amd64.deb
    job/debs/libdrm-radeon1_2.4.21-1~squeeze3_amd64.deb
    job/debs/x11proto-xext-dev_7.1.1-2_all.deb
    job/debs/freeglut3-dev_2.6.0-1_amd64.deb
    job/debs/libxt6_1%3a1.0.7-1_amd64.deb
    job/debs/libxxf86vm1_1%3a1.1.0-2_amd64.deb
    job/debs/libgl1-mesa-dev_7.7.1-5_amd64.deb
    job/debs/libgl1-mesa-glx_7.7.1-5_amd64.deb

The plan is to create a job to do debian archive downloads on
a jobrunner with network support.
