import argparse
import statistics
import time

import requests


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", help="URL serwera HTTP")
	parser.add_argument("-n", "--requests", type=int, default=1000,
						help="Liczba żądań (domyślnie: 1000)")
	args = parser.parse_args()

	latencies = []
	total_bytes = 0
	successful = 0

	start = time.perf_counter()

	for _ in range(args.requests):
		request_start = time.perf_counter()

		try:
			response = requests.get(args.url, timeout=10)
			latency = time.perf_counter() - request_start

			latencies.append(latency)
			total_bytes += len(response.content)

			if 200 <= response.status_code < 400:
				successful += 1

		except requests.RequestException as e:
			print(f"Request failed: {e}")

	elapsed = time.perf_counter() - start

	if not latencies:
		print("No successful HTTP responses.")
		return

	latencies_ms = [latency * 1000 for latency in latencies]

	print("\n--- HTTP Benchmark Results ---")
	print(f"URL:             {args.url}")
	print(f"Total requests:  {args.requests}")
	print(f"Received:        {len(latencies)}")
	print(f"Successful:      {successful}")
	print(f"Total time:      {elapsed:.3f} s")
	print(f"Throughput:      {len(latencies) / elapsed:.2f} req/s")
	print(f"Avg latency:     {statistics.mean(latencies_ms):.2f} ms")
	print(f"Median latency:  {statistics.median(latencies_ms):.2f} ms")
	print(f"Min latency:     {min(latencies_ms):.2f} ms")
	print(f"Max latency:     {max(latencies_ms):.2f} ms")
	print(f"P95 latency:     {sorted(latencies_ms)[int(0.95 * (len(latencies_ms) - 1))]:.2f} ms")
	print(f"Response size:   {total_bytes / 1024:.2f} KiB")
	print(f"Transfer rate:   {total_bytes / elapsed / 1024:.2f} KiB/s")


if __name__ == "__main__":
	main()