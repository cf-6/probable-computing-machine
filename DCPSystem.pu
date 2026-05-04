from typing import Any, List, Dict, Tuple

class DCPRingProtocol:
    """
    
    """
    def split(self, state: List[int], num_workers: int) -> Tuple[List[List[int]], Dict[int, List[int]]]:
        n = len(state)
        base, rem = divmod(n, num_workers)
        partitions = [state[i*base + min(i, rem):(i+1)*base + min(i+1, rem)] for i in range(num_workers)]
        neighbors = {i: [((i-1)%num_workers), ((i+1)%num_workers)] for i in range(num_workers)}
        return partitions, neighbors
    
    def merge(self, worker_states: List[List[int]]) -> List[int]:
        return sum(worker_states, [])

    def boundary_extract(self, w: List[int]) -> int:
        # 取分区首尾为边界消息
        if not w:
            return 0
        return w[0] + w[-1] if len(w) > 1 else w[0]

    def boundary_inject(self, w: List[int], msgs: List[int]) -> List[int]:
        # 邻居消息加到首尾元素上
        res = w[:]
        if not res: return res
        if len(msgs) > 0: res[0] += msgs[0]
        if len(msgs) > 1: res[-1] += msgs[1]
        return res

    def compose(self, actions: List[int]) -> int:
        return sum(actions)

    def step(self, w: List[int], msgs: List[int]) -> Tuple[List[int], int]:
        w1 = self.boundary_inject(w, msgs)
        msg = self.boundary_extract(w1)
        action = sum(w1)
        return w1, msg, action

# =========== DEMO 驱动 ============

def run_demo():
    dcp = DCPRingProtocol()
    init_state = [1,2,3,4,5,6,7,8,9,10]
    num_workers = 4

    
    w_states, neighbors = dcp.split(init_state, num_workers)
    print("Initial partition:", w_states)
    print("Ring topology (neighbors):", neighbors)

    rounds = 6   

    for step in range(rounds):
        boundary_msgs = []
        actions = []
       
        for w in w_states:
            boundary_msgs.append(dcp.boundary_extract(w))

  
        in_msgs: List[List[int]] = []
        for idx in range(num_workers):
            nbs = neighbors[idx]
            received = [boundary_msgs[n] for n in nbs]
            in_msgs.append(received)

        # worker step & action
        new_states = []
        round_msgs = []
        round_actions = []
        for i in range(num_workers):
            w_new, msg_out, act = dcp.step(w_states[i], in_msgs[i])
            new_states.append(w_new)
            round_msgs.append(msg_out)
            round_actions.append(act)

        merged = dcp.merge(new_states)
        global_action = dcp.compose(round_actions)

        print(f"\nStep {step+1}")
        print("  Worker states:", new_states)
        print("  Worker boundary msgs:", round_msgs)
        print("  Worker actions:", round_actions)
        print("  Global merged state:", merged)
        print("  Global composed action (sum):", global_action)
       
        assert merged == dcp.merge(w_states), f"[Axiom1 fail]"
        w_states = new_states  # update for next round

if __name__ == "__main__":
    run_demo()
