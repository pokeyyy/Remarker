import gradio as gr
import plotly.graph_objects as go
import numpy as np
from config import num_points, random_color
import copy
import pickle
import tempfile
import tkinter as tk
from tkinter import filedialog

from iterator import generate_label

#global variable
pointer = 0
clusters = [] #原始数据
label_list = [] #导出的最终标签结果
clusters_revise = [] #暂存修改结果

reflection = ['unknow','管道','管廊支架','储罐','钢结构','unknow','unknow','人影鬼影','其他','联排管道','管道圆柱','管道拐弯','三通四通','管道法兰','管道阀门','管道仪表','管道支架','储罐圆柱','储罐顶面','储罐管嘴','储罐附件','房屋外壳','其他墙壁','楼板天花板','管道其他','储罐其他','钢结构其他']

# Function to generate a random point cloud
def generate_fig_nx9(pcd):
    downsample_step = max(1, len(pcd) // num_points)
    pcd = pcd[::downsample_step, :]

    ori_colors = pcd[:, 3:6]
    labels_0 = pcd[:, 6].astype(int)
    labels_1 = pcd[:, 7].astype(int)
    masks = pcd[:, 8].astype(int)

    valid_indices = masks != 0

    colors = copy.copy(ori_colors)
    colors[valid_indices] = random_color[labels_0[valid_indices]]
    color_strings = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    hover_text = [f'label: {reflection[label]}' for label in labels_0]
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
    fig.update_layout(scene=dict(
        xaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        yaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        zaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        aspectmode='data'  # Ensures the axes have the same scale
    ))

    colors = copy.copy(ori_colors)
    colors[valid_indices] = random_color[labels_1[valid_indices]]
    color_strings = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    hover_text = [f'label: {reflection[label]}' for label in labels_1]
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
    fig2.update_layout(scene=dict(
        xaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        yaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        zaxis=dict(showbackground=False, showgrid=False, showline=False, zeroline=False, showticklabels=False,
                   title=''),
        aspectmode='data'  # Ensures the axes have the same scale
    ))

    return fig, fig2


def generate_fig_nx4(pcd):
    downsample_step = max(1, len(pcd) // num_points)
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
    downsample_step = max(1, len(pcd) // num_points)
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
    return fig, fig


def generate_fig(pcd):
    if pcd.shape[1] == 6:
        return generate_fig_nx6(pcd)
    elif pcd.shape[1] == 4:
        return generate_fig_nx4(pcd)
    elif pcd.shape[1] == 9:
        return generate_fig_nx9(pcd)


def upload_and_plot(file_obj):
    global label_list,clusters,clusters_revise
    print(file_obj.name)
    with open(file_obj.name, 'rb') as file:
        clusters = pickle.load(file)
    clusters_revise = copy.deepcopy(clusters)
    for i in range(len(clusters)):
        label = clusters[i][:,-3].copy()
        label = label.reshape(-1,1)
        label_list.append(label)
    pcd = clusters[pointer]
    print(pcd.shape)
    fig = generate_fig(pcd)
    #label
    labels = generate_label(pcd)
    return fig[0],fig[1],reflection[labels[0]],reflection[labels[1]]

def next_then_plot():
    global pointer
    if pointer < len(clusters) - 1 :
        pointer += 1
    print(pointer)
    fig = generate_fig(clusters[pointer])
    labels = generate_label(clusters_revise[pointer])
    return fig[0],fig[1],reflection[labels[0]],reflection[labels[1]],pointer

def pre_then_plot():
    global pointer
    if pointer > 0 :
        pointer -= 1
    fig = generate_fig(clusters[pointer])
    labels = generate_label(clusters_revise[pointer])
    return fig[0],fig[1],reflection[labels[0]],reflection[labels[1]],pointer

def accept_new():
    global label_list,clusters_revise
    label_new = clusters[pointer][:,-2].copy()
    clusters_revise[pointer][:, -3] = label_new.copy()
    clusters_revise[pointer][:, -2] = label_new.copy()
    label_new.reshape(-1,1)
    label_list[pointer] = label_new
    labels = generate_label(clusters_revise[pointer])
    return reflection[labels[0]],reflection[labels[1]]

def accept_original():
    global label_list,clusters_revise
    label_new = clusters[pointer][:, -3].copy()
    clusters_revise[pointer][:, -3] = label_new.copy()
    clusters_revise[pointer][:, -2] = label_new.copy()
    label_new.reshape(-1, 1)
    label_list[pointer] = label_new
    labels = generate_label(clusters_revise[pointer])
    return reflection[labels[0]], reflection[labels[1]]

def jump_page(page_input):
    global pointer
    if(page_input < 0):
        pointer = 0
    elif(page_input >= len(clusters)):
        pointer = len(clusters) - 1
    else:
        pointer = page_input
    fig = generate_fig(clusters[pointer])
    labels = generate_label(clusters_revise[pointer])
    return fig[0],fig[1],reflection[labels[0]],reflection[labels[1]],pointer

def label_output():
    # 使用 tempfile 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp_file:
        pickle.dump(label_list, tmp_file, protocol=pickle.HIGHEST_PROTOCOL)
        return tmp_file.name

def file_output():
    # 使用 tempfile 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp_file:
        pickle.dump(clusters_revise, tmp_file, protocol=pickle.HIGHEST_PROTOCOL)
        return tmp_file.name

with gr.Blocks() as demo:
    with gr.Row():
        file_input = gr.File(label="Upload .pkl File")
    with gr.Row():
        with gr.Column():
            ori_label = gr.Textbox(label="Original Label", value="请导入文件", interactive=False)
        with gr.Column():
            pre_label = gr.Textbox(label="Predicted Label", value="请导入文件", interactive=False)
    with gr.Row():
        with gr.Column():
            left_plot = gr.Plot(label="Left Plot")
        with gr.Column():
            right_plot = gr.Plot(label="Right Plot")
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            accept_ori_btn = gr.Button("Accept Original")
            pre_btn = gr.Button("Prev")
        with gr.Column(scale=1):
            page_input = gr.Number(value=0, label="Enter page number:")
            jump_page_btn = gr.Button("Go to Page")
        with gr.Column(scale=1):
            accept_predict_btn = gr.Button("Accept Predict")
            next_btn = gr.Button("Next")
    with gr.Row():
        with gr.Column():
            label_output_btn = gr.Button("Output Label File!")
            label_file_output = gr.File(label="Download Label File")
        with gr.Column():
            file_output_btn = gr.Button("Output Point Cloud File!")
            clusters_file_output = gr.File(label="Download Point Cloud File")


    file_input.change(fn=upload_and_plot, inputs=[file_input], outputs=[left_plot, right_plot, ori_label, pre_label])

    next_btn.click(fn=next_then_plot, inputs=[], outputs=[left_plot, right_plot, ori_label, pre_label, page_input])
    pre_btn.click(fn=pre_then_plot, inputs=[], outputs=[left_plot, right_plot, ori_label, pre_label, page_input])
    accept_ori_btn.click(fn=accept_original,inputs=[],outputs=[ori_label, pre_label])
    accept_predict_btn.click(fn=accept_new,inputs=[],outputs=[ori_label, pre_label])
    jump_page_btn.click(fn=jump_page, inputs=[page_input], outputs=[left_plot, right_plot, ori_label, pre_label, page_input])
    label_output_btn.click(fn=label_output, inputs=[], outputs=[label_file_output])
    file_output_btn.click(fn=file_output, inputs=[], outputs=[clusters_file_output])
    # refresh_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    # reset_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

    # demo.load(refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

# Launch the app
if __name__ == "__main__":
    demo.launch()
