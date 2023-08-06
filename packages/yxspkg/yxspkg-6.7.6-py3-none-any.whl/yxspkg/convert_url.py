import re
from urllib.parse import urlparse
from pathlib import Path
import os
from multiprocessing import Pool
import sys
import click
def get_all_url(filename):
    href = re.compile(b'((href|src)="[^"]*")|((href|src)=\'[^\']*\')')
    p = Path(filename)
    if p.is_file():
        htmls = [p]
    else:
        htmls = [Path(root) / j for root,_,files in os.walk(p) for j in files if j.endswith('.html')]
    urls = [h.group() for i in htmls  for h in href.finditer(open(i,'rb').read())]
    return urls
def convert_local(filename,website,href=None,rate=None,local_level=None):
    # print(f'\b\b\b\b\b\b\b{rate:.2f}%',end='')
    print(filename)
    if href is None:
        href = re.compile(b'((href|src)="[^"]*")|((href|src)=\'[^\']*\')')
    os.chdir(Path(filename).parent)
    def local_url(matched):
        s = matched.groups()
        url = s[1]
        if url.startswith(b'"') or url.startswith(b"'"):
            url = url[1:-1]
        level = None
        if not url or not url.isascii():
            return s[0] + b'=' + s[1]
        urlp = urlparse(url)
        
        netloc = urlp.netloc
        if netloc:
            level = 1
            url = urlp.path
            if not url:
                url =b'/'
        # print(urlp,url)
        if url.startswith(b'/'):
            level = 1
        if level is not None:
            if local_level == 1:
                if netloc:
                    url = b'../'+netloc+url
                else:
                    url = b'.'+url 
            else:
                lt = b''
                if level==1 and netloc:
                    lt=b'../'+netloc+b'/'
                url = b'../'*(local_level - level)+lt+url[1:]
        # print(urlp,url,'ttttttt')
        #补全
        dpath = Path(url.decode('utf8'))
        if not dpath.suffix and dpath.is_dir() and dpath.name:
            index_file = dpath / 'index.html'
            suffix = b''
            if index_file.is_file():
                if url[-1:] == b'/':
                    suffix = b'index.html'
                else:
                    suffix = b'/index.html'
            else:
                index_file = dpath.with_suffix('.html')
                if index_file.is_file():
                    suffix = b'.html'
                
            url += suffix
        # print(url,'ttt')reboot
        return s[0] + b'="' + url + b'"'
    if local_level is None:
        n = filename.find(website)
        ff = filename[n+len(website):]
        local_level = ff.count('/')
    ttt = open(filename,'rb').read()
    t = href.sub(local_url,ttt)
    open(filename,'wb').write(t)
def convert_dir(dirname,threads=9):
    p = Path(dirname).absolute()
    website = p.name
    href = re.compile(b'(href|src|url) *= *("[^" ]*"|\'[^\' ]*\'|\\S+)')
    htmls = []
    now_level = len(p.parts)
    for root,_,files in os.walk(p):
        for j in files:
            if j.endswith('.html'):
                p = Path(root) / j
                if p.name.endswith('html.html'):
                    os.remove(p)
                    continue
                # if p.name == '467428.html':
                htmls.append((str(p),len(p.parts) - now_level))
                # convert_local(htmls[0][0],website,href,1,htmls[0][1])
    n = len(htmls)
    print(n)
    if threads > 1:
        po = Pool(threads)
        for i,(h,level) in enumerate(htmls):
            po.apply_async(convert_local,(h,website,href,i/n,level))
            # print(h)
            # convert_local(h,website,href,i/n,level)
        po.close()
        po.join()
    else:
        for i,(h,level) in enumerate(htmls):
            convert_local(h,website,href,i/n,level)
@click.command()
@click.argument('dirname')
@click.option('--threads','-t',default=9,help="并行线程数")
def main(dirname,threads=9):
    convert_dir(dirname,threads)
if __name__=='__main__':
    # convert_dir(sys.argv[1])
    convert_dir('/media/yxs/4C68B86268B84C88/DCIM/web/444luo.com/444luo.com/')