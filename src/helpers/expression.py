MONGO_OP_DICT = {
    "=": "$eq"
}

# { "songs.song.title": {"$eq": "Separuh Jiwaku Pergi" }
def evaluate(field, op, value):
    mongo_op = MONGO_OP_DICT[op]
    filter = { field: { mongo_op: value }}
    return filter
