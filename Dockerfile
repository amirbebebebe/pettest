FROM ubuntu:22.04

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    curl \
    vim \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    libappindicator1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    xdg-utils \
    fonts-wqy-zenhei \
    && rm -rf /var/lib/apt/lists/*

# 安装Chrome和ChromeDriver（使用稳定版本）
RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/chrome.deb || apt-get install -f -y \
    && rm /tmp/chrome.deb

# 安装对应版本的ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1) \
    && CHROMEDRIVER_MAJOR=$(echo $CHROME_VERSION | cut -d. -f1) \
    && curl -sL "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROMEDRIVER_MAJOR}" -o /tmp/chromedriver_version.txt \
    && CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version.txt) \
    && curl -sL "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -o /tmp/chromedriver.zip \
    && unzip -q /tmp/chromedriver.zip -d /tmp \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 /tmp/chromedriver_version.txt

# 安装Python依赖
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir flask requests selenium

# 复制项目文件
COPY . .

# 创建数据目录
RUN mkdir -p /app/content /app/data /app/logs

# 设置环境变量
ENV PYTHONPATH=/app
ENV PHONE=13810119101
ENV DISPLAY=:99

# 创建非root用户（Chrome需要）
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /home/appuser/.cache/pip

# 切换到非root用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# 默认启动服务（可在GitHub Actions中覆盖）
CMD ["python3", "scripts/cloud_publisher.py"]
