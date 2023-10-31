# Ransomware-testing
## 简述
一个勒索程序模拟脚本，客户端生成随机key，为了防止被中间流量监控设备捕获key,使用非对称加密算法将key加密，同时根据cpu等信息生成唯一的一串字符hash标识，并将加密的key和唯一标识发送至服务端，服务端解密Key后将其存入数据库。

脚本不具备提权和自动传播等操作，仅做加解密测试，要加密尽可能多的文件请用管理员权限运行client
## 服务端
server.py为服务端脚本，运行前请修改34行的数据库连接信息

运行后会检查是否有相应的数据库及表，没有则自动创建。

随后生成随机公私钥密钥对，并开启一个http服务来下发公钥，默认监听5000端口

服务端收到发送过来的id和Key后，使用rsa私钥解密key，并将其存入数据库中。

![Snipaste_2023-10-27_11-11-34](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/d4e986b2-058d-412e-a5cd-ba9c29cfd9fe)

![Snipaste_2023-10-26_16-40-02](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/77f8140f-1b77-4cdd-aee4-4ad5b6cbfeff)


## 客户端
client.py为客户端脚本，运行前修改166和167行的服务端地址，运行脚本有点麻烦，可以打包成exe格式。

安装相应库
`pip install -r requirements.txt`

运行后会向服务端请求rsa公钥

随后生成128位的随机aes秘钥，并使用rsa公钥加密aes秘钥

根据cpu等信息生成一段唯一的ID

将加密的key和唯一ID发送至服务端。

随后遍历文件，将相关后缀的文件进行逐一加密（如ppt、docx等）

### 效果
![Snipaste_2023-10-30_14-01-56](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/20f43dc1-ca5e-44d5-b70d-0cc88e52b093)

被加密的文件后缀全为love，在桌面生成勒索信息.txt文档
![Snipaste_2023-10-30_14-04-41](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/17543553-78ec-408e-bbf2-8b74956e8a72)

![Snipaste_2023-10-30_14-05-58](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/83729e72-058f-4df2-bd6f-2def61139824)

![Snipaste_2023-10-30_14-05-07](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/2c539b01-4286-4f31-825c-101b8db39eca)

## 解密

decrypt为解密脚本，后面跟上秘钥即可
![Snipaste_2023-10-31_11-48-42](https://github.com/laohuan12138/Ransomware-testing/assets/42142726/1ebea4a6-d26c-493d-92c9-cfc5c3ce28d1)


