import { app } from "electron";
import serve from "electron-serve";
import { PythonShell } from "python-shell";
import { createWindow } from "./helpers";

const isProd: boolean = process.env.NODE_ENV === "production";

if (isProd) {
  serve({ directory: "app" });
} else {
  app.setPath("userData", `${app.getPath("userData")} (development)`);
}

(async () => {
  await app.whenReady();

  PythonShell.run("./backend/app.py", null, (err, result) => {
    if (err) throw err;
    console.log(result);
  });

  const mainWindow = createWindow("main", {
    width: 1000,
    height: 600,
  });
  const controllerWindow = createWindow("controller", {
    width: 300,
    height: 600,
  });

  if (isProd) {
    await mainWindow.loadURL("app://./sessions.html");
    await controllerWindow.loadURL("app://./controller.html");
  } else {
    const port = process.argv[2];
    await mainWindow.loadURL(`http://localhost:${port}/sessions`);
    await controllerWindow.loadURL(`http://localhost:${port}/controller`);
    mainWindow.webContents.openDevTools();
    controllerWindow.webContents.openDevTools();
  }
})();

app.on("window-all-closed", () => {
  app.quit();
});
