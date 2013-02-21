Collection of build images
==========================
Each image contains a booting system which after booting will

1. Extract the job image as **root**: `tar -C / -xJf jobimage.tar.xz`.
2. Change the working directory to `/job`.
3. Execute the `/job/construir` file using bash as **root**.

Image names begin with a lowercase _i_ followed by an index number and have the `qcow2` extension.

Each image is described below with a download url.

i0
--
Arch Linux installation with nothing installed. Bare minimal image.

 * Status: Final
 * SHA1: 4eef182f3412c970050549ddd78453fa2f944c4f
 * Locations:
   [bneijt.nl](http://bneijt.nl/pr/construir/image/i0.qcow2)
   [mega.co.nz](https://mega.co.nz/#!p4NWVagb!DvPD4DEhXzr_iQ-vNEzb2SFk_kQEBZZl8FR8eFGHYv0)




