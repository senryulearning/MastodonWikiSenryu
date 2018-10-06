from mastodon import Mastodon
import datetime
import dateutil.parser
from pytz import timezone

def toot_before_hour():

    try:
        #マストドンのインスタンスを生成
        mastodon = Mastodon(
        client_id="app_key.txt",
        access_token="user_key.txt",
        api_base_url = "https://theboss.tech")

        #1時間前にトゥートがあったか調べる。
        timeline = mastodon.timeline(max_id=None, limit=1)
        if len(timeline) == 0:
            return False

        today_datetime = datetime.datetime.today()
        beforehourdatetime = today_datetime - datetime.timedelta(hours=1)
        beforehourdatetime = datetime.datetime(beforehourdatetime.year, beforehourdatetime.month, beforehourdatetime.day, beforehourdatetime.hour, beforehourdatetime.minute, beforehourdatetime.second)

        created_at = timeline[0].created_at
        created_at = toot_time_to_date_time(created_at)
        lasttoottime = datetime.datetime(created_at.year, created_at.month, created_at.day, created_at.hour, created_at.minute, created_at.second)
        return lasttoottime > beforehourdatetime
    except :
         return None

def toot_time_to_date_time(toot_time):
    if type(toot_time) == str:
        toot_time = dateutil.parser.parse(toot_time)
    return toot_time.astimezone(timezone('Asia/Tokyo'))