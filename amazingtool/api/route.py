# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User
import api.handler.EncryptHandler as Encrypt
import api.handler.EncodeHandler as Encode
import api.handler.DecodeHandler as Decode
import api.handler.DecryptHandler as Decrypt
import api.handler.IpHandler as Ip
import api.handler.QueryHandler as Query

route = [
    (r'/', Index.index),
    (r'/user/(.*)', User.index),

    (r'/encrypt', Encrypt.index),
    (r'/decrypt', Decrypt.index),
    (r'/encode', Encode.index),
    (r'/ip', Ip.index),
    (r'/isbn', Query.isbn),
    # (r'/decode/md5', Decode.md5),
]
