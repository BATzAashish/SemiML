import axios from "axios";

const client = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || "", timeout: 9000 });
const wait = (ms = 450) => new Promise((resolve) => setTimeout(resolve, ms));
const mock = async (data, ms) => { await wait(ms); return structuredClone(data); };
const useMock = () => !import.meta.env.VITE_API_BASE_URL;

export const mockDataProfile = {
  overview: { rows: 18420, columns: 36, missingValues: 742, target: "readmission_risk", classes: 3 },
  missingValues: [{ name: "age", value: 0.4 }, { name: "lab_glucose", value: 6.7 }, { name: "medication", value: 2.8 }, { name: "visits", value: 1.1 }],
  distributions: [{ feature: "Age", low: 18, mid: 47, high: 82 }, { feature: "Visits", low: 0, mid: 4, high: 19 }, { feature: "Glucose", low: 70, mid: 128, high: 260 }],
  classes: [{ name: "Low", value: 48 }, { name: "Medium", value: 34 }, { name: "High", value: 18 }],
  correlations: [[1, .42, -.18, .31], [.42, 1, .27, -.11], [-.18, .27, 1, .38], [.31, -.11, .38, 1]],
};

export const mockPipeline = {
  steps: ["Schema validation", "Missingness-aware imputation", "Robust scaling", "Mutual information feature selection", "Calibrated gradient boosting", "SHAP audit layer"],
  models: [
    { name: "Explainable Gradient Boosting", accuracy: .914, precision: .902, recall: .888, confidence: .93, selected: true },
    { name: "Random Forest + SHAP", accuracy: .891, precision: .874, recall: .861, confidence: .86 },
    { name: "Logistic Regression Baseline", accuracy: .842, precision: .819, recall: .792, confidence: .78 },
  ],
};

export const mockTrace = [
  { decision: "Prioritized recall-aware classification", reason: "Context indicated missed high-risk cases are costlier than false positives.", source: "rules", confidence: .91 },
  { decision: "Rejected deep neural baseline", reason: "Dataset size and explainability priority favored calibrated tabular models.", source: "meta-learning", confidence: .84 },
  { decision: "Selected SHAP audit layer", reason: "Stakeholder constraints require global and local feature attribution.", source: "RAG", confidence: .95 },
  { decision: "Enabled continuous learning checkpoint", reason: "Performance drift risk detected from temporal feature distribution.", source: "meta-learning", confidence: .88 },
];

export const mockEvaluation = {
  metrics: [{ metric: "Accuracy", value: .914 }, { metric: "F1 score", value: .897 }, { metric: "RMSE", value: .284 }, { metric: "AUC", value: .941 }],
  confusion: [[412, 34, 12], [28, 301, 26], [9, 31, 177]],
  roc: [{ fpr: 0, tpr: 0 }, { fpr: .06, tpr: .42 }, { fpr: .13, tpr: .71 }, { fpr: .24, tpr: .86 }, { fpr: .41, tpr: .95 }, { fpr: 1, tpr: 1 }],
};

export const mockExplainability = {
  importance: [{ feature: "prior_admissions", value: .32 }, { feature: "lab_glucose", value: .26 }, { feature: "age", value: .21 }, { feature: "medication_count", value: .16 }, { feature: "visit_gap", value: .12 }],
  shap: [{ feature: "prior_admissions", impact: .44 }, { feature: "lab_glucose", impact: .29 }, { feature: "age", impact: -.18 }, { feature: "visit_gap", impact: .15 }, { feature: "medication_count", impact: -.11 }],
  prediction: { class: "High risk", probability: .82, drivers: ["Prior admissions +0.31", "Glucose variability +0.18", "Recent visit gap +0.09"] },
};

export const mockExperiments = [
  { id: "EXP-1042", dataset: "patient_readmission.csv", model: "Explainable Gradient Boosting", performance: .914, date: "2026-04-22" },
  { id: "EXP-1037", dataset: "claims_quality.csv", model: "Random Forest + SHAP", performance: .887, date: "2026-04-18" },
  { id: "EXP-1029", dataset: "manufacturing_yield.csv", model: "XGBoost + PDP", performance: .902, date: "2026-04-11" },
];

export async function uploadDataset(payload) {
  if (useMock()) return mock({ ok: true, experimentId: "EXP-1048", received: { fileName: payload.file?.name, ...payload } }, 700);
  const formData = new FormData();
  Object.entries(payload).forEach(([key, value]) => value != null && formData.append(key, value));
  const { data } = await client.post("/upload", formData);
  return data;
}
export const getDataProfile = async () => useMock() ? mock(mockDataProfile) : (await client.get("/data-profile")).data;
export const getPipeline = async () => useMock() ? mock(mockPipeline) : (await client.get("/pipeline")).data;
export const getDecisionTrace = async () => useMock() ? mock(mockTrace) : (await client.get("/decision-trace")).data;
export const getEvaluation = async () => useMock() ? mock(mockEvaluation) : (await client.get("/evaluation")).data;
export const getExplainability = async () => useMock() ? mock(mockExplainability) : (await client.get("/explainability")).data;
export const getExperiments = async () => useMock() ? mock(mockExperiments) : (await client.get("/experiments")).data;
export async function sendChatMessage(message, history = []) {
  if (useMock()) return mock({ role: "assistant", content: `The recommendation is driven by traceable constraints: ${message.toLowerCase().includes("why") ? "recall priority, calibrated confidence, and SHAP-compatible model structure." : "I would re-profile the dataset, compare drift, and update the pipeline confidence before replacing the selected model."}` }, 650);
  const { data } = await client.post("/chat", { message, history });
  return data;
}
