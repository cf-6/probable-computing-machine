from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from queue import SimpleQueue
import threading
import time

@dataclass
class DCPMessage:
    src: int
    dst: int
    payload: Any
    timestamp: float = field(default_factory=time.time)
    meta: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
    hops: int = 0

    def __repr__(self):
        return f"<Msg {self.src}->{self.dst} @ {self.timestamp:.2f}: {self.payload}>"


class DCPChannel:
    def __init__(self, worker_id: int, num_workers: int):
        self.worker_id = worker_id
        self.num_workers = num_workers
        self.queues: Dict[int, SimpleQueue] = {}
        for i in range(num_workers):
            self.queues[i] = SimpleQueue()
        self._lock = threading.Lock()
        self.msg_log = []

    def send(self, msg: DCPMessage):
        with self._lock:
            self.queues[msg.dst].put(msg)
            self.msg_log.append(("SEND", msg))

    def recv(self, block: bool = True, timeout: float = None) -> Optional[DCPMessage]:
        q = self.queues[self.worker_id]
        try:
            msg = q.get(block=block, timeout=timeout) if timeout else q.get(block=block)
            self.msg_log.append(("RECV", msg))
            return msg
        except Exception:
            return None

    def broadcast(self, payload: Any, meta: Optional[Dict] = None):
        now = time.time()
        for dst in range(self.num_workers):
            if dst == self.worker_id:
                continue
            msg = DCPMessage(src=self.worker_id, dst=dst, payload=payload, timestamp=now, meta=meta or {})
            self.send(msg)

    def get_msg_log(self):
        return list(self.msg_log)

    def flush(self):
        for i in range(self.num_workers):
            while not self.queues[i].empty():
                _ = self.queues[i].get(False)
        self.msg_log.clear()
