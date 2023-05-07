# chat bot service

## 必要な環境変数

下記の環境変数が必要なため、backend配下にsecret.jsonを下記のように作成すること.

```
{
  "OPENAI_API_KEY": "xxxxx",
  "GOOGLE_CSE_ID": "xxxxx",
  "GOOGLE_API_KEY": "xxxxx"
}
```

## サービスの起動

下記コマンドを実行する.

```
docker-compose up
```

## サービスへのアクセス

ブラウザを起動し、下記のURLにアクセスする.

* http://localhost:8501
