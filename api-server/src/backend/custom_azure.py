from storages.backends.azure_storage import AzureStorage
import os

azure_key = os.getenv('AZURE_STORAGE_KEY')


class AzureMediaStorage(AzureStorage):
    account_name = 'jtf191blobstorage' # Must be replaced by your <storage_account_name>
    account_key = azure_key
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'jtf191blobstorage' # Must be replaced by your storage_account_name
    account_key = azure_key
    azure_container = 'static'
    expiration_secs = None
