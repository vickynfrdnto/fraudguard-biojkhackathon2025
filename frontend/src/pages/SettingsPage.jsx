// src/pages/SettingsPage.jsx
import React, { useState } from "react";

export default function SettingsPage() {
  const [emailNotif, setEmailNotif] = useState(true);
  const [twoFA, setTwoFA] = useState(false);

  return (
    <div className="space-y-6 max-w-3xl">
      <h2 className="text-2xl font-bold text-gray-800">System Settings</h2>

      <section className="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Notification Preferences</h3>
        <div className="flex items-center justify-between">
          <span>Email Alerts</span>
          <input
            type="checkbox"
            checked={emailNotif}
            onChange={() => setEmailNotif(!emailNotif)}
            className="w-5 h-5"
          />
        </div>
        <div className="flex items-center justify-between">
          <span>Two-Factor Authentication</span>
          <input
            type="checkbox"
            checked={twoFA}
            onChange={() => setTwoFA(!twoFA)}
            className="w-5 h-5"
          />
        </div>
      </section>

      <section className="bg-white p-6 rounded-lg shadow space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">User Preferences</h3>
        <div>
          <label className="block text-sm mb-1">Default Language</label>
          <select className="border rounded w-full px-3 py-2 text-sm">
            <option>English</option>
            <option>Bahasa Indonesia</option>
          </select>
        </div>
        <div>
          <label className="block text-sm mb-1">Theme</label>
          <select className="border rounded w-full px-3 py-2 text-sm">
            <option>Light</option>
            <option>Dark</option>
          </select>
        </div>
      </section>

      <div>
        <button className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700">
          Save Changes
        </button>
      </div>
    </div>
  );
}