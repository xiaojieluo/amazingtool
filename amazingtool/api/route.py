# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User

route = [
    (r'/', Index.index),
    (r'/user/(.*)', User.index),
]
