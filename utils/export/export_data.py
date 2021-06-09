from urllib.request import urlopen

import numpy as np
import plotly.graph_objects as go
import cv2

from utils import collection
import time

from utils.constant import FRAME


def export_mp4(fig, filename, backup):
    images = []
    frames = []
    num_frames = len(fig['frames'])
    # num_frames = 5

    # print(fig)
    for i in range(num_frames):
        if 'pointers' in fig['frames'][i]:
            export_data= [ fig['data'][1]]
            for pt in fig['frames'][i]['pointers']:
                temp = eval(f"backup{pt}")
                export_data.append(temp)
            # export_data = [fig['frames'][i]['data'][0], fig['data'][1]]
        else:
            export_data=[ fig['frames'][i]['data'][0], fig['data'][1] ] if len(fig['data']) > 1 else  fig['frames'][i]['data'][0]
        # fig2 = go.Figure(data=fig['frames'][i]['data'][0], layout=fig['layout'])
        fig2 = go.Figure(data=export_data, layout=fig['layout'])

        fig2.layout.title.text = fig['frames'][i]['name']
        img_bytes = fig2.to_image(format="png", scale=4)
        # print(img_bytes )

        images.append(img_bytes)


    for im in images:
        nparr = np.fromstring(im, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        height, width, layers = frame.shape
        size = (width, height)
        frames.append(frame)

    pathout = f'assets/export/{filename}.mp4'
    out = cv2.VideoWriter(pathout, cv2.VideoWriter_fourcc(*'mp4v'), 2, size)
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()
    print('done export')


###############################################################################################################################
def export_img_mp4(index, filename):
    images = []
    frames = []
    data = collection.data[index]
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 20)
    fontScale = 1
    color = (0, 0, 255)
    thickness = 2
    fix_shape = None

    for x in range(0, len(data)):  # len(data)
        req = urlopen(data.iloc[x]['link']).read()
        images.append(req)

    for count, im in enumerate(images):
        nparr = np.fromstring(im , np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if fix_shape is None:
            height, width, layers = frame.shape
            fix_shape = (width, height)
        else:
            frame = cv2.resize(frame,fix_shape)

        frame = cv2.putText(frame, data.iloc[count][FRAME], org, font,  fontScale, color, thickness, cv2.LINE_AA)
        frames.append(frame)
    pathout = f'assets/export/{filename}.mp4'
    out = cv2.VideoWriter(pathout, cv2.VideoWriter_fourcc(*'mp4v'), 2, fix_shape)
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()
    print('done export')