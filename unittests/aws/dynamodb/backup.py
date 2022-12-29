import unittest
from luckywood.aws.dynamodb.backup import AwsDynamoDbBackup


class AwsDynamoDbBackupTest(unittest.TestCase):

    def test_import(self):
        imports = [
            {
                "folder": "",
                "table_name": ""
            }
        ]
        for import_job in imports:
            self.assertGreater(
                AwsDynamoDbBackup.import_s3_backup(
                    import_job["folder"],
                    import_job["table_name"],
                    True
                ),
                0
            )


if __name__ == '__main__':
    unittest.main()
