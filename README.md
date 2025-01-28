# arxivtrend

このプロジェクトは、arXiv に投稿されている論文の概要に含まれる、名詞、動詞、形容詞を抽出して集計することで、特定の分野で重要視されている問題、その移り変わりを可視化しようという試みです。

論文の概要は公式のAPIを用いて取得します。

arxiv api https://info.arxiv.org/help/api/user-manual.html

## 使い方

### 初期構築

1. docker をインストールする https://docs.docker.com/engine/install/
1. docker-compose をインストールする https://matsuand.github.io/docs.docker.jp.onthefly/compose/install/

1. docker イメージのビルド
```
docker compose build
```

1. python, poetry のインストール


### 実行方法

1. DBの起動
```
docker compose up -d
```

1. プログラムの実行
```
poetry run python -m arxivtrend.main search [search_query] -b [submitted_begin] -e [submitted_end]
```
