# Generate Emoji sprite sheets for Telegram Desktop

## About
These are my scripts to generate emoji sprite sheets for [Telegram Desktop](https://github.com/telegramdesktop/tdesktop),
particularly with the [Noto Color Emoji](https://github.com/googlei18n/noto-emoji) intended for use
with the [telegram-desktop-systemqt-notoemoji](https://aur.archlinux.org/packages/telegram-desktop-systemqt-notoemoji)
AUR package which I maintain.

## Build Instructions

**Note!** You may need to clear Telegram's emoji cache after updating to a new version with replaced
emoji. I still saw the Apple emoji until I deleted the directory `~/.TelegramDesktop/tdata/emoji`

### I. Prerequisites
* python3 (for my scripts)
* python2 (for Google's Noto tools)
* imagemagick (for tiling and converting the images)
* all of Telegrams build dependencies

### I. Get the emoji codepoint list from Telegram.
Rather than using actual fonts, Telegram stores emoji as spritemaps (based on the Apple emoji) in
a set of five webp files located in `tdesktop/Telegram/Resources/emoji`. The tricky first step was
figuring out the proper order of emoji that Telegram expects.

1. Clone the `tdesktop` source code
2. Apply `generator.cpp.patch` from this repo
3. Use `gyp` and `cmake` to set up Makefiles (the details of this step are left as an exercise for
   the reader)
4. cd to `tdesktop/out/Release` and run `make codegen_emoji`
5. run `./codegen_emoji ../../Telegram/Resources/emoji_autocomplete.json >emojilist.txt` and copy `emojilist.txt` to this repo
   1. This creates a file that contains one emoji per line

### II. Get and prepare the Noto Color Emoji
1. Clone noto-emoji and nototools into this directory
```
git submodule update --init
```
2. Apply `collect_emoji.patch` and run `collect_emoji_svg.py` in the noto-emoji directory.
```
cd noto-emoji
patch -p1 -i ../collect_emoji.patch
PYTHONPATH=$PWD/../nototools python2 collect_emoji_svg.py out -f third_party/region-flags/svg -e svg
cd ..
```
This will collect all the SVG emoji and flag files into a single `noto-emoji/out` directory.

### III. Build the sprite sheets
This step's easy:
```
./gen-emoji-grid.py
```

### IV. Build Telegram Desktop with the new emoji
1. Go back to your tdesktop source and clean it
2. Copy the webp files from `telegram-noto-emoji` into `tdesktop/Telegram/Resources/emoji`
   (overwrite the existing files)
3. Compile tdesktop as usual.

# Credits
* k3a's [telegram-emoji-list](https://github.com/k3a/telegram-emoji-list) repository which helped me
  find the right place to extract the emoji codepoint order
* [PeterCxy](https://github.com/PeterCxy) for making the original
  `telegram-desktop-systemqt-notoemoji` AUR package before I adopted it.
* OriginCode on the AUR site for pointing out to me that Telegram recently refactored their emoji
  code, spurring me to figure all this out and update it.

# License
* [Telegram Desktop](https://github.com/telegramdesktop/tdesktop/blob/dev/LEGAL) is copyright John
  Preston, licensed as GPLv3+ with OpenSSL exception
* [Noto Color Emoji](https://github.com/googlei18n/noto-emoji/blob/master/LICENSE) and
  [Noto Tools](https://github.com/googlei18n/nototools/blob/master/LICENSE) are copyright Google,
   licensed as Apache 2.0

My original scripts in this repository are released under the MIT license:
```
Copyright 2018 Allen Wild

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
