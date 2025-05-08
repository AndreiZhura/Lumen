async function send() {
    const user_input = document.getElementById("input").value;
    const user_name = document.getElementById("name").value;
    const response = await fetch("/ask", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_input, user_name})
    });
    const data = await response.json();
    document.getElementById("response").innerText = data.reply;
  }