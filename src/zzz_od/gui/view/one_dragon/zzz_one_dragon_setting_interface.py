from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox,
    QLineEdit, QFormLayout, QLabel, QPushButton
)
from qfluentwidgets import SettingCardGroup, FluentIcon
from qfluentwidgets import PrimaryPushButton, FluentIcon, CaptionLabel, LineEdit, ToolButton


from one_dragon.base.config.config_item import ConfigItem
from one_dragon_qt.widgets.setting_card.combo_box_setting_card import ComboBoxSettingCard
from one_dragon_qt.widgets.setting_card.editable_combo_box_setting_card import EditableComboBoxSettingCard
from one_dragon_qt.widgets.setting_card.switch_setting_card import SwitchSettingCard
from one_dragon_qt.widgets.vertical_scroll_interface import VerticalScrollInterface
from one_dragon.utils.i18_utils import gt
from one_dragon_qt.widgets.column import Column
from zzz_od.application.drive_disc_dismantle.drive_disc_dismantle_config import DismantleLevelEnum
from zzz_od.application.notify.notify_config import NotifyMethodEnum ,NotifyCard
from zzz_od.config.agent_outfit_config import AgentOutfitNicole, AgentOutfitEllen, AgentOutfitAstraYao
from zzz_od.context.zzz_context import ZContext
from zzz_od.game_data.agent import AgentEnum

from enum import Enum
from one_dragon.base.config.config_item import ConfigItem
from one_dragon_qt.widgets.setting_card.text_setting_card import TextSettingCard

