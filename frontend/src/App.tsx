import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { DecisionSystemProvider } from "@/context/DecisionSystemContext";
import { AppLayout } from "@/components/dashboard/AppLayout";
import { appRoutes } from "./routes.js";
import NotFound from "./pages/NotFound.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <DecisionSystemProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route element={<AppLayout />}>
              {appRoutes.map(({ path, element: Element }) => <Route key={path} path={path} element={<Element />} />)}
            </Route>
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </DecisionSystemProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
