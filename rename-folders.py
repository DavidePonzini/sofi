from pathlib import Path
from datetime import datetime
import dav_tools


def rename_folders(folders: list[str]):
    for folder in folders:
        folder = Path(folder)
        if not folder.is_dir():
            continue

        old_name = folder.name

        try:
            date = datetime.strptime(old_name, '%d%m%Y')
        except ValueError:
            dav_tools.messages.warning(f'Skipping invalid folder name: {old_name}')
            continue

        new_name = date.strftime('%Y%m%d')
        new_path = folder.with_name(new_name)

        if new_path.exists():
            dav_tools.messages.warning(f'Skipping {old_name}: target already exists ({new_name})')
            continue

        folder.rename(new_path)
        dav_tools.messages.info(f'Renamed {old_name} -> {new_name}')


if __name__ == '__main__':
    dav_tools.argument_parser.add_argument('folders', nargs='+', help='Folders to rename')
    dav_tools.argument_parser.parse_args()

    rename_folders(dav_tools.argument_parser.args.folders)