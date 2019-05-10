import logging
import os

import asyncio

from aiohttp import web
import aiofiles

from config import CONFIG


async def get_archive_part(data_path):
    chunk_archive = await asyncio.create_subprocess_shell(
        f'zip -r - {CONFIG["photos_path"]}/{data_path}/| base64 | base64 -d',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return chunk_archive


async def check_data_path_exist(data_path):
    return os.path.exists(f'{CONFIG["photos_path"]}/{data_path}')


async def archive_handle(request):
    response = web.StreamResponse()
    archive_hash = request.match_info.get('archive_hash')
    is_path_exist = await check_data_path_exist(archive_hash)
    if not is_path_exist:
        return web.Response(
            text='Архив не существует или был удален',
            status=404
        )
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_hash}.zip"'

    await response.prepare(request)

    chunk_archive = await get_archive_part(archive_hash)

    try:
        while True:
            stdout = await chunk_archive.stdout.readline()
            logging.debug('Sending archive chunk ...')
            if not stdout:
                break
            await response.write(stdout)
            await asyncio.sleep(CONFIG['response_timeout'])
    except asyncio.CancelledError:
        chunk_archive.kill()
        response.force_close()
        raise
    await response.write_eof()
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    if CONFIG['logging']:
        logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    host = CONFIG['host']
    port = CONFIG['port']
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive_handle),
    ])
    web.run_app(app, host=host, port=port)
