module.exports = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.target = "electron-renderer";
    }

    return config;
  },
  rewrites: () => {
    return [
      {
        source: "/api/python/:path*",
        destination: "http://localhost:8889/api/:path*",
      },
    ];
  },
};
