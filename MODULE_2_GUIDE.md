# Module 2: Data Processing Layer - Implementation Guide

## Overview

Module 2 implements the **Data Processing Layer** - the first functional backend module that handles dataset upload, validation, and management.

## Backend Implementation

### Files Created

1. **`backend/app/services/data_processor.py`**
   - `DataProcessor` class with methods:
     - `validate_file()` - Validates file type and size
     - `save_file()` - Saves uploaded file to disk
     - `load_and_validate_data()` - Loads and extracts metadata
     - `get_dataset_info()` - Retrieves dataset information
     - `delete_dataset()` - Deletes a dataset
     - `list_datasets()` - Lists all uploaded datasets

2. **`backend/app/routers/data_processing.py`**
   - API endpoints:
     - `POST /api/upload-dataset` - Upload a new dataset
     - `GET /api/dataset/{dataset_id}` - Get dataset info
     - `GET /api/datasets` - List all datasets
     - `DELETE /api/dataset/{dataset_id}` - Delete a dataset

### Backend Endpoints

#### 1. Upload Dataset
```
POST /api/upload-dataset
Content-Type: multipart/form-data

Parameters:
- file: File (CSV, XLSX, JSON, Parquet) - Max 100MB
- description: string (optional)

Response:
{
  "status": "success",
  "dataset_id": "uuid",
  "filename": "data.csv",
  "file_size": 1024000,
  "data_summary": {
    "num_rows": 1000,
    "num_columns": 10,
    "columns": ["col1", "col2", ...],
    "missing_values": {...},
    "duplicates": 5
  }
}
```

#### 2. Get Dataset Info
```
GET /api/dataset/{dataset_id}

Response:
{
  "status": "success",
  "data": {
    "dataset_id": "uuid",
    "filename": "data.csv",
    "file_path": "/uploads/uuid/data.csv",
    "file_size": 1024000,
    "upload_time": "2024-05-04T10:30:00",
    "data_metadata": {...}
  }
}
```

#### 3. List All Datasets
```
GET /api/datasets

Response:
{
  "status": "success",
  "count": 3,
  "datasets": [...]
}
```

#### 4. Delete Dataset
```
DELETE /api/dataset/{dataset_id}

Response:
{
  "status": "success",
  "message": "Dataset {dataset_id} deleted successfully"
}
```

## Frontend Implementation

### Files Created

1. **`frontend/src/services/backend.ts`** - Updated with new functions:
   - `uploadDataset(file, description)` - Upload file
   - `getDatasetInfo(datasetId)` - Fetch dataset details
   - `listDatasets()` - List all datasets
   - `deleteDataset(datasetId)` - Delete a dataset

2. **`frontend/src/components/DatasetUpload.tsx`** - New component
   - File upload with drag-and-drop support
   - File validation and size display
   - Dataset list with metadata
   - Delete functionality
   - Real-time status updates

3. **`frontend/src/pages/DataUploadTestPage.tsx`** - New test page
   - Full page layout for testing Module 2
   - Integration guide

4. **`frontend/src/routes.js`** - Updated
   - Added route: `/data-upload-test` → DataUploadTestPage

### Frontend Component Usage

```tsx
import DatasetUpload from "@/components/DatasetUpload";

export default function MyPage() {
  return <DatasetUpload />;
}
```

## How to Test Module 2

### 1. Start Backend
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Backend should run on: `http://localhost:8000`

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

Frontend should run on: `http://localhost:5173`

### 3. Test Endpoints

#### Via Browser UI
1. Open frontend: `http://localhost:5173/data-upload-test`
2. Select a CSV/Excel/JSON/Parquet file
3. Click "Upload Dataset"
4. View uploaded datasets in the table below

#### Via cURL/Postman
```bash
# Upload
curl -X POST http://localhost:8000/api/upload-dataset \
  -F "file=@test.csv" \
  -F "description=Test data"

# List datasets
curl http://localhost:8000/api/datasets

# Get dataset info
curl http://localhost:8000/api/dataset/{dataset_id}

# Delete dataset
curl -X DELETE http://localhost:8000/api/dataset/{dataset_id}
```

## Data Storage

- Uploaded files are stored in: `backend/uploads/{dataset_id}/`
- Each dataset gets a unique UUID
- Metadata is extracted automatically
- Original files are preserved

## Supported File Formats

| Format | Extension |
|--------|-----------|
| CSV | .csv |
| Excel | .xlsx |
| JSON | .json |
| Parquet | .parquet |

## Features

✅ File upload with validation
✅ Automatic metadata extraction
✅ Dataset listing and management
✅ Delete functionality
✅ Error handling
✅ Logging for all operations
✅ CORS support for frontend
✅ Multi-file support

## Error Handling

Common errors and responses:

| Error | Code | Message |
|-------|------|---------|
| Invalid file type | 400 | File type not allowed |
| File too large | 400 | File size exceeds maximum |
| Dataset not found | 404 | Dataset not found |
| Server error | 500 | Error uploading dataset |

## Next Steps

Module 3 will add:
- Meta-feature extraction from datasets
- Automatic feature engineering suggestions
- Dataset profiling and analysis

---

**Module 2 Status: ✅ COMPLETE**

All endpoints tested and working. Ready to proceed with Module 3.
