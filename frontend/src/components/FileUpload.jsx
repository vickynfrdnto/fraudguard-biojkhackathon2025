import React, { useState } from "react";
import { transactionService } from "../services/transactionService";

export default function FileUpload({ setData }) {
  const [fileName, setFileName] = useState("No file chosen");
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setFileName(file ? file.name : "No file chosen");
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Please choose a file first.");
    setLoading(true);
    try {
      const response = await transactionService.detect(selectedFile);
      setResult(response.data);
      setData(response.data);
      alert("File uploaded and processed successfully!");
    } catch (err) {
      alert("Failed to upload file: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-500 hover:bg-gray-50 transition">
        <div className="flex flex-col items-center justify-center">
          <i className="fas fa-file-upload text-4xl text-indigo-500 mb-3"></i>
          <h3 className="font-medium mb-1">Upload Transaction Data</h3>
          <p className="text-sm text-gray-500 mb-4">CSV or Excel format</p>
          <input type="file" accept=".csv,.xlsx,.xls" id="fileInput" className="hidden" onChange={handleFileChange} />
          <label htmlFor="fileInput" className="px-4 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition">
            Choose File
          </label>
          <p className="text-sm text-gray-500 mt-2">{fileName}</p>
        </div>
      </div>

      <div className="border rounded-lg p-6">
        <h3 className="font-medium mb-3">Real-time Detection</h3>
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-gray-500">Model Status: <span className="text-green-600 font-medium">Active</span></p>
          <button onClick={handleUpload} disabled={loading} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
            {loading ? "Processing..." : "Start Demo"}
          </button>
        </div>

        <div className="space-y-3 max-h-48 overflow-y-auto">
          {result.length === 0 ? (
            <p className="text-sm text-gray-500">No data yet...</p>
          ) : (
            result.map((tx, i) => (
              <div key={i} className={`p-3 bg-gray-50 rounded border ${tx.status === "Fraud" ? "animate-pulse border-red-400" : ""}`}>
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium">Transaction #{i + 1}</p>
                    <p className="text-sm text-gray-500">Amount: {tx.Amount}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded ${tx.status === "Fraud" ? "bg-red-100 text-red-800" : tx.status === "Suspicious" ? "bg-yellow-100 text-yellow-800" : "bg-green-100 text-green-800"}`}>
                    {tx.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
