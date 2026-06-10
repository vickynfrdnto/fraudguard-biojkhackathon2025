import api from "../api/client";

export const transactionService = {
  list: () => api.get("/transactions").then((res) => res.data),
  create: (payload) => api.post("/transactions", payload).then((res) => res.data),
  update: (id, payload) => api.put(`/transactions/${id}`, payload).then((res) => res.data),
  remove: (id) => api.delete(`/transactions/${id}`).then((res) => res.data),
  detect: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/transactions/detect", formData, { headers: { "Content-Type": "multipart/form-data" } }).then((res) => res.data);
  }
};
