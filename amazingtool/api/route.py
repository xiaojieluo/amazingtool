# Route

import api.handler.IndexHandler as Index
import api.handler.UserHandler as User
import api.handler.QueryHandler as Query
import api.handler.CodeHandler as Code
import api.handler.GenerateHandler as Generate
import api.handler.DataHandler as Data

route = [
    (r'/', Index.index),
    (r'/session', User.session),
    (r'/encrypt/(.*)', Code.encrypt),
    (r'/decrypt/(.*)', Code.decrypt),
    (r'/encode/(.*)', Code.encode),
    (r'/ip/(.*)', Query.ip),
    (r'/isbn/(.*)', Query.isbn),
    (r'/history', Query.history),


    (r'/data/gdp', Data.gdp),
]
