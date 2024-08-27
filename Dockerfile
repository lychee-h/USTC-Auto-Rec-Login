# 使用 CentOS 7 作为基础镜像
FROM centos:7

# 安装 Tesseract-OCR
RUN yum install -y epel-release
RUN yum install -y tesseract

# 安装 Python 和 pip
RUN yum install -y python3 python3-pip

# 工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flask环境变量
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 运行的端口
EXPOSE 5000

CMD ["flask", "run"]