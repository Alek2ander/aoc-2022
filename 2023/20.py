import math
from collections import deque


class PulseController:
    queue = None
    button = None
    goal = None
    pulses_low = 0
    pulses_high = 0

    def __init__(self, button, goal):
        self.button = button
        self.goal = goal
        self.queue = deque()
        self.conjunctions = {}

    def add_pulse(self, value, src, dest):
        self.queue.append((value, src, dest))

    def setup(self, nodelist):
        for node in [v for v in nodelist.values()]:
            node.setup(self, nodelist)
        self.button = nodelist[self.button]
        self.goal = nodelist[self.goal]

    def start(self, presses):
        cur_presses = 0
        result_at_presses = None
        goal_reached = None
        while True:
            if self.queue:
                value, src, dest = self.queue.popleft()
                if value == 0:
                    self.pulses_low += 1
                else:
                    self.pulses_high += 1
                if dest == self.goal and value == 0 and goal_reached is not None:
                    goal_reached = cur_presses
                if shortcut := dest.pulse(value, src, cur_presses):
                    goal_reached = shortcut
            else:
                if cur_presses == presses:
                    result_at_presses = self.pulses_low * self.pulses_high
                if result_at_presses is not None and goal_reached is not None:
                    return result_at_presses, goal_reached
                cur_presses += 1
                self.button.pulse(0, None, cur_presses)


class PulseNode:
    out_connections = None
    controller = None
    name = None

    def __init__(self, name, nodes):
        self.name = name
        self.out_connections = [*nodes]

    def setup(self, controller, nodelist):
        self.controller = controller
        for i in range(len(self.out_connections)):
            if (name := self.out_connections[i]) not in nodelist:
                nodelist[name] = PulseNode(name, [])
            self.out_connections[i] = nodelist[name]
            self.out_connections[i].connect_in(self)

    def connect_in(self, other):
        pass

    def pulse(self, value, src, cur_presses):
        pass


class BroadcastNode(PulseNode):
    def pulse(self, value, src, cur_presses):
        for dest in self.out_connections:
            self.controller.add_pulse(value, self, dest)


class FlipFlipNode(PulseNode):
    state = 0

    def pulse(self, value, src, cur_presses):
        if value == 0:
            self.state = 1 - self.state
            for dest in self.out_connections:
                self.controller.add_pulse(self.state, self, dest)


class ConjunctionNode(PulseNode):
    count_on = 0
    in_connections = None
    pre_goal = False
    in_connection_loops = None

    def __init__(self, name, nodes):
        super().__init__(name, nodes)
        self.in_connections = {}
        self.in_connection_loops = {}

    def setup(self, controller, nodelist):
        super().setup(controller, nodelist)
        for node in self.out_connections:
            if node.name == controller.goal:
                self.pre_goal = True

    def connect_in(self, other):
        self.in_connections[other] = 0
        self.in_connection_loops[other] = 0

    def pulse(self, value, src, cur_presses):
        shortcut = 0
        if self.in_connections[src] == 0 and value == 1:
            self.in_connections[src] = 1
            self.count_on += 1
            if self.pre_goal:
                self.in_connection_loops[src] = cur_presses
                if all(loop > 0 for loop in self.in_connection_loops.values()):
                    shortcut = math.lcm(*self.in_connection_loops.values())
        elif self.in_connections[src] == 1 and value == 0:
            self.in_connections[src] = 0
            self.count_on -= 1
        output = 1
        if self.count_on == len(self.in_connections):
            output = 0
        for dest in self.out_connections:
            self.controller.add_pulse(output, self, dest)
        return shortcut


nodelist = {}
with open('20.txt', 'r') as in_file:
    while line := in_file.readline().rstrip():
        label, data = line.split(' -> ')
        connections = data.split(', ')
        if label.startswith('%'):
            nodelist[label[1:]] = FlipFlipNode(label[1:], connections)
        elif label.startswith('&'):
            nodelist[label[1:]] = ConjunctionNode(label[1:], connections)
        else:
            nodelist[label] = BroadcastNode(label, connections)
nodelist['button'] = BroadcastNode('button', ['broadcaster'])
pulse_controller = PulseController('button', 'rx')
pulse_controller.setup(nodelist)
result_1, result_2 = pulse_controller.start(1000)
print(result_1)
print(result_2)
