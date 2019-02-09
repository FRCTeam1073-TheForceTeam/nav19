# Find Line Segments Example
#
# This example shows off how to find line segments in the image. For each line object
# found in the image a line object is returned which includes the line's rotation.

# find_line_segments() finds finite length lines (but is slow).
# Use find_line_segments() to find non-infinite lines (and is fast).

enable_lens_corr = False # turn on for straighter lines...

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.set_brightness(-2)
sensor.set_saturation(1)
sensor.skip_frames(time = 3000)
clock = time.clock()

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

img = sensor.snapshot()
roi = (10,10,5,5)
#hist = img.get_histogram()
#lo = hist.get_percentile(0.05)
#hi = hist.get_percentile(0.95)
#thresh  = hist.get_threshold()

thresh = [(80,100),(-1,1),(-1,1)]

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # Locate blobs to create a set of ROIs to use for line searching:
    blobs = img.find_blobs(thresh, pixels_threshold=60, area_threshold=50,
                           merge=False, margin=10)


    # `merge_distance` controls the merging of nearby lines. At 0 (the default), no
    # merging is done. At 1, any line 1 pixel away from another is merged... and so
    # on as you increase this value. You may wish to merge lines as line segment
    # detection produces a lot of line segment results.

    # `max_theta_diff` controls the maximum amount of rotation difference between
    # any two lines about to be merged. The default setting allows for 15 degrees.
    linesegs = []
    for b in blobs:
        img.draw_rectangle(b.rect())
        roi = (b.x(), b.y(), b.w()+4, b.h()+4)
        if b.area() < 1500:
            linesegs += img.find_line_segments(roi=roi, merge_distance = 0, max_theta_diff = 5)

    for l in linesegs:
        img.draw_line(l.line(), color = (255, 0, 0))
        # print(l)

    print("FPS %f" % clock.fps())
