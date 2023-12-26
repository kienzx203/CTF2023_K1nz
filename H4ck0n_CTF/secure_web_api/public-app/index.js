import "dotenv/config.js";
import express from "express";
import { request } from "./http-client.js";

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

app.get("/flag", (req, res) => {
    if (!req.query.token) {
        res.status(500).send("[!] You need to provide a token");
        return;
    }

    request(`http://${process.env.SECURE_BACKEND}:9000/flag`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${req.query.token}`,
        },
    })
        .then((response) => {
            res.send(response);
        })
        .catch((err) => {
            console.log(err);
            res.status(500).send("[!] Internal server error. The secure backend service crashed.");
        });
});

app.get("/register-token", (req, res) => {
    if (!req.query.token) {
        res.status(500).send("[!] You need to provide a token");
        return;
    }

    if (!req.query.auth || req.query.auth_token !== process.env.AUTH_TOKEN) {
        res.status(500).send("[!] You need to provide a valid 'auth_token'");
        return;
    }

    request(`http://${process.env.SECURE_BACKEND}:9000/register-token?token=${req.query.token}`, {
        method: "GET",
    })
        .then((response) => {
            res.send(response);
        })
        .catch((err) => {
            console.log(err);
            res.status(500).send("[!] Internal server error. The secure backend service crashed.");
        });
});

app.listen(3000, () => {
    console.log("[+] Public app up and running");
});
