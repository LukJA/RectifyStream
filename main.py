# RectifyStream
# Dependecy azure-storage-blob

# Rectify resource keys:
# DefaultEndpointsProtocol=https;AccountName=rectify;AccountKey=a9be73PYVTFWPW9piDagZ0n2CeESLwXbajh7bPhM5nyfUFSPgGaqR1WEHg08Wl8pLk+TZGS54FkeQeXUzTuR7A==;EndpointSuffix=core.windows.net

import os, uuid, time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Define a user ID for container storage 
containerID = "conone"
# setup connection string
connect_str = "DefaultEndpointsProtocol=https;AccountName=rectify;AccountKey=a9be73PYVTFWPW9piDagZ0n2CeESLwXbajh7bPhM5nyfUFSPgGaqR1WEHg08Wl8pLk+TZGS54FkeQeXUzTuR7A==;EndpointSuffix=core.windows.net"


# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "test_container"

# Create the container
container_client = blob_service_client.create_container(container_name)


# Create a file in local Documents directory to upload and download
local_path = "./data"
local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"
upload_file_path = os.path.join(local_path, local_file_name)

# Write text to the file
file = open(upload_file_path, 'w')
file.write("Hello, World!")
file.close()

# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

# Upload the created file
with open(upload_file_path, "rb") as data:
    blob_client.upload_blob(data)

print("\nListing blobs...")

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

# Clean up
time.sleep(5)

print("Deleting blob container...")
container_client.delete_container()

print("Deleting the local source and downloaded files...")
os.remove(upload_file_path)
os.remove(download_file_path)

print("Done")