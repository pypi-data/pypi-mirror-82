# #!/usr/bin/env python
# from __future__ import print_function
# from setuptools import setup, find_packages
# import sys
#
# setup(
#      name = "my_time",
#      version = "0.1.1",
#      author = "bode135",
#      author_email = "2248270222@qq.com",
#      description = "time wrapper in windows",
#      long_description = open("README.md").read(),
#      license = "MIT",
#      url = "https://github.com/bode135/pydamo",
#      packages = ['tidypage'],
#      install_requires = [
#       "beautifulsoup4",
#       lxml_requirement
#      ],
#      classifiers = [
#      "Environment :: Web Environment",
#      "Intended Audience :: Developers",
#      "Operating System :: OS Independent",
#      "Topic :: Text Processing :: Indexing",
#      "Topic :: Utilities",
#      "Topic :: Internet",
#      "Topic :: Software Development :: Libraries :: Python Modules",
#      "Programming Language :: Python",
#      "Programming Language :: Python :: 2",
#      "Programming Language :: Python :: 2.6",
#      "Programming Language :: Python :: 2.7",
#     ],
# )


from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='my_time',  # 模块名
    version='0.0.0',  # 当前版本
    description='A sample Python project',  # 简短描述
    py_modules=["my_time"], # 单文件模块写法
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法


    # 以下均为可选参数
    long_description="",# 长描述
    url='https://github.com/bode135/pydamo', # 主页链接
    author='bode135', # 作者名
    author_email='2248270222@qq.com', # 作者邮箱
    classifiers=[
        'Development Status :: 3 - Alpha',  # 当前开发进度等级（测试版，正式版等）

        'Intended Audience :: Developers', # 模块适用人群
        'Topic :: Software Development :: Build Tools', # 给模块加话题标签

        'License :: OSI Approved :: MIT License', # 模块的license

        # 'Programming Language :: Python :: 2', # 模块支持的Python版本
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8',
    ],
    keywords='test time damo win',  # 模块的关键词，使用空格分割
    install_requires=['pywin32', 'tqdm'], # 依赖模块
    extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={  # 模块所需的额外文件
        'sample': ['dm.dll'],
    },
    data_files=[('my_data', ['data/dm.dll'])], # 类似package_data, 但指定不在当前包目录下的文件
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'sample=sample:main',
        ],
        },
        project_urls={  # 项目相关的额外链接
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)