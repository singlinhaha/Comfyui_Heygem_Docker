import os
import time
import uuid
import torchaudio
from heygem_tools import (query_task_status, submit_task,
                          save_tensor_as_video, video_to_tensor)


BASE_DIR = os.getcwd()
# 创建保存文件的临时目录
TEMP_DIR = os.path.join(BASE_DIR, 'input', 'heygem_result/temp')
SERVER_SAVE_DIR= '/code/data/temp'
os.makedirs(TEMP_DIR, exist_ok=True)

heygem_submit = "easy/submit"
heygem_query = "easy/query"

SERVICE_DICT = {
   9999: '系统异常',
   10000: '成功',
   10001: '忙碌中',
   10002: '参数异常',
   10003: '获取锁异常',
   10004: '任务不存在',
   10005: '任务处理超时',
   10006: '无法提交任务，请检查服务状态',
}


class HeygemDockerRunner:
    @classmethod
    def INPUT_TYPES(self):
        return {"required":
                    {
                        "service_url": ("STRING", {"default": "http://127.0.0.1:8383", "multiline": False}),
                        "audio": ("AUDIO",),
                        "video": ("IMAGE", ),
                     },
            "optional": {
                 "video_info": ("VHS_VIDEOINFO", ),
            },
                }

    CATEGORY = "heygem"
    RETURN_TYPES = ("IMAGE", "FLOAT")
    RETURN_NAMES = ("VIDEO", "FPS")

    FUNCTION = "run"

    def run(self, service_url, video, audio, video_info=None):
        print("==============开始执行任务==============")
        # 生成唯一的文件名
        audio_filename = f"{uuid.uuid4()}.wav"
        video_filename = f"{uuid.uuid4()}.mp4"

        audio_service_path = os.path.join(SERVER_SAVE_DIR, audio_filename)
        video_service_path = os.path.join(SERVER_SAVE_DIR, video_filename)
        audio_save_path = os.path.join(TEMP_DIR, audio_filename)
        video_save_path = os.path.join(TEMP_DIR, video_filename)
        print("audio save path: {}".format(audio_save_path))
        print("video save path: {}".format(video_save_path))

        # 保存音频
        waveform = audio["waveform"].squeeze(0)
        sample_rate = audio["sample_rate"]
        torchaudio.save(audio_save_path, waveform, sample_rate)

        # 保存视频
        if video_info is not None:
            print("video_info: ", video_info)
            fps = video_info['loaded_fps']
        else:
            fps = 24
        save_tensor_as_video(
            image_tensor=video,
            output_path=video_save_path,
            fps=fps,
        )

        # 提交任务
        code = str(uuid.uuid4())
        heygem_service_submit_url = os.path.join(service_url, heygem_submit)
        result = submit_task(
            submit_url=heygem_service_submit_url,
            audio_path=audio_service_path,
            video_path=video_service_path,
            code=code)
        if result is None:
            raise ValueError(SERVICE_DICT[9999])
        if result['code'] != 10000:
            raise ValueError(SERVICE_DICT[result['code']])

        # 查询任务状态
        query_number = 0
        heygem_service_query_url = os.path.join(service_url, heygem_query)
        while True:
            query_number += 1
            if query_number > 100:
                raise ValueError(SERVICE_DICT[10001])
            result = query_task_status(heygem_service_query_url, code)
            print(f"第{query_number}次查询，查询结果：{result}")
            if result['code'] == 10000 and result['data']['status'] == 2:
                break
            elif result['data']['status'] == 3:
                raise ValueError(result['data']['msg'])
            elif result['code'] == 10004:
                raise ValueError(SERVICE_DICT[10004])
            time.sleep(1)

        print("获取结果成功！")

        # 对结果进行处理
        result_name = result['data']['result'][1:]
        result_video_path = os.path.join(TEMP_DIR, result_name)
        images_tensor = video_to_tensor(result_video_path)
        return (images_tensor, fps, )
