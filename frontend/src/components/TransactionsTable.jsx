import React from "react";

export default function TransactionsTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-semibold mb-4">Recent Transactions</h2>
        <p className="text-gray-500 text-sm">No transaction data available.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b flex justify-between items-center">
        <h2 className="text-lg font-semibold">Recent Transactions</h2>
        <div className="flex space-x-2">
          <div className="relative">
            <input
              type="text"
              placeholder="Search..."
              className="pl-8 pr-4 py-2 border rounded-lg text-sm"
            />
            <i className="fas fa-search absolute left-3 top-3 text-gray-400"></i>
          </div>
          <button className="px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded">
            Filter
          </button>
        </div>
      </div>
      <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th
                  key={key}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, idx) => (
              <tr
                key={idx}
                className={
                  row.status === "Fraud" ? "bg-red-50" : row.status === "Suspicious" ? "bg-yellow-50" : ""
                }
              >
                {Object.values(row).map((val, j) => (
                  <td
                    key={j}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                  >
                    {val}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}