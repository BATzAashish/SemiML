/**
 * Data Upload Page
 * Location: frontend/src/pages/DataUploadTestPage.tsx
 * 
 * Page for testing dataset upload functionality
 */

import DatasetUpload from "@/components/DatasetUpload";
import { Card } from "@/components/ui/card";

export default function DataUploadTestPage() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold">Data Upload & Management</h1>
          <p className="text-muted-foreground mt-2">
            Upload and manage your datasets for ML pipeline analysis
          </p>
        </div>

        {/* Instructions */}
        <Card className="bg-blue-50 border-blue-200 p-4">
          <div className="space-y-2">
            <h3 className="font-semibold text-blue-900">About Module 2: Data Processing</h3>
            <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
              <li>Upload datasets in CSV, Excel, JSON, or Parquet format</li>
              <li>Automatically validates data and extracts metadata</li>
              <li>Stores datasets securely with unique IDs</li>
              <li>View dataset statistics (rows, columns, data types)</li>
              <li>Manage multiple datasets in one place</li>
            </ul>
          </div>
        </Card>

        {/* Upload Component */}
        <DatasetUpload />
      </div>
    </div>
  );
}
