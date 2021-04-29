# ZHToolkit

For WSL under windows here are some ways to redirect to other drive

1.安装Chocolatey 

2. ```choco install lxrunoffline```

3.下载wsl镜像  *.tar.gz from: https://lxrunoffline.apphb.com/download/UbuntuFromMS/16

4.安装镜像e:\UbuntuSubsys\16.04.2-server-cloudimg-amd64-root.tar.gz 到 e:\UbuntuSubsys\Ubuntu16 命名为 Ub16

```LxRunOffline i -n Ub16 -d e:\UbuntuSubsys\Ubuntu16 -f E:\UbuntuSubsys\16.04.2-server-cloudimg-amd64-root.tar.gz -s```

5.启动环境：
```wsl```

或

```LxRunOffline r -n Ub16```

或

桌面双击Ub16图标

## Useful toolkits

1. Model information: torchinfo
  ```
  pip install torchinfo
  ```
