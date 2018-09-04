# これは何
YouTubeのチャンネルを検索して、新しい動画があったときにdiscrodに通知します。  
チェックするYoutubeチャンネルリストを作っておくと、自動的にdiscordサーバに同名チャンネルを作ってbotが通知します。  
herokuでの動かし方が書いてありますが、pythonが動けばどこでも動きます。

# 使い方
1. channellist.csvに「discordで表示させたいチャンネル名」「youtubeのチャンネルID」を書いてコミットする
2. google data api v3のトークンを取得する
3. discordのbotを作ってAPIトークンを取得する
4. discordを開発者モードにして、botを作ったサーバのサーバIDを取得する
5. herokuのアカウントを作り、heroku CLIをインストールする
6. heroku cliで下をやる
    * heroku login
    * heroku create [アプリ名]
    * heroku git:remote -a youtube-notification
    * config:set DISCORD_TOKEN="[3で取ったトークン]"
    * config:set DISCORD_SERVER="[4で取ったID]"
    * config:set GOOGLEDATAAPI_TOKEN="[2で取ったトークン]"
    * git push heroku master
    * ※heroku logs --tailでログを見る
    * herokuのアプリ設定のResourcesタブで、デフォルト起動offになってるので起動させる
    
