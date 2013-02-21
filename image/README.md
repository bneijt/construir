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

Status: **not final yet**

Download: http://bneijt.nl/pr/construir/image/i0.qcow2



