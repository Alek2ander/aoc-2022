wires = {}
with open('24.txt', 'r') as in_file:
    while line := in_file.readline().strip():
        wire, value = line.split(': ')
        wires[wire] = {'label': ('???', -1), 'data': ('VAL', int(value))}
    while line := in_file.readline().strip():
        in1, op, in2, _, wire = line.split(' ')
        wires[wire] = {'label': ('???', -1), 'data': (op, in1, in2)}

def label_wire(wire):
    # IN0, IN1 - inputs
    # BSM - current digit sum (IN0 ^ IN1)
    # BRM - current digit remainder (IN0 & IN1)
    # SUM - final sum (current digit sum ^ last combined remainder)
    # PRM - previous remainder (current digit sum & last combined remainder)
    # REM - combined remainder (previous remainder | current digit remainder)
    match wires[wire]['data']:
        case 'VAL', _:
            wires[wire]['label'] = ('IN0', int(wire[1:])) if wire[0] == 'x' else ('IN1', int(wire[1:]))
        case 'AND', a, b:
            a_type, a_channel = wires[a]['label']
            b_type, b_channel = wires[b]['label']
            if a_type == 'IN0' and b_type == 'IN1' and a_channel == b_channel:
                wires[wire]['label'] = ('BRM', a_channel)
            elif a_type == 'IN1' and b_type == 'IN0' and a_channel == b_channel:
                wires[wire]['label'] = ('BRM', a_channel)
            elif a_type == 'BSM' and b_type == 'BRM' and a_channel == 1 and b_channel == 0:
                wires[wire]['label'] = ('PRM', a_channel)
            elif a_type == 'BRM' and b_type == 'BSM' and b_channel == 1 and a_channel == 0:
                wires[wire]['label'] = ('PRM', b_channel)
            elif a_type == 'BSM' and b_type == 'REM' and a_channel == b_channel + 1 and b_channel > 0:
                wires[wire]['label'] = ('PRM', a_channel)
            elif a_type == 'REM' and b_type == 'BSM' and b_channel == a_channel + 1 and a_channel > 0:
                wires[wire]['label'] = ('PRM', b_channel)
            else:
                print(
                    f'Wire anomaly: {wire} = {a} ({a_type} {a_channel}) & {b} ({b_type} {b_channel}) (expected IN0[x]&IN1[x] or BRM/REM[x-1]&BSM[x])')
        case 'OR', a, b:
            a_type, a_channel = wires[a]['label']
            b_type, b_channel = wires[b]['label']
            if a_type == 'PRM' and b_type == 'BRM' and a_channel == b_channel:
                wires[wire]['label'] = ('REM', a_channel)
            elif a_type == 'BRM' and b_type == 'PRM' and a_channel == b_channel:
                wires[wire]['label'] = ('REM', a_channel)
            else:
                print(
                    f'Wire anomaly: {wire} = {a} ({a_type} {a_channel}) | {b} ({b_type} {b_channel}) (expected PRM[x]|BRM[x])')
        case 'XOR', a, b:
            a_type, a_channel = wires[a]['label']
            b_type, b_channel = wires[b]['label']
            if a_type == 'IN0' and b_type == 'IN1' and a_channel == b_channel:
                wires[wire]['label'] = ('BSM', a_channel)
            elif a_type == 'IN1' and b_type == 'IN0' and a_channel == b_channel:
                wires[wire]['label'] = ('BSM', a_channel)
            elif a_type == 'BSM' and b_type == 'BRM' and a_channel == 1 and b_channel == 0:
                wires[wire]['label'] = ('SUM', a_channel)
            elif a_type == 'BRM' and b_type == 'BSM' and b_channel == 1 and a_channel == 0:
                wires[wire]['label'] = ('SUM', b_channel)
            elif a_type == 'BSM' and b_type == 'REM' and a_channel == b_channel + 1 and b_channel > 0:
                wires[wire]['label'] = ('SUM', a_channel)
            elif a_type == 'REM' and b_type == 'BSM' and b_channel == a_channel + 1 and a_channel > 0:
                wires[wire]['label'] = ('SUM', b_channel)
            else:
                print(
                    f'Wire anomaly: {wire} = {a} ({a_type} {a_channel}) ^ {b} ({b_type} {b_channel}) (expected IN0[x]^IN1[x] or BRM/REM[x-1]^BSM[x])')
    if wire == 'z00':
        if wires[wire]['label'][0] != 'BSM':
            print(f'Wire anomaly: {wire} not BSM: ' + str(wires[wire]['label']))
    elif wire == 'z45':
        if wires[wire]['label'][0] != 'REM':
            print(f'Wire anomaly: {wire} not REM: ' + str(wires[wire]['label']))
    elif wire[0] == 'z' and wires[wire]['label'][0] != 'SUM':
        print(f'Wire anomaly: {wire} not SUM: ' + str(wires[wire]['label']))

def get_wire_value(wire, label = False):
    if wire not in wires:
        return 0
    match wires[wire]['data']:
        case 'VAL', value:
            result = value
        case 'AND', a, b:
            result = get_wire_value(a, label) & get_wire_value(b, label)
        case 'OR', a, b:
            result = get_wire_value(a, label) | get_wire_value(b, label)
        case 'XOR', a, b:
            result = get_wire_value(a, label) ^ get_wire_value(b, label)
        case _:
            result = 0
    if label:
        label_wire(wire)
    return result

print(sum(get_wire_value(f'z{n:02}', False) * 2 ** n for n in range(46)))

# Didn't try to get a general solution, used labelling to find the necessary fixes and apply them manually.
fixes = {('z06', 'fhc'), ('z11', 'qhj'), ('ggt', 'mwh'), ('z35', 'hqk')}
for a, b in fixes:
    wires[a], wires[b] = wires[b], wires[a]
_ = sum(get_wire_value(f'z{n:02}', True) * 2 ** n for n in range(46))
print(','.join(sorted(x for pair in fixes for x in pair)))
