https://backtracker-3hat.onrender.com/api/custom-issues/

# BackTracker

CONEXION_BD

HOST: centerbeam.proxy.rlwy.net
PORT: 16317
DATABASE: railway
USERNAME: postgres
PASSWORD: ATHnpvdGVFoIUjktuHGQgkFHciwkLsOL

create table users (
	id_user SERIAL PRIMARY KEY,
	username VARCHAR(50) not null unique,
	email varchar(100) not null unique,
	avatar_url varchar(255)
);

create table issue (
	id_issue SERIAL primary key,
	title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(100),
    priority_id VARCHAR(100),
    created_by INTEGER NOT NULL REFERENCES users(id_user),
    assigned_to INTEGER REFERENCES users(id_user),
    deadline DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE attachments (
    attachment_id SERIAL PRIMARY KEY,
    issue_id INTEGER NOT NULL REFERENCES issue(id_issue),
    file_url TEXT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP
);

CREATE TABLE comments (
    id_comment SERIAL PRIMARY KEY,
    issue_id INTEGER NOT NULL REFERENCES issue(id_issue),
    user_id INTEGER NOT NULL REFERENCES users(id_user),
    content TEXT NOT NULL,
    created_at TIMESTAMP 
);

CREATE TABLE watchers (
    issue_id INTEGER NOT NULL REFERENCES issue(id_issue),
    user_id INTEGER NOT NULL REFERENCES users(id_user),
    PRIMARY KEY (issue_id, user_id)
);

insert into users values(1, 'admin', 'danielespinalt@gmail.com', null);


