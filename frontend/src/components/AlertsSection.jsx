import React from "react";
import SkeletonBlock from "./SkeletonBlock";

export default function AlertsSection({ alerts = [], loading = false }) {
  const colorMap = {
    red: "bg-red-50 border-red-500",
    yellow: "bg-yellow-50 border-yellow-500",
  };

  if (loading) {
    return <SkeletonBlock className="h-72 mb-6" />;
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <h2 className="text-lg font-semibold mb-4">Recent Alerts</h2>
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <p className="text-gray-500 text-sm">No alerts available.</p>
        ) : alerts.map((alert, i) => (
          <div
            key={i}
            className={`p-3 ${colorMap[alert.color]} border-l-4 rounded-r`}
          >
            <div className="flex justify-between">
              <p className="font-medium">{alert.type}</p>
              <span className="text-xs text-gray-500">{alert.time}</span>
            </div>
            <p className="text-sm">{alert.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
