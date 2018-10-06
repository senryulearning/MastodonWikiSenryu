import sys
import re
import time
import datetime
from mastodon import Mastodon
import MeCab
from collections import Counter

def hour_trend():

    counter_sum = Counter()

    try:
        mastodon = Mastodon(
        client_id="app_key.txt",
        access_token="user_key.txt",
        api_base_url = "https://theboss.tech")

        today_datetime = datetime.datetime.today()
        before_hour_datetime = today_datetime - datetime.timedelta(hours=1)
        before_hour_datetime = datetime.datetime(before_hour_datetime.year, before_hour_datetime.month, before_hour_datetime.day, before_hour_datetime.hour, before_hour_datetime.minute, before_hour_datetime.second)

        time_line_list = []
        next_id = None
        loop = True
        toot_count = 0

        while loop:
            timeline = mastodon.timeline(
                timeline='local',
                since_id=None,
                limit=40,
                max_id=next_id
            )

            loop = True
            next_id = timeline[-1]['id']
            toot_count += 40
            if  toot_count > 1000:
                break

            for toot in timeline:
                time_line_list.append(toot)

        trendlist = list(reversed(time_line_list))

        conv = re.compile(r"<[^>]*?>")
        tagger = MeCab.Tagger('-Ochasen')

        for toot in trendlist:
            #センシティブなトゥートは対象外とする
            if toot['sensitive'] == True:
                continue

            counter = Counter()
            toot_text = conv.sub("", toot['content'])
            nodes = tagger.parseToNode(toot_text)
            while nodes:
                feature_split =  nodes.feature.split(',')
                if feature_split[0] == '名詞'  and feature_split[1] != '非自立':
                    word = nodes.surface
                    if counter[word] < 1:
                        counter[word] += 1
                nodes = nodes.next

            for word, cnt in counter.most_common():
               counter_sum[word] += cnt

        return counter_sum
    except :
        return counter_sum

def toot_time_to_date_time(toot_time):
    from datetime import datetime
    import dateutil.parser
    from pytz import timezone
    if type(toot_time) == str:
        toot_time = dateutil.parser.parse(toot_time)
    return toot_time.astimezone(timezone('Asia/Tokyo'))

