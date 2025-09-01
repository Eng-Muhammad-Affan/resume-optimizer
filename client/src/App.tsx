import { Routes, Route, Link } from "react-router-dom";
import { Home } from "./components";
import { useEffect } from "react";
import axios from "axios";

function App() {
  return (
    <div>
      {/* Navigation */}
      <nav>
        <Link to="/">Home</Link> |{" "}
        <Link to="/about">About</Link> |{" "}
        <Link to="/projects">Projects</Link>
      </nav>

      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
