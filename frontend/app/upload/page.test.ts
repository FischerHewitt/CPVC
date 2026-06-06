import { describe, it, expect, vi } from "vitest";

const mockRedirect = vi.fn();

vi.mock("next/navigation", () => ({
  redirect: mockRedirect,
  useRouter: vi.fn(),
}));

describe("/upload route", () => {
  it("redirects to /", async () => {
    const { default: UploadPage } = await import("./page");
    UploadPage();
    expect(mockRedirect).toHaveBeenCalledWith("/");
  });
});
