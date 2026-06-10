import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import LoginPage from "./pages/LoginPage";

describe("LoginPage", () => {
  it("renders FraudGuard authentication", () => {
    render(<LoginPage />);
    expect(screen.getByText("FraudGuard")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Login" })).toBeInTheDocument();
  });
});
