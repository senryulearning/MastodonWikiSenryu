import wiki_senryu
import time_line_trend
import toot_word_file
import my_time_line

##追加ライブラリ
import urllib
import requests
from mastodon import Mastodon
import time

OUTPUT_COUNT = 5

def main():
    mastodon = Mastodon(
        client_id="app_key.txt",
        access_token="user_key.txt",
        api_base_url = "https://theboss.tech")

    print('川柳bot稼働中')
    while True:

        toot_result = my_time_line.toot_before_hour()

        if toot_result is None:
            print('マイトート取得エラー')
            time.sleep(600)
            continue

        if toot_result == True:
            print('スリープ')
            time.sleep(600)
            continue

        counter_sum = time_line_trend.hour_trend()
        for word, cnt in counter_sum.most_common():
            if toot_word_file.is_toot_word(word):
                continue

            result = wiki_senryu.createSenryu(word)
            if result.errormessage == '':
                break

        if len(counter_sum) == 0:
            print('ローカルタイムライン取得エラー')
            time.sleep(600)
            continue

        toot_text = '川柳投稿テスト' + '\n'
        toot_text += 'Wikipediaより「' + result.word + '」で一句' + '\n'
        toot_text += requests.get(result.url).url + '\n'
        toot_text += result.url + '\n'
        toot_text += result.senryu + '\n'
        toot_text += result.furigana + '\n'
        toot_word_file.write_word(word)
        print(toot_text)


        mastodon.toot(toot_text)

        #mastodon.status_post(toot_text, visibility='unlisted')

if __name__ == '__main__':
    main()
