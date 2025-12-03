import React, {useState} from "react";

export default function Chat(){
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const send = async () => {
    const userMsg = {role:"user", text:query};
    setMessages(prev => [...prev, userMsg]);
    const res = await fetch("/api/chat", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({query})
    });
    const data = await res.json();
    const botMsg = {role:"bot", text: data.message || JSON.stringify(data)};
    setMessages(prev => [...prev, botMsg]);
    // If recommendations included, add as separate messages for UI
    if (data.recommendations) {
      setMessages(prev => [...prev, {role:"bot_products", products: data.recommendations}]);
    }
    setQuery("");
  }

  return (
    <div style={{padding:24}}>
      <h1>Chat</h1>
      <div style={{minHeight:300, border:"1px solid #eee", padding:12}}>
        {messages.map((m,i) => (
          <div key={i} style={{marginBottom:12}}>
            {m.role === "user" && <div style={{textAlign:"right"}}><b>You:</b> {m.text}</div>}
            {m.role === "bot" && <div><b>Bot:</b> {m.text}</div>}
            {m.role === "bot_products" && m.products.map(p => (
              <div key={p.id} style={{border:"1px solid #ddd", padding:8, marginTop:6}}>
                <img src={p.image_url||"https://via.placeholder.com/150"} style={{width:100,float:"left", marginRight:8}}/>
                <div>
                  <div><b>{p.title}</b></div>
                  <div>{p.reason}</div>
                  <div><a href={p.source_url} target="_blank" rel="noreferrer">Source</a></div>
                </div>
                <div style={{clear:"both"}}/>
              </div>
            ))}
          </div>
        ))}
      </div>
      <div style={{marginTop:12}}>
        <input value={query} onChange={e=>setQuery(e.target.value)} style={{width:"70%"}} placeholder="Looking for something I can wear in gym and meetings..." />
        <button onClick={send}>Send</button>
      </div>
    </div>
  )
}
