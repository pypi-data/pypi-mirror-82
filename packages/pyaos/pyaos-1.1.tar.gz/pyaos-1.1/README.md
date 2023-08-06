# pyaos 开发文档

AOS链接口和AOS钱包接口的调用方法相同，在这里我会给出几个调用示例，其他方法的调用与此相通。

## AOS 链接口调用示例

pyaos/chain.py 技术文档

- **chain.get_info**

功能：获取与节点相关的最新信息

参数：

无

调用示例：

```python
from pyaos.chain import chain

chain = chain("http://yournode.test")
print(chain.get_info())
```



参数example：

```json
{'head_block_num': 33707199, 'chain_id': '907345e081e731497946845186a03a50030c6c9ee14bacfcb1922feae873f31b', 'head_block_time': '2020-10-19T12:33:56.000', 'head_block_producer': 'aoslosangele', 'head_block_id': '020254bfacb33c92188962a285ce7d9dc8e6f9a69ce8cfe46ae79a01435024be', 'last_irreversible_block_num': 33706870, 'virtual_block_cpu_limit': 3800000000, 'server_version': '95da4496', 'fork_db_head_block_id': '020254bfacb33c92188962a285ce7d9dc8e6f9a69ce8cfe46ae79a01435024be', 'block_net_limit': 1048576, 'virtual_block_net_limit': 1048576000, 'last_irreversible_block_id': '020253762f631efdb3071fca525a3a87dad244edf09efc79b7ec233f3ab400c7', 'fork_db_head_block_num': 33707199, 'block_cpu_limit': 3799900, 'server_version_string': 'push-dirty'}
```

- **chain.get_block**

功能：获取一个块的信息

参数：

| Key             | Value           | Required |
| --------------- | --------------- | -------- |
| block_num_or_id | 块的id或者num值 | Y        |

调用示例：

```python
from pyaos.chain import chain

chain = chain("http://yournode.test")
print(chain.get_block(1))
```



参数example：

```json
{'producer': '', 'transaction_mroot': '0000000000000000000000000000000000000000000000000000000000000000', 'block_num': 1, 'timestamp': '2018-12-13T02:02:13.000', 'producer_signature': 'SIG_K1_111111111111111111111111111111111111111111111111111111111111111116uk5ne', 'header_extensions': [], 'ref_block_prefix': 2778271483, 'id': '00000001dbcd954bfb0e99a5571cb4c7e9008ab3b28d829b8b59d0c49a1663ac', 'transactions': [], 'schedule_version': 0, 'new_producers': None, 'block_extensions': [], 'confirmed': 1, 'action_mroot': '907345e081e731497946845186a03a50030c6c9ee14bacfcb1922feae873f31b', 'previous': '0000000000000000000000000000000000000000000000000000000000000000'}
```



## AOS 钱包接口调用示例

pyaos/wallet.py 技术文档

- **wallet.wallet_create**

功能：用给定的名称创建一个新的钱包.

参数：

| Key         | Value    | Required |
| ----------- | -------- | -------- |
| wallet_name | 钱包名称 | Y        |

调用示例：

```python
from pyaos.wallet import wallet

wallet = wallet("http://yournode.test")
print(wallet.wallet_create(wallet_name="YOUR_WALLET_NAME"))
```



参数example：

```json
PW5KFWYKqvt63d4iNvedfDEPVZL227D3RQ1zpVFzuUwhMAJmRAYyX
```



- **wallet.wallet_open**

功能：打开给定名称的现有钱包.

参数：

| Key         | Value    | Required |
| ----------- | -------- | -------- |
| wallet_name | 钱包名称 | Y        |

调用示例：

```python
from pyaos.wallet import wallet

wallet = wallet("http://yournode.test")
print(wallet.wallet_create(wallet_name="YOUR_WALLET_NAME"))
```



参数example：

```json
{}
```



- **wallet.wallet_lock**

功能：锁定所有钱包。

参数：

| Key         | Value    | Required |
| ----------- | -------- | -------- |
| wallet_name | 钱包名称 | Y        |

调用示例：

```python
from pyaos.wallet import wallet

wallet = wallet("http://yournode.test")
print(wallet.wallet_lock_all(wallet_name="YOUR_WALLET_NAME"))
```

参数example：

```json
{}
```



## AOS 加密函数

另外，AOS专门封装了一些加密和签名的函数，便于开发者使用，以保护数据的隐私性和匿名性。

- **ECDSA签名函数**

功能：实现ECDSA签名

```python
from aosencryfunc import ecdsa_sign

data = b'hello, AOS'
privkey = "0x2e66dbbfc7b8ae9ebd3bdce831509ce5136bc0a54055eaa4bff364e07291f5ab"
signature = ecdsa_sign(data, privkey)
print(signature)
# (signature：签名结果, data：签名对象, verifing_key：验签object)
```

结果Example：

```python
(b'/\xdd\xceA"\x8d\x0b \x97\xa6\x9f\xb5\xd6\x9d\xdd\xfcoo7\xd9]N5\xa0\x80\x1e{\x95<\xfe\xfa:[\xe9rW\x9b\x925eV\x9b\x8b\x8a\xcb\x13SKsb\x9eDt\xc5\x18.\xb0\x89N\x9b\x064\x8c\xc7', b'hello, AOS', VerifyingKey.from_string(b'\x03 \xa2\x1a\xd4\x0etj\x1f\x99\xab=b\xca\x95g\xab+u%\xa1\xaf\xb6\xb8v\tf\x0f\xcbD\xd9!3', SECP256k1, sha1))
```



- **ECDSA验签**

功能：验证ECDSA的签名

```python
from aosencryfunc import ecdsa_sign, ecdsa_verifing

data = b'hello, AOS'
privkey = "0x2e66dbbfc7b8ae9ebd3bdce831509ce5136bc0a54055eaa4bff364e07291f5ab"
signature = ecdsa_sign(data, privkey)
verify = ecdsa_verifing(signature=signature[0], data=signature[1], verifing_key=signature[2])
print(verify)
verify_false = ecdsa_verifing(signature='test signature', data=signature[1], verifying_key=signature[2])
print(verify_false)
```

结果Example:

```python
True
False
```

- **Hash加密**

功能：Hash加密函数

```python
from aosencryfunc import Hash

data = b'hello, AOS'
hash_msg = Hash(data)
print(hash_msg)
```

结果Example：

```python
ba6077e30df147039255e6e981cfb2d2a53c0e40bd2f36dd009e9feded709884
```

- **Base64加密/解密**

功能：Base64加密/解密函数

```python
from aosencryfunc import base64_decode, base64_encode

data = b'hello, AOS'
encode_msg = base64_encode(data)
print(encode_msg)
decode_msg = base64_decode(encode_msg)
print(decode_msg)
```

结果Example：

```python
aGVsbG8sIEFPUw==
b'hello, AOS'
```

- **bytes与list的转换函数**

功能：转换bytes为list，将list转换为bytes

```python
from aosencryfunc import list_to_binary, binary_to_list

num_list = [221, 223, 16]
binary = list_to_binary(num_list)
list_test = binary_to_list(binary)

print(binary)
print(list_test)
```

结果Example：

```python
b'\xdd\xdf\x10'
[221, 223, 16]
```

还有许多加密函数还在开发ing，期待开发者的更新...