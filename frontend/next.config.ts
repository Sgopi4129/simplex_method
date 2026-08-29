import type { NextConfig } from "next";

const outputMode = process.env.NEXT_OUTPUT_MODE || "standalone";

const nextConfig: NextConfig = {
  output: outputMode === "export" ? "export" : "standalone",
  trailingSlash: outputMode === "export",
  images: {
    unoptimized: outputMode === "export",
  },
};

export default nextConfig;
