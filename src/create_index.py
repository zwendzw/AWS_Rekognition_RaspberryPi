import boto3

# use aws cli credentials
s3_client = boto3.client('s3')
rek_client = boto3.client('rekognition', region_name = 'eu-west-1')

# custom access key
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id='',
#     aws_secret_access_key='',
# )
# rek_client=boto3.client('rekognition',
#                             aws_access_key_id='',
#                             aws_secret_access_key='',
#                             region_name = 'eu-west-1')

collectionId = 'facecollection' #collection name

bucket = 'face-indexs' #S3 bucket name
all_objects = s3_client.list_objects(Bucket = bucket )

list_response=rek_client.list_collections(MaxResults = 2)

if collectionId in list_response['CollectionIds']:
    rek_client.delete_collection(CollectionId = collectionId)

rek_client.create_collection(CollectionId = collectionId)

for content in all_objects['Contents']:
    collection_name,collection_image = content['Key'].split('/')
    if collection_image:
        label = collection_name
        print('indexing: ',label)
        image = content['Key']
        # 使用 rekognition API "index_faces" 
        index_response=rek_client.index_faces(CollectionId = collectionId,
                                Image={'S3Object': {'Bucket' : bucket,'Name' : image}},
                                ExternalImageId = label,
                                MaxFaces = 1,
                                QualityFilter = "AUTO",
                                DetectionAttributes = ['ALL'])
        print('FaceId: ',index_response['FaceRecords'][0]['Face']['FaceId'])
