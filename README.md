# USTC-Auto-Rec-Login
## 描述

自动获取睿客云盘登录凭证

## 使用方法

docker部署

请求路径：/token

请求方式：POST

接口描述：登录睿客云盘并获取登录凭证

请求参数：

| **参数名**  | **类型** | **是否必须** |
| ----------- | -------- | ------------ |
| username    | string   | 必须         |
| password    | string   | 必须         |
| resultinput | string   | 必须         |

响应参数：

```json
{
    "token": ""
}
```

## 参考

[中科大健康打卡](https://github.com/windshadow233/USTC-Auto-Health-Report)
