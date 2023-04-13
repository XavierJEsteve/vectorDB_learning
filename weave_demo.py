import weaviate
import json

def schema_config(client) :
    client.schema.delete_all()
    class_obj = {
        "class": "Command",
        "description": "A list of useful commands for an interactive game.",
        "properties": [
            {
                "dataType": ["text"],
                "name": "command"
            }
        ],
        "vectorizer": "text2vec-transformers"  # Or "text2vec-cohere" or "text2vec-huggingface"
    }
    client.schema.create_class(class_obj)

def test_schema(client):
    print(json.dumps(client.schema.get(), indent=4))

def load_data(client):
    json_file_path = './house_nav.json'
    data = [{}]
    # Open the file and load the JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    with client.batch as batch:
        batch.batch_size=1
        for i, d in enumerate(data):
            properties = {
                "command": d["phrase"],
            }

            client.batch.add_data_object(properties, "Command")

def check_data(client):
    print(client.query.aggregate("Command").with_meta_count().do())
################################################################

client = weaviate.Client(
    url = "http://localhost:8080",  # Replace with your endpoint
)

schema_config(client)
test_schema(client)
load_data(client)
check_data(client)

nearText = {"concepts": ["head to aquarium"]}

result = (
    client.query
    .get("Command", ["command"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(result)
