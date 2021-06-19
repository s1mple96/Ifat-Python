# 数据驱动接口自动化
此项目是为了对自己一个学习的总结
以及工作中如何更好的落地实现自动化项目
# 使用方法
1.pip install -r requirements.txt  
2.python run.py
# 使用到的技术栈有:
1.测试框架方面使用到了:[Pytest](https://learning-pytest.readthedocs.io/zh/latest/)  
2.HTTP库方面用到的是:[Requests](https://docs.python-requests.org/en/master/)  
3.测试报告用到的是:[Allure](https://docs.qameta.io/allure/)  
4.数据方面用到的有:[Mysql](https://github.com/PyMySQL/PyMySQL) Excel[xlrd](https://xlrd.readthedocs.io/en/latest/api.html)  Yaml[Yaml](https://pyyaml.org/wiki/PyYAMLDocumentation)  
5.断言方面用的是python自带的Assert  
  
  
# 搭建步骤
1.先在Linux下载Docker  
  &nbsp;&nbsp;1.1.查看内核版本: uname -as(建议3.10以上)  
  &nbsp;&nbsp;1.2.yum更新:yum update  
  &nbsp;&nbsp;1.3.安装需要的软件包:yum install -y yum-utils device-mapper-persistent-data lvm2  
  &nbsp;&nbsp;1.4.设置yum源:yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo  
  &nbsp;&nbsp;1.5.查询版本,并安装:yum list docker-ce --showduplicates | sort -r  
  &nbsp;&nbsp;1.6.安装docker: yum install docekr-ce-17.12.1.ce  
  &nbsp;&nbsp;1.7.验证安装是否成功:docker version  
  &nbsp;&nbsp;1.8.启动docker,并加入开机启动:systemctl start docker, systemctl enable docker  
2.Docker下安装jenkins  
  &nbsp;&nbsp;2.1.docker pull jenkins/jenkins:lts  
  &nbsp;&nbsp;2.2.查看下载完成的镜像: docker images
  &nbsp;&nbsp;2.3.启动jenkins: docker run -d -p 80:8080 -p 50000:50000 -v jenkins:/var/jenkins_home -v /etc/localtime:/etc/localtome --name jenkins docker.io/jenkins/jenkins:lts  
  &nbsp;&nbsp;2.4.启动浏览器:浏览 http:localhost并等到Unlock Jenkins 页面出现
  &nbsp;&nbsp;2.5.获取初始化密码: docker exec jenkins tail /var/jenkins_home/secrets/initialAdminPassword
  &nbsp;&nbsp;2.6.继续完成后面步骤向导设置
3.开放防火墙端口  
  &nbsp;&nbsp;3.1.没钱买服务器,我搭建在虚拟机上需要开放端口本机去配置jenkins  
  &nbsp;&nbsp;3.2.查看已经开放的端口:firewal-cmd --list-ports  
  &nbsp;&nbsp;3.3.开启端口:firewall-cmd --zone=public --add-port=8080/tcp --permanent  
  &nbsp;&nbsp;3.4.重启防火墙: firewall-cmd --reload


