import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";

export default function Home(){
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch("/api/products")
      .then(r => r.json())
      .then(setProducts)
      .catch(console.error)
  }, []);
  return (
    <div style={{padding:24}}>
      <h1>Products</h1>
      <div style={{display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(220px, 1fr))", gap:16}}>
        {products.map(p => (
          <div key={p.id} style={{border:"1px solid #eee", padding:12, borderRadius:8}}>
            <Link to={`/product/${p.id}`}>
              <img src={p.image_url || "https://via.placeholder.com/300"} alt={p.title} style={{width:"100%", height:160, objectFit:"cover"}}/>
              <h3>{p.title}</h3>
            </Link>
            <p>{p.price}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
