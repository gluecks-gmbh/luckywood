"""

"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Frederik Glücks - Glücks GmbH"

# Built-in/Generic Imports
import gzip
import glob
import json

# External libs/modules
import boto3
from boto3.dynamodb.types import TypeDeserializer


# own libs


class AwsDynamoDbBackup:
    __dynamodb = boto3.resource("dynamodb", use_ssl=True, verify=True)

    @staticmethod
    def import_s3_backup(folder: str, table_name: str, show_progress=False) -> int:
        """

        @param show_progress: If true the imported line will be printed
        @param folder: Folder that contains the AWS DynamoDB S3 Backup
        @param table_name: DynamoDB table name
        @return: int - Returns the number of imported lines
        """
        # Add data to folder, to get backup jsons
        folder = f"{folder}/data/*"

        # create DynamoDB table
        table_obj = AwsDynamoDbBackup.__dynamodb.Table(table_name)

        # go through all backup jsons

        type_deserializer = TypeDeserializer()

        number_of_lines: int = 0

        for filename in glob.glob(folder):
            with gzip.open(filename, 'rb') as f:
                json_lines = f.read().decode('utf-8').split("\n")

                for json_line in json_lines:
                    if json_line != "":
                        table_obj.put_item(
                            Item=type_deserializer.deserialize({
                                "M": json.loads(json_line)["Item"]
                            })
                        )
                        number_of_lines += 1

                        if show_progress is True:
                            print(json_line)

        return number_of_lines
