import subprocess
import re
import matplotlib.pyplot as plt

concurrency_levels = range(50, 101, 10)
throughputs = []
latencies = []

for n in concurrency_levels:
	output = subprocess.check_output(
		["python", "benchmark.py", "--requests", "1000", "--concurrency", str(n)],
		text=True,
	)
	print(output)

	throughput = re.search(r"Throughput \(successful\): ([\d.]+)", output)
	latency = re.search(r"Mean latency \(successful\): ([\d.]+)", output)

	throughputs.append(float(throughput.group(1)))
	latencies.append(float(latency.group(1)))

fig, ax1 = plt.subplots()

ax1.plot(concurrency_levels, throughputs, "o-", label="Throughput")
ax1.set_xlabel("Concurrency")
ax1.set_ylabel("Throughput (req/s)")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(concurrency_levels, latencies, "s-", label="Latency")
ax2.set_ylabel("Mean latency (ms)")

plt.title("Throughput and Latency vs Concurrency")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

plt.tight_layout()
plt.show()