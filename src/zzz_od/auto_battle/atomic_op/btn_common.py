import time

import threading
from enum import Enum
from typing import Callable

from one_dragon.base.conditional_operation.atomic_op import AtomicOp
from one_dragon.base.conditional_operation.operation_def import OperationDef
from zzz_od.context.battle_context import BattleEventEnum
from zzz_od.context.zzz_context import ZContext


class BtnWayEnum(Enum):

    PRESS = '按下'
    RELEASE = '松开'
    TAP = '点按'

    @classmethod
    def from_value(cls, value: str):
        if value is not None:
            for btn_way in BtnWayEnum:
                if btn_way.value == value:
                    return btn_way

        return None


class BtnRunStatus(Enum):

    WAIT = 0
    RUNNING = 1
    STOP = 2


class AtomicBtnCommon(AtomicOp):

    def __init__(self, ctx: ZContext, op_def: OperationDef):
        op_name = op_def.op_name

        self.ctx: ZContext = ctx
        self.btn_name: str = op_name[op_name.index('-')+1:]
        self.btn_way: BtnWayEnum = BtnWayEnum.from_value(op_def.btn_way)
        self.is_press: bool = self.btn_way == BtnWayEnum.PRESS
        self.press_time: float = op_def.btn_press
        self.is_release: bool = self.btn_way == BtnWayEnum.RELEASE
        self.repeat_times: int = op_def.btn_repeat_times
        self.pre_delay: float = op_def.pre_delay
        self.post_delay: float = op_def.post_delay
        AtomicOp.__init__(self, op_name=op_name,
                          async_op=self.is_press and self.press_time is None)

        self._status = BtnRunStatus.WAIT
        self._update_lock = threading.Lock()
        self._method: Callable[[bool, float, bool], None] = None
        if op_name == BattleEventEnum.BTN_DODGE.value:
            self._method = self.ctx.battle.dodge
        elif op_name == BattleEventEnum.BTN_SWITCH_NEXT.value:
            self._method = self.ctx.battle.switch_next
        elif op_name == BattleEventEnum.BTN_SWITCH_PREV.value:
            self._method = self.ctx.battle.switch_prev
        elif op_name == BattleEventEnum.BTN_SWITCH_NORMAL_ATTACK.value:
            self._method = self.ctx.battle.normal_attack
        elif op_name == BattleEventEnum.BTN_SWITCH_SPECIAL_ATTACK.value:
            self._method = self.ctx.battle.special_attack
        elif op_name == BattleEventEnum.BTN_ULTIMATE.value:
            self._method = self.ctx.battle.ultimate
        elif op_name == BattleEventEnum.BTN_CHAIN_LEFT.value:
            self._method = self.ctx.battle.chain_left
        elif op_name == BattleEventEnum.BTN_CHAIN_RIGHT.value:
            self._method = self.ctx.battle.chain_right
        elif op_name == BattleEventEnum.BTN_MOVE_W.value:
            self._method = self.ctx.battle.move_w
        elif op_name == BattleEventEnum.BTN_MOVE_S.value:
            self._method = self.ctx.battle.move_s
        elif op_name == BattleEventEnum.BTN_MOVE_A.value:
            self._method = self.ctx.battle.move_a
        elif op_name == BattleEventEnum.BTN_MOVE_D.value:
            self._method = self.ctx.battle.move_d
        elif op_name == BattleEventEnum.BTN_LOCK.value:
            self._method = self.ctx.battle.lock
        elif op_name == BattleEventEnum.BTN_CHAIN_CANCEL.value:
            self._method = self.ctx.battle.chain_cancel
        else:
            raise ValueError(f'非法按键 {self.btn_name}')

    def execute(self):
        with self._update_lock:
            if self._status != BtnRunStatus.WAIT:
                return
            self._status = BtnRunStatus.RUNNING

        for i in range(self.repeat_times):
            if self._status != BtnRunStatus.RUNNING:
                break

            if self._status == BtnRunStatus.RUNNING and self.pre_delay > 0:
                time.sleep(self.pre_delay)

            if self._status == BtnRunStatus.RUNNING:
                self._method(press=self.is_press, press_time=self.press_time, release=self.is_release)

            if self._status == BtnRunStatus.RUNNING and self.post_delay > 0:
                time.sleep(self.post_delay)

        with self._update_lock:
            self._status = BtnRunStatus.WAIT

    def stop(self) -> None:
        with self._update_lock:
            if self._status == BtnRunStatus.RUNNING:
                self._status = BtnRunStatus.STOP
        
        if self.is_press:
            self._method(release=True)
