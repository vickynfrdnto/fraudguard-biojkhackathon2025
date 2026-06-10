import React from "react";
import SkeletonBlock from "./SkeletonBlock";

export default function StatsCards({ stats = [], loading = false }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[0, 1, 2, 3].map((item) => <SkeletonBlock key={item} className="h-32" />)}
      </div>
    );
  }

  if (!stats.length) {
    return <div className="bg-white rounded-lg shadow p-4 mb-6 text-sm text-gray-500">No dashboard summary available.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, i) => (
        <div key={i} className="bg-white rounded-lg shadow p-4">
          <div className="flex justify-between">
            <div>
              <p className="text-gray-500">{stat.title}</p>
              <h3 className="text-2xl font-bold">{stat.value}</h3>
            </div>
            <div className={`w-12 h-12 rounded-full ${stat.bg} flex items-center justify-center`}>
              <i className={`fas ${stat.icon} ${stat.text}`}></i>
            </div>
          </div>
          <p className={`text-sm mt-2 ${stat.changeColor}`}>{stat.change}</p>
        </div>
      ))}
    </div>
  );
}
