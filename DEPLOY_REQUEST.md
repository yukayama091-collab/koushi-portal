# 講師ポータル 反映依頼（2026-07-31）

`https://app.levela.co.jp/instructor-dashboard/` で配信している講師ポータルの HTML を、
最新版に差し替えていただきたいです。

## 依頼内容

- **差し替えるファイル**: リポジトリ `yukayama091-collab/koushi-portal` の `koushi_portal.html`
- **反映するコミット**: `da8b337`（main の最新）
- **配置先**: 現在 `https://app.levela.co.jp/instructor-dashboard/` で配信しているファイル（nginx のドキュメントルート配下、おそらく `instructor-dashboard/index.html`）を、上記ファイルの内容で置き換え

ファイル名がリポジトリ側と配信側で違う可能性があります（リポジトリは `koushi_portal.html`、
配信側はディレクトリURLなので `index.html` と思われます）。**中身をそのままコピーするだけ**で、
ファイル名は現在配信中のものに合わせてください。

```bash
git clone https://github.com/yukayama091-collab/koushi-portal.git
# もしくは既存クローンで
git pull
# 例（配置先は実際のパスに合わせてください）
cp koushi-portal/koushi_portal.html /var/www/.../instructor-dashboard/index.html
```

## 現在配信中の版

配信中のファイルはコミット `37332f0`（2026-07-21）の内容と一致していました。
そのため、今回は**9日分・3コミット**がまとめて反映されます。

| コミット | 日付 | 内容 |
|---|---|---|
| `327597c` | 07-29 | 受け持ちクラスカードの「第?回まで実施」を修正 |
| `4298b4c` | 07-29 | 0回実施のクラスも「未実施」と正しく表示 |
| `da8b337` | 07-30 | 担当講師カード／講師マスタから Discord クラスチャンネルを開けるようにした |

## 変更の性質

- **単一の静的 HTML ファイルの差し替えのみ**です。サーバー設定・nginx 設定・証明書・DNS の変更は不要です
- ビルド作業はありません（依存パッケージなし、単一ファイル完結）
- バックエンド（GAS 受付窓口）側の対応は反映済みで、**先に配置しても問題ありません**

## 反映前にお願いしたいこと

現在配信中のファイルのバックアップを取っておいてください。切り戻しはそれを書き戻すだけです。

```bash
cp instructor-dashboard/index.html instructor-dashboard/index.html.20260731.bak
```

## 反映後の確認方法

1. `https://app.levela.co.jp/instructor-dashboard/` をブラウザで開く（**強制リロード**推奨: Mac は Cmd+Shift+R）
2. ダッシュボードの「担当講師」カードに **「担当クラス（クリックでDiscord）」** の行が出ていること
3. そこに表示されるクラス名のチップをクリックすると Discord のクラスチャンネルが開くこと

灰色のチップが混ざっていますが**正常**です（対応する Discord チャンネルが見つからなかった旧期クラス）。

## 切り戻し

上記バックアップを書き戻すだけで元に戻ります。データベースやシートには一切影響しません。

## 連絡先

不明点があれば 山下優花（CS/CTO室）まで。
