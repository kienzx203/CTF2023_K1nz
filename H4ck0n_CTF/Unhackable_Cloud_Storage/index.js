import "dotenv/config";
import express from "express";
import fs from "fs";

const admin_id = 0;
const admin_password = process.env.ADMIN_PASSWORD;

const USERS = [[admin_id, admin_password]];

const app = express();

app.use((req, _, next) => {
    let data = "";
    req.setEncoding("utf8");
    req.on("data", (chunk) => {
        data += chunk;
    });

    req.on("end", () => {
        req.body = data;
        next();
    });
});

app.get("/register", (req, res) => {
    const userId = req.query.user_id ?? "";
    const userPassword = req.query.user_password ?? "";

    if (userId == admin_id) {
        res.send("[-] You can't register as an admin user");
    }

    USERS.push([userId, userPassword]);

    res.send(`[+] User '${userId}' registered`);
});

const authOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    const userPassword = req.query.user_password ?? "";

    const user = USERS.find((user) => user[0] == userId && user[1] == userPassword);

    if (!user) {
        res.send("[-] Invalid credentials. You need to register first.");
        return false;
    }

    return true;
};

const adminOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    if (parseInt(userId) != admin_id) {
        res.send("[-] Invalid credentials. Only admins can access this endpoint");
        return false;
    }

    return true;
};

app.get("/bucket", (req, res) => {
    if (!authOnly(req, res)) {
        return;
    }

    const filePath = (req.query.file_path ?? "").toString();
    if (!filePath.startsWith("/tmp")) {
        if (!adminOnly(req, res)) {
            return;
        }
    }

    res.send(getFileContent(filePath));
});

const getFileContent = (filePath) => {
    const f = fs.openSync(filePath, "r");

    if (filePath.includes("flag")) {
        return "[No flag for you]";
    }

    const buf = Buffer.alloc(100);
    fs.readSync(f, buf, 0, 100, 0);
    fs.closeSync(f);

    const fileContent = buf.toString();

    return fileContent;
};

app.listen(7500, () => {
    console.log("[+] API up and running");
});
