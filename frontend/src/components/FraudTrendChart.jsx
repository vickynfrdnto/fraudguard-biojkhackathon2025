// src/components/FraudTrendChart.jsx
import React, { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";

export default function FraudTrendChart({ monthlyData, yearlyData }) {
  const chartRef = useRef();
  const chartInstanceRef = useRef(null);
  const [view, setView] = useState("monthly");

  const chartData = {
    monthly: {
      labels: monthlyData?.labels || [],
      normal: monthlyData?.datasets?.[0]?.data || [],
      fraud: monthlyData?.datasets?.[1]?.data || [],
    },
    yearly: {
      labels: yearlyData?.labels || monthlyData?.labels || [],
      normal: yearlyData?.datasets?.[0]?.data || monthlyData?.datasets?.[0]?.data || [],
      fraud: yearlyData?.datasets?.[1]?.data || monthlyData?.datasets?.[1]?.data || [],
    },
  };

  useEffect(() => {
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext("2d");
    chartInstanceRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: chartData[view].labels,
        datasets: [
          {
            label: "Normal Transactions",
            data: chartData[view].normal,
            borderColor: "#3B82F6",
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            tension: 0.4,
            fill: true,
          },
          {
            label: "Fraud Detected",
            data: chartData[view].fraud,
            borderColor: "#EF4444",
            backgroundColor: "rgba(239, 68, 68, 0.1)",
            tension: 0.4,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    });

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [view]);

  return (
    <div>
      <div className="flex justify-end gap-2 mb-4">
        <button
          onClick={() => setView("monthly")}
          className={`px-3 py-1 text-sm rounded ${
            view === "monthly"
              ? "bg-indigo-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          Monthly
        </button>
        <button
          onClick={() => setView("yearly")}
          className={`px-3 py-1 text-sm rounded ${
            view === "yearly"
              ? "bg-indigo-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          Yearly
        </button>
      </div>

      <div className="relative w-full h-[240px] md:h-[260px]">
        <canvas ref={chartRef} className="absolute inset-0" />
      </div>
    </div>
  );
}
