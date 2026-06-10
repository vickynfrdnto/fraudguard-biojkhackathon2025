// src/components/Sidebar.jsx
import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();
  const path = location.pathname;

  const menuItems = [
    { icon: "fa-tachometer-alt", text: "Dashboard", path: "/" },
    { icon: "fa-chart-line", text: "Analytics", path: "/analytics" }, // bisa nanti ditambah
    { icon: "fa-exchange-alt", text: "Transactions", path: "/transactions" },
    { icon: "fa-bell", text: "Alerts", path: "/alerts" },
    { icon: "fa-cog", text: "Settings", path: "/settings" },
  ];

  return (
    <aside className="bg-indigo-800 text-white w-64 h-screen p-4 hidden md:flex flex-col fixed md:relative">
      <div className="flex items-center space-x-2 mb-6">
        <i className="fas fa-shield-alt text-2xl"></i>
        <h1 className="text-xl font-bold">FraudGuard</h1>
      </div>

      <nav className="space-y-2 flex-1">
        {menuItems.map((item, i) => (
          <Link
            key={i}
            to={item.path}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
              path === item.path ? "bg-indigo-700 font-semibold" : "hover:bg-indigo-700"
            }`}
          >
            <i className={`fas ${item.icon}`}></i>
            <span>{item.text}</span>
          </Link>
        ))}
      </nav>

      <div className="text-sm text-gray-300 mt-auto">
        <p>Logged in as</p>
        <p className="font-semibold text-white">Admin</p>
      </div>
    </aside>
  );
}