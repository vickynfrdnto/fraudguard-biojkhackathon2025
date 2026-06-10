import api from "../api/client";

export const dashboardService = {
  summary: () => api.get("/dashboard/summary").then((res) => res.data),
  riskOverview: () => api.get("/dashboard/risk-overview").then((res) => res.data),
  transactionTrends: () => api.get("/dashboard/transaction-trends").then((res) => res.data),
  fraudAnalysis: () => api.get("/dashboard/fraud-analysis").then((res) => res.data),
  branchComparison: () => api.get("/dashboard/branch-comparison").then((res) => res.data),
  recentTransactions: () => api.get("/dashboard/recent-transactions").then((res) => res.data),
  alerts: () => api.get("/dashboard/alerts").then((res) => res.data),
  analyticsSummary: () => api.get("/dashboard/analytics-summary").then((res) => res.data)
};
