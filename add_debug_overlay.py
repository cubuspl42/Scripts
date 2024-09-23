#!/usr/bin/env python3
import os
import shutil
import json

component_name = 'DebugOverlayWrapper'

# Ensure package.json exists
if not os.path.isfile(os.path.join(os.getcwd(), 'package.json')):
    raise FileNotFoundError('package.json not found in current working directory')

# Get script's own directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Copy the .tsx file
shutil.copy(os.path.join(script_dir, f'{component_name}.tsx'),
            os.path.join(os.getcwd(), 'src', 'components', f'{component_name}.tsx'))

# Edit App.tsx
app_tsx_path = os.path.join(os.getcwd(), 'src', 'App.tsx')
with open(app_tsx_path, 'r') as file:
    lines = file.readlines()

# Find last import line and add new import
for i, line in reversed(list(enumerate(lines))):
    if line.startswith('import'):
        lines.insert(i + 1, f'import {component_name} from "@components/{component_name}";\n')
        break

# Wrap <Expensify/>
lines = [line.replace('<Expensify />', f'<{component_name}><Expensify /></{component_name}>') for line in lines]

# Write back to file
with open(app_tsx_path, 'w') as file:
    file.writelines(lines)
