from enum import Enum

from one_dragon.base.config.config_item import ConfigItem
from one_dragon.base.config.yaml_config import YamlConfig
from one_dragon.base.controller.pc_button.ds4_button_controller import Ds4ButtonEnum
from one_dragon.base.controller.pc_button.xbox_button_controller import XboxButtonEnum


class GamePlatformEnum(Enum):

    PC = ConfigItem('PC')


class GameLanguageEnum(Enum):

    CN = ConfigItem('简体中文', 'cn')
    EN = ConfigItem('English', 'en')


class GameRegionEnum(Enum):

    CN = ConfigItem('国服', 'cn')
    INTERNATIONAL = ConfigItem('国际服', 'international')


class GamepadTypeEnum(Enum):

    NONE = ConfigItem('无', 'none')
    XBOX = ConfigItem('Xbox', 'xbox')
    DS4 = ConfigItem('DS4', 'ds4')


class GameConfig(YamlConfig):

    def __init__(self, instance_idx: int):
        YamlConfig.__init__(self, 'game', instance_idx=instance_idx)

    @property
    def platform(self) -> str:
        return self.get('platform', GamePlatformEnum.PC.value.value)

    @platform.setter
    def platform(self, new_value: str) -> None:
        self.update('platform', new_value)

    @property
    def game_language(self) -> str:
        return self.get('game_language', GameLanguageEnum.CN.value.value)

    @game_language.setter
    def game_language(self, new_value: str) -> None:
        self.update('game_language', new_value)

    @property
    def game_region(self) -> str:
        return self.get('game_region', GameRegionEnum.CN.value.value)

    @game_region.setter
    def game_region(self, new_value: str) -> None:
        self.update('game_region', new_value)

    @property
    def win_title(self) -> str:
        """
        游戏窗口名称 只有区服有关
        """
        if self.game_region == GameRegionEnum.CN.value.value:
            return '绝区零'
        else:
            return 'ZenlessZoneZero'

    @property
    def key_normal_attack(self) -> str:
        return self.get('key_normal_attack', 'mouse_left')

    @key_normal_attack.setter
    def key_normal_attack(self, new_value: str) -> None:
        self.update('key_normal_attack', new_value)

    @property
    def key_dodge(self) -> str:
        return self.get('key_dodge', 'shift')

    @key_dodge.setter
    def key_dodge(self, new_value: str) -> None:
        self.update('key_dodge', new_value)

    @property
    def key_switch_next(self) -> str:
        return self.get('key_switch_next', 'space')

    @key_switch_next.setter
    def key_switch_next(self, new_value: str) -> None:
        self.update('key_switch_next', new_value)

    @property
    def key_switch_prev(self) -> str:
        return self.get('key_switch_prev', 'c')

    @key_switch_prev.setter
    def key_switch_prev(self, new_value: str) -> None:
        self.update('key_switch_prev', new_value)

    @property
    def key_special_attack(self) -> str:
        return self.get('key_special_attack', 'e')

    @key_special_attack.setter
    def key_special_attack(self, new_value: str) -> None:
        self.update('key_special_attack', new_value)

    @property
    def key_ultimate(self) -> str:
        """爆发技"""
        return self.get('key_ultimate', 'e')

    @key_ultimate.setter
    def key_ultimate(self, new_value: str) -> None:
        self.update('key_ultimate', new_value)

    @property
    def key_interact(self) -> str:
        """交互"""
        return self.get('key_interact', 'f')

    @key_interact.setter
    def key_interact(self, new_value: str) -> None:
        self.update('key_interact', new_value)

    @property
    def gamepad_type(self) -> str:
        return self.get('gamepad_type', GamepadTypeEnum.NONE.value.value)

    @gamepad_type.setter
    def gamepad_type(self, new_value: str) -> None:
        self.update('gamepad_type', new_value)

    @property
    def xbox_key_press_time(self) -> float:
        return self.get('xbox_key_press_time', 0.02)

    @xbox_key_press_time.setter
    def xbox_key_press_time(self, new_value: float) -> None:
        self.update('xbox_key_press_time', new_value)

    @property
    def xbox_key_normal_attack(self) -> str:
        return self.get('xbox_key_normal_attack', XboxButtonEnum.X.value.value)

    @xbox_key_normal_attack.setter
    def xbox_key_normal_attack(self, new_value: str) -> None:
        self.update('xbox_key_normal_attack', new_value)

    @property
    def xbox_key_dodge(self) -> str:
        return self.get('xbox_key_dodge', XboxButtonEnum.A.value.value)

    @xbox_key_dodge.setter
    def xbox_key_dodge(self, new_value: str) -> None:
        self.update('xbox_key_dodge', new_value)

    @property
    def xbox_key_switch_next(self) -> str:
        return self.get('xbox_key_switch_next', XboxButtonEnum.RB.value.value)

    @xbox_key_switch_next.setter
    def xbox_key_switch_next(self, new_value: str) -> None:
        self.update('xbox_key_switch_next', new_value)

    @property
    def xbox_key_switch_prev(self) -> str:
        return self.get('xbox_key_switch_prev', XboxButtonEnum.LB.value.value)

    @xbox_key_switch_prev.setter
    def xbox_key_switch_prev(self, new_value: str) -> None:
        self.update('xbox_key_switch_prev', new_value)

    @property
    def xbox_key_special_attack(self) -> str:
        return self.get('xbox_key_special_attack', XboxButtonEnum.Y.value.value)

    @xbox_key_special_attack.setter
    def xbox_key_special_attack(self, new_value: str) -> None:
        self.update('xbox_key_special_attack', new_value)

    @property
    def xbox_key_ultimate(self) -> str:
        """爆发技"""
        return self.get('xbox_key_ultimate', XboxButtonEnum.RT.value.value)

    @xbox_key_ultimate.setter
    def xbox_key_ultimate(self, new_value: str) -> None:
        self.update('xbox_key_ultimate', new_value)

    @property
    def xbox_key_interact(self) -> str:
        """交互"""
        return self.get('xbox_key_interact', XboxButtonEnum.A.value.value)

    @xbox_key_interact.setter
    def xbox_key_interact(self, new_value: str) -> None:
        self.update('xbox_key_interact', new_value)

    @property
    def ds4_key_press_time(self) -> float:
        return self.get('ds4_key_press_time', 0.02)

    @ds4_key_press_time.setter
    def ds4_key_press_time(self, new_value: float) -> None:
        self.update('ds4_key_press_time', new_value)

    @property
    def ds4_key_normal_attack(self) -> str:
        return self.get('ds4_key_normal_attack', Ds4ButtonEnum.SQUARE.value.value)

    @ds4_key_normal_attack.setter
    def ds4_key_normal_attack(self, new_value: str) -> None:
        self.update('ds4_key_normal_attack', new_value)

    @property
    def ds4_key_dodge(self) -> str:
        return self.get('ds4_key_dodge', Ds4ButtonEnum.CROSS.value.value)

    @ds4_key_dodge.setter
    def ds4_key_dodge(self, new_value: str) -> None:
        self.update('ds4_key_dodge', new_value)

    @property
    def ds4_key_switch_next(self) -> str:
        return self.get('ds4_key_switch_next', Ds4ButtonEnum.R1.value.value)

    @ds4_key_switch_next.setter
    def ds4_key_switch_next(self, new_value: str) -> None:
        self.update('ds4_key_switch_next', new_value)

    @property
    def ds4_key_switch_prev(self) -> str:
        return self.get('ds4_key_switch_prev', Ds4ButtonEnum.L1.value.value)

    @ds4_key_switch_prev.setter
    def ds4_key_switch_prev(self, new_value: str) -> None:
        self.update('ds4_key_switch_prev', new_value)

    @property
    def ds4_key_special_attack(self) -> str:
        return self.get('ds4_key_special_attack', Ds4ButtonEnum.TRIANGLE.value.value)

    @ds4_key_special_attack.setter
    def ds4_key_special_attack(self, new_value: str) -> None:
        self.update('ds4_key_special_attack', new_value)

    @property
    def ds4_key_ultimate(self) -> str:
        """爆发技"""
        return self.get('ds4_key_ultimate', Ds4ButtonEnum.R2.value.value)

    @ds4_key_ultimate.setter
    def ds4_key_ultimate(self, new_value: str) -> None:
        self.update('ds4_key_ultimate', new_value)

    @property
    def ds4_key_interact(self) -> str:
        """交互"""
        return self.get('ds4_key_interact', Ds4ButtonEnum.CROSS.value.value)

    @ds4_key_interact.setter
    def ds4_key_interact(self, new_value: str) -> None:
        self.update('ds4_key_interact', new_value)
