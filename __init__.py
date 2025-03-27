import os
import subprocess
import sys
main_path = os.path.dirname(__file__)
sys.path.append(main_path)

from heygem_node import HeygemDockerRunner

NODE_CLASS_MAPPINGS = {
    "HeygemDockerRunner": HeygemDockerRunner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HeygemDockerRunner": "HeygemDockerRunner",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

try:
    # 执行SH脚本并检查返回值
    subprocess.run(["custom_nodes/Comfyui_Heygem_Docker/docker_run.sh"], check=True)
except subprocess.CalledProcessError as e:
    print(f"SH 脚本执行失败: {e}", file=sys.stderr)
    sys.exit(1)