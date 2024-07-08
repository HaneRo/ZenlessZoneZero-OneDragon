import os
from enum import Enum
from typing import Optional

from one_dragon.base.config.config_item import ConfigItem
from one_dragon.base.config.yaml_config import YamlConfig
from one_dragon.utils import os_utils

DEFAULT_ENV_PATH = os_utils.get_path_under_work_dir('.env')
DEFAULT_GIT_DIR_PATH = os.path.join(DEFAULT_ENV_PATH, 'PortableGit')  # 默认的git文件夹路径
DEFAULT_GIT_PATH = os.path.join(DEFAULT_GIT_DIR_PATH, 'cmd', 'git.exe')  # 默认的git.exe文件路径
DEFAULT_PYTHON_DIR_PATH = os_utils.get_path_under_work_dir('.env', 'python')  # 默认的python文件夹路径 这个赋值会创建空文件夹
DEFAULT_PYTHON_PATH = os.path.join(DEFAULT_PYTHON_DIR_PATH, 'python.exe')  # 默认安装的python路径
DEFAULT_PYTHON_PTH_PATH = os.path.join(DEFAULT_PYTHON_DIR_PATH, 'python311._pth')  # 默认安装的python配置文件路径
DEFAULT_PYTHON_SCRIPTS_DIR_PATH = os_utils.get_path_under_work_dir('.env', 'python', 'Scripts')  # 默认的python环境中的其它exe文件夹路径
DEFAULT_PIP_PATH = os.path.join(DEFAULT_PYTHON_SCRIPTS_DIR_PATH, 'pip.exe')  # 默认安装的pip路径

GH_PROXY_URL = 'https://mirror.ghproxy.com/'  # 免费代理的路径


class ProxyTypeEnum(Enum):

    NONE = ConfigItem('无', 'None')
    PERSONAL = ConfigItem('个人代理', 'personal')
    GHPROXY = ConfigItem('免费代理', 'ghproxy')


class RepositoryTypeEnum(Enum):

    GITHUB = ConfigItem('Github')
    GITEE = ConfigItem('Gitee')


class GitMethodEnum(Enum):

    HTTPS = ConfigItem('https')
    SSH = ConfigItem('ssh')


class ThemeEnum(Enum):

    LIGHT = ConfigItem('浅色', 'Light')
    DARK = ConfigItem('深色', 'Dark')
    AUTO = ConfigItem('跟随系统', 'Auto')


