import { useEffect, useState } from "react";
import "./App.css";

type Todo = { id: number; title: string; done: boolean };

const API_URL = import.meta.env.VITE_API_URL as string;

function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  const [version, setVersion] = useState(0);
  const reload = () => setVersion((v) => v + 1);

  useEffect(() => {
    fetch(`${API_URL}/todos`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<Todo[]>;
      })
      .then((data) => {
        setTodos(data);
        setError(null);
      })
      .catch((e) => setError(`Impossible de joindre l'API (${String(e)})`));
  }, [version]);

  async function add(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    await fetch(`${API_URL}/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    setTitle("");
    reload();
  }

  async function toggle(id: number) {
    await fetch(`${API_URL}/todos/${id}`, { method: "PATCH" });
    reload();
  }

  async function remove(id: number) {
    await fetch(`${API_URL}/todos/${id}`, { method: "DELETE" });
    reload();
  }

  return (
    <section>
      <h1>Todo list en production</h1>
      <p>React · FastAPI · PostgreSQL · Scalingo</p>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <form onSubmit={add}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Nouvelle tâche"
        />
        <button type="submit">Ajouter</button>
      </form>
      <ul>
        {todos.map((t) => (
          <li key={t.id}>
            <label>
              <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
              <span style={{ textDecoration: t.done ? "line-through" : "none" }}>
                {t.title}
              </span>
            </label>
            <button onClick={() => remove(t.id)}>Supprimer</button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default App;
