import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Rules
  getRules: async () => {
    const res = await apiClient.get('/rules');
    return res.data;
  },
  createRule: async (data: any) => {
    const res = await apiClient.post('/rules', data);
    return res.data;
  },
  updateRule: async (id: number, data: any) => {
    const res = await apiClient.put(`/rules/${id}`, data);
    return res.data;
  },
  deleteRule: async (id: number) => {
    const res = await apiClient.delete(`/rules/${id}`);
    return res.data;
  },

  // Upload & Validate
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },
  validateDocument: async (documentId: string, ruleTemplateId: number) => {
    const res = await apiClient.post('/validate', {
      document_id: documentId,
      rule_template_id: ruleTemplateId,
    });
    return res.data;
  },
  getReport: async (reportId: string) => {
    const res = await apiClient.get(`/reports/${reportId}`);
    return res.data;
  },
};
