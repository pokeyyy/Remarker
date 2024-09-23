import gradio as gr
import plotly.graph_objects as go
import numpy as np
from config import num_points, random_color
import copy

from iterator import get_next_pcd,accept_new,accept_original

# Function to generate a random point cloud
def generate_fig_nx9(pcd):
    downsample_step = max(1, len(pcd)//num_points)  
    pcd = pcd[::downsample_step, :] 

    ori_colors = pcd[:, 3:6]
    labels_0 = pcd[:, 6].astype(int)
    labels_1 = pcd[:, 7].astype(int)
    masks = pcd[:, 8].astype(int)
    
    valid_indices = masks != 0

    colors = copy.copy(ori_colors)
    colors[valid_indices] = random_color[labels_0[valid_indices]]
    color_strings = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    hover_text = [f'label: {label}' for label in labels_0]
    fig = go.Figure(data=[go.Scatter3d(
        x=pcd[:, 0], y=pcd[:, 1], z=pcd[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=color_strings,
            opacity=0.8
        ),
        hovertext=hover_text,  # Add hover labels
    )])

    colors = copy.copy(ori_colors)
    colors[valid_indices] = random_color[labels_1[valid_indices]]
    color_strings = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    hover_text = [f'label: {label}' for label in labels_1]
    fig2 = go.Figure(data=[go.Scatter3d(
        x=pcd[:, 0], y=pcd[:, 1], z=pcd[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=color_strings,
            opacity=0.8
        ),
        hovertext=hover_text,  # Add hover labels
    )])

    return fig,fig2

def generate_fig_nx4(pcd):
    downsample_step = max(1, len(pcd)//num_points)  
    pcd = pcd[::downsample_step, :] 

    labels = pcd[:, 3]
    random_color = np.random.rand(len(labels), 3)
    colors = random_color[labels.astype(int)]
    colors = colors / 255.0
    color_strings = ['rgb({}, {}, {})'.format(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]
    hover_text = ['R: {}, G: {}, B: {}'.format(int(r), int(g), int(b)) for r, g, b in colors]

    fig = go.Figure(data=[go.Scatter3d(
        x=pcd[:, 0], y=pcd[:, 1], z=pcd[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=color_strings,
            opacity=0.8
        ),
        hovertext=hover_text,  # Add hover labels
    )])
    return fig

def generate_fig_nx6(pcd):
    downsample_step = max(1, len(pcd)//num_points)  
    pcd = pcd[::downsample_step, :] 
    colors = pcd[:, 3:]   
    colors = colors / 255.0
    color_strings = ['rgb({}, {}, {})'.format(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]
    hover_text = ['R: {}, G: {}, B: {}'.format(int(r), int(g), int(b)) for r, g, b in colors]

    fig = go.Figure(data=[go.Scatter3d(
        x=pcd[:, 0], y=pcd[:, 1], z=pcd[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=color_strings,
            opacity=0.8
        ),
        hovertext=hover_text,  # Add hover labels
    )])
    return fig,fig

def generate_fig(pcd):
    if pcd.shape[1] == 6:
        return generate_fig_nx6(pcd)
    elif pcd.shape[1] == 4:
        return generate_fig_nx4(pcd)
    elif pcd.shape[1] == 9:
        return generate_fig_nx9(pcd)

def upload_and_plot(file_obj):
    pcd = np.load(file_obj.name)
    print(pcd.shape)
    fig = generate_fig(pcd)
    return fig

def next_then_plot():
    pcd = get_next_pcd()
    return generate_fig(pcd)

with gr.Blocks() as demo:
    with gr.Row():
        file_input = gr.File(label="Upload .npy File")
    with gr.Row():
        with gr.Column():
            left_plot = gr.Plot(label="Left Plot")
        with gr.Column():
            right_plot = gr.Plot(label="Right Plot")
    with gr.Row():
        with gr.Column():
            accept_predict_btn = gr.Button("Accept Predict")
            next_btn = gr.Button("Prev")
        with gr.Column():
            accept_ori_btn = gr.Button("Accept Original")
            next_btn = gr.Button("Next")

    file_input.change(fn=upload_and_plot, inputs=[file_input], outputs=[left_plot, right_plot])

    next_btn.click(fn=next_then_plot,inputs=[],outputs=[left_plot,right_plot])
    accept_ori_btn.click(fn=accept_original)
    accept_predict_btn.click(fn=accept_new)

    # refresh_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    # reset_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    
    # demo.load(refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

# Launch the app
if __name__ == "__main__":
    demo.launch()
