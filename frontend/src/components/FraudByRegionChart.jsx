// src/components/FraudByRegionChart.jsx
import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

export default function FraudByRegionChart({ chartData }) {
  const chartRef = useRef();
  const chartInstanceRef = useRef();

  useEffect(() => {
    if (!chartData) return;
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext("2d");
    chartInstanceRef.current = new Chart(ctx, {
      type: "bar",
      data: {
        labels: chartData.labels,
        datasets: chartData.datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 5 },
          },
        },
      },
    });

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [chartData]);

  return (
    <div className="relative w-full h-[240px] md:h-[260px]">
      <canvas ref={chartRef} className="absolute inset-0" />
    </div>
  );
}
