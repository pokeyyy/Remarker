import gradio as gr
import plotly.graph_objects as go
import numpy as np
from config import num_points, random_color
import copy
import pickle
import tkinter as tk
from tkinter import filedialog

from iterator import get_next_pcd,accept_new,accept_original

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
    clusters_revise = clusters.copy()
    for i in range(len(clusters)):
        label = clusters[i][:,-3].reshape(-1,1)
        label_list.append(label)
    pcd = clusters[pointer]
    print(pcd.shape)
    fig = generate_fig(pcd)
    #label
    mask = pcd[:,-1].astype(bool)
    diff = pcd[mask]
    label_ori = int(diff[0,-3])
    label_pre = int(diff[0,-2])
    label_ori = reflection[label_ori]
    label_pre = reflection[label_pre]
    return fig[0],fig[1],label_ori,label_pre

def next_then_plot():
    global pointer
    if pointer < len(clusters) - 1 :
        pointer += 1
    print(pointer)
    pcd = clusters[pointer]
    return generate_fig(pcd)

def pre_then_plot():
    global pointer
    if pointer > 0 :
        pointer -= 1
    pcd = clusters[pointer]
    return generate_fig(pcd)

def accept_new():
    global label_list
    label_new = clusters[pointer][:,-2]
    label_new.reshape(-1,1)
    label_list[pointer] = label_new

def file_output():
    # 创建 tkinter 根窗口（隐藏）
    root = tk.Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(defaultextension=".pkl",
                                             filetypes=[("pickle Files", "*.pkl"),
                                                        ("All Files", "*.*")])
    root.quit()
    with open(path, 'wb') as file:
        pickle.dump(label_list, file, protocol=pickle.HIGHEST_PROTOCOL)


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
    with gr.Row():
        with gr.Column():
            accept_ori_btn = gr.Button("Accept Original")
            pre_btn = gr.Button("Prev")
        with gr.Column():
            accept_predict_btn = gr.Button("Accept Predict")
            next_btn = gr.Button("Next")
    with gr.Row():
        file_output_btn = gr.Button("Output File!")


    file_input.change(fn=upload_and_plot, inputs=[file_input], outputs=[left_plot, right_plot, ori_label, pre_label])

    next_btn.click(fn=next_then_plot, inputs=[], outputs=[left_plot, right_plot])
    pre_btn.click(fn=pre_then_plot, inputs=[], outputs=[left_plot, right_plot])
    accept_ori_btn.click(fn=accept_original)
    accept_predict_btn.click(fn=accept_new)
    file_output_btn.click(fn=file_output)

    # refresh_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])
    # reset_button.click(fn=refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

    # demo.load(refresh_point_cloud, inputs=[], outputs=[left_plot, right_plot])

# Launch the app
if __name__ == "__main__":
    demo.launch()
