from fontTools.ttLib import TTFont
import sys

def get_supported_chars(font_path):
    font = TTFont(font_path)
    all_supported_chars = set()

    for cmap_table in font['cmap'].tables:
        if cmap_table.cmap:
            all_supported_chars.update(cmap_table.cmap.keys())

    font.close()
    return all_supported_chars

def get_unicode_ranges(font_path):
    supported_chars = sorted(get_supported_chars(font_path))

    if not supported_chars:
        return []

    ranges = []

    start = supported_chars[0]
    last = start

    for char in supported_chars[1:]:
        if char == last + 1:
            last = char
        else:
            if start == last:
                ranges.append(f'{start:X}')
            else:
                ranges.append(f'{start:X}-{last:X}')

            start = char
            last = char

    if start == last:
        ranges.append(f'{start:X}')
    else:
        ranges.append(f'{start:X}-{last:X}')

    return ranges

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: python ranges.py <path/to/font.ttf>')
        sys.exit(0)

    font_path = args[0]

    try:
        ranges = get_unicode_ranges(font_path)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    if ranges:
        print(' '.join(ranges))
    else:
        print('No supported Unicode characters found in the font.', file=sys.stderr)

if __name__ == '__main__':
    main()
