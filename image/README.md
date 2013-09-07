Collection of build images
==========================
Each image contains a booting system which after booting will

1. Extract the job image as **root**: `tar -C / -xJf jobimage.tar.xz`.
2. Zero the output device: `dd if=/dev/zero of=/dev/sdb`
3. Change the working directory to `/job`.
4. Execute the `/job/construir` file using bash as **root** and store the output in `/job_output.txt`.

Image names begin with a lowercase _i_ followed by an index number and have the `qcow2` extension.

Each image is described below with a download url.

i0
--
Arch Linux installation with nothing installed. Bare minimal image.

 * Status: Final
 * SHA1: 73670e2a857f1c57731df69b74e7d11f329d84ce
 * Locations:
   [mega.co.nz](https://mega.co.nz/#!gslVUbxY!BdocrV4Kau59GebjZXX4UEH3jttCJaIVHDXUE3KKSfI)




