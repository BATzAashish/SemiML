/**
 * Backend Connection Test Component
 * Location: frontend/src/components/BackendStatus.tsx
 * 
 * Use this component to display and test backend connection status
 */

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import backendService, { BACKEND_URL } from "@/services/backend";

export default function BackendStatus() {
  const [status, setStatus] = useState<"idle" | "loading" | "connected" | "disconnected">("idle");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Test connection on component mount
  useEffect(() => {
    testBackendConnection();
  }, []);

  const testBackendConnection = async () => {
    setStatus("loading");
    setError(null);
    try {
      const result = await backendService.testConnection();
      setData(result);
      setStatus("connected");
    } catch (err: any) {
      setError(err.message);
      setStatus("disconnected");
    }
  };

  const getSystemInfo = async () => {
    setStatus("loading");
    try {
      const result = await backendService.getSystemInfo();
      setData(result);
      setStatus("connected");
    } catch (err: any) {
      setError(err.message);
      setStatus("disconnected");
    }
  };

  const checkHealth = async () => {
    setStatus("loading");
    try {
      const result = await backendService.checkHealth();
      setData(result);
      setStatus("connected");
    } catch (err: any) {
      setError(err.message);
      setStatus("disconnected");
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Backend Connection Status</CardTitle>
            <CardDescription>Monitor SemiML Backend Connection</CardDescription>
          </div>
          <Badge
            variant={
              status === "connected"
                ? "default"
                : status === "disconnected"
                ? "destructive"
                : "secondary"
            }
          >
            {status === "connected" && "✓ Connected"}
            {status === "disconnected" && "✗ Disconnected"}
            {status === "loading" && "⟳ Loading..."}
            {status === "idle" && "○ Idle"}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Status Buttons */}
        <div className="flex gap-2 flex-wrap">
          <Button
            onClick={testBackendConnection}
            variant="outline"
            disabled={status === "loading"}
          >
            {status === "loading" ? "Testing..." : "Test Connection"}
          </Button>
          <Button
            onClick={checkHealth}
            variant="outline"
            disabled={status === "loading"}
          >
            {status === "loading" ? "Checking..." : "Check Health"}
          </Button>
          <Button
            onClick={getSystemInfo}
            variant="outline"
            disabled={status === "loading"}
          >
            {status === "loading" ? "Loading..." : "System Info"}
          </Button>
        </div>

        {/* Response Data */}
        {data && (
          <div className="space-y-3">
            <div className="bg-muted p-4 rounded-lg">
              <h4 className="font-semibold mb-2">Response:</h4>
              <pre className="text-sm overflow-auto max-h-64 whitespace-pre-wrap break-words">
                {JSON.stringify(data, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {/* Connection Info */}
        {status === "connected" && (
          <Alert>
            <AlertDescription className="text-green-700">
              ✓ Backend is running on {BACKEND_URL}
            </AlertDescription>
          </Alert>
        )}

        {status === "disconnected" && (
          <Alert variant="destructive">
            <AlertDescription>
              ✗ Cannot connect to backend. Make sure it's running on {BACKEND_URL}
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}
