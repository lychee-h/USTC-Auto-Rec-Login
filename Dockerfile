# 使用官方的 Python 3.7 镜像作为基础镜像
FROM python:3.7

# 设置工作目录
WORKDIR /app

RUN rm -f /etc/apt/sources.list.d/* && \
    echo "deb http://mirrors.aliyun.com/debian/ buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list

#RUN apt-get update
#RUN apt-get install libgl1-mesa-glx

RUN apt-get update && \
    apt-get install -y aptitude && \
    aptitude install -y \
        libgl1-mesa-glx \
        tesseract-ocr

#RUN apt-get install tesseract-ocr
RUN export PATH=$PATH:/usr/local/bin
#        libgl1-mesa-dri \
#        libglvnd0 \
#        libx11-xcb1 \
#        libxext6 \
#        libxrender1 \
#        libsm6 \
#        libxrandr2 \
#        libxfixes3 \
#       libgl1
# RUN apt-get install libgl1
# RUN apt-get install libgl1-mesa-glx


# 将依赖文件添加到工作目录
COPY requirements.txt requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 将应用代码添加到工作目录
COPY . .

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "main.py"]
