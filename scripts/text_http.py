#!/usr/bin/env python3

import argparse
import aiohttp
import asyncio
import time
import uvloop
import gevent.pool
import json
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

SITE = "https://mock-site.herokuapp.com/text"

async def aiohttp_fetch() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(SITE) as response:
            return await response.text()


async def execute_asyncio_requests(number_of_requests: int) -> None:
    await asyncio.wait([aiohttp_fetch() for i in range(number_of_requests)])


def gevent_fetch(http):
    http.get("/")


def execute_gevent_requests(number_of_requests: int) -> None:
    url = URL(SITE)
    http = HTTPClient.from_url(url, concurrency=1)

    pool = gevent.pool.Pool(20)
    for _ in range(1, number_of_requests):
        pool.spawn(gevent_fetch, http)

    pool.join()
    http.close()

async def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP requests with text/plain benchmark")
    parser.add_argument("--requests", type=int, default=1, help="number of requests", required=False)
    parser.add_argument("--type", type=str, default=1, help="number of requests", choices=["asyncio", "gevent", "uvloop"], required=True)

    args = parser.parse_args()

    if args.type == "asyncio":
        s = time.perf_counter()
        await execute_asyncio_requests(args.requests)
    if args.type == "uvloop":
        uvloop.install()
        s = time.perf_counter()
        await execute_asyncio_requests(args.requests)
    if args.type == "gevent":
        import geventhttpclient.httplib
        geventhttpclient.httplib.patch()
        s = time.perf_counter()
        execute_gevent_requests(args.requests)

    elapsed = time.perf_counter() - s
    print(f"Benchmark executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    s = time.perf_counter()

    asyncio.run(main())

