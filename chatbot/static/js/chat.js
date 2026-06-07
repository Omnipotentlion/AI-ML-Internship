let currentChatId = null;

const input =
document.getElementById("messageInput");

const sendBtn =
document.getElementById("sendBtn");

const chatArea =
document.getElementById("chatArea");

const newChatBtn =
document.getElementById("newChat");

newChatBtn.onclick = createChat;

sendBtn.onclick = sendMessage;

async function createChat(){

    const response =
    await fetch("/new_chat",{
        method:"POST"
    });

    const data =
    await response.json();

    currentChatId =
    data.chat_id;

    chatArea.innerHTML = "";

    loadChats();
}

async function sendMessage(){

    const message =
    input.value.trim();

    if(!message) return;

    if(!currentChatId){

        await createChat();
    }

    addMessage(
        "user",
        message
    );

    input.value="";

    const response =
    await fetch(
        "/send_message",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                chat_id:currentChatId,
                message:message
            })
        }
    );

    const data =
    await response.json();

    addMessage(
        "assistant",
        data.response
    );
}

function addMessage(role,text){

    const div =
    document.createElement("div");

    div.className =
    role;

    div.innerHTML =
    marked.parse(text);

    div.querySelectorAll("pre code")
    .forEach((block)=>{
         hljs.highlightElement(block);
});

    chatArea.appendChild(div);

    chatArea.scrollTop =
    chatArea.scrollHeight;
}

async function loadChats(){

    const response =
    await fetch("/get_chats");

    const chats =
    await response.json();

    const history =
    document.querySelector(".history");

    history.innerHTML = "";

    chats.forEach(chat=>{

        const item =
        document.createElement("div");

        item.innerText =
        chat.title;

        item.onclick = ()=>{

            currentChatId =
            chat.id;

            loadMessages(
                chat.id
            );
        };

        history.appendChild(item);
    });
}

async function loadMessages(chatId){

    const response =
    await fetch(
        `/get_messages/${chatId}`
    );

    const messages =
    await response.json();

    chatArea.innerHTML = "";

    messages.forEach(msg=>{

        addMessage(
            msg.role,
            msg.content
        );

    });
}

loadChats();
const pdfBtn =
document.getElementById("pdfBtn");

const pdfInput =
document.getElementById("pdfInput");

pdfBtn.onclick = ()=>{

    pdfInput.click();

};

pdfInput.onchange = async ()=>{

    if(!currentChatId){

        await createChat();
    }

    const file =
    pdfInput.files[0];

    const formData =
    new FormData();

    formData.append(
        "pdf",
        file
    );

    formData.append(
        "chat_id",
        currentChatId
    );

    const response =
    await fetch(
        "/upload_pdf",
        {
            method:"POST",
            body:formData
        }
    );

    const data =
    await response.json();

    alert(
        `${data.filename} uploaded`
    );
};