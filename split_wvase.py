import re
from dav_tools import argument_parser, messages

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    argument_parser.add_argument('file', help='Input filename')
    argument_parser.add_argument('--skip', type=int, default=4, help='Number of lines to skip at the start of the file')
    argument_parser.add_argument('--angle-column', type=int, default=1, help='Column number for angle values (starting from zero)')
    argument_parser.add_argument('--dpol-angle-column', type=int, default=2, help='Column number for dpol angle values (starting from zero)')

    filename = argument_parser.args.file
    filename_name = '.'.join(filename.split('.')[:-1])
    filename_ext = filename.split('.')[-1]
    skip_lines = argument_parser.args.skip
    angle_column = argument_parser.args.angle_column
    dpol_angle_column = argument_parser.args.dpol_angle_column

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Clean up whitespace in each line
    lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]

    # Skip the first lines
    lines = lines[skip_lines:]

    results = {}
    results_dpol = {}

    for line in lines:
        columns = line.split(' ')

        if len(columns) < 1:
            continue

        col1 = columns[0]

        if is_float(col1):
            if len(columns) < angle_column:
                messages.error(f'Line has insufficient columns: {line}')
            
            angle = columns[angle_column]

            if angle not in results:
                results[angle] = []

            results[angle].append(line)
        elif col1.isalpha():
            if len(columns) < dpol_angle_column:
                messages.error(f'Line has insufficient columns: {line}')

            dpol_angle = columns[dpol_angle_column]

            if dpol_angle not in results_dpol:
                results_dpol[dpol_angle] = []

            results_dpol[dpol_angle].append(line)
        else:
            messages.error(f'Unexpected line format: {columns}')

    for key, value in results.items():
        with open(f'{filename_name}_{key}.{filename_ext}', 'w') as out_file:
            for line in value:
                out_file.write(f'{line}\n')
            messages.info(f'Wrote {len(value)} lines to {filename_name}_{key}.{filename_ext}')

    for key, value in results_dpol.items():
        with open(f'{filename_name}_dpol_{key}.{filename_ext}', 'w') as out_file:
            for line in value:
                out_file.write(f'{line}\n')
            messages.info(f'Wrote {len(value)} lines to {filename_name}_dpol_{key}.{filename_ext}')

    messages.success('Processing complete <3')