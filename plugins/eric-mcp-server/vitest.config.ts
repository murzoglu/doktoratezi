import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    server: {
      deps: {
        // tests/index.test.ts drives the real default export, which pulls in
        // @cloudflare/workers-oauth-provider. That library imports the
        // workerd-only `cloudflare:workers` module; inlining it lets vite
        // transform the import so the test's vi.mock stand-in applies instead
        // of Node's ESM loader rejecting the `cloudflare:` scheme.
        inline: ["@cloudflare/workers-oauth-provider"]
      }
    }
  }
});
