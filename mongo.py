from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new client and connect to the server

uri = "YOUR_API"
client = MongoClient(uri)
mongo_db = client['data']
suppliers = mongo_db['suppliers']
materials = mongo_db['materials']
fences = mongo_db['fences']
roofs = mongo_db['roofs']
foundations = mongo_db['foundations']
walls = mongo_db['walls']
houses = mongo_db['houses']

# suppliers_list = [
#     {"_id": 0, "name": "ООО СтройМир", "address": "г. Москва, ул. Ленина, 10", "phone": "+7 (495) 123-45-67"},
#     {"_id": 1, "name": "ИП Иванов", "address": "Адрес: г. Санкт-Петербург, ул. Пушкина, 5", "phone": "+7 (812) 555-55-55"},
#     {"_id": 2, "name": "ООО СтройСервис", "address": "г. Екатеринбург, ул. Гагарина, 20", "phone": "+7 (343) 987-65-43"}
# ]
# suppliers.insert_many(suppliers_list)

# materials_list = [
#     {'_id': 0, 'name': 'Бетон', 'supplier_id': 0},
#     {'_id': 1, 'name': 'Сталь', 'supplier_id': 1},
#     {'_id': 2, 'name': 'Железобетон', 'supplier_id': 0},
#     {'_id': 3, 'name': 'Дерево', 'supplier_id': 2},
#     {'_id': 4, 'name': 'Кирпич', 'supplier_id': 1},
#     {'_id': 5, 'name': 'газобетон', 'supplier_id': 0},
#     {'_id': 6, 'name': 'Металл', 'supplier_id': 0}
# ]
# materials.insert_many(materials_list)

# fences.insert_many([
#     {'_id': 0, "name": "Забор из кирпича", "material_id": materials.find_one({"name": "Кирпич"})['_id']},
#     {'_id': 1, "name": "Забор из стали", "material_id": materials.find_one({"name": "Сталь"})['_id']},
#     {'_id': 2, "name": "Забор из бетона", "material_id": materials.find_one({"name": "Бетон"})['_id']}
# ])
#
# foundations.insert_many([
#   {'_id': 0, 'name': "Свайный", "material_id": materials.find_one({"name": "Сталь"})['_id']},
#   {'_id': 1, 'name': "Монолитный", "material_id": materials.find_one({"name": "Бетон"})['_id']},
#   {'_id': 2, 'name': "Железобетонный",  "material_id": materials.find_one({"name": "Железобетон"})['_id']}
# ])
#
# roofs.insert_many([
#     {'_id': 0, 'name': "Деревянная черепица", "material_id": materials.find_one({"name": "Дерево"})['_id']},
#     {'_id': 1, 'name': "Металлочерепица", "material_id": materials.find_one({"name": "Металл"})['_id']},
#     {'_id': 2, 'name': "Профнастил", "material_id": materials.find_one({"name": "Металл"})['_id']}
# ])
#
# walls.insert_many([
#   {'_id': 0, 'name': "Кирпичный", "material_id": materials.find_one({"name": "Кирпич"})['_id']},
#   {'_id': 1, 'name': "Газобетонный", "material_id": materials.find_one({"name": "Газобетон"})['_id']}
# ])
#
# houses.insert_many([
#     {'_id': 0, 'name': "Дом из кирпича с металлочерепицей",
#         "foundation_id": foundations.find_one({"name": "Железобетонный"})['_id'],
#         "roof_id": roofs.find_one({"name": "Металлочерепица"})['_id'],
#         "wall_id": walls.find_one({"name": "Кирпичный"})['_id']
#     }
# ])



