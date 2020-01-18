# RectifyStream
# Dependecy azure-storage-blob , picamera

# Rectify resource keys:
# DefaultEndpointsProtocol=https;AccountName=rectify;AccountKey=a9be73PYVTFWPW9piDagZ0n2CeESLwXbajh7bPhM5nyfUFSPgGaqR1WEHg08Wl8pLk+TZGS54FkeQeXUzTuR7A==;EndpointSuffix=core.windows.net

import os, uuid, time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from picamera import PiCamera


# configure camera
camera = PiCamera()
camera.resolution = (1024, 768)

# setup connection string
#connect_str = "DefaultEndpointsProtocol=https;AccountName=rectify;AccountKey=a9be73PYVTFWPW9piDagZ0n2CeESLwXbajh7bPhM5nyfUFSPgGaqR1WEHg08Wl8pLk+TZGS54FkeQeXUzTuR7A==;EndpointSuffix=core.windows.net"
connect_str = "DefaultEndpointsProtocol=https;AccountName=rectify;AccountKey=gjfOU1J6UkImVEbsvzXDv+aOO7EODefXZUbsX4faXZ83yI4G8XleQxPR7MquxIvZmF86mhJApEmM+dCPjotJMw==;EndpointSuffix=core.windows.net"

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "container" + str(uuid.uuid4())

# Create the container
container_client = blob_service_client.create_container(container_name)

try:
    while(True):

        # Generate a new image
        camera.start_preview()
        time.sleep(2)
        # Generate a unique name
        file_name = "img" + str(uuid.uuid4()) + ".jpg"
        img_name = "/home/pi/data/" + file_name
        camera.capture(img_name)
        camera.stop_preview()

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        print("\nUploading image to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        with open(img_name, "rb") as data:
            blob_client.upload_blob(data)

        print("\nListing blobs...")

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)

        time.sleep(30)

except KeyboardInterrupt:
    # Clean up
    time.sleep(5)

    print("Deleting blob container...")
    container_client.delete_container()


print("Teardown Complete")
