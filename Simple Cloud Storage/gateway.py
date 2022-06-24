from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug import Response


class GatewayService:
    name = 'gateway'

    filerpc = RpcProxy('file_service')


    #upload file
    @http('POST', '/upload')
    def upload(self, request):
        file = request.files['file']
        filename = file.filename
        print(filename)
        path = 'file/{}'.format(filename)
        file.save(path)
        files = self.filerpc.upload(path)
        if files == True:
            return 'File uploaded successfully'
        else:
            return 'File upload failed'
        
    @http('GET', '/download/<int:id>')
    def download(self, request, id):
        file = self.filerpc.download(id)

        path = file['file']
        response = Response(open(path, 'rb').read())
        #get file type
        file_type = path.split('.')[-1]
        if file_type == 'png':
            response.mimetype = 'image/png'
        elif file_type == 'jpg':
            response.mimetype = 'image/jpeg'
        elif file_type == 'pdf':
            response.mimetype = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(path)
        return response
        
