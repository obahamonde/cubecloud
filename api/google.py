import json

from typing import Iterable

from api.services import Aiogoogle

from api.config import env

from aiogoogle.auth.creds import ServiceAccountCreds


creds = json.loads(open(env.GOOGLE_APPLICATION_CREDENTIALS).read())


class Storage:

    """Class for interacting with Cloud Functions and GCS"""


    @property

    def credentials(self) -> ServiceAccountCreds:

        """Service account credentials object"""

        return ServiceAccountCreds(**creds, scopes=env.GOOGLE_SCOPES)


    async def list_storage_buckets(self):

        async with Aiogoogle(service_account_creds=self.credentials) as aiogoogle:

            storage = await aiogoogle.discover("storage", "v1")

            return await aiogoogle.as_service_account(

                storage.buckets.list(project=creds["project_id"])
            )

    async def upload_file(self, file: bytes, key: str, content_type: str):

        async with Aiogoogle(service_account_creds=self.credentials) as aiogoogle:

            storage = await aiogoogle.discover("storage", "v1")

            try: 
                return await aiogoogle.as_service_account(

                    storage.objects.insert(

                        bucket=env.BUCKET_NAME,

                        name=key,

                       upload_file=file,
                       
                       content_type=content_type

                    )

                )
            except Exception as e:
                print(e)
                print(content_type)
                return e
            
    async def get_objects_from_bucket(self):
        async with Aiogoogle(service_account_creds=self.credentials) as aiogoogle:
            storage = await aiogoogle.discover("storage", "v1")
            try: 
                return await aiogoogle.as_service_account(
                    storage.objects.list(bucket=env.BUCKET_NAME)
                )
                
            except Exception as e:
                print(e)
                return e
            
         