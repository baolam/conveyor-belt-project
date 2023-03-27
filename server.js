const express = require("express");
const http = require("http");
const path = require("path");
const socketio = require("socket.io");

const PORT = process.env.PORT || 3000;
const layout = path.join(__dirname, "src", "interface", "layout", "build");

const app = express();
const server = http.createServer(app);
const io = new socketio.Server(server, { 
    allowEIO3 : true, 
    cors : { origin : "*" },
    maxHttpBufferSize : 1e7
});

app.use("/", express.static(path.join(layout)));

app.get("/", (req, res) => {
    res.sendFile(path.join(layout, "index.html"));
});

function update_stack(yellow, blue, undef)
{
    return { 
        yellow_stack : yellow,
        blue_stack : blue,
        undefined_stack : undef
    }
}

/// Phần quản lí
const user = io.of("/user");
user.on("connection", (_socket) => {
    _socket.emit("update-stack", update_stack(-1, -1, -1));
    _socket.emit("ready");

    _socket.on("update-mode", (mode) => {
        device.emit("mode", mode);
   }); 

    _socket.on("reset", () => {
        _socket.emit("update-stack", update_stack(0, 0, 0));
    });
});

/// Thiết bị
const device = io.of("/device");
device.on("connection", (_socket) => {
    _socket.on("disconnect", () => {
        console.log("Dừng server");
        process.exit(0);
    });

    _socket.on("streaming", (r) => {
        user.emit("streaming", r);
    });

    _socket.on("update-classification", r => {
        user.emit("update-classification", r);
    })
});

server.listen(PORT, () => {
    console.log("Server is listening on port " + PORT);
});