const chat = {
    fetch: async prompt => {
        return fetch('/company/messages/account-375491', {
            method: 'POST',
            headers:  { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        })
    },

    post: data => {
        const name = data.company ? data.company : 'me';
        const title = document.createElement('span');

        title.innerHTML = name;
        title.classList.add('name');

        const top = document.createElement('div');

        top.append(title);

        const bottom = document.createElement('div');

        bottom.innerHTML = data.content;

        const post = document.createElement('div');
        post.append(top, bottom);
        post.classList.add('post');
        document.getElementById('chat').appendChild(post);

        Prism.highlightAll();
        MathJax.typesetPromise();

        document.title = data.company;
        post.scrollIntoView({ behavior: 'smooth' });
    },

    prompt: async prompt => {
        chat.waiting = true;

        chat.post({content: prompt});

        await chat.fetch(prompt)
        .then(response => response.json())
        .then(data => {

            data.content = data.content.replace(/\\/g, '\\\\');  // so markdown won't trample LaTex
            data.content = marked.parse(data.content)

            chat.post(data);
            chat.waiting = false;
        });
    },
};

window.onload = () => {
    chat.post({company: "The Mall", content: "Welcome to The Mall. Where would you like to go?"})
};

window.addEventListener("unload", () => fetch('Good-bye'));
