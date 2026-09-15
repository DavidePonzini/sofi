from dataclasses import dataclass
import re
from dav_tools import argument_parser, messages
import random


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

def random_messages() -> str:
    return random.choice([
        '<3',
        '(^_^)',
        '(*^_^*)',
        '(o_o)',
        '(>_<)',
        'Ti amo tanto',
        'Sei bellissima',
        'Gilaffina adolabile',
        'Ti auguro una giolnata melavigliosa almeno quanto lo sei tu',
    ])

@dataclass(frozen=True)
class Header:
    method: str
    angle: str

def output_filename(base: str, Header: Header, ext: str) -> str:
    return f'{base}_{Header.method}_{Header.angle}.{ext}'

if __name__ == '__main__':
    argument_parser.add_argument('file', help='Input filename')
    argument_parser.add_argument('--skip', type=int, default=4, help='Number of lines to skip at the start of the file')

    filename = argument_parser.args.file
    filename_name = '.'.join(filename.split('.')[:-1])
    filename_ext = filename.split('.')[-1]
    skip_lines = argument_parser.args.skip

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Clean up whitespace in each line
    lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]

    # Skip the first lines
    lines = lines[skip_lines:]

    results: dict[Header, list[str]] = {}

    for line in lines:
        columns = line.split(' ')

        if len(columns) < 1:
            continue

        method = columns[0]
        angle = columns[2]

        header = Header(method=method, angle=angle)

        results.setdefault(header, []).append(line)

    for header, lines in results.items():
        with open(output_filename(filename_name, header, filename_ext), 'w') as out_file:
            for line in lines:
                out_file.write(f'{line}\n')
            messages.info(f'Wrote {len(lines)} lines to {output_filename(filename_name, header, filename_ext)}')

    messages.success(f'Processing complete! {random_messages()}')