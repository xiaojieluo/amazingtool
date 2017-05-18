# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User
import api.handler.EncodeHandler as Encode

route = [
    (r'/', Index.index),
    (r'/user/(.*)', User.index),
    (r'/encode/md5', Encode.md5),
    (r'/encode/sha256', Encode.sha256),
    (r'/encode/sha224', Encode.sha224),
]
