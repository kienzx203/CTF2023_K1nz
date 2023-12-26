import "dotenv/config";
import express from "express";

const tokens = [];
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

app.get("/register-token", (req, res) => {
    const token = req.query.token ?? "";

    if (token.length < 10) {
        res.send("[-] Token must be at least 10 characters long");
    } else {
        tokens.push(req.query.token);
        res.send("[+] Token registered successfully");
    }
});

app.get("/flag", (req, res) => {
    const token = req.headers["authorization"].split(" ")[1] ?? "";

    if (tokens.includes(token)) {
        res.send(`[+] Here is the flag: ${process.env.FLAG}. Apparently, you can't hide behind seven proxies.`);
    } else {
        res.status(500).send("[-] Invalid token");
    }
});

app.listen(9000, () => {
    console.log("[+] Backend up and running");
});
