# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User
import api.handler.EncodeHandler as Encode
import api.handler.DecodeHandler as Decode

route = [
    (r'/', Index.index),
    (r'/user/(.*)', User.index),

    (r'/encode', Encode.index),
    #
    # (r'/encode/md5', Encode.md5),
    # (r'/encode/sha1', Encode.sha1),
    # (r'/encode/sha224', Encode.sha224),
    # (r'/encode/sha256', Encode.sha256),
    # (r'/encode/sha384', Encode.sha384),
    # (r'/encode/sha512', Encode.sha512),
    # (r'/encode/blake2b', Encode.blake2b),
    # (r'/encode/shake128', Encode.shake128),
    # (r'/encode/shake256', Encode.shake256),

    (r'/decode/md5', Decode.md5),
]
