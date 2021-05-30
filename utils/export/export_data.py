import numpy as np
import plotly.graph_objects as go
import cv2

def export_mp4(fig, filename, backup):
    images = []
    frames = []
    num_frames = len(fig['frames'])
    # print(fig)
    for i in range(3):
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
        print(f'loading img ' )
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