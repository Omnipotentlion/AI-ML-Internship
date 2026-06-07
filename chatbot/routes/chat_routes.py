from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from flask import jsonify

from database import get_db_connection
from services.gemini_service import generate_response
import os

from flask import current_app

from services.pdf_service import extract_pdf_text

chat_bp = Blueprint('chat',__name__)

@chat_bp.route("/new_chat", methods=["POST"])
def new_chat():

    if "user_id" not in session:
        return jsonify({"error":"Unauthorized"}),401

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO chats(user_id,title)
        VALUES(?,?)
        """,
        (
            session["user_id"],
            "New Chat"
        )
    )

    chat_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "chat_id": chat_id
    })

@chat_bp.route("/send_message", methods=["POST"])
def send_message():

    if "user_id" not in session:
        return jsonify({"error":"Unauthorized"}),401

    data = request.get_json()

    chat_id = data["chat_id"]
    user_message = data["message"]

    conn = get_db_connection()

    previous_messages = conn.execute(
        """
        SELECT role,content
        FROM messages
        WHERE chat_id=?
        ORDER BY id
        """,
        (chat_id,)
    ).fetchall()

    history = []
    pdfs = conn.execute(
    """
    SELECT extracted_text
    FROM pdfs
    WHERE chat_id=?
    """,
    (chat_id,)
).fetchall()

    for msg in previous_messages:

        history.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    pdf_context = ""

    for pdf in pdfs:



        pdf_context += pdf["extracted_text"]

    history.append({
    "role":"system",
    "content":
    f"PDF CONTENT:\n{pdf_context[:50000]}"
})
    ai_response = generate_response(
        user_message,
        history
    )

    conn.execute(
        """
        INSERT INTO messages(chat_id,role,content)
        VALUES(?,?,?)
        """,
        (
            chat_id,
            "user",
            user_message
        )
    )

    conn.execute(
        """
        INSERT INTO messages(chat_id,role,content)
        VALUES(?,?,?)
        """,
        (
            chat_id,
            "assistant",
            ai_response
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "response": ai_response
    })

@chat_bp.route("/get_messages/<int:chat_id>")
def get_messages(chat_id):

    conn = get_db_connection()

    messages = conn.execute(
        """
        SELECT role,content
        FROM messages
        WHERE chat_id=?
        ORDER BY id
        """,
        (chat_id,)
    ).fetchall()

    conn.close()

    return jsonify([
        dict(row)
        for row in messages
    ])

@chat_bp.route("/get_chats")
def get_chats():

    conn = get_db_connection()

    chats = conn.execute(
        """
        SELECT *
        FROM chats
        WHERE user_id=?
        ORDER BY updated_at DESC
        """,
        (
            session["user_id"],
        )
    ).fetchall()

    conn.close()

    return jsonify([
        dict(chat)
        for chat in chats
    ])
@chat_bp.route("/chat")
def chat():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "chat.html",
        username=session["user_name"]
    )
@chat_bp.route("/upload_pdf", methods=["POST"])
def upload_pdf():

    if "user_id" not in session:
        return jsonify({"error":"Unauthorized"}),401

    file = request.files.get("pdf")

    chat_id = request.form.get("chat_id")

    if not file:
        return jsonify({
            "error":"No file uploaded"
        })

    filename = file.filename

    upload_folder = "static/uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    filepath = os.path.join(
        upload_folder,
        filename
    )

    file.save(filepath)

    extracted_text = extract_pdf_text(
        filepath
    )

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO pdfs(
            user_id,
            chat_id,
            filename,
            filepath,
            extracted_text
        )
        VALUES(?,?,?,?,?)
        """,
        (
            session["user_id"],
            chat_id,
            filename,
            filepath,
            extracted_text
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success":True,
        "filename":filename
    })