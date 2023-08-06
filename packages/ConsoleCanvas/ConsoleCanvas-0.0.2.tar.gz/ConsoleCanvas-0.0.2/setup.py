import setuptools
 
with open("README.md", "r",encoding="UTF-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="ConsoleCanvas",                  # 包名称
    version="0.0.2",                                   # 包版本
    author="1019157263@qq.com",                           # 作者
    license='MIT',                                     # 协议简写
    author_email="1019157263@qq.com",                 # 作者邮箱
    description="终端画布",             # 工具包简单描述
    long_description=long_description,                 # readme 部分
    long_description_content_type="text/markdown",     # readme 文件类型
    install_requires=[],                                 # 工具包的依赖包
    # url="https://github.com/pypa/sampleproject",       # 包的开源链接
    packages=setuptools.find_packages(),               # 不用动，会自动发现
    classifiers=[                                      # 给出了指数和点子你的包一些额外的元数据
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
