import requests
import imageio
import numpy as np
import torch


def submit_task(submit_url, audio_path, video_path, code, watermark_switch=0, digital_auth=0, chaofen=0, pn=0):
    """
    提交一个新的任务。
    :param submit_url: 提交任务的URL。
    :param audio_path: 音频文件的本地地址。
    :param video_path: 视频文件的本地地址。
    :param code: 任务代码，用于标识和查询任务。
    :param watermark_switch: 是否开启水印，默认为0（关闭）。
    :param digital_auth: 数字授权选项，默认为0（关闭）。
    :param chaofen: 超分选项，默认为0（关闭）。
    :param pn: 其他选项，默认为0。
    :return: 返回服务器响应的结果，通常包括状态码、成功标志、消息等信息。
    """
    payload = {
        'audio_url': audio_path,
        'video_url': video_path,
        'code': code,
        'watermark_switch': watermark_switch,
        'digital_auth': digital_auth,
        'chaofen': chaofen,
        'pn': pn
    }

    try:
        response = requests.post(submit_url, json=payload)
        if response.status_code == 200:
            return response.json()  # 假设服务器返回JSON格式的数据
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"发生异常：{e}")
        return None


def query_task_status(query_url, code):
    """
    查询指定任务的状态。
    :param query_url: 查询任务状态的URL。
    :param code: 任务代码，用于标识不同的任务。
    :return: 返回服务器响应的结果，通常包括状态、进度、结果等信息。
    """
    params = {
        'code': code,
    }

    try:
        response = requests.get(query_url, params=params)
        if response.status_code == 200:
            return response.json()  # 假设服务器返回JSON格式的数据
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"发生异常：{e}")
        return None


def save_tensor_as_video(image_tensor, output_path, fps=24):
    """
    将形状为 [frames, height, width, channels] 的 PyTorch 张量保存为视频文件。

    :param tensor: 形状为 [frames, height, width, channels] 的 PyTorch 张量，范围为 [0, 1]
    :param output_path: 输出视频文件路径
    :param fps: 视频帧率
    """
    # 确保张量在 CPU 上并且转换为 NumPy 数组
    if image_tensor.is_cuda:
        tensor = image_tensor.cpu()
    tensor_np = image_tensor.numpy()

    # 将张量值从 [0, 1] 范围转换为 [0, 255] 范围，并确保数据类型为 uint8
    tensor_np = (tensor_np * 255).astype(np.uint8)

    # 使用 imageio 写入视频文件
    with imageio.get_writer(output_path, fps=fps) as writer:
        for frame in tensor_np:
            writer.append_data(frame)


def video_to_tensor(video_path):
    """
    将本地视频文件转换为形状为 [frames, height, width, channels] 的 PyTorch 张量，
    范围为 [0, 1]。

    :param video_path: 本地视频文件路径
    :return: 形状为 [frames, height, width, channels] 的 PyTorch 张量
    """
    # 使用 imageio 读取视频文件
    reader = imageio.get_reader(video_path)

    frames = []
    for frame in reader:
        # 将每一帧从 uint8 类型转换为 float32 类型，并归一化到 [0, 1] 范围
        frame_normalized = (frame.astype(np.float32) / 255.0)
        frames.append(frame_normalized)

    # 将列表转换为 NumPy 数组
    frames_np = np.stack(frames, axis=0)

    # 将 NumPy 数组转换为 PyTorch 张量
    tensor = torch.tensor(frames_np, dtype=torch.float32)

    return tensor