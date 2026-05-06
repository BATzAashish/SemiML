import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import BackendStatus from "@/components/BackendStatus";
import { BACKEND_URL } from "@/services/backend";


describe("BackendStatus", () => {
  it("calls the backend connect endpoint on mount", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "connected" }),
    });

    vi.stubGlobal("fetch", fetchMock);

    render(<BackendStatus />);

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalled();
    });

    const [url] = fetchMock.mock.calls[0];
    expect(String(url)).toBe(`${BACKEND_URL}/api/connect`);

    expect(await screen.findByText("✓ Connected")).toBeInTheDocument();

    vi.unstubAllGlobals();
  });
});
