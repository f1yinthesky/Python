from typing import List, Set
import asyncio
from queue import SimpleQueue
from datetime import datetime
from urllib import parse

def getUrlDomain(url:str) -> str:
    return parse.urlparse(url).netloc

def removeFragement(url:str) -> str:
    return parse.urlparse(url)._replace(fragment="").geturl()

async def genUrls(url: str) -> List[str]:
    await asyncio.sleep(2)
    path = url.split("/")
    reply_urls = []
    if len(path) < 6:
        letter = path[-1][-1]
        for i in range(4):
            new_url = url + "/" + chr(ord(letter) + i + 1)
            reply_urls.append(new_url)
            reply_urls.append(parse.urlparse(new_url)._replace(netloc="b.com").geturl())
    return reply_urls

def getUrls(url: str) -> List[str]:
    return asyncio.run(genUrls(url))

async def visitOneUrl(url_queue: SimpleQueue, visited_url: Set[str], domain_name:str) -> None:
    if url_queue.empty():
        return
    url = url_queue.get()
    print(f"{datetime.now()} url {url}")
    if url not in visited_url:
        all_urls = await genUrls(url)
    visited_url.add(url)
    for url in all_urls:
        if url not in visited_url and getUrlDomain(url) == domain_name:
            url_queue.put(url)


async def main():

    url_queue = SimpleQueue()
    first_url = "https://a.com#dd"
    domain_name = getUrlDomain(first_url)
    url_queue.put(removeFragement(first_url))

    visited_url = set()
    while not url_queue.empty():
        all_workers = []
        for i in range(10):
            all_workers.append(visitOneUrl(url_queue, visited_url, domain_name))
        await asyncio.gather(*all_workers)



if __name__=="__main__":
    asyncio.run(main())