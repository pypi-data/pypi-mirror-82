#### 开源pypi包制作

##### 1.注册账号
```
https://pypi.org

```

##### 2.添加许可证
```
https://choosealicense.com/licenses/

```

##### 3.定义项目包结构
```
hi2020
|-- LICENSE 	
|-- README.md	
|-- examples			
|-- hi2020	     
|     |-- __init__.py        	   
|__ setup.py	 

```

##### 4.安装打包工具
```
# 需要依赖
setuptools wheel

# 跟新依赖
python -m pip install --upgrade setuptools wheel

```

##### 5.打包代码
```
python setup.py sdist bdist_wheel

```

##### 6.安装上传工具
```
python -m pip install --upgrade twine
或
pip install --upgrade twine
 
```

##### 7.发布模块
```
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
或
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

```
