import boto3 
import json 
 
s3 = boto3.resource("s3") # the object that will help you read data from S3 5 
# Gets data from the file "users.json" 
# which is within the folder "lab2" 
# which is within the bucket "cse-427" 
def get_data(): 
    obj = s3.Object("put-your-bucket-name-here", "put-your-folder-and-data-here") # gets the file contents 
    body = obj.get()['Body'].read() # reads the file contents as a string 
    users_data = json.loads(body) # converts string into json 
    users = [
        {
            "name": user["name"],
            "phone": user["phone"],
            "fave_color": user["fave_color"],
        }
        for user in users_data.get("users", [])
    ]
    return users # returns json from file 
 
print(get_data()) # calls and prints returned json data
