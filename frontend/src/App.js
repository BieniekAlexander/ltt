// imports
import React from 'react';
import Popover from 'react-bootstrap/Popover';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import './App.css';
import Navbar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomeBody from './pages';
import AboutBody from './pages/about';
import AnnotationsBody from './pages/Annotations';
import InflectionsBody from './pages/Inflections';
import TextSubmissionForm from './components/TextSubmissionForm';


const App = () => {
// const popover = (
//   <Popover id="popover-basic">
//     <Popover.Header as="h3">Popover right</Popover.Header>
//     <Popover.Body>
//       And here's some <strong>amazing</strong> content. It's very engaging.
//       right?
//     </Popover.Body>
//   </Popover>
// );

// const Example = () => (
//   <div>
//     <span>Click </span>
//     <OverlayTrigger trigger="click" placement="right" overlay={popover}>
//       <span>me </span>
//       {/* variant="success" */}
//     </OverlayTrigger>
//     <span>to see</span>
//   </div>
// );


  return (
    // <div className="background">
    //   <Router>
    //   <Navbar />
    //     <Routes>
    //       <Route path="/" element={<HomeBody/>} />
    //       <Route path="/about" element={<AboutBody/>} />
    //       <Route path="/annotations" element={<AnnotationsBody/>} />
    //       <Route path="/inflections" element={<InflectionsBody/>} />
    //     </Routes>
    //   </Router>
    // </div>
   <div>
      <TextSubmissionForm/>
    </div>
  );
}

export default App;