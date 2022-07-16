def generator():
    import pyrealsense2 as rs
    import numpy as np
    import cv2
    import time
    import math
    import numpy as np

    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)
    # depth_sensor = profile.get_device().first_depth_sensor()
    # depth_scale = depth_sensor.get_depth_scale()

    # We will be removing the background of objects more than
    #  clipping_distance_in_meters meters away
    # clipping_distance_in_meters = 3
    # clipping_distance = clipping_distance_in_meters / depth_scale


    align_to = rs.stream.color
    align = rs.align(align_to)

    setp = 5
    index = 0

    while True:
        if index == setp:
            index = 0
        else:
            index += 1
            continue
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)
        # aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        #
        # depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # # Remove background - Set pixels further than clipping_distance to grey
        # grey_color = 153
        # depth_image_3d = np.dstack((depth_image, depth_image, depth_image))  # depth image is 1 channel, color is 3 channels
        # bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        #
        # # Render images
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # images = np.hstack((bg_removed, depth_colormap))

        # bg_removed, color_image, depth_colormap = cv2.resize(bg_removed, (640, 360)), cv2.resize(color_image, (640, 360)), cv2.resize(depth_colormap, (640, 360))

        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        yield color_image
