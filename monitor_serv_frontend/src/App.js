import {Header} from "./components/Header";
import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import Dashboard from "./components/dashboard/Dashboard";
import Charts from "./components/dashboard/Charts";
import {Footer} from "./components/Footer";
import {Login} from "./components/auth/Login";

function App() {
  return (
   <Router>
       <Header />
       <Routes>
           <Route path="/" element={<Login/>}/>
           <Route path="/targets" element={<Dashboard/>}/>
           <Route path="/targets/detail" element={<Charts/>}/>
       </Routes>
       <Footer />
   </Router>
  );
}

export default App;
