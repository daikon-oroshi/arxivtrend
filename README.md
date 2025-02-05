# arxivtrend

このプロジェクトは、arXiv に投稿されている論文の概要に含まれる、名詞、動詞、形容詞を抽出して集計することで、特定の分野で重要視されている問題、その移り変わりを可視化しようという試みです。

論文の概要は arXiv 公式のAPIを用いて取得します。

https://info.arxiv.org/help/api/user-manual.html

## 使い方

### 初期構築

1. docker をインストールする https://docs.docker.com/engine/install/

1. docker-compose をインストールする https://matsuand.github.io/docs.docker.jp.onthefly/compose/install/

1. docker イメージのビルド
    ```
    docker compose build
    ```

1. python, poetry のインストール

1. モジュールのインストール
    ```
    poetry install
    ```

1. .env ファイルの設定
    ```
    cp .env.dist .env
    ```
    必要があれば .env の設定を変更する。


### 実行方法

1. DBの起動
    ```
    docker compose up -d mongo
    ```

2. プログラムの実行
    ```
    poetry run python -m arxivtrend.main search [search_query] -b [submitted_begin] -e [submitted_end] -c [category]
    ```

3. PDF化 (ファイルの指定はtab補完できます。)
    ```
    FILE=report/generated/[フォルダ名]/report.adoc docker compose up report
    ```

これで ~/report/generated/[フォルダ名]/report.pdf にレポートが作成されます。

## その他

### 検索時のカテゴリー指定について

カテゴリーは以下の中で部分一致させます。
https://arxiv.org/category_taxonomy

カテゴリーの一覧は
```
poetry run python -m arxivtrend.main show-categories
```
でも取得できます。

### ストップワードの指定、追加

集計に意味がなさそうな単語はレポートから除くことができます。~/stop_words/ 以下にテキストファイルを作成し、.env の STOP_WORD_FILES にそのファイルを追加してください。