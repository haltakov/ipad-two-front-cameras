import sys
from shutil import copyfile
from scripts.create_virtual_image import main

frames = 20
step = 1.0 / (frames-1)

# copyfile('images/image_left.png', 'images/video/frame_000.png')

for i in range(1, frames-1):
    sys.argv = ['create_virtual_image', '-i', 'images', '-p', 'images/video/frame_%03d.png' % i, '-o', str(i*step)]
    main()

copyfile('images/image_right.png', 'images/video/frame_%03d.png' % (frames-1))

for i in range(1, frames-1):
    copyfile('images/video/frame_%03d.png' % i, 'images/video/frame_%03d.png' % (frames*2-i-2))


1/20 * 10