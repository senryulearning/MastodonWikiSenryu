import os
import os.path
import sys
import datetime

SAVE_TOOT_LIMIT = 10000
LOG_FILE_NAME = 'TootWord.txt'

def is_toot_word(word):

    if os.path.exists(LOG_FILE_NAME) == False:
        return False

    lines = open(LOG_FILE_NAME).readlines()

    for line in lines:
       line = line.replace('\r','')
       line = line.replace('\n','')
       if line == word:
            return True

    return False

def write_word(word):

    # 1万行以上の場合はリセット
    if os.path.exists(LOG_FILE_NAME) == True:
        toot_count = sum(1 for line in open(LOG_FILE_NAME))
        if toot_count >= SAVE_TOOT_LIMIT:
            os.remove(filepath)

    f = open(LOG_FILE_NAME, "a")
    f.write(word + '\n')
    f.close()

if __name__ == '__main__':
    main()
