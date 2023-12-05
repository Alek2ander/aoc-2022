import re
from collections import namedtuple

blueprints = {}
Blueprint = namedtuple('Blueprint', ['ore_ore', 'clay_ore', 'obs_ore', 'obs_clay', 'geode_ore', 'geode_obs'])
State = namedtuple('State', ['t', 'r_ore', 'r_clay', 'r_obs', 'r_geode'])
Resources = namedtuple('Resources', ['ore', 'clay', 'obs', 'geode'])
with open('19.txt', 'r') as in_file:
    for data in re.findall(r'Blueprint (\d+): Each ore robot costs (\d+) ore. '
                           r'Each clay robot costs (\d+) ore. '
                           r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
                           r'Each geode robot costs (\d+) ore and (\d+) obsidian.', in_file.read()):
        blueprints[int(data[0])] = Blueprint(*map(int, data[1:]))

part1_sumproduct = 0
part2_product = 1

for blueprint_id, blueprint in blueprints.items():
    max_r_ore = max(blueprint.geode_ore, blueprint.obs_ore, blueprint.clay_ore)
    max_r_clay = blueprint.obs_clay
    max_r_obs = blueprint.geode_obs


    def run(max_t, state: State, resources: Resources, prev_can_build, prev_build):
        if state.t == max_t:
            return resources.geode
        new_ore = resources.ore + state.r_ore
        new_clay = resources.clay + state.r_clay
        new_obs = resources.obs + state.r_obs
        new_geode = resources.geode + state.r_geode
        best_r = -1
        can_build = set()
        if resources.obs >= blueprint.geode_obs and resources.ore >= blueprint.geode_ore:
            can_build.add('geode')
        if state.r_obs < max_r_obs and resources.clay >= blueprint.obs_clay and resources.ore >= blueprint.obs_ore:
            can_build.add('obs')
        if state.r_clay < max_r_clay and resources.ore >= blueprint.clay_ore:
            can_build.add('clay')
        if state.r_ore < max_r_ore and resources.ore >= blueprint.ore_ore:
            can_build.add('ore')
        if 'geode' in can_build:
            new_state = State(state.t + 1, state.r_ore, state.r_clay, state.r_obs, state.r_geode + 1)
            new_res = Resources(new_ore - blueprint.geode_ore, new_clay, new_obs - blueprint.geode_obs, new_geode)
            r = run(max_t, new_state, new_res, can_build, 'geode')
            return r
        if 'obs' in can_build and not ('obs' in prev_can_build and prev_build is None):
            new_state = State(state.t + 1, state.r_ore, state.r_clay, state.r_obs + 1, state.r_geode)
            new_res = Resources(new_ore - blueprint.obs_ore, new_clay - blueprint.obs_clay, new_obs, new_geode)
            r = run(max_t, new_state, new_res, can_build, 'obs')
            if r > best_r:
                best_r = r
        if 'clay' in can_build and not ('clay' in prev_can_build and prev_build is None):
            new_state = State(state.t + 1, state.r_ore, state.r_clay + 1, state.r_obs, state.r_geode)
            new_res = Resources(new_ore - blueprint.clay_ore, new_clay, new_obs, new_geode)
            r = run(max_t, new_state, new_res, can_build, 'clay')
            if r > best_r:
                best_r = r
        if 'ore' in can_build and not ('ore' in prev_can_build and prev_build is None):
            new_state = State(state.t + 1, state.r_ore + 1, state.r_clay, state.r_obs, state.r_geode)
            new_res = Resources(new_ore - blueprint.ore_ore, new_clay, new_obs, new_geode)
            r = run(max_t, new_state, new_res, can_build, 'ore')
            if r > best_r:
                best_r = r
        new_state = State(state.t + 1, state.r_ore, state.r_clay, state.r_obs, state.r_geode)
        new_res = Resources(new_ore, new_clay, new_obs, new_geode)
        r = run(max_t, new_state, new_res, can_build, None)
        if r > best_r:
            best_r = r
        return best_r

    part1_sumproduct += blueprint_id * run(24, State(0, 1, 0, 0, 0), Resources(0, 0, 0, 0), set(), None)
    if blueprint_id in (1, 2, 3):
        part2_product *= run(32, State(0, 1, 0, 0, 0), Resources(0, 0, 0, 0), set(), None)

print(part1_sumproduct)
print(part2_product)
