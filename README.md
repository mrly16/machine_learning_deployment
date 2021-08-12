# ml_template

## Intro
基于机器学习最基础的应用场景之一 —— 房价预测开发的简单模型（使用数仓中房价数据为训练与测试集），为了突出重点省略了调参和模型评价的步骤，最终可以以flask服务的形式部署。

## Usage
打包docker镜像

```DOCKER_BUILDKIT=1 docker build --tag ml_template:test .```

运行docker服务

```docker run -p 5000:5000 ml_template:test```

训练模型

浏览器访问 http://127.0.0.1:5000/train

预测

浏览器访问 http://127.0.0.1:5000/inference