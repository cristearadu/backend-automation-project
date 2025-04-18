// always overwrite db.json
const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'db.json');

const defaultDbContent = {
  posts: [
    { id: 1, title: "Post 1", author: "Author 1" },
    { id: 2, title: "Post 2", author: "Author 2" }
  ],
  comments: [
    { id: 1, body: "some comment", postId: 1 },
    { id: 2, body: "another comment", postId: 1 }
  ],
  profile: { name: "typicode" }
};

// always write db.json from scratch
fs.writeFileSync(dbPath, JSON.stringify(defaultDbContent, null, 2), { encoding: 'utf-8' });
console.log('db.json overwritten successfully.');