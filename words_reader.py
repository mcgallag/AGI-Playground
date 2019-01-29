import struct
import sys
import json


def build_offsets(fp):
    offsets = []
    for i in range(26):
        word = fp.read(2)
        i = (256*int(word[0])) + int(word[1])
        offsets.append(i)
    return offsets


def get_next_word(fp, previous_word):
    b = fp.read(1)
    prev_word_chars = int(b[0])
    new_word = previous_word[0:prev_word_chars]

    while True:
        c = fp.read(1)
        if not c:
            return None
        c = struct.unpack("B", c)[0]

        if c > 128:
            c -= 128
            c = c ^ 127
            new_word += chr(c)
            return new_word
        elif c < 32:
            new_word += chr(c ^ 127)
        elif c == 95:
            new_word += " "


def get_wordnum(fp):
    word = fp.read(2)
    wordnum = (256 * int(word[0])) + int(word[1])
    return wordnum


def exit(fp):
    fp.close()
    sys.exit(0)


def parse_words_file(filename="WORDS.TOK"):
    f = open(filename, "rb")

    offsets = build_offsets(f)
    f.seek(offsets[0])

    vocabulary = {}
    word = ""

    while True:
        previous_word = word
        word = get_next_word(f, previous_word)
        if word is None:
            break
        wordnum = get_wordnum(f)
        try:
            vocabulary[wordnum].append(word)
        except KeyError:
            vocabulary[wordnum] = []
            vocabulary[wordnum].append(word)

    f.close()
    del vocabulary[0]
    return vocabulary


vocab = parse_words_file()
print(json.dumps(vocab, sort_keys=True, indent=2))