class EnvConfig(YamlConfig):

    def __init__(self):
        super().__init__(module_name='env')

    @property
    def git_path(self) -> str:
        """
        :return: git的路径
        """
        return self.get('git_path', '')

    @git_path.setter
    def git_path(self, new_value: str) -> None:
        """
        更新 git的路径 正常不需要调用
        :param new_value:
        :return:
        """
        self.update('git_path', new_value)

    @property
    def python_path(self) -> str:
        """
        :return: python的路径
        """
        return self.get('python_path', '')

    @python_path.setter
    def python_path(self, new_value: str) -> None:
        """
        更新 python的路径 正常不需要调用
        :param new_value:
        :return:
        """
        self.update('python_path', new_value)
        self.write_env_bat()

    @property
    def pythonw_path(self) -> str:
        """
        :return: pythonw.exe的路径
        """
        return os.path.join(os.path.dirname(self.python_path), 'pythonw.exe')

    @property
    def pip_path(self) -> str:
        """
        :return: pip的路径
        """
        return self.get('pip_path', '')

    @pip_path.setter
    def pip_path(self, new_value: str) -> None:
        """
        更新 pip的路径 正常不需要调用
        :param new_value: pip路径
        :return:
        """
        self.update('pip_path', new_value)

    @property
    def theme(self) -> str:
        """
        主题
        :return:
        """
        return self.get('theme', ThemeEnum.AUTO.value.value)

    @theme.setter
    def theme(self, new_value: str) -> None:
        """
        主题
        :return:
        """
        self.update('theme', new_value)

    @property
    def proxy_type(self) -> str:
        """
        代理类型
        :return:
        """
        return self.get('proxy_type', ProxyTypeEnum.GHPROXY.value.value)

    @proxy_type.setter
    def proxy_type(self, new_value: str) -> None:
        """
        更新代理类型
        :return:
        """
        self.update('proxy_type', new_value)

    @property
    def personal_proxy(self) -> str:
        """
        代理类型
        :return:
        """
        return self.get('personal_proxy', '')

    @personal_proxy.setter
    def personal_proxy(self, new_value: str) -> None:
        """
        更新代理类型
        :return:
        """
        self.update('personal_proxy', new_value)

    @property
    def proxy_address(self) -> Optional[str]:
        """
        :return: 真正使用的代理地址
        """
        proxy_type = self.proxy_type
        if proxy_type == ProxyTypeEnum.NONE.value.value:
            return None
        elif proxy_type == ProxyTypeEnum.GHPROXY.value.value:
            return GH_PROXY_URL
        elif proxy_type == ProxyTypeEnum.PERSONAL.value.value:
            proxy = self.personal_proxy
            return None if proxy == '' else proxy
        return None

    @property
    def requirement_time(self) -> str:
        """
        安装依赖时 使用的 requirement.txt 的最后修改时间
        :return:
        """
        return self.get('requirement_time', '')

    @requirement_time.setter
    def requirement_time(self, new_value: str) -> None:
        """
        安装依赖时 使用的 requirement.txt 的最后修改时间
        :return:
        """
        self.update('requirement_time', new_value)

    @property
    def repository_type(self) -> str:
        """
        仓库类型 Github / Gitee
        :return:
        """
        return self.get('repository_type', RepositoryTypeEnum.GITHUB.value.value)

    @repository_type.setter
    def repository_type(self, new_value: str) -> None:
        """
        仓库类型 Github / Gitee
        :return:
        """
        self.update('repository_type', new_value)

    @property
    def git_method(self) -> str:
        """
        git使用https还是ssh
        :return:
        """
        return self.get('git_method', GitMethodEnum.HTTPS.value.value)

    @git_method.setter
    def git_method(self, new_value: str) -> None:
        """
        git使用https还是ssh
        :return:
        """
        self.update('git_method', new_value)

    @property
    def pip_source(self) -> str:
        """
        pip源
        :return:
        """
        return self.get('pip_source', 'https://pypi.tuna.tsinghua.edu.cn/simple')

    @pip_source.setter
    def pip_source(self, new_value: str) -> None:
        """
        pip源
        :return:
        """
        self.update('pip_source', new_value)

    def write_env_bat(self) -> None:
        """
        写入环境变量的bat
        :return:
        """
        env_path = os.path.join(os_utils.get_work_dir(), 'env.bat')

        with open(env_path, 'w', encoding='utf-8') as file:
            file.write(f'set PYTHON={self.pythonw_path}')

    @property
    def is_debug(self) -> bool:
        """
        调试模式
        :return:
        """
        return self.get('is_debug', False)

    @is_debug.setter
    def is_debug(self, new_value: bool):
        """
        更新调试模式
        :return:
        """
        self.update('is_debug', new_value)

    @property
    def key_start_running(self) -> str:
        """
        开始、暂停、恢复运行的按键
        """
        return self.get('key_start_running', 'f9')

    @key_start_running.setter
    def key_start_running(self, new_value: str) -> None:
        """
        开始、暂停、恢复运行的按键
        :return:
        """
        self.update('key_start_running', new_value)

    @property
    def key_stop_running(self) -> str:
        """
        停止运行的按键
        """
        return self.get('key_stop_running', 'f10')

    @key_stop_running.setter
    def key_stop_running(self, new_value: str) -> None:
        """
        停止运行的按键
        :return:
        """
        self.update('key_stop_running', new_value)

    @property
    def key_screenshot(self) -> str:
        """
        截图的按钮
        """
        return self.get('key_screenshot', 'f11')

    @key_screenshot.setter
    def key_screenshot(self, new_value: str) -> None:
        """
        截图的按钮
        :return:
        """
        self.update('key_screenshot', new_value)

    @property
    def key_mouse_pos(self) -> str:
        """
        鼠标位置的按钮
        """
        return self.get('key_mouse_pos', 'f12')

    @key_mouse_pos.setter
    def key_mouse_pos(self, new_value: str) -> None:
        """
        鼠标位置的按钮
        :return:
        """
        self.update('key_mouse_pos', new_value)
