import React, { Suspense, lazy, useState } from "react";
import { BrowserRouter as Router, Navigate, Route, Routes } from "react-router-dom";

import ErrorBoundary from "./components/ErrorBoundary";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import SkeletonBlock from "./components/SkeletonBlock";
import StatsCards from "./components/StatsCards";
import ChartSection from "./components/ChartSection";
import AlertsSection from "./components/AlertsSection";
import FileUpload from "./components/FileUpload";
import TransactionsTable from "./components/TransactionsTable";
import { useAsync } from "./hooks/useAsync";
import { dashboardService } from "./services/dashboardService";
import { useAuthStore } from "./store/authStore";

const AnalyticsPage = lazy(() => import("./pages/AnalyticsPage"));
const SettingsPage = lazy(() => import("./pages/SettingsPage"));
const LoginPage = lazy(() => import("./pages/LoginPage"));

function DashboardPage() {
  const [uploadedData, setUploadedData] = useState([]);
  const summary = useAsync(dashboardService.summary, []);
  const trends = useAsync(dashboardService.transactionTrends, []);
  const alerts = useAsync(dashboardService.alerts, []);

  return (
    <>
      <StatsCards stats={summary.data?.cards || []} loading={summary.loading} />
      <ChartSection chartData={trends.data} loading={trends.loading} />
      <AlertsSection alerts={alerts.data || []} loading={alerts.loading} />
      <FileUpload setData={setUploadedData} />

      {uploadedData.length > 0 && (
        <div className="mt-6">
          <h3 className="text-xl font-bold mb-3">Detected Transactions</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {uploadedData.map((tx, i) => (
              <div key={i} className={`p-3 bg-gray-50 rounded border ${tx.status === "Fraud" ? "border-red-400" : tx.status === "Suspicious" ? "border-yellow-400" : "border-green-400"}`}>
                <div className="flex justify-between">
                  <p className="font-medium">Transaction #{i + 1}</p>
                  <p className="text-sm">{tx.Amount} - {tx.status}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

function TransactionsPage() {
  const transactions = useAsync(dashboardService.recentTransactions, []);
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Transaction List</h2>
      {transactions.loading ? <SkeletonBlock className="h-80" /> : <TransactionsTable data={transactions.data || []} />}
    </div>
  );
}

function AlertsPage() {
  const alerts = useAsync(dashboardService.alerts, []);
  return <AlertsSection alerts={alerts.data || []} loading={alerts.loading} />;
}

function ProtectedRoute({ children }) {
  const accessToken = useAuthStore((state) => state.accessToken);
  if (!accessToken) return <Navigate to="/login" replace />;
  return children;
}

function AppShell() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto">
        <Header />
        <main className="p-4">
          <ErrorBoundary>
            <Suspense fallback={<SkeletonBlock className="h-96" />}>
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/transactions" element={<TransactionsPage />} />
                <Route path="/alerts" element={<AlertsPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Routes>
            </Suspense>
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Suspense fallback={<SkeletonBlock className="h-screen" />}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/*" element={<ProtectedRoute><AppShell /></ProtectedRoute>} />
        </Routes>
      </Suspense>
    </Router>
  );
}
