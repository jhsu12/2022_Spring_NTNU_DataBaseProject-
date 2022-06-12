from django.db import connection

# turn data to dict
def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

# execute raw sql query
def SQL(SQL):
    cursor = connection.cursor()
    cursor.execute(SQL)
    data = dictfetchall(cursor)
    return data