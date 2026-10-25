import argparse
import asyncio
from pathlib import Path
from time import perf_counter

import httpx


async def benchmark(url, image_path, num_requests, concurrency):
    image = Path(image_path)
    files = {"file": (image.name, image.read_bytes())}
    latencies = []
    errors = 0
    concurrency = min(concurrency, num_requests)

    async with httpx.AsyncClient(
        timeout=30.0, limits=httpx.Limits(max_connections=concurrency)
    ) as client:
        # Warm up the server and connection outside the measured interval.
        response = await client.post(url, files=files)
        response.raise_for_status()

        async def worker(count):
            nonlocal errors
            for _ in range(count):
                start = perf_counter()
                try:
                    response = await client.post(url, files=files)
                    response.raise_for_status()
                except httpx.HTTPError:
                    errors += 1
                else:
                    latencies.append(perf_counter() - start)

        start = perf_counter()
        await asyncio.gather(*(
            worker(len(range(i, num_requests, concurrency)))
            for i in range(concurrency)
        ))
        elapsed = perf_counter() - start

    print(f"Requests: {num_requests} | Concurrency: {concurrency}")
    print(f"Successful: {len(latencies)} | Failed: {errors}")
    print(f"Elapsed: {elapsed:.3f} s")
    print(f"Throughput (successful): {len(latencies) / elapsed:.2f} req/s")
    if latencies:
        print(f"Mean latency (successful): {sum(latencies) / len(latencies) * 1000:.2f} ms")


def main():
    parser = argparse.ArgumentParser(description="Benchmark the MNIST inference API")
    parser.add_argument("--url", default="http://127.0.0.1:8000/predict")
    parser.add_argument("--image", default="images/two.png")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=10)
    args = parser.parse_args()
    if args.requests <= 0 or args.concurrency <= 0:
        parser.error("--requests and --concurrency must be positive")
    try:
        asyncio.run(benchmark(args.url, args.image, args.requests, args.concurrency))
    except (OSError, httpx.HTTPError) as error:
        parser.exit(1, f"Benchmark failed: {error}\n")


if __name__ == "__main__":
    main()
