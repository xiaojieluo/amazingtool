# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User
import api.handler.EncodeHandler as Encode

route = [
    (r'/', Index.index),
    (r'/user/(.*)', User.index),
    (r'/encode/md5', Encode.md5),
]
