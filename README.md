## プロジェクト名
**Django-wordbook**

英単語を検索・登録し、フラッシュカードで効率的に復習できるWebアプリです。

---

## デモ
- アプリURL  
  https://django-wordbook.onrender.com

- テスト用アカウント
  - ID: test
  - PW: test5test

※ renderの無料プランのため、初回アクセス時に起動まで時間がかかる場合があります。

---

## 機能
- ExcelAPIを使った単語の意味の検索と結果の保存
- 手動での意味の登録
- 登録した単語とその意味のリスト
- 登録した単語の編集・削除
- フラッシュカード
- サインアップ / ログイン / ユーザー認証

---

## 技術スタック

### バックエンド
- Python3.12.9
- Django6.0

### フロントエンド
- HTML
- CSS
- JavaScript
- Bulma

### データベース
- SQLite（開発環境）
- PostgreSQL（本番環境）

### 他技術
- Authentication: Django built-in auth
- External API: ExcelAPI 英和辞典
- Deployment: Render

---

## 工夫した点
- ExcelAPIに単語の意味をリクエストすると（json形式などではなく）ただの文字列データが返ってくるので、それをリスト化して使いやすいようにしています
- 単語の意味の検索と登録がダイレクトにつながっており、複数意味がある場合はその一つだけを選んだりすべてを選んだり編集したりして登録できます
  - htmlテンプレートでforloop.last、forloop.counterなどを使って意味の表示の仕方を工夫しました
  - view側では、意味全てを登録する場合、「１．意味　２．意味　３．意味…」のような書式で自動でデータベースに保存されるようにコードが書かれています。
- ユーザーごとにデータを分離するためForeignKey設計を採用
- 基本的にログインしないと使えない機能が多いが、ログインしていない場合でも意味の検索は使え、また登録した単語リストには全ユーザーが登録したものが表示される（ログインしていれば、そのユーザーのものだけ）
- 単語のリストやフラッシュカードでは、登録されたとき（「今日」「直近一週間」「直近一か月」）によってソートできるようになっています
  - django.utilsのtimezoneやdatetimeのtimedeltaなどを使いました
  
---

## セットアップ（ローカル実行方法）

```bash
git clone https://github.com/riku5-coder/django-wordbook.git
cd django-wordbook

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## その他
 - 設計・開発・デプロイを独学で行いました
 - デフォルトブランチはmainですが、Renderに上げているブランチはfeature/rendertestです
 - mainはローカルで動かすセッティングのままです
