# update-kabu
KabuステーションAPIを用いて、銘柄情報を最新化する。

## 設定
### プロパティファイル
以下項目を記載したconfig.iniをディレクトリ直下に置く。

| Section | Key | Type | Value（Description） |
| --- | --- | --- | --- |
| kabusapi | host | str | Kabuステーションが起動するホスト名です。基本的には localhost となります。 |
| kabusapi | port | str | Kabuステーションのポートです。 |
| database | db_host | str | MySQLのホスト名です。 |
| database | db_user | str | MySQLのユーザ名です。 |
| database | db_pswd | str | MySQLのパスワードです。 |
| database | db_name | str | MySQLのデータベース名です。 |

## 起動
```
python -m update-kabu
```
