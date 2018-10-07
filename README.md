# MastodonWikiSenryu

●このプログラムを一言でいうと
wikipediaから川柳を作ってマストドンにトゥートするbotです。

●事前準備
以下のプログラムを用意してください。

〇プログラム本体
・Python 3.7.0 以上

〇パッケージ
・MeCab
・urllib
・requests
・Mastodon
・pytz

〇レジストレーションとログインを行う。
このプログラムを実行するためにはレジストレーションとログインを行う必要があります。
以下のコードを実行してapp_key.txtとuser_key.txtを作成してください。

#url = マストドンのインスタンスURL
Mastodon.create_app(name,
    api_base_url = url,
    to_file = "app_key.txt"
)

#マストドンのインスタンスを作成
mastodon = Mastodon(
    client_id="app_key.txt",
    api_base_url = url)

#マストドンへログイン    
mastodon.log_in(
    mail,
    passwd,
    to_file = "user_key.txt")
print('user_key作成完了!')

●プログラムの実行
事前準備をすべて終えた後、
senryu_toot.pyを実行してください。

●ライセンスについて
ライセンスは今後の状況によって変更する可能性があります。あらかじめご了承ください。

●連絡先
記述するべきところが不足しているかもしれません。
何かありましたらこちらにご連絡ください。
http://twitter.com/@MI9tUoBGpQGspwZ