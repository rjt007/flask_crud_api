import schema

user_schema = schema.Schema({
    'name': str,
    'email': str,
    'password': str
})

schema_error = schema.SchemaError