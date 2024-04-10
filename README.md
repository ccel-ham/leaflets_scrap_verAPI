<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fimg.shields.io%2Fbadge%2F-Python-F2C63C.svg%3Flogo%3Dpython%26style%3Dfor-the-badge?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=c17144ccc12f9c19e9dbba2eec5c7980" data-canonical-src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&amp;style=for-the-badge" srcset="https://qiita-user-contents.imgix.net/https%3A%2F%2Fimg.shields.io%2Fbadge%2F-Python-F2C63C.svg%3Flogo%3Dpython%26style%3Dfor-the-badge?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=max&amp;s=5d7d909c2f70c6c8a0fc0477bd1a56ae 1x" loading="lazy">

# プロジェクトの概要
このプロジェクトは、特定のウェブサイトからチラシの画像を取得し、更新があればLINE通知を送信するためのスクリプトです。
TokubaiBot クラスは、特定の店舗からチラシの画像を取得し、必要に応じて LINE Notify を使用して新しいチラシを通知します。
また、YamadaBotCustomTokubai クラスは、特定のウェブサイトからのチラシ画像を取得するために TokubaiBotクラスを拡張しています。

# 使用ライブラリ
**requests**: HTTPリクエストを送信するためのPythonライブラリです。

**BeautifulSoup**: HTMLやXMLからデータを抽出するためのPythonライブラリです。

**PIL (Python Imaging Library)**: 画像処理ライブラリであり、画像の圧縮や処理を行うために使用されます。

**base64**: バイナリデータをテキストデータにエンコードするためのPythonモジュールです。

**hashlib**: ハッシュ関数を提供するPython標準ライブラリです。

# 使用上の注意
チラシ更新の管理にGASのエンドポイントを使用しています。
更新のみの取得にはGASのプログラムも必要です。
Get requestsで”leaflet_hash”がキーになる、保存中のチラシのhash値が ” , ” 区切りの文字列で返されます。
Post requestsでファイル名と画像データをGoogleDriveへ保存します。
