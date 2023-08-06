from flask import Flask
from flask import render_template, redirect,url_for,make_response
from flask import request,Response,send_from_directory
from pathlib import Path
import os
from io import BytesIO
#这是一个基于flask的文件服务器
app = Flask(__name__)
mimetype_dict={
    '.jpg':"image/jpg",
    '.jpeg':"image/jpeg",
    '.html':"text/html",
    '.css':"text/css",
    '.xml':"text/xml",
    '.js':'text/javascript'
}
text_suffix = {'.html','.xml','.css','.js'}
def generate_html(d_path):
    html_string1 = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="maximum-scale=1.0,minimum-scale=1.0,user-scalable=no,
    width=device-width,initial-scale=1.0" />
'''
    fs1 = '<title>Directory listing for /{dirname}/</title>'
    html_string2='''</head>
<script>
    function change(){  
        document.getElementById("file_name").value=document.getElementById("file_content").value;  
    }  
</script>
<body>
'''
    fs2 = '<h1>Directory listing for /{dirname}/</h1>'
    html_string3 = '''<hr>
<form method="post"  enctype="multipart/form-data">
    <div class="col-sm-4">  
        <ul>
    '''
    fs3 = '     <li><a href="{i}">{j}</a></li>\n'
    html_string4='''    </ul>
</div>  
</form>
</hr>
</body>
</html>
'''
    body=[]
    for i in d_path.glob('*'):
        name = i.name
        if i.is_dir():
            dir_sep = '/'
        else:
            dir_sep = ''
        name += dir_sep
        body.append([name,name])
    dirname = d_path.name
    html_bytes = BytesIO()
    html_bytes.write(html_string1.encode('utf8'))
    html_bytes.write(fs1.format(dirname = dirname).encode('utf8'))
    html_bytes.write(html_string2.encode('utf8'))
    html_bytes.write(fs2.format(dirname = dirname).encode('utf8'))
    html_bytes.write(html_string3.encode('utf8'))
    a = [fs3.format(i=i,j=j) for i,j in body]
    html_bytes.write(''.join(a).encode('utf8'))
    html_bytes.write(html_string4.encode('utf8'))
    length = html_bytes.tell()
    html_bytes.seek(0,0)
    header = {'Content-Type':'text/html','Content-Length':str(length)}
    return html_bytes.read(),200,header
@app.route('/download/<path:filename>',methods=['POST','GET'])
def downloader(filename):
    return send_from_directory('./',filename,as_attachment=True)

def player(filename):
    BUF_SIZE=1024*1024*2
    hg = request.headers
    http_range = hg.get('Range',None)
    if http_range:
        neq = http_range.find('=')
        http_range = http_range[neq+1:].split('-')
        start = int(http_range[0])
    else:
        start = 0
    fp = open(filename,'rb')
    fp.seek(start,0)
    data = fp.read(BUF_SIZE)
    fp.close()
    file_length = Path(filename).stat().st_size
    if data:
        end =start + len(data) - 1
    else:
        end = start
    headers = {'Content-Range':f'bytes {start}-{end}/{file_length}',
            'Content-Type': 'video/mp4',
            'Accept-Ranges': 'bytes'}
    return Response(data,206,headers = headers)
@app.route('/<path:upath>')
def home(upath):
    if upath.endswith('/'):
        upath += 'index.html'
    upath_p = Path(upath)
    suffix = upath_p.suffix
    if upath_p.exists():
        if suffix in text_suffix:
            data = open(upath,encoding='utf8').read()
            mtype = mimetype_dict[suffix]
        elif suffix == '.mp4':
            return player(upath_p)
        else:
            data = open(upath,'rb').read()
            mtype = mimetype_dict.get(suffix)
        return Response(data,mimetype=mtype)
    elif upath_p.name == 'index.html':
        return generate_html(upath_p.parent)
    return ''
@app.route('/')
def home_index():
    return redirect('/index.html')
def main(port=8080,ssl=False):
    app.run('0.0.0.0',port)
if __name__ == '__main__':
    os.chdir('/media/yxs/4C68B86268B84C88/DCIM/video')
    app.run('0.0.0.0',8081)