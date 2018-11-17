#!/usr/bin/env python3

import os, sys, subprocess, math

OUT_DIR = 'telegram-noto-emoji'
EMOJI_COLLECT_DIR = os.path.join('noto-emoji', 'out')

def emoji_to_filename(e, edir=EMOJI_COLLECT_DIR):
    fn = 'emoji_u%s.svg'%'_'.join('%04x'%ord(c) for c in e if ord(c) != 0xfe0f)
    return os.path.join(edir, fn)

def main():
    try:
        os.mkdir(OUT_DIR)
    except FileExistsError:
        pass

    with open('emojilist.txt', 'r') as fp:
        emoji_list = fp.read().splitlines()

    filenames = list(map(emoji_to_filename, emoji_list))
    if 0:
        for f in filenames:
            print(f)
        return 0

    page_size = 32 * 16
    num_pages = math.ceil(len(filenames) / page_size)
    if num_pages != 5:
        print('WARNING: number of pages is %d, not 5!'%num_pages)

    err = 0
    for p in range(num_pages):
        start = p * page_size
        outfile = os.path.join(OUT_DIR, 'emoji_%d.webp'%(p+1))
        cmd = ['magick', 'montage', '-background', 'transparent']
        cmd.extend(filenames[start:start+page_size])
        cmd.extend(['-tile', '32x', '-geometry', '72x72+0+0',
                    '-define', 'webp:lossless=true', outfile])
        print('Generating %s...'%outfile)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            print('ERROR: failed to generate %s'%outfile)
            err += 1
            try:
                os.remove(outfile)
            except:
                pass

    return err

if __name__ == '__main__':
    sys.exit(main())
