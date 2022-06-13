var CELERY_TODO = 'PENDING';
var ACCESS_TOKEN = NaN;  // TODO: This is just a demo! Here acces token is exposed to emulate session.


(function() {
    console.log('Hello there!');
})();

function readTasksInfo() {
    fetch('/user/tasks', {
        method: 'GET', 
        headers: {'accept': 'application/json', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
    })
    .then(res => res.json()).then(res => {
        console.log('Read tasks info..');
        let todo = 0;
        let table = document.getElementById('tasks');
        table.innerHTML = '';
        for (i = 0; i < res.length; i++) {
            let task = res[i];
            let status = task.status;
            let src = task.src;
            let html_src = `<a href=${src} download><img src=${src} width="20" height="20"></a>`;
            if (status === CELERY_TODO) { 
                todo++; 
                html_src = NaN
            };
            let html_row = `<tr><td>${task.id}</td><td>${status}</td><td>${html_src}</td></tr>`;
            document.getElementById('tasks').insertRow(0).innerHTML = html_row;
        }
        if (todo === 0) return false;
        setTimeout(function() { readTasksInfo(); }, 3600);
    })
    .catch(err => console.log(err));
};

function createTask() {
    fetch('/user/tasks/new', {
        method: 'POST', 
        headers: {'accept': 'application/json', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
    })    
    .then(res => res.json()).then(res => {
        console.log(`Init task: ${res.tasks_id[-1]}`);
        if (ACCESS_TOKEN) assertAuth();
    })
    .catch(err => console.log(err));
}

function loginUser() {
    var user = document.getElementById('user').value;
    var pwd = document.getElementById('pwd').value;    
    fetch('/login', {
        method: 'POST', 
        headers: {'accept': 'application/json'}, 
        body: new URLSearchParams({'username': user, 'password': pwd})
    })    
    .then(res => res.json()).then(res => {
        console.log(`Try login: ${user}`);
        if (res.access_token) {
            ACCESS_TOKEN = res.access_token;
            assertAuth()
        } else {
            console.log(`Refresh page..`);
            location.reload();  // del ACCESS_TOKEN
        };
    })
    .catch(err => {
        console.log(err);
        location.reload();  // del ACCESS_TOKEN
    });
}

function assertAuth() {
    fetch('/user', {
        method: 'GET', 
        headers: {'accept': 'application/json', 'Authorization': 'Bearer ' + ACCESS_TOKEN}
    })
    .then(res => res.json()).then(res => {
        console.log(`Test auth: ${res.username}`);
        if (res.username) {
            let html_btn = '<button type="button" class="btn btn-primary" onclick="createTask()">forge</button>'
            let html_msg = 'Hello ' + `<b>${res.username}</b>` + '! '
            let msg = 'To create fractal press '; 
            document.getElementById('hello').innerHTML = html_msg + msg + html_btn + '.';
        } 
        readTasksInfo();
    })
    .catch(err => console.log(err));
}

if (ACCESS_TOKEN) assertAuth();
