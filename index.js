#!/usr/bin/env node

import http from "http";

let addData = (data) => {
    // Function add new task

    let send_data = JSON.stringify({
        task: data,
        is_done: false,
    });
    var request = http.request({
        hostname: "localhost",
        path: "/add",
        method: "POST",
        port: 8000,
        headers: {
            "Content-Type": "application/json",
            "Content-Length": send_data.length,
        },
    });

    request.write(send_data);
    request.end();
};

let delData = (index) => {
    // Function delete a task for given id
    var request = http.request({
        host: "localhost",
        port: 8000,
        method: "GET",
        path: `/delete?id=${index}`,
    });

    request.end();
};

let doneData = (index) => {
    // Function mark the task is done
    var request = http.request({
        host: "localhost",
        port: 8000,
        method: "GET",
        path: `/done?id=${index}`,
    });

    request.end();
};

let undoneData = (index) => {
    // Function mark the task is undone
    var request = http.request({
        host: "localhost",
        port: 8000,
        method: "GET",
        path: `/undone?id=${index}`,
    });

    request.end();
};

let showData = () => {
    // Function show all task as table
    var request = http.request(
        {
            host: "localhost",
            port: 8000,
            method: "GET",
            path: `/todos`,
        },
        (res) => {
            var str = "";
            res.on("data", (chunk) => {
                str += chunk;
            });

            res.on("end", () => {
                let data = JSON.parse(str);
                let td = {};
                for (let index = 0; index < data.length; index++) {
                    const element = data[index];
                    let id = element.id;
                    delete element.id;
                    td[id] = element;
                    if (element["is_done"]) {
                        element["is_done"] = "✔️";
                    } else {
                        element["is_done"] = "❌";
                    }
                }
                console.table(td);
            });
        }
    );

    request.end();
};

let get_arg = (name) => {
    // Function parses the cli args
    const args = {};
    const stdin = process.argv.slice(2);
    args[stdin[0]] = stdin[1];
    if (stdin.includes(name)) {
        return args[name];
    } else {
        return null;
    }
};

let add = get_arg("add");
let del = get_arg("del");
let done = get_arg("done");
let undone = get_arg("undone");

if (add) {
    addData(add);
    showData();
} else if (del) {
    delData(del);
    showData();
} else if (done) {
    doneData(done);
    showData();
} else if (undone) {
    undoneData(undone);
    showData();
} else {
    showData();
}
