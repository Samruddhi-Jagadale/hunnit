import React, {useEffect, useState} from "react";
import { useParams } from "react-router-dom";

export default function Product(){
  const {id} = useParams();
  const [p, setP] = useState(null);
  useEffect(() => {
    fetch(`/api/products/${id}`).then(r=>r.json()).then(setP)
  }, [id]);
  if (!p) return <div>Loading...</div>
  return (
    <div style={{padding:24}}>
      <h1>{p.title}</h1>
      <img src={p.image_url || "https://via.placeholder.com/600"} style={{width:400}}/>
      <h3>{p.price}</h3>
      <p>{p.description}</p>
      <ul>{(p.features||[]).map((f,i)=><li key={i}>{f}</li>)}</ul>
      <a href={p.source_url} target="_blank" rel="noreferrer">Source</a>
    </div>
  )
}
