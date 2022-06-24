from nameko.rpc import rpc

import dependencies

class fileservice:
    name = 'file_service'

    database = dependencies.Database()

    @rpc
    def upload(self, path):
        return self.database.upload_file(path)

    @rpc
    def download(self, id):
        return self.database.download_file(id)