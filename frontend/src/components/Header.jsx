import React from "react";

export default function Header() {
  return (
    <header className="bg-white shadow-sm p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Fraud Detection Dashboard</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <i className="fas fa-bell text-gray-500"></i>
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </div>
          <span className="text-sm font-medium">BI-OJK Hackathon 2025</span>
        </div>
      </div>
    </header>
  );
}