# ComfyUI Heygem

用于在comfyUI中调用heygem数字人服务。


1. 原仓库: [HeyGem.ai](https://github.com/GuijiAI/HeyGem.ai) 
2. [HeyGem数字人优化版一键启动,音频驱动视频,推理速度提升50%,解决任务队列阻塞问题,支持超长视频生成,8G显存可玩,暂不支持50系显卡,基于Docker
](https://www.bilibili.com/video/BV1kCoxYZEtc/?spm_id_from=333.337.search-card.all.click&vd_source=7c43af1b18f3ab7914df7cc0f093f28f)

感谢作者的分享。
dokcer镜像来自刘悦大佬分享的网盘链接

## 改动点
- 由于heygem项目支持且仅支持python3.8 环境，因此很难兼容到comfyui环境，所以采用docker部署的方式
- 由于heygen的docker镜像是在window下wsl打包的，直接迁移到ubuntu进行部署会有驱动识别问题，因此写了一个脚本去创建容器时自动适配驱动链接
- 如果是在wsl下部署，请参考[HeyGem数字人优化版一键启动,音频驱动视频,推理速度提升50%,解决任务队列阻塞问题,支持超长视频生成,8G显存可玩,暂不支持50系显卡,基于Docker
](https://www.bilibili.com/video/BV1kCoxYZEtc/?spm_id_from=333.337.search-card.all.click&vd_source=7c43af1b18f3ab7914df7cc0f093f28f)

## 安装说明
1. 下载docker镜像
下载刘悦大佬的一键整合包:  [https://pan.quark.cn/s/7bf7d4f74875](https://pan.quark.cn/s/7bf7d4f74875)
解压后加载heygem.tar镜像

```powershell
docker load -i heygem.tar
```
2. 克隆项目
```powershell
cd custom_nodes
git clone https://github.com/singlinhaha/Comfyui_Heygem_Docker.git
```
3. 启动项目
启动comfyui时会自动创建容器并启动heygem服务。服务地址为：http://127.0.0.1:8383
