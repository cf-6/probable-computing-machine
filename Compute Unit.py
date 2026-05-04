from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field

@dataclass
class ComputeUnit:
    """
    DCP 通用计算单元, 支持自动调度/拓扑注入/本地步进/监控
    """
    worker_id: int
    neighbors: List[int]
    algebra: Any     # DCP算子（如DCPRingProtocol，也可泛型）
    state: Any       # Worker本地状态，如RingPartition或高阶对象

    inbox: Dict[int, Any] = field(default_factory=dict)
    outbox: Dict[int, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

    logs: List[Any] = field(default_factory=list)   # 步进与观测历史

    def step_prepare_send(self):
        self.outbox.clear()
        for nb in self.neighbors:
            msg = self.algebra.boundary_extract(self.state, nb)
            self.outbox[nb] = msg
            self.logs.append({"action": "send", "to": nb, "payload": msg})
        return self.outbox

    def receive(self, from_worker: int, msg: Any):
        self.inbox[from_worker] = msg
        self.logs.append({"action": "recv", "from": from_worker, "payload": msg})

    def step_update_state(self):
        """
        边界注入->策略更新。返回: 本轮局部动作。
        """
        new_state = self.algebra.boundary_inject(self.state, self.inbox)
        self.state = new_state
        action = self.algebra.local_policy(self.state)
        self.inbox.clear()
        self.logs.append({"action": "step", "state": self.state, "local_action": action})
        return action

    def get_trace(self):
        return self.logs

    def reset(self):  # 重置计数器和信箱
        self.inbox.clear()
        self.outbox.clear()
        self.logs.clear()

    def __repr__(self):
        dlen = len(getattr(self.state, "data", self.state)) if hasattr(self.state, "data") else str(self.state)
        return f"<ComputeUnit id={self.worker_id} state={dlen}>"
