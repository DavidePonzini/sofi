from dav_tools import argument_parser, messages
from enum import Enum

class Order(Enum):
    NONE = 'unknown'
    ASC = 'retraction'
    DESC = 'approachment'

if __name__ == '__main__':
    argument_parser.add_argument('file', help='Path to the file to be split')

    filename = argument_parser.args.file
    filename_name = '.'.join(filename.split('.')[:-1])
    filename_ext = filename.split('.')[-1]
    
    with open(filename, 'r') as f:
        lines = f.readlines()

    current_order = Order.NONE
    last_value = None

    output_lines = []
    file_counter = 1

    for line in lines:
        col1, col2 = line.strip().split()

        if last_value is None:
            last_value = col1
            continue

        old_order = current_order

        if col1 > last_value:
            current_order = Order.ASC
        elif col1 < last_value:
            current_order = Order.DESC

        # Same order as before, continue accumulating lines
        if old_order is not None and current_order == old_order:
            output_lines.append(line)
            continue

        # Order changed, write out the accumulated lines
        output_filename = f'{filename_name}_{current_order.value}_{file_counter}.{filename_ext}'
        with open(output_filename, 'w') as out_f:
            out_f.write('\n'.join(output_lines) + '\n')
            messages.info(f'Wrote {len(output_lines)} lines to {output_filename}')

        file_counter += 1
        output_lines = [ line ]  # Start new accumulation with current line

    messages.success('File splitting completed.')