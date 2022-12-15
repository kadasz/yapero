#!/usr/bin/env python3

import yaml
import ujson
import asyncio
import aioredis
import argparse

async def enc(node: str):
    pool = aioredis.ConnectionPool.from_url('redis://localhost/1', port=6380, max_connections=10, decode_responses=True)
    redis = aioredis.Redis(connection_pool=pool)
    lookup_host = await redis.execute_command('keys' , f'host:{node}:*')
    if lookup_host:
        validate_host = ':'.join(''.join(lookup_host).split(':')[1:])
        out = await redis.execute_command('get', f'puppet:{validate_host}')
        print(yaml.dump(ujson.loads(out)))


def main():
    parser = argparse.ArgumentParser(description='YAPERO')
    parser.add_argument('--node',
                        dest='node'
                        help='Type node name like hostname')
    args=parser.parse_args()
    nodename= ''.join(args.node.split('.')[0::-1]) if '.' in args.node else args.node
    asyncio.run(enc(nodename))

if __name__ == 'main':
    main()
