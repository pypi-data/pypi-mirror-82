# NCMB Python SDK

ニフクラ mobile backendを利用するためのPython SDKです。

# 使い方

## インポート

```
pip install NCMB
```

## 初期化

```py
from NCMB.Client import NCMB
ncmb = NCMB('YOUR_APPLICATION_KEY', 'YOUR_CLIENT_KEY')
```

## データストア

### データ保存

```py
obj = ncmb.Object('Python')
obj.set(
  'message', 'Hello from Python'
).set(
  'message2', 'Hello from Python'
).set(
  'number', 100
).save()
```

カラムへのアクセスは get を使います。

```py
print(obj.get('objectId'))
# -> 5CN1U23KLd6zatu8など
```

### データ検索

```py
query = ncmb.Query('Python')
query.equal_to('number', 100)
ary = query.fetch_all()
```

#### 検索用メソッドについて

検索条件は以下に対応しています。

```py
equal_to(self, key, value):
greater_than_or_equal_to(self, key, value):
not_equal_to(self, key, value):
less_than(self, key, value):
less_than_or_equal_to(self, key, value):
greater_than(self, key, value):
in_value(self, key, values):
not_in(self, key, values):
exists(self, key, exist = True):
regular_expression_to(self, key, regex):
in_array(self, key, values):
not_in_array(self, key, values):
all_in_array(self, key, values):
```

このほか `limit` / `order` / `skip` で並び替えやデータの取得件数の変更を行えます。

```py
query.limit(1)  # 取得件数指定
query.order('updateDate') # 並び替え
query.skip(100) # スキップする件数
```

# LICENSE

MIT.
