#!/bin/sh

# 定义容器名称
CONTAINER_NAME="heygem_service"
# 定义镜像名称
IMAGE_NAME="heygem"
# 驱动版本号（必须与实际版本一致）
DRIVER_VERSION="550.120"
# 容器内代码运行目录
CONTAINER_CODE_DIR="/code"

# 创建结果保存目录
SAVE_DIR="$(pwd)/input/heygem_result"
if [ ! -d "$SAVE_DIR" ]; then
    mkdir -p "$SAVE_DIR"
    echo "创建目录：$SAVE_DIR"
else
    echo "目录已存在：$SAVE_DIR"
fi

# 启动服务
echo "启动docker服务"
if docker inspect --format='{{.Name}}' "$CONTAINER_NAME" > /dev/null 2>&1; then
    echo "容器 '$CONTAINER_NAME' 已存在，跳过创建"
else
    echo "正在创建并启动容器..."
    # 关键修改：将应用作为主进程启动
    docker run --name $CONTAINER_NAME \
      --net=host \
      -v $SAVE_DIR:/code/data \
      -p 8383:8383 \
      -d \
      --gpus all \
      --init \
      --restart=always \
      $IMAGE_NAME \
      bash -c "
        echo '==== 配置驱动符号链接 ===='
        cd /usr/lib/x86_64-linux-gnu || exit 1

        # 处理 libcuda.so
        [[ -f libcuda.so ]] && mv -v libcuda.so libcuda.so.backup
        ln -svf libcuda.so.1 libcuda.so

        # 处理 libcuda.so.1
        [[ -f libcuda.so.1 ]] && mv -v libcuda.so.1 libcuda.so.1.backup
        cp -v libcuda.so.$DRIVER_VERSION libcuda.so.1

        # 处理 libnvidia-ml.so.1
        [[ -f libnvidia-ml.so.1 ]] && mv -v libnvidia-ml.so.1 libnvidia-ml.so.1.backup
        ln -svf libnvidia-ml.so.$DRIVER_VERSION libnvidia-ml.so.1

        echo '==== 启动应用 ===='
        exec python $CONTAINER_CODE_DIR/app_run.py  # 前台运行
      "

    # 检查容器是否启动成功
    if [ $? -ne 0 ]; then
        echo "错误：容器创建失败，请检查日志！"
        exit 1
    fi

    echo -e "\n操作成功完成！容器在后台运行中。"
    echo "验证命令：docker logs $CONTAINER_NAME"
fi

sleep 5
echo "脚本执行完毕，容器 $CONTAINER_NAME 已在后台运行"