/**
 * Dataset Upload Component
 * Location: frontend/src/components/DatasetUpload.tsx
 * 
 * Component for uploading datasets to the backend
 */

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import backendService from "@/services/backend";

interface Dataset {
  dataset_id: string;
  filename: string;
  file_size: number;
  upload_time: string;
  data_metadata?: {
    num_rows: number;
    num_columns: number;
    columns: string[];
  };
}

export default function DatasetUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState("");
  const [uploadedDataset, setUploadedDataset] = useState<any>(null);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loadingDatasets, setLoadingDatasets] = useState(false);

  // Load datasets on component mount
  React.useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    setLoadingDatasets(true);
    try {
      const response = await backendService.listDatasets();
      setDatasets(response.datasets || []);
    } catch (error: any) {
      setMessage(`Error loading datasets: ${error.message}`);
      setUploadStatus("error");
    } finally {
      setLoadingDatasets(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadStatus("idle");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file to upload");
      setUploadStatus("error");
      return;
    }

    setUploading(true);
    setUploadStatus("idle");
    setMessage("");

    try {
      const response = await backendService.uploadDataset(file, description);
      setUploadedDataset(response);
      setMessage(response.message);
      setUploadStatus("success");
      setFile(null);
      setDescription("");
      
      // Reload datasets list
      loadDatasets();
    } catch (error: any) {
      setMessage(`Upload failed: ${error.message}`);
      setUploadStatus("error");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (datasetId: string) => {
    if (!confirm("Are you sure you want to delete this dataset?")) {
      return;
    }

    try {
      await backendService.deleteDataset(datasetId);
      setMessage("Dataset deleted successfully");
      setUploadStatus("success");
      loadDatasets();
    } catch (error: any) {
      setMessage(`Delete failed: ${error.message}`);
      setUploadStatus("error");
    }
  };

  return (
    <div className="space-y-6 w-full">
      {/* Upload Card */}
      <Card>
        <CardHeader>
          <CardTitle>Upload Dataset</CardTitle>
          <CardDescription>
            Upload CSV, Excel, JSON, or Parquet files (Max 100MB)
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Status Message */}
          {message && (
            <Alert variant={uploadStatus === "success" ? "default" : "destructive"}>
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}

          {/* File Input */}
          <div className="space-y-2">
            <Label htmlFor="file">Select File</Label>
            <Input
              id="file"
              type="file"
              accept=".csv,.xlsx,.json,.parquet"
              onChange={handleFileChange}
              disabled={uploading}
            />
            {file && (
              <p className="text-sm text-muted-foreground">
                Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </p>
            )}
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Description (Optional)</Label>
            <Textarea
              id="description"
              placeholder="Add a description for this dataset..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={uploading}
              rows={3}
            />
          </div>

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full"
          >
            {uploading ? "Uploading..." : "Upload Dataset"}
          </Button>

          {/* Upload Success Details */}
          {uploadStatus === "success" && uploadedDataset && (
            <div className="bg-muted p-4 rounded-lg space-y-2">
              <h4 className="font-semibold">Upload Successful</h4>
              <p className="text-sm">
                <strong>Dataset ID:</strong> {uploadedDataset.dataset_id}
              </p>
              <p className="text-sm">
                <strong>Rows:</strong> {uploadedDataset.data_summary.num_rows}
              </p>
              <p className="text-sm">
                <strong>Columns:</strong> {uploadedDataset.data_summary.num_columns}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Datasets List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Uploaded Datasets</CardTitle>
              <CardDescription>Manage your uploaded datasets</CardDescription>
            </div>
            <Badge variant="outline">{datasets.length} datasets</Badge>
          </div>
        </CardHeader>
        <CardContent>
          {loadingDatasets ? (
            <p className="text-center text-muted-foreground">Loading datasets...</p>
          ) : datasets.length === 0 ? (
            <p className="text-center text-muted-foreground">No datasets uploaded yet</p>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Filename</TableHead>
                    <TableHead>Rows</TableHead>
                    <TableHead>Columns</TableHead>
                    <TableHead>Size</TableHead>
                    <TableHead>Uploaded</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {datasets.map((dataset) => (
                    <TableRow key={dataset.dataset_id}>
                      <TableCell className="font-medium">{dataset.filename}</TableCell>
                      <TableCell>
                        {dataset.data_metadata?.num_rows.toLocaleString() || "N/A"}
                      </TableCell>
                      <TableCell>
                        {dataset.data_metadata?.num_columns || "N/A"}
                      </TableCell>
                      <TableCell>
                        {(dataset.file_size / 1024 / 1024).toFixed(2)} MB
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {new Date(dataset.upload_time).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(dataset.dataset_id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
