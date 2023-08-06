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

# LICENSE

MIT.
