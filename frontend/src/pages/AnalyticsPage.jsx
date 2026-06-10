// src/pages/AnalyticsPage.jsx
import React, { useRef } from "react";
import FraudTrendChart from "../components/FraudTrendChart";
import StatusPieChart from "../pages/StatusPieChart";
import FraudByRegionChart from "../components/FraudByRegionChart";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { dashboardService } from "../services/dashboardService";
import { useAsync } from "../hooks/useAsync";
import SkeletonBlock from "../components/SkeletonBlock";

export default function AnalyticsPage() {
  const exportRef = useRef(null);
  const trend = useAsync(dashboardService.transactionTrends, []);
  const status = useAsync(dashboardService.fraudAnalysis, []);
  const branch = useAsync(dashboardService.branchComparison, []);
  const summary = useAsync(dashboardService.analyticsSummary, []);

  const handleExportPDF = async () => {
    const element = exportRef.current;
    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");

    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("fraud-analytics.pdf");
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Analytics Overview</h2>
        <div className="space-x-2">
          <button
            onClick={handleExportPDF}
            className="px-4 py-2 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            Export Report
          </button>
          <button className="px-4 py-2 text-sm border rounded text-gray-700 hover:bg-gray-100">
            Filter Data
          </button>
        </div>
      </div>

      {/* === Export Target Start === */}
      <div className="space-y-8" ref={exportRef}>
        {/* Ringkasan */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {summary.loading ? [0, 1, 2].map((item) => <SkeletonBlock key={item} className="h-24" />) : (summary.data || []).map((stat, i) => (
            <div key={i} className="bg-white p-4 rounded-lg shadow">
              <p className="text-sm text-gray-500">{stat.label}</p>
              <p className={`text-xl font-semibold ${stat.color}`}>{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Chart Bagian 1 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Fraud Trend</h3>
            {trend.loading ? <SkeletonBlock className="h-[260px]" /> : <FraudTrendChart monthlyData={trend.data} />}
          </div>
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Status Breakdown</h3>
            {status.loading ? <SkeletonBlock className="h-[260px]" /> : <StatusPieChart chartData={status.data} />}
          </div>
        </div>

        {/* Chart Bagian 2 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2">Fraud by Region</h3>
          {branch.loading ? <SkeletonBlock className="h-[260px]" /> : <FraudByRegionChart chartData={branch.data} />}
        </div>
      </div>
      {/* === Export Target End === */}
    </div>
  );
}
