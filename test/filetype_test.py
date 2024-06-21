import filetype

def main():
    kind = filetype.guess(r'E:\botDet\video\2024-06-14 16-34-03.mp4')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)

if __name__ == '__main__':
    main()