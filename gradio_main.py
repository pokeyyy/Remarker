import gradio as gr
import plotly.graph_objects as go
import numpy as np

# Function to generate a random point cloud

def generate_fig_nx7(pcd):
    num_points = 10000
    downsample_step = max(1, len(pcd)//num_points)  
    pcd = pcd[::downsample_step, :] 

    colors = pcd[:, 3:6]
    labels = pcd[:, 6].astype(int)
    random_color = np.random.rand(len(labels), 3)*255

    valid_indices = labels != -1

    colors[valid_indices] = random_color[labels[valid_indices]]

    color_strings = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    hover_text = [f'labels {label}' for label in labels]

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

def generate_fig_nx4(pcd):
    num_points = 10000
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
    num_points = 10000
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
    return fig

def generate_fig(pcd):
    if pcd.shape[1] == 6:
        return generate_fig_nx6(pcd)
    elif pcd.shape[1] == 4:
        return generate_fig_nx4(pcd)

def upload_and_plot(file_obj):
    pcd = np.load(file_obj.name)
    print(pcd.shape)
    fig = generate_fig(pcd)
    return fig,fig

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
            refresh_button = gr.Button("Prev")
        with gr.Column():
            reset_button = gr.Button("Next")

    file_input.change(fn=upload_and_plot, inputs=[file_input], outputs=[left_plot, right_plot])

    # refresh_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    # reset_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    
    # demo.load(refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

# Launch the app
if __name__ == "__main__":
    demo.launch()
