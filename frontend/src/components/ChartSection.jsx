import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";
import SkeletonBlock from "./SkeletonBlock";

export default function ChartSection({ chartData, loading = false }) {
  const chartRef = useRef();
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (!chartData || !chartRef.current) return;
    if (chartInstanceRef.current) chartInstanceRef.current.destroy();
    const ctx = chartRef.current.getContext("2d");
    chartInstanceRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: chartData.labels,
        datasets: chartData.datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
          tooltip: { mode: "index", intersect: false },
        },
        scales: { y: { beginAtZero: true } },
      },
    });
    return () => chartInstanceRef.current?.destroy();
  }, [chartData]);

  if (loading) {
    return <SkeletonBlock className="h-[372px] mb-6" />;
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Fraud Detection Trend</h2>
        <div className="flex space-x-2">
          <button className="px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded">Day</button>
          <button className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded">Week</button>
          <button className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded">Month</button>
        </div>
      </div>
      <div style={{ height: "300px" }}>
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
}