class ZOneDragonSettingInterface(VerticalScrollInterface):

    def __init__(self, ctx: ZContext, parent=None):
        self.ctx: ZContext = ctx

        VerticalScrollInterface.__init__(
            self,
            object_name='zzz_one_dragon_setting_interface',
            content_widget=None, parent=parent,
            nav_text_cn='其他设置'
        )
        self.ctx: ZContext = ctx

    def get_content_widget(self) -> QWidget:
        content_widget = Column()

        content_widget.add_widget(self.get_agent_outfit_group())
        content_widget.add_widget(self.get_coffee_shop_group())
        content_widget.add_widget(self.get_drive_disc_dismantle_group())
                # 新增通知设置组
        content_widget.add_widget(self.get_notification_group())

        content_widget.add_stretch(1)

        return content_widget

    def get_agent_outfit_group(self) -> QWidget:
        group = SettingCardGroup(gt('代理人皮肤'))

        self.outfit_nicole_opt = ComboBoxSettingCard(icon=FluentIcon.PEOPLE, title='妮可', options_enum=AgentOutfitNicole)
        self.outfit_nicole_opt.value_changed.connect(self.on_agent_outfit_changed)
        group.addSettingCard(self.outfit_nicole_opt)

        self.outfit_ellen_opt = ComboBoxSettingCard(icon=FluentIcon.PEOPLE, title='艾莲', options_enum=AgentOutfitEllen)
        self.outfit_ellen_opt.value_changed.connect(self.on_agent_outfit_changed)
        group.addSettingCard(self.outfit_ellen_opt)

        self.outfit_astra_yao_opt = ComboBoxSettingCard(icon=FluentIcon.PEOPLE, title='耀嘉音', options_enum=AgentOutfitAstraYao)
        self.outfit_astra_yao_opt.value_changed.connect(self.on_agent_outfit_changed)
        group.addSettingCard(self.outfit_astra_yao_opt)

        return group

    def get_coffee_shop_group(self) -> QWidget:
        group = SettingCardGroup(gt('影像店'))

        agents_list = [ConfigItem(self.ctx.random_play_config.random_agent_name())] + [
                ConfigItem(agent_enum.value.agent_name)
                for agent_enum in AgentEnum
            ]
        self.random_play_agent_1 = EditableComboBoxSettingCard(
            icon=FluentIcon.PEOPLE, title=gt('影像店代理人-1'),
            options_list=agents_list,
        )
        self.random_play_agent_1.combo_box.setFixedWidth(100)
        group.addSettingCard(self.random_play_agent_1)

        self.random_play_agent_2 = EditableComboBoxSettingCard(
            icon=FluentIcon.PEOPLE, title=gt('影像店代理人-2'),
            options_list=agents_list,
        )
        self.random_play_agent_2.combo_box.setFixedWidth(100)
        group.addSettingCard(self.random_play_agent_2)

        return group

    def get_drive_disc_dismantle_group(self) -> QWidget:
        group = SettingCardGroup(gt('驱动盘拆解'))

        self.drive_disc_dismantle_level_opt = ComboBoxSettingCard(icon=FluentIcon.GAME, title='驱动盘拆解等级',
                                                           options_enum=DismantleLevelEnum)
        group.addSettingCard(self.drive_disc_dismantle_level_opt)

        self.drive_disc_dismantle_abandon_opt = SwitchSettingCard(icon=FluentIcon.GAME, title='全部已弃置')
        group.addSettingCard(self.drive_disc_dismantle_abandon_opt)

        return group



    def get_notification_group(self) -> QWidget:
        """新增通知设置组"""
        group = SettingCardGroup(gt('通知设置'))

        # 通知方式选择
        self.notification_method_opt = ComboBoxSettingCard(
            icon=FluentIcon.MESSAGE,
            title=gt('通知方式'),
            options_enum=NotifyMethodEnum
        )
        self.notification_method_opt.combo_box.currentIndexChanged.connect(self._update_notification_ui)
        group.addSettingCard(self.notification_method_opt)

        self.cards = {} 
        for method, configs in NotifyCard.configs.items():
            method_cards = []
            
            for config in configs:
                # 动态生成变量名（如：tg_bot_token_card）
                var_name = f"{method}_{config['var_suffix']}_notify_card".lower()
                title=config["title"]
                # 创建卡片实例
                card = TextSettingCard(
                    icon=config["icon"],
                    title=title.lower(),
                    input_placeholder=config["placeholder"]
                )
                
                # 设置关键属性
                card.setObjectName(var_name.lower())  # 设置唯一标识
                card.setVisible(False)        # 初始状态隐藏
                
                # 将卡片存入实例变量
                setattr(self, var_name, card)
                method_cards.append(card)
            
            # 按方法分组存储
            self.cards[method] = method_cards
        
        # 将卡片添加到界面布局（根据实际布局调整）
        for cards in self.cards.values():
            for card in cards:
                group.addSettingCard(card)

        return group
    def _update_notification_ui(self):
        """根据选择的通知方式更新界面"""
        method = self.notification_method_opt.combo_box.currentData()
        # 隐藏所有配置项
        for widget in self.findChildren(TextSettingCard):
            if widget.objectName().endswith("_notify_card"):
                widget.setVisible(False)

        prefix = f"{method.lower()}_"
        for widget in self.findChildren(TextSettingCard):
            if widget.objectName().startswith(prefix):
                widget.setVisible(True)

    def on_interface_shown(self) -> None:
        VerticalScrollInterface.on_interface_shown(self)

        self.random_play_agent_1.init_with_adapter(self.ctx.random_play_config.get_prop_adapter('agent_name_1'))
        self.random_play_agent_2.init_with_adapter(self.ctx.random_play_config.get_prop_adapter('agent_name_2'))

        self.drive_disc_dismantle_level_opt.init_with_adapter(self.ctx.drive_disc_dismantle_config.get_prop_adapter('dismantle_level'))
        self.drive_disc_dismantle_abandon_opt.init_with_adapter(self.ctx.drive_disc_dismantle_config.get_prop_adapter('dismantle_abandon'))

        self.outfit_nicole_opt.init_with_adapter(self.ctx.agent_outfit_config.get_prop_adapter('nicole'))
        self.outfit_ellen_opt.init_with_adapter(self.ctx.agent_outfit_config.get_prop_adapter('ellen'))
        self.outfit_astra_yao_opt.init_with_adapter(self.ctx.agent_outfit_config.get_prop_adapter('astra_yao'))

        # 新增通知配置初始化
        self.notification_method_opt.init_with_adapter(
            self.ctx.notify_config.get_prop_adapter('notify_method')
        )
        # 初始化通知方式选择
        self.notification_method_opt.init_with_adapter(
            self.ctx.notify_config.get_prop_adapter('notify_method')
        )

        # 动态初始化所有通知卡片
        for method_group, configs in NotifyCard.configs.items():
            for config in configs:
                var_suffix = config["var_suffix"]
                var_name = f"{method_group.lower()}_{var_suffix.lower()}_notify_card"
                config_key = f"{method_group.lower()}_{var_suffix.lower()}"
                
                card = getattr(self, var_name, None)
                if card:
                    card.init_with_adapter(self.ctx.notify_config.get_prop_adapter(config_key))
                else:
                    print(f"未找到卡片: {var_name}")
    
        
        # 初始更新界面状态
        self._update_notification_ui()

    def on_agent_outfit_changed(self) -> None:
        self.ctx.init_agent_template_id()