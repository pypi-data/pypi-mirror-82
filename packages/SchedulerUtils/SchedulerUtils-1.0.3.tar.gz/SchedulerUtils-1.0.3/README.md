**StrategiesManager**

# 这是一个任务管理工具类

## 格式

### 配置文件参数：
### 基础必须字段：
- name 任务名称，唯一
- exec_cmd 执行命令
- exec_path 执行路径，‘/’结尾
- job_type 任务类型，1 定时任务 2 循环间隔任务 3 保活任务

可选基础字段
- desc 未使用
- enable 是否启用，默认启用 1,不启用 0

1）1 定时任务

可选字段：
- day_of_week 默认"0-6"
- hour 默认0
- minute 默认0
- second 默认0

2）2 循环间隔任务

必须字段：
- second

3）3 保活任务

必须字段：
- task_name 任务管理器的程序名.后缀

可选字段：
- second 默认5

### **注意事项**
1）保活任务支持python跟exe文件
2）taskkill 自定义命令
```
"exec_cmd": "taskkill xxxx.py"
"exec_cmd": "taskkill xxxx.exe"
```
3）执行路径要使用斜杠
```
"exec_path": "C:/Users/Administrator/Desktop/klDataService"
```
4）任务配置文件使用utf-8编码，不支持中文字符

5）除了执行python命令跟bat文件是启动单独窗口之外其它的命令都在父窗口执行，如果要单独窗口可以在命令前添加‘start’指令
```
[{
    "exec_cmd": "start QuoteKLHistoryService.exe",
...
}]
```

### 例子
配置文件：task.conf
```
[
    {
        "name": "KILL_TQ_H_KL_WEB",
        "exec_cmd": "taskkill tq_server.py",
        "exec_path": "./",
        "job_type": 1,
        "day_of_week": "0-6",
        "hour": 5,
        "minute": 10,
        "second": 0,
        "desc": "杀死天勤历史服务"
    },
    {
        "name": "KILL_TQ_KL_PUSH",
        "exec_cmd": "taskkill TQ_KL_PUSH.py",
        "exec_path": "./",
        "job_type": 1,
        "day_of_week": "0-6",
        "hour": 5,
        "minute": 10,
        "second": 0,
        "desc": "杀死天勤推送服务"
    },
    {
        "name": "H_KL_WEBGATE",
        "exec_cmd": "python webgate.py -p 10039",
        "exec_path": "./",
        "job_type": 3,
        "task_name": "webgate.py",
        "second": 5
    },
    {
        "name": "TQ_H_KL_WEB",
        "exec_cmd": "python tq_server.py -p 10022",
        "exec_path": "./",
        "job_type": 3,
        "task_name": "tq_server.py"
    },
    {
        "name": "FT_H_KL_WEB",
        "exec_cmd": "python ft_server.py -p 10023",
        "exec_path": "./",
        "job_type": 3,
        "task_name": "ft_server.py"
    },
    {
        "name": "TQ_KL_PUSH",
        "exec_cmd": "python TQ_KL_PUSH.py",
        "exec_path": "G:/WS_VS/InQuoteKLPushService-idea/",
        "job_type": 3,
        "task_name": "TQ_KL_PUSH.py",
        "enable": 1
    }
]
```
例子：
```python
from framework.keepalive_task import doJobs

doJobs(path='./conf/task.conf')
```

### 更新日志
- 2020.10.19
    1) 修复小bug,杀死进程exe类型的错误
    
- 2020.10.16
    1) 修复小bug
    
- 2020.09.18
    1) 完成基本定时任务启动框架
